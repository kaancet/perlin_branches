import time
import py5_tools
import py5
from branches import Branch
from perlin import Perlin
import numpy as np

w = 800
h = 600
orientation = 'vertical'
branches = []
current_lengths = {}
isGrowing = {}

def bloom(j,i):
    """ j is branch key for dicts and i is leaf index"""
    global current_lengths,isGrowing,branches
    
    if py5.frame_count%2 == 0:
        if isGrowing[j][i]:
            if current_lengths[j][i]<=branches[j].leaves[i]:
                current_lengths[j][i] += 1
            else:
                isGrowing[j][i] = False
        else:
            if current_lengths[j][i]>=3:
                current_lengths[j][i] -= 1
            else:
                isGrowing[j][i] = True
        
def setup():
    global w,h,orientation,branches,current_lengths
    py5.size(w, h, py5.P2D)
    py5.frame_rate(60)
    py5.stroke_weight(8)
    py5.color_mode(py5.HSB,360,100,100)
    
    origins = np.array([[100,h],
                        [200,h],
                        [300,h],
                        [400,h],
                        [500,h],
                        [600,h],
                        [700,h]])
    
    for j,o in enumerate(origins):
        n = np.random.randint(30,50)
        b = Branch(o,
                   length=np.random.randint(4,7)*100,
                   orientation=orientation,
                   n=n,
                   branchiness=np.random.randint(30,100))
        b.make_leaves(length_min=30,length_max=80)
        b.make_color_gradient(c1=[np.random.randint(0,360), np.random.randint(0,100), np.random.randint(0,100)],
                              c2=[np.random.randint(0,360), np.random.randint(0,100), np.random.randint(0,100)],)
        branches.append(b)
        current_lengths[j] = np.zeros(n)
        isGrowing[j] = np.ones(n,dtype=bool)
    
    
def draw():
    global origins,current_lengths,isGrowing
    py5.background(py5.color(51, 5, 100))

    for j,b in enumerate(branches):
        for i,p in enumerate(b.branch_points):
            # py5.circle(p[0],p[1],2)
            py5.stroke(py5.color(b.colors[i][0],b.colors[i][1],b.colors[i][2]))
            
            py5.line(p[0]-current_lengths[j][i],p[1],p[0]+current_lengths[j][i],p[1])
            
            bloom(j,i)
                    
py5.run_sketch()