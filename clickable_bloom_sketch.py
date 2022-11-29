import py5
import time
import numpy as np
from branches import Branch

w = 800
h = 600
branches = []

def reset() -> None:
    """ Resets the branches that have already been instantiated in the branches list"""
    print('Resetting Sketch')
    for b in branches:
        b.init_branch()
        
def constrained_length(o,orientation,direction) -> int:
    """ Chooses the max length depending on the origin point, direction and orientation"""
    global w,h
    if orientation == 'vertical':
        if direction == 1:
            l_max = o[1] - 1
        elif direction == -1:
            l_max = h - o[1]
    elif orientation == 'horizontal':
        if direction == 1:
            l_max = w - o[0]
        elif direction == -1:
            l_max = o[0] - 1
    return l_max

def mouse_check() -> None:
    """ Checks for mouse and key(CMD) presses for branch direction and orientation """
    global branches
    direction = None
    if py5.is_mouse_pressed:
        time.sleep(0.15)
        if py5.is_key_pressed:
            # grow left or right with CTRL
            if py5.key_code == 157:
                orientation = 'horizontal'
                if py5.is_mouse_pressed and py5.mouse_button == py5.LEFT:
                    direction = 1
                elif py5.is_mouse_pressed and py5.mouse_button == py5.RIGHT:
                    direction = -1
        else:
            orientation = 'vertical'
            # grow up or down with mouse alone
            if py5.is_mouse_pressed and py5.mouse_button == py5.LEFT:
                direction = 1
            elif py5.is_mouse_pressed and py5.mouse_button == py5.RIGHT:
                direction = -1

    if direction is not None:
        o = np.array([py5.mouse_x,py5.mouse_y])
        mode = 'fixed_space'
        n = np.random.randint(30,50) if mode=='fixed_count' else 10
        l_max = constrained_length(o,orientation,direction)
        b = Branch(o,
                   length=np.random.randint(20,l_max),
                   direction=direction,
                   orientation=orientation,
                   mode=mode,
                   mode_n=n,
                   branchiness=np.random.randint(30,100))
        b.make_leaves(length_min=30,length_max=80,p_mode='uniform')
        b.make_color_gradient(c1=[np.random.randint(0,360), np.random.randint(0,100), np.random.randint(0,100)],
                              c2=[np.random.randint(0,360), np.random.randint(0,100), np.random.randint(0,100)])
        branches.append(b)
        print(b.n)
        
def setup():
    global w,h,orientation,branches
    py5.size(w, h, py5.P2D)
    py5.frame_rate(60)
    py5.stroke_weight(8)
    py5.color_mode(py5.HSB,360,100,100,100)
    
def draw():
    global branches
    py5.background(py5.color(51, 5, 100))
    
    # User interaction
    if py5.is_key_pressed:
        if py5.key in ['R','r']:
            reset()
    
    mouse_check()
    
    for b in branches:
        for i,p in enumerate(b.branch_points):
            py5.stroke(py5.color(b.colors[i][0],b.colors[i][1],b.colors[i][2],60))
            
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