import pygame

visited = []
queue = []

def dfs(draw, grid, start, end):
	visited.append(start)
	queue.append(start)
	while queue:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
  
		if visited[-1].neighbors == []:
			visited.pop()
			queue.append(neighbor)
			neighbor.make_open()
  
		for neighbor in visited[-1].neighbors:
			if neighbor == end:
				start.make_start()
				end.make_end()
				return True
			elif neighbor not in visited:
				visited.append(neighbor)
				queue.append(neighbor)
				neighbor.make_open()
		
   
		draw()
		if visited[-1] != start:
			visited[-1].make_closed()
	return False
				