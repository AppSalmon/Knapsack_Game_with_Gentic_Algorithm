import pygame
import matplotlib.pyplot as plt
import numpy as np
import random as rd
import pandas as pd
from random import randint
import sys
from GA import *


def create_text(x, color, size): # Tạo chữ
	font = pygame.font.SysFont('sans', size)
	return font.render(x, True, color)


# ================ Khởi tạo bài toán =================

number_of_item = 10 # Số đồ vật
range_of_weight = (1, 10) # Phạm vi cân nặng
range_of_value = (1, 10) # Phạm vi giá trị
knapsack_threshold = 15    # Trọng lượng tối đa mà túi đựng được
num_generations = 50 # Số lượng thế hệ
solutions_per_pop = 8 # Số con tạo ra trong mỗi thế hệ

item_number = np.arange(1,number_of_item + 1) # Để in STT

weight = np.random.randint(range_of_weight[0], range_of_weight[1], size = number_of_item) # Khởi tạo weight
value = np.random.randint(range_of_value[0], range_of_value[1], size = number_of_item) # Khởi tạo value


pop_size = (solutions_per_pop,item_number.shape[0]) 

# Tạo ma trận (dân số ban đầu) - 0 không lấy vật phẩm, 1 lấy vật phẩm
initial_population = np.random.randint(2, size = pop_size) 
initial_population = initial_population.astype(int)

# Solve
parameters, fitness_history = optimize_gentic_algorithm(weight, value, initial_population, pop_size, num_generations, knapsack_threshold)
print('The optimized parameters for the given inputs are: \n{}'.format(parameters))

# In kết quả
selected_items = item_number * parameters # Chuyển NST về số thứ tự vật phẩm
print('\nSelected items that will maximize the knapsack without breaking it:')
for i in range(selected_items.shape[1]):
	if selected_items[0][i] != 0:
		print(f'Vật phẩm {selected_items[0][i]}: weight: {weight[i]}, value: {value[i]}\n')

def reset_problem():
	global weight, value, initial_population, selected_items, fitness_history, item_number, parameters
	weight = np.random.randint(range_of_weight[0], range_of_weight[1], size = number_of_item) # Khởi tạo weight
	value = np.random.randint(range_of_value[0], range_of_value[1], size = number_of_item) # Khởi tạo value

	# Tạo ma trận (dân số ban đầu) - 0 không lấy vật phẩm, 1 lấy vật phẩm
	initial_population = np.random.randint(2, size = pop_size) 
	initial_population = initial_population.astype(int)

	# Solve
	parameters, fitness_history = optimize_gentic_algorithm(weight, value, initial_population, pop_size, num_generations, knapsack_threshold)
	print('The optimized parameters for the given inputs are: \n{}'.format(parameters))

	# In kết quả
	selected_items = item_number * parameters # Chuyển NST về số thứ tự vật phẩm
	print('\nSelected items that will maximize the knapsack without breaking it:')
	for i in range(selected_items.shape[1]):
		if selected_items[0][i] != 0:
			print(f'Vật phẩm {selected_items[0][i]}: weight: {weight[i]}, value: {value[i]}\n')

# ==================================================


# ================ Khởi tạo Pygame ==================
pygame.init()
pygame.display.set_caption("GA knapsack")

# Kích thước cửa sổ Pygame
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800

# Tính toán vị trí để cửa sổ nằm giữa màn hình
window_position = (pygame.display.Info().current_w - SCREEN_WIDTH) // 2, (pygame.display.Info().current_h - SCREEN_HEIGHT) // 2

# Tạo cửa sổ Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



# Color
BACKGROUND = (214, 214, 214) # Màu background
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (147, 153, 35)
PURPLE = (255,0,255)
SKY = (0,255,255)
ORANGE = (255,125,25)
GRAPE = (100,25,125)
GRASS = (55,155,65)
list_position_item = [(100, 100), (100, 250), (100, 400), (100, 550), (100, 700), (250, 100), (250, 250), (250, 400), (250, 550), (250, 700)]

running = True
clock = pygame.time.Clock() # Tạo FPS
player_win = 0
bot_win = 0

player_total_weight = 0
player_total_value = 0
player_list_item = []

bot_total_weight = 0
bot_total_value = 0
bot_list_item = []


