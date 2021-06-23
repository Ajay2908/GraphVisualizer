import pygame
import copy
from graph import WEIGHTED_GRAPH 
import time
from heapq import heapify, heappush, heappop 

weighted_graph = []
display_width = 800
display_height = 600
radius = 30
speed = 2

grey = (100, 100, 100)
white = (255, 255, 255)
yellow = (200, 200, 0)
red = (200,0,0) 
black = (0, 0, 0)
blue = (50,50,160) 


def find(parent, i):
    if parent[i] == i:
        return i
    return find(parent, parent[i])
 

def union(parent, rank, x, y):
    xroot = find(parent, x)
    yroot = find(parent, y)

    if rank[xroot] < rank[yroot]:
        parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        parent[yroot] = xroot
    else:
        parent[yroot] = xroot
        rank[xroot] += 1

def krushkal():
    global edges
    V = 19
    edgeGraph = []
    for e in edges.values():
        (n1, n2,n3), color = e
        edgeGraph.append([n1,n2,n3,color])
    result = []  
    i = 0
    e = 0
    edgeLis = sorted(edgeGraph,key=lambda item: item[2])
    parent = []
    rank = []

    for node in range(V+1):
        parent.append(node)
        rank.append(0)

    while e < V - 1:

        u, v, w,c = edgeLis[i]
        i = i + 1
        x = find(parent, u)
        y = find(parent, v)

        if x != y:
            e = e + 1
            edges[(min(u,v),max(u,v),w)][1] = yellow
            weighted_graph[u][2] = blue
            weighted_graph[v][2] = blue
            update()
            result.append([u, v, w])
            union(parent, rank, x, y)


def run():
    global screen, edges, clock,d,weighted_graph
    weighted_graph = copy.deepcopy(WEIGHTED_GRAPH)


    for element in weighted_graph:
      element.extend([grey, black])

    build_edges()
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((display_width, display_height))
    update()
    pygame.time.delay(2000)
    krushkal()
    time.sleep(5)
    pygame.quit()


def edge_id(n1, n2):
    return (min(n1,n2),max(n1,n2))

def build_edges():
    global edges
    edges = {}
    check = {}
    for n1, (_, adjacents, _, _) in enumerate(weighted_graph):
        for n2 in adjacents:
            eid = edge_id(n1, n2[0])
            if eid not in check:
                check[eid] = [True]
                edges[(min(n1,n2[0]),max(n1,n2[0]),n2[1])] = [(min(n1,n2[0]),max(n1,n2[0]),n2[1]), grey]

def draw_graph():
    global weighted_graph, screen, edges,d

    screen.fill((0, 0, 0,))

    for e in edges.values():
        (n1, n2,n3), color = e
        pygame.draw.line(screen, color, weighted_graph[n1][0], weighted_graph[n2][0], 2)
        x = weighted_graph[n1][0][0] + weighted_graph[n2][0][0]
        y = weighted_graph[n1][0][1] + weighted_graph[n2][0][1]
        x/=2
        y/=2
        if(color == white):
           display(n3,(x,y),blue)
        else:
           display(n3,(x,y))
        
        
    cntr = 0
    for xy, _, lcolor, fcolor in weighted_graph:
        circle_fill(xy, lcolor, fcolor, 25, 2)
        display(cntr,xy)
        cntr+=1


def update():
  global clock
  draw_graph()
  pygame.display.update()
  clock.tick(speed)

def circle_fill(xy, line_color, fill_color, radius, thickness):
    global screen
    pygame.draw.circle(screen, line_color, xy, radius)
    pygame.draw.circle(screen, fill_color, xy, radius - thickness)

def display(num, position,color=(255, 255, 255)):
    global screen
    font = pygame.font.SysFont('Roboto', 30)
    text = font.render(str(num), True, color)
    textRect = text.get_rect()
    textRect.center = position
    screen.blit(text,textRect)
