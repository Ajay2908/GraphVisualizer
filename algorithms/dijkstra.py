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


INF = 1000000000
d = [INF]*(19)
def dijkstra(node):
    global d
    
    d[node] = 0
    update()
    n = 18
    queue = []
    heapify(queue)
    heappush(queue,(0,node))

    while queue:
        d_v,v = heappop(queue)
        current = weighted_graph[v]
        current[2] = white 
        current[3] = yellow
        if (d_v != d[v]):
            current[3] = blue
            update()
            continue
        for x in weighted_graph[v][1]:
            to = x[0]
            length = x[1]
            if d[v]+length < d[to]:
                d[to] = d[v]+length
                weighted_graph[to][2] = white
                weighted_graph[to][3] = red
                update()
                heappush(queue,(d[to],to))
        current[3] = blue
        update()



def run(node):
    global screen, edges, clock,d,weighted_graph
    weighted_graph = copy.deepcopy(WEIGHTED_GRAPH)
    for element in weighted_graph:
      element.extend([grey, black])

    build_edges()
    time.sleep(3)
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((display_width, display_height))
    
    update()
    pygame.time.delay(2000)
    dijkstra(node)
    d = [INF]*19
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
        display(d[cntr],xy)
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
    if num == INF:
        num = 'INF'
    text = font.render(str(num), True, color)
    textRect = text.get_rect()
    textRect.center = position
    screen.blit(text,textRect)
    
