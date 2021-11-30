import pygame
import random
import math
from pygame import mixer

# Creating a variable which is true as long as the game is running
running = True
# Initialize the pygame
pygame.init()
# Create the screen with 600height en 800width
screen = pygame.display.set_mode((800, 600))
# Create the variable for the icon
icon = pygame.image.load("ufo.png")
# Create the variable for the background
background = pygame.image.load("background.png")
# # Loading the background sound
# mixer.music.load('background.wav')
# # Playing the background sound on loop(-1)
# mixer.music.play(-1)
# Setting the title of the game window
pygame.display.set_caption("Space Invaders")
# Setting the icon of the game window
pygame.display.set_icon(icon)
# Score van de game
score = 0



# Player
playerImg = pygame.image.load("player.png") # Create the variable for the player image
playerX = 370 # The x-coordinate of the player
playerY = 480 # The y-coordinate of the player
playerX_change = 0 # The amount that is going to change the x-coordinate when moving

# Enemy
enemyImg = [] # Create the variable for the enemy image
enemyX = [] # The x-coordinate of the enemy
enemyY = [] # The y-coordinate of the enemy
enemyX_change = [] # The amount that is going to change the x-coordinate when moving
enemyY_change = [] # The amount that is going to change the Y-coordinate when moving
num_of_enemies = 6

for i in range(num_of_enemies):
	enemyImg.append(pygame.image.load("enemy.png")) # Create the variable for the bullet image
	enemyX.append(random.randint(0, 735)) # The x-coordinate of the bullet
	enemyY.append(random.randint(50, 150)) # The y-coordinate of the bullet
	enemyX_change.append(4) # The amount that is going to change the x-coordinate when moving
	enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load("bullet.png") # Create the variable for the bullet image
bulletX = 0 # The x-coordinate of the bullet
bulletY = 480 # The y-coordinate of the bullet
bulletX_change = 0 # The amount that is going to change the x-coordinate when moving
bulletY_change = 10 # The amount that is going to change the Y-coordinate when moving
bullet_state = "ready" # Ready means you can shoot a bullet

# Score
score_value = 0
# The font and how the big it should be
font = pygame.font.Font('freesansbold.ttf', 32)
# Coordinates of the sccore
textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over():
	over_text = over_font.render("GAME OVER", True, (255, 255, 255))
	screen.blit(over_text, (200, 250))

def show_score(x, y):
	# First have to render the score. First parameter is the text. Second is if we want to show it. Third the color
	score = font.render("Score: " + str(score_value), True, (255, 255, 255))
	# Then draw the rendered font(which is the variable score in this case)
	screen.blit(score, (x, y))

def player(x, y):
	# Drawing the player. First parameter is the image, the second is the coordinates
	screen.blit(playerImg, (x, y))

def enemy(x, y, i):
	# Drawing the enemy. First parameter is the image, the second is the coordinates
	screen.blit(enemyImg[i], (x, y))

def bullet():
	global bulletY
	global bullet_state
	global bulletY_change
	global bulletX
	global bulletY

	# If the bullet hits the border than place it back at the spaceship
	if bulletY <= 0:
		bulletY = 480
		bullet_state = "ready"
	if bullet_state == "fire": # Decrease bulletY by 10 so the bullet goes to up
		fire_bullet(bulletX, bulletY) # Give the coordinates of the spaceship
		bulletY -= bulletY_change

def fire_bullet(x, y):
	global bullet_state

	bullet_state = "fire"
	# Draw the bullet at the given coordinates 
	screen.blit(bulletImg, (x + 16, y + 10))

# Checking if there is a collision between the bullet and the enemy
def isCollision(enemyX, enemyY, bulletX, bulletY):
	# The formula to calculate the differences between coordinates
	distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
	# If the difference is less than 27 than there is a collision
	if distance < 27:
		return True
	else:
		return False

# Creating a function to check if the game should end
def checkEnd(event):
	global running

	# If the type of the event is quit then make running false and escape the while loop
	if event.type == pygame.QUIT:
		running = False



# While the program is running run the following code
while running:
	# RGB colour of the background you want to fill
	screen.fill((0, 0, 0))
	# Drawing the background at 0, 0
	screen.blit(background, (0,0))
	# For every event that happens run the following code
	for event in pygame.event.get():
		checkEnd(event)
		# If the event type is a keystroke being pressed AND the key being pressed is left arrow run following code
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				# Setting the change of the x-coordinate. In this case to the left
				playerX_change = -5 # 5 + -0.1 = 4.9
			# If the event type is a keystroke being pressed AND the key being pressed is right arrow run following code
			if event.key == pygame.K_RIGHT:
				# Setting the change of the x-coordinate. In this case to the right
				playerX_change = 5 # 5 + 0.1 = 5.1
			# If space is pressed AND the bullet state is ready
			if event.key == pygame.K_SPACE and bullet_state == "ready":
				# Saving the current coordinate of the player otherwise it will go with the player when they move
				bulletX = playerX
				fire_bullet(bulletX, bulletY)
				# Creatung variable so the sound only plays once thats why Sound() but not load()
				bullet_sound = mixer.Sound('laser.wav')
				# Play the bullet sound
				bullet_sound.play()

		# If the event type is a keystroke being released AND the key being released is left/right arrow run following code	
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or pygame.K_RIGHT:
				playerX_change = 0

	# Changing the x-coordinate of the player
	playerX += playerX_change
	# If the x coordinate is less than 0 then make the coordinate 0
	if playerX <= 0:
		playerX = 0
	# If the x coordinate is higher than 736 then make the coordinate 736
	elif playerX >= 736:
		playerX = 736

	# Looping through through all enemies so we can change their values
	for i in range(num_of_enemies):

		# Game Over
		if enemyY[i] > 440:
			for j in range(num_of_enemies):
				enemyY[j] = 2000
			game_over()
			break

		enemyX[i] += enemyX_change[i]
		# If the x coordinate is less than 0 then make the coordinate 0
		if enemyX[i] <= 0: # If enemyX is <= 0 then go to left side
			enemyX_change[i] = 4
			enemyY[i] += enemyY_change[i]
		# If the x coordinate is higher than 736 then make the coordinate 736
		elif enemyX[i] >= 736: # if venemyXal is >= 736 then go to right side
			enemyX_change[i] = -4
			enemyY[i] += enemyY_change[i]

		# True or False. Depending on if there is a collision
		collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
		# If collision is true run following code
		if collision:
			# Creatung variable so the sound only plays once thats why Sound() but not load()
			explosion_sound = mixer.Sound('explosion.wav')
			# Play the explosion sound
			explosion_sound.play()
			# Reset de bullet
			bulletY = 480
			bullet_state = "ready"
			# Adding 1 to score
			score_value += 1
			# Respawning the enemy
			enemyX[i] = random.randint(0, 735)
			enemyY[i] = random.randint(50, 150)
		enemy(enemyX[i], enemyY[i], i)

	player(playerX, playerY)
	show_score(textX, textY)
	bullet()


	# Update the screen(because everything is gonna be changing)
	pygame.display.update()

