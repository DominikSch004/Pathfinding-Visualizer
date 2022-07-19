import pygame
import sys
from node import Spot
from button import Button
from algorithms.a_star import a_star
from algorithms.dijkstra import dijkstra
from algorithms.depth_first_search import dfs
from algorithms.breadth_first_search import bfs

pygame.init()
font = pygame.font.Font(pygame.font.get_default_font(), 25)

WIDTH = 800
ROWS = 50
WIN = pygame.display.set_mode((WIDTH, WIDTH))
font = pygame.font.Font(pygame.font.get_default_font(), 30)
pygame.display.set_caption("Path Finding Algorithms")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
BLACK = (0, 0, 0)


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, WHITE, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, WHITE, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def main_menu(win):
	while True:
		win.fill((80, 140, 255))

		MENU_MOUSE_POS = pygame.mouse.get_pos()

		MENU_TEXT = font.render("MAIN MENU", True, "#ffffff")
		MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

		PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(WIDTH//2, 250), 
							text_input="VISUALIZER", font=font, base_color="#ffffff", hovering_color="Red")
		OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(WIDTH//2, 400), 
							text_input="CONTROLS", font=font, base_color="#ffffff", hovering_color="Red")
		QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(WIDTH//2, 550), 
							text_input="QUIT", font=font, base_color="#ffffff", hovering_color="Red")

		win.blit(MENU_TEXT, MENU_RECT)

		for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
			button.changeColor(MENU_MOUSE_POS)
			button.update(win)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
					visualizer(win, WIDTH, ROWS)
				if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
					controls(win)
				if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
					pygame.quit()
					sys.exit()

		pygame.display.update()

def controls(win):
	pygame.display.set_caption("Menu")
	while True:
		win.fill(WHITE)
		OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
  
		OPTIONS_TEXT = font.render("These are the controls for the Visualizer:", True, "Black")
		OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH//2, 60))
		win.blit(OPTIONS_TEXT, OPTIONS_RECT)
		OPTIONS_TEXT = font.render("Reset the Grid:	Press C", True, "Black")
		OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH//2, 310))
		win.blit(OPTIONS_TEXT, OPTIONS_RECT)
		OPTIONS_TEXT = font.render("Use the A* Algorithm:	Press A", True, "Black")
		OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH//2, 360))
		win.blit(OPTIONS_TEXT, OPTIONS_RECT)
		OPTIONS_TEXT = font.render("Use the Dijstra Algorithm:	Press D", True, "Black")
		OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH//2, 410))
		win.blit(OPTIONS_TEXT, OPTIONS_RECT)
		OPTIONS_TEXT = font.render("Use the Breath First Search Algorithm:	Press B", True, "Black")
		OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH//2, 410))
		win.blit(OPTIONS_TEXT, OPTIONS_RECT)
		OPTIONS_TEXT = font.render("Use the Depth First Search Algorithm:	Press S", True, "Black")
		OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH//2, 410))
		win.blit(OPTIONS_TEXT, OPTIONS_RECT)

		OPTIONS_BACK = Button(image=None, pos=(WIDTH//2, 650), 
							text_input="BACK", font=font, base_color="Black", hovering_color="Red")

		OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
		OPTIONS_BACK.update(win)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
					main_menu(win)

		pygame.display.update()


def visualizer(win, width, rows):
	grid = make_grid(rows, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, rows, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, rows, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, rows, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					dfs(lambda: draw(win, grid, rows, width), grid, start, end)
	 
				if event.key == pygame.K_d and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					dijkstra(lambda: draw(win, grid, rows, width), grid, start, end)
	 
				if event.key == pygame.K_s and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					dfs(lambda: draw(win, grid, rows, width), grid, start, end)
	 
				if event.key == pygame.K_b and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					bfs(lambda: draw(win, grid, rows, width), grid, start, end)
   
				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(rows, width)

	pygame.quit()

if __name__ == '__main__':
	main_menu(WIN)