import time
import py5_tools
import py5
from branches import Branch
from perlin import Perlin
import numpy as np

w = 800
h = 600
branches = []      

def reset():
    print('Resetting Sketch')
    for b in branches:
        b.init_branch()
        
def recreate():
    print('Recreating branches')
    create_branches()
        
def create_branches():
    pass
        
def setup():
    global w,h,orientation,branches
    
    py5.size(w, h, py5.P2D)
    # time.sleep(6)
    py5.frame_rate(60)
    py5.stroke_weight(8)
    py5.color_mode(py5.HSB,360,100,100,100)
    
    #vertical branches
    origins_vertical = np.array([[200,h],
                                 [400,0],
                                 [600,h]])

    for o in origins_vertical:
        n = np.random.randint(30,50)
        b = Branch(o,
                   length=np.random.randint(4,7)*100,
                   direction=-1 if o[1] == 0 else 1,
                   orientation='vertical',
                   mode='fixed_count',
                   mode_n=n,
                   branchiness=np.random.randint(100,200))
        b.make_leaves(length_min=30,length_max=80)
        b.make_color_gradient(c1=[np.random.randint(0,360), np.random.randint(0,100), np.random.randint(0,100)],
                              c2=[np.random.randint(0,360), np.random.randint(0,100), np.random.randint(0,100)])
        branches.append(b)
        
    # horizontal branches
    origins_horizontal = np.array([[w,200],
                                   [0,400]])
    
    for o in origins_horizontal:
        n = np.random.randint(30,50)
        b = Branch(o,
                   length=np.random.randint(4,7)*100,
                   direction=1 if o[0] == 0 else -1,
                   orientation='horizontal',
                   mode='fixed_count',
                   mode_n=n,
                   branchiness=np.random.randint(30,100))
        b.make_leaves(length_min=30,length_max=80)
        b.make_color_gradient(c1=[np.random.randint(0,360), np.random.randint(0,100), np.random.randint(0,100)],
                              c2=[np.random.randint(0,360), np.random.randint(0,100), np.random.randint(0,100)])
        branches.append(b)
    
def draw():
    global branches
    py5.background(py5.color(51, 5, 100))
    
    # User interaction
    if py5.is_key_pressed:
        if py5.key in ['R','r']:
            reset()
        elif py5.key in ['N','n']:
            recreate()

    for b in branches:
        for i,p in enumerate(b.branch_points):
            py5.stroke(py5.color(b.colors[i][0],b.colors[i][1],b.colors[i][2],80))
            
            if b.isDrawable(i):
                if b.orientation == 'vertical':
                    py5.line(p[0]-b.current_lengths[i],p[1],p[0]+b.current_lengths[i],p[1])
                elif b.orientation == 'horizontal':
                    py5.line(p[0],p[1]-b.current_lengths[i],p[0],p[1]+b.current_lengths[i])
                
                if py5.frame_count % 2 == 0:
                    b.bloom(i,degrow=False)
                
            if py5.frame_count%10==0:
                b.update_draw_limit()
                

py5.run_sketch()