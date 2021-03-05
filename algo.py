import pygame
import math
from queue import PriorityQueue


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))

pygame.display.set_caption("Path Finding Algorithms")


RED = (118, 200, 147)
GREEN = (24, 78, 119)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
	def __init__(self,row,col,width,total_rows):
		self.row = row
		self.col = col
		self.x = row*width
		self.y = col*width
		self.color = WHITE
		self.neighbours = []
		self.width =width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row,self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_obstacle(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == BLUE

	def is_end(self):
		return self.color == ORANGE

	def reset(self):
		self.color = WHITE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_obstacle(self):
		self.color = BLACK

	def make_start(self):
		self.color = BLUE

	def make_end(self):
		self.color = ORANGE

	def make_path(self):
		self.color = PURPLE

	def draw(self,win):
		pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))

	def update_neighbours(self,grid):
		self.neighbours = []

		if(self.row <self.total_rows-1 and not grid[self.row+1][self.col].is_obstacle()):
			self.neighbours.append(grid[self.row+1][self.col])#DOWN


		if(self.row > 0 and not grid[self.row-1][self.col].is_obstacle()):
			self.neighbours.append(grid[self.row-1][self.col])#UP


		if(self.col <self.total_rows-1 and not grid[self.row][self.col+1].is_obstacle()):
			self.neighbours.append(grid[self.row][self.col+1])#RIGHT


		if(self.col > 0 and not grid[self.row][self.col-1].is_obstacle()):
			self.neighbours.append(grid[self.row][self.col-1])#LEFT

	def __lt__(self,other):
		return False


def H(p1,p2):
	x1,y1 = p1
	x2,y2 = p2
	return abs(x1-x2)+abs(y1-y2)

def make_grid(rows,width):
	grid =[]
	gap = width//rows


	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i,j,gap,rows)
			grid[i].append(node)


	return grid

def draw_grid(win,rows,width):
	GAP = width//rows
	for i in range(rows):
	 	pygame.draw.line(win,GREY,(0,i*GAP),(width,i*GAP))
	 	for j in range(rows):
	 		pygame.draw.line(win,GREY,(j*GAP,0),(j*GAP,width))


def draw(win,grid,rows,width):
	win.fill(WHITE)

	for row in grid:
		for node in row:
			node.draw(win)
	draw_grid(win,rows,width)
	pygame.display.update()

def get_clicked_pos(pos,rows,width):
	gap = width//rows
	i,j = pos
	row = i //gap
	col = j //gap
	return row,col
def reconstruct_path(previous_node,current,draw):
	while current in previous_node:
		current = previous_node[current]
		current.make_path()
		draw()



def algorithm(draw,grid,start,end):
	count = 0
	open_set = PriorityQueue()

	open_set.put((0,count,start))
	previous_node = {}
	g_score = {node:float("inf") for row in grid for node in row}
	g_score[start]=0
	f_score = {node:float("inf") for row in grid for node in row}
	f_score[start]=H(start.get_pos(),end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(previous_node,end,draw)
			end.make_end()
			start.make_start()
			return True #path found finally 


		for neighbour in current.neighbours:
			temp_g_score = g_score[current]+1

			if(temp_g_score < g_score[neighbour]):
				previous_node[neighbour]=current
				g_score[neighbour]=temp_g_score
				f_score[neighbour]=temp_g_score+H(neighbour.get_pos(),end.get_pos())

				if neighbour  not in open_set_hash:
					count+=1
					open_set.put((f_score[neighbour],count,neighbour))
					open_set_hash.add(neighbour)
					neighbour.make_open()
		draw()

		if current != start:
			current.make_closed()



	return False




def main(win,width):
	ROWS = 50
	grid = make_grid(ROWS,width)

	start = None
	end = None

	run = True 
	started = False


	while run:
		draw(win,grid,ROWS,width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False


			if started:
				continue

			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				row,col = get_clicked_pos(pos,ROWS,width)
				node = grid[row][col]

				if not start:
					start = node
					start.make_start()
				elif not end:
					end = node
					end.make_end()

				elif node != start and node != end :
					node.make_obstacle()


			elif pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()
				row,col = get_clicked_pos(pos,ROWS,width)
				node = grid[row][col]
				node.reset()

				if node  == start:
					start = None
				elif node == end:
					end = None


			if event.type == pygame.KEYDOWN:
				if event.key ==  pygame.K_SPACE and not started:
					for row in grid:
						for node in row:
							node.update_neighbours(grid)


					algorithm(lambda: draw(win,grid,ROWS,width),grid,start,end)





	pygame.quit()


main(WIN,WIDTH)