def reset_player():
	global player_list_item, player_total_weight, player_total_value, bot_total_value, bot_total_weight, bot_list_item
	player_total_weight = 0
	player_total_value = 0
	player_list_item = []

	bot_total_weight = 0
	bot_total_value = 0
	bot_list_item = []
# ===============================================


# ================ Biểu đồ =======================
def draw_graph():
	global fitness_history
	plt.figure(figsize=(3, 2))
	fitness_history_mean = [np.mean(fitness) for fitness in fitness_history]
	fitness_history_max = [np.max(fitness) for fitness in fitness_history]
	plt.plot(list(range(num_generations)), fitness_history_mean, label = 'Mean Fitness')
	plt.plot(list(range(num_generations)), fitness_history_max, label = 'Max Fitness')
	plt.legend()
	plt.title('Fitness through the generations')
	plt.xlabel('Generations')
	plt.ylabel('Fitness')
	print(np.asarray(fitness_history).shape)
	# Lưu biểu đồ vào một tệp hình ảnh
	plt.savefig('graph.png')

	# Load hình ảnh biểu đồ vào Pygame
	chart_image = pygame.image.load('graph.png')
	return chart_image
chart_image = draw_graph()
# ==============================================




# Main loop
while running:
	clock.tick(60)
	screen.fill(BACKGROUND)



	# ========= Inter face ======== #

	# Vẽ vật phẩm
	screen.blit(create_text('List item', BLACK, 30), (135, 10))
	for i in range(len(list_position_item)):
		pygame.draw.circle(screen, BLUE, list_position_item[i], 40)

	# Viết STT vật phẩm
	for i in range(len(list_position_item)):
		screen.blit(create_text(str(i+1), BLACK, 30), (list_position_item[i][0]-10,list_position_item[i][1]-15))

	# Viết thông số vật phẩm
	for i in range(len(list_position_item)):
		screen.blit(create_text(f"W = " + str(weight[i]) + ", V = " + str(value[i]), BLACK, 20), (list_position_item[i][0]-70,list_position_item[i][1]+50))

	# Vẽ 2 cái túi
	pygame.draw.rect(screen, GRASS, (400, 150, 200, 150)) # x, y, size, size
	pygame.draw.rect(screen, GRASS, (400, 400, 200, 150)) # x, y, size, size
	
	# Viết cân nặng tối đa
	screen.blit(create_text("Max Weight: " + str(knapsack_threshold), BLACK, 30), (400, 10))

	# Viết thông số cho túi
	screen.blit(create_text("Your knapsack", BLACK, 30), (400, 100))
	screen.blit(create_text("Total weight: " + str(player_total_weight), BLACK, 25), (400+10, 150))
	screen.blit(create_text("Total value: " + str(player_total_value), BLACK, 25), (400+10, 180))
	screen.blit(create_text("List item: ", BLACK, 25), (400+10, 210))
	screen.blit(create_text(str(player_list_item), BLACK, 25), (400+10, 240))



	screen.blit(create_text("Salmon's knapsack", BLACK, 30), (400, 350))
	screen.blit(create_text("Total weight: " + str(bot_total_weight), BLACK, 25), (400+10, 400))
	screen.blit(create_text("Total value: " + str(bot_total_value), BLACK, 25), (400+10, 430))
	screen.blit(create_text("List item: ", BLACK, 25), (400+10, 460))
	screen.blit(create_text(str(bot_list_item), BLACK, 25), (400+10, 490))



	# Vẽ biểu đồ
	screen.blit(create_text("Salmon's optimization graph", BLACK, 20), (650, 270))

	# Tạo nút & Kích thước và vị trí của các nút
	button_solo = pygame.Rect(750, 660, 200, 50)
	button_again = pygame.Rect(750, 720, 200, 50)

	# Tạo nút vật phẩm
	d = 40*2
	# [(100, 100), (100, 250), (100, 400), (100, 550), (100, 700), (250, 100), (250, 250), (250, 400), (250, 550), (250, 700)]
	item1 = pygame.Rect(100-40, 100-40, d, d)
	item2 = pygame.Rect(100-40, 250-40, d, d)
	item3 = pygame.Rect(100-40, 400-40, d, d)
	item4 = pygame.Rect(100-40, 550-40, d, d)
	item5 = pygame.Rect(100-40, 700-40, d, d)
	item6 = pygame.Rect(250-40, 100-40, d, d)
	item7 = pygame.Rect(250-40, 250-40, d, d)
	item8 = pygame.Rect(250-40, 400-40, d, d)
	item9 = pygame.Rect(250-40, 550-40, d, d)
	item10 = pygame.Rect(250-40, 700-40, d, d)


	# Vẽ tỉ số:
	pygame.draw.rect(screen, WHITE, (680, 350, 220, 100))
	screen.blit(create_text("Score", BLACK, 30), (700, 350))
	screen.blit(create_text(f"Player: {player_win} / {bot_win} :Bot", BLACK, 30), (700, 400))
	

	# Vẽ check weight
	if player_total_weight > knapsack_threshold:
		# pygame.draw.rect(screen, BLUE, (750, 600, 200, 50))
		screen.blit(create_text("Weight is invalid", RED, 50), (650, 500))
	# else:
	# 	# pygame.draw.rect(screen, RED, (750, 600, 200, 50))
	# 	screen.blit(create_text("Weight is invalid", WHITE, 30), (755, 600))
	
	# Vẽ nút solo with bot
	pygame.draw.rect(screen, GRAPE, (750, 660, 200, 50))
	screen.blit(create_text("Solo with Salmon", WHITE, 30), (755, 660))

	# Vẽ nút Play again
	pygame.draw.rect(screen, GRAPE, (750, 720, 200, 50))
	screen.blit(create_text("Play again", WHITE, 30), (755, 720))

	# Vẽ kết quả
	if bot_total_value == 0 or player_total_value == 0:
		pygame.draw.rect(screen, WHITE, ((650, 50), (300, 200)))
		screen.blit(create_text("Result: click solo...", BLACK, 50), (350, 650))
	else:
		screen.blit(chart_image, (650, 50))
		if bot_total_value < player_total_value:
			screen.blit(create_text("Result: You Win", YELLOW, 50), (350, 650))
		elif bot_total_value > player_total_value:
			screen.blit(create_text("Result: You Lose", RED, 50), (350, 650))
		else:
			screen.blit(create_text("Result: Draw", BLUE, 50), (350, 650))

	# Lấy tọa độ chuột
	mouse_x, mouse_y = pygame.mouse.get_pos()


	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): # Click chuột quit hoặc bấm ESC
			pygame.quit()
			sys.exit()

		# Lúc bấm chuột
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Kiểm tra nút trái của chuột
			
			# Check xem có phải hành động lấy vật phẩm không
			index = 0

			
			if button_solo.collidepoint(mouse_x, mouse_y):
				bot_total_weight = 0
				bot_total_value = 0

				bot_list_item = []
				for it in selected_items[0]:
					if it != 0:
						bot_list_item.append(it)

				for i in bot_list_item:
					bot_total_weight += weight[i-1]
					bot_total_value += value[i-1]

				if bot_total_value != 0 and player_total_value != 0: # Update tỉ số
					if bot_total_value < player_total_value:
						player_win += 1
					elif bot_total_value > player_total_value:
						bot_win += 1

					print(player_win, bot_win)

			elif button_again.collidepoint(mouse_x, mouse_y):
				reset_player()
				reset_problem()
				chart_image = draw_graph()



			elif item1.collidepoint(mouse_x, mouse_y):
				index = 1
			elif item2.collidepoint(mouse_x, mouse_y):
				index = 2
			elif item3.collidepoint(mouse_x, mouse_y):
				index = 3
			elif item4.collidepoint(mouse_x, mouse_y):
				index = 4
			elif item5.collidepoint(mouse_x, mouse_y):
				index = 5
			elif item6.collidepoint(mouse_x, mouse_y):
				index = 6
			elif item7.collidepoint(mouse_x, mouse_y):
				index = 7
			elif item8.collidepoint(mouse_x, mouse_y):
				index = 8
			elif item9.collidepoint(mouse_x, mouse_y):
				index = 9
			elif item10.collidepoint(mouse_x, mouse_y):
				index = 10

			if index != 0:
				if index in player_list_item:
					player_list_item.remove(index)
				else:
					player_list_item.append(index)

				player_total_weight = 0
				player_total_value = 0
				for i in player_list_item:
					player_total_weight += weight[i-1]
					player_total_value += value[i-1]





	

	pygame.display.flip()

# Kết thúc Pygame
pygame.quit()
