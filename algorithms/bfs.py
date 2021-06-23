import pygame
import copy
from graph import GRAPH
import time
from heapq import heapify, heappush, heappop 

graph = []
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


def bfs(node):
    queue = [node] 
    while len(queue) > 0:
        n1 = queue.pop(0)
        current = graph[n1]   
        current[2] = white 
        current[3] = yellow
        for n2 in current[1]:
            if graph[n2][3] == black and n2 not in queue:
                queue.append(n2) 

                graph[n2][2] = white
                graph[n2][3] = red
                edges[edge_id(n1,n2)][1] = white
                update()

        current[3] = blue
        update()



def run(node):
    global screen, edges, clock,graph
    graph = copy.deepcopy(GRAPH)
    for element in graph:
      element.extend([grey, black])

    build_edges()
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((display_width, display_height))

    draw_graph()
    update()
    pygame.time.delay(2000)
    bfs(node)
    time.sleep(5)
    pygame.quit()


def edge_id(n1, n2): return tuple(sorted((n1, n2)))  

def build_edges():
    global edges
    edges = {}
    for n1, (_, adjacents, _, _) in enumerate(graph):
        for n2 in adjacents:
            eid = edge_id(n1, n2)
            if eid not in edges:
                edges[eid] = [(n1, n2), grey]

def draw_graph():
    global graph, screen, edges

    screen.fill((0, 0, 0,))

    for e in edges.values():
        (n1, n2), color = e
        pygame.draw.line(screen, color, graph[n1][0], graph[n2][0], 2)
        
        
    cntr = 0
    for xy, _, lcolor, fcolor in graph:
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

def display(num, position):
    global screen
    font = pygame.font.SysFont('Roboto', 30)
    text = font.render(str(num), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = position
    screen.blit(text,textRect)
