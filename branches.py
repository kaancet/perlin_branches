import numpy as np
from perlin import Perlin

class Branch(Perlin):
    def __init__(self, origin:list, length:float, direction:int, orientation:str='vertical', branch_count:int=0, branchiness:float=80, mode:str='fixed_count', mode_n:int=50):
        super().__init__()
        self.origin_point = origin
        self.length = length
        self.direction = direction #either -1 or 1
        self.orientation = orientation
        self.branch_count = branch_count
        
        self.branchiness = branchiness # basically noise scale
        
        assert self.direction in [-1,1], f"direction argument can only be -1 or 1, got: {self.direction}"
        assert self.orientation in ['vertical', 'horizontal'], f"orientation argument can only be 'horizontal' or 'vertical', got: {self.orientation}"
        
        self.mode = mode
        if self.mode == 'fixed_count':
            self.n = mode_n
        elif self.mode == 'fixed_space':
            self.n = int(self.length / mode_n)
        
        self.init_branch()
        self.__make_branch_points()
        # self.__make_child_branch_origins()
        
    def __repr__(self):
        skip = ['gradients']
        ret = f"""Branch:\n"""
        for k,v in self.__dict__.items():
            if not callable(v):
                if k not in skip:
                    ret += f"""{k} : {v}\n"""
        return ret
    
    def init_branch(self) -> None:
        """ Initializes the branch variables that are responsible for growing"""
        #keep track for each leaf segment
        self.current_lengths = np.zeros(self.n)
        self.isGrowing = np.ones(self.n,dtype=bool)
        
        if self.orientation == 'vertical':
            self.draw_limit = self.origin_point[1]
            if self.direction == 1:
                #grow up
                self.end_point = self.origin_point - [0, self.length]
            else:
                #grow down
                self.end_point = self.origin_point + [0, self.length]
        
        elif self.orientation == 'horizontal':
            self.draw_limit = self.origin_point[0]
            if self.direction == 1:
                # grow right
                self.end_point = self.origin_point + [self.length,0]
            else:
                # grow left
                self.end_point = self.origin_point - [self.length,0]
    
    def isDrawable(self,leaf_idx:int) -> bool:
        """ Checks if drawable depending on direction and orientation and limit"""
        ret = False
        if self.orientation == 'vertical':
            if self.direction==1 and self.branch_points[leaf_idx][1] > self.draw_limit:
                ret = True
            elif self.direction==-1 and self.branch_points[leaf_idx][1] < self.draw_limit:
                ret = True

        elif self.orientation == 'horizontal':
            if self.direction==1 and self.branch_points[leaf_idx][0] < self.draw_limit:
                ret = True
            elif self.direction==-1 and self.branch_points[leaf_idx][0] > self.draw_limit:
                ret = True
            
        return ret
        
    def bloom(self,leaf_idx,grow_speed:int=1,min_length:int=3,degrow:bool=True) -> None:
        """ Updates the current length of leaves """
        if self.isGrowing[leaf_idx]:
            if self.current_lengths[leaf_idx] <= self.leaves[leaf_idx]:
                self.current_lengths[leaf_idx] += grow_speed
            else:
                self.isGrowing[leaf_idx] = False
        else:
            if degrow:
                if self.current_lengths[leaf_idx] >= min_length:
                    self.current_lengths[leaf_idx] -= grow_speed
                else:
                    self.isGrowing[leaf_idx] = True
                    
    def update_draw_limit(self,speed:float=0.1):
        if self.orientation == 'vertical' and self.direction == 1:
            # growing up 
            if self.draw_limit >= 0:
                self.draw_limit -= speed
        
        elif self.orientation == 'vertical' and self.direction == -1:
            # growing down
            if self.draw_limit <= 2000: #arbitrary cap to stop from increasing non stop
                self.draw_limit += speed
                
        elif self.orientation == 'horizontal' and self.direction == 1:
            # growing right
            if self.draw_limit <= 2000: #arbitrary cap to stop from increasing non stop
                self.draw_limit += speed
        
        elif self.orientation == 'horizontal' and self.direction == -1:
            # growing left
            if self.draw_limit >= 0:
                self.draw_limit -= speed
        
    def make_color_gradient(self,c1:tuple,c2:tuple) -> None:
        """ makes a color gradient between two colors in the vary dimension """
        if len(c1) != len(c2):
            raise ValueError(f'Length of c1({len(c1)} not equal to length of c2({len(c2)})')
        
        #TODO: Ugly seperate dimension way of doing it
        # self.colors = np.zeros((self.n,len(c1)))
        # for i in range(len(c1)):
        #     temp = np.linspace(c1,c2,self.n)
        #     self.colors[:,i] = temp
        self.colors = np.linspace(c1,c2,self.n)
            
    def make_leaves(self,length_min:int,length_max:int,p_mode:str='uniform',p_kwargs:dict=None)->None:
        """ Creates the leaf lengths depending on p_mode"""
        lengths = np.arange(length_min,length_max)
        if p_mode == 'uniform':
            self.leaves = np.random.choice(lengths,len(self.branch_points),replace=True)
        elif p_mode == 'gaussian':
            if p_kwargs is None:
                p_kwargs = {'mean':(length_max+length_min)/2,
                            'std':(length_max - length_min)/5}
                
            m = p_kwargs.get('mean',(length_max+length_min)/2)
            s = p_kwargs.get('std',(length_max - length_min)/5)
            p = np.random.normal(m, s, len(lengths))
            p /= np.sum(p)
            self.leaves = np.random.choice(lengths,len(self.branch_points),replace=True,p=p)
        elif p_mode == 'fixed':
            pass
        else:
            self.leaves = np.random.choice(np.arange(length_min,length_max),len(self.branch_points),replace=True)
            print(f'>> WARNING << {p_mode} is not a valid p_mode, using "uniform". Try one of: [uniform, gaussian, fixed]!')
        
    def __make_branch_points(self) -> None:
        """ """
        # define indices to create points, depending on the orientation
        grow_dim_idx = 1 if self.orientation == 'vertical' else 0
        perlin_dim_idx = int(not grow_dim_idx)
        
        #make points
        points = np.linspace(self.end_point[grow_dim_idx],self.origin_point[grow_dim_idx],self.n).reshape(-1,1)
        values = np.array([self.branchiness * self.valueAt(i) + self.origin_point[perlin_dim_idx] for i in points]).reshape(-1,1)
        
        if grow_dim_idx:
            self.branch_points = np.hstack((values,points))
            self.branch_points = self.branch_points[::-1]
        else:
            self.branch_points = np.hstack((points,values))
            