import pygame
from random import randint
import math
from sklearn.cluster import KMeans

#Create function to calculate the distance of 2 points A(x1, y1) -> B(x2, y2): ((x1-x2)^2 + (y1-y2)^2)^1/2
def distance(p1,p2):
	return math.sqrt((p1[0]-p2[0]) * (p1[0]-p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))

# Color of all button 
BACKGROUND = (214, 214, 214)
BLACK = (0,0,0)
BACKGROUND_PANEL = (249, 255, 230)
WHITE = (255,255,255)


# Color of cluster (K_max = 8)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (147, 153, 35)
PURPLE = (255,0,255)
SKY = (0,255,255)
ORANGE = (255,125,25)
GRAPE = (100,25,125)
GRASS = (55,155,65)

# Create a list that contains 8 colors for K
COLORS = [RED,GREEN,BLUE,YELLOW,PURPLE,SKY,ORANGE,GRAPE,GRASS]


pygame.init()
screen = pygame.display.set_mode((1200,700))
pygame.display.set_caption("Kmeans Visualization")
clock = pygame.time.Clock()

#Set up font for words 
font = pygame.font.SysFont('sans', 40)
font_medium = pygame.font.SysFont('sans', 30)
font_small = pygame.font.SysFont('sans', 20)

# Draw symbols on its panel (TRUE means antialiasing, pixels are smoother)
text_menu = font_medium.render('Menu Options', True, BLACK)
text_plus = font.render('+', True, BLACK)
text_minus = font.render('-', True, BLACK)
text_run = font_medium.render("Run Manually", True, BLACK)
text_random = font_medium.render("Random K Position", True, BLACK)
text_algorithm = font_medium.render(" Run K-Means", True, BLACK)
text_reset = font_medium.render("Reset", True, BLACK)

running = True

K = 0
error = 0
points = []
labels = []
clusters = []

while running:
	clock.tick(60)
	screen.fill(BACKGROUND)
	# Get mouse action when clicking on the screen
	mouse_x, mouse_y = pygame.mouse.get_pos()

# Draw interface

	# Draw panel for creating data points
	pygame.draw.rect(screen, BLACK, (50,50,700,600))
	pygame.draw.rect(screen, BACKGROUND_PANEL, (51,51,698,598))

	# Draw panel for menu options
	pygame.draw.rect(screen, BLACK, (888,50,195,50))
	pygame.draw.rect(screen, BACKGROUND_PANEL, (889,51,193,48))
	screen.blit(text_menu, (891,55))

	# Draw panel for button 
	pygame.draw.rect(screen, BLACK, (777,120,400,520))
	pygame.draw.rect(screen, BACKGROUND_PANEL, (778,121,398,518))

	# K button + 
	pygame.draw.rect(screen, BLACK, (830,160,50,50))
	pygame.draw.rect(screen, BACKGROUND_PANEL, (831,161,48,48))
	screen.blit(text_plus, (844,163))

	# K button -
	pygame.draw.rect(screen, BLACK, (940,160,50,50))
	pygame.draw.rect(screen, BACKGROUND_PANEL, (941,161,48,48))
	screen.blit(text_minus, (959,160))

	# K value
	text_k = font.render("K = " + str(K), True, BLACK)
	screen.blit(text_k, (1050,160))

	# Run button
	pygame.draw.rect(screen, BLACK, (880,250,200,50))
	pygame.draw.rect(screen, BACKGROUND_PANEL, (881,251,198,48))
	screen.blit(text_run, (886,256))

	# Random button
	pygame.draw.rect(screen, BLACK, (850,340,267,50))
	pygame.draw.rect(screen, BACKGROUND_PANEL, (851,341,265,48))
	screen.blit(text_random, (855,346))

	# Error value
	text_error = font.render("Error = " + str(int(error)), True, BLACK)
	screen.blit(text_error, (890,410))

	# Algorithm button
	pygame.draw.rect(screen, BLACK, (880,470,208,50))
	pygame.draw.rect(screen, BACKGROUND_PANEL, (881,471,206,48))
	screen.blit(text_algorithm, (885,475))	

	# Reset button
	pygame.draw.rect(screen, BLACK, (935,550,100,50))
	pygame.draw.rect(screen, BACKGROUND_PANEL, (936,551,98,48))
	screen.blit(text_reset, (945,555))	

	# Draw mouse position when mouse is in panel
	if 50 < mouse_x < 750 and 50 < mouse_y < 650:
		text_mouse = font_small.render("(" + str(mouse_x - 50) + "," + str(mouse_y - 50) + ")",True, BLACK)
		screen.blit(text_mouse, (mouse_x + 10, mouse_y))

	# End draw interface

	# Action on panel
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			# Create point on panel
			if 50 < mouse_x < 750 and 50 < mouse_y < 650:
				labels = []
				point = [mouse_x - 50, mouse_y - 50]
				points.append(point)
				print(points)

			# Change K button +
			if 830 < mouse_x < 880 and 160 < mouse_y < 210:
				if K < 8:
					K = K+1
				print("Press K +")
				
			# Change K button -
			if 940 < mouse_x < 990 and 160 < mouse_y < 210:
				if K > 0:
					K -= 1
				print("Press K -")

			# Run button
			if 880 < mouse_x < 1080 and 250 < mouse_y < 300:
				print("run pressed")
				labels = []
				if clusters == []:
					continue

				# Assign points to closet clusters
				for p in points:
					distances_to_cluster = []
					for c in clusters:
						dis = distance(p,c)
						distances_to_cluster.append(dis)
					
					min_distance = min(distances_to_cluster)
					label = distances_to_cluster.index(min_distance)
					labels.append(label)

				# Update clusters
				for i in range(K):
					sum_x = 0
					sum_y = 0
					count = 0
					for j in range(len(points)):
						if labels[j] == i:
							sum_x += points[j][0]
							sum_y += points[j][1]
							count += 1

					if count != 0:
						new_cluster_x = sum_x/count
						new_cluster_y = sum_y/count
						clusters[i] = [new_cluster_x, new_cluster_y]

			# Random button
			if 850 < mouse_x < 1117 and 340 < mouse_y < 390:
				labels = []
				clusters = []
				for i in range(K):
					random_point = [randint(0,700), randint(0,500)]
					clusters.append(random_point)
				print("random pressed")	


			# Algorithm button
			if 880 < mouse_x < 1088 and 470 < mouse_y < 520:
				try:
					kmeans = KMeans(n_clusters=K).fit(points) 
					labels = kmeans.predict(points)
					clusters = kmeans.cluster_centers_
				except:
					print("error")
				print("Algorithm button pressed")

			
			# Reset button
			if 935 < mouse_x < 1035 and 550 < mouse_y < 600:
				K = 0
				error = 0
				points = []	
				clusters = []
				labels = []
				print("reset button pressed")


	# Draw cluster
	for i in range(len(clusters)):
		pygame.draw.circle(screen,COLORS[i], (int(clusters[i][0]) + 50, int(clusters[i][1]) + 50), 10)
		
	# Draw point
	for i in range(len(points)):	
		pygame.draw.circle(screen,BLACK, (points[i][0] + 50, points[i][1] + 50), 6)
		
		if labels == []:
			pygame.draw.circle(screen,WHITE, (points[i][0] + 50, points[i][1] + 50), 5)
		else:
			pygame.draw.circle(screen,COLORS[labels[i]], (points[i][0] + 50, points[i][1] + 50), 5)

	# Calculate and draw error
	error = 0
	if clusters != [] and labels != []:
		for i in range(len(points)):
			error += distance(points[i], clusters[labels[i]])
		
	pygame.display.flip()
	
pygame.quit()