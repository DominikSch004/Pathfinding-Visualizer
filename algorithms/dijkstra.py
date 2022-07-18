from queue import PriorityQueue
import pygame

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

def dijkstra(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((count, start))
	came_from = {}
	
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	
	open_set_hash = {start}
	
	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
	
		current = open_set.get()[1]
		open_set_hash.remove(current)
		
		if current == end:
			reconstruct_path(came_from, end, draw)
			start.make_start()
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1
			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()
	 
		draw()
		if current != start:
			current.make_closed()
	return False