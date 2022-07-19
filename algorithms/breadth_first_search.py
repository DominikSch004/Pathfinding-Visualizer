import pygame

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

def bfs(draw, grid, start, end):
	came_from = {}
	visited = {start}	
	next_node = [start]
	
	while next_node:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
	
		current = next_node.pop(0)
		
		if current == end:
			reconstruct_path(came_from, end, draw)
			start.make_start()
			end.make_end()
			return True

		for neighbor in current.neighbors:
			if neighbor not in visited:
				came_from[neighbor] = current
				visited.add(neighbor)
				next_node.append(neighbor)
				neighbor.make_open()
	 
		draw()
		if current != start:
			current.make_closed()
	return False