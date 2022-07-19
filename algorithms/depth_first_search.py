import pygame

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

def dfs(draw, grid, start, end): 
	next_node = [start]

	visited = {start}

	came_from = {}

	current_node = start
	while next_node:
		draw()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		if current_node not in (start, end):
			current_node.make_closed()

		current_node = next_node.pop()

		if current_node == end:
			reconstruct_path(came_from, end, draw)
			start.make_start()
			end.make_end()
			return True

		if current_node not in visited:
			visited.add(current_node)

		for neighbour in current_node.neighbors:

			if neighbour not in visited:
				came_from[neighbour] = current_node
				next_node.append(neighbour)
		
		if current_node not in (start, end):
			current_node.make_open()
	
	return False