import pygame
import random
import math

# Initialization
pygame.init()

# Creating Window for game
screen_height = 600
screen_width = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Caption and Icon of the game
pygame.display.set_caption("Fighter Plane with Ajay")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)


def welcome():
    running = True
    while running:

        screen.fill((0, 0, 0))
        homeImg = pygame.image.load("home.jpg")
        screen.blit(homeImg, (0, 0))

        # Events for game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Taking keystrokes
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.load("back.mp3")
                    pygame.mixer.music.play(-1)
                    gameloop()
        pygame.display.update()


def gameloop():
    # Adding Images
    bgImg = pygame.image.load("back.jpg")

    # Adding music

    # Speeding Elements
    bulletSpeed = 4
    enemySpeed = 2
    playerSpeed = 3

    # Player of our game
    playerImg = pygame.image.load("player1.png")
    playerX = 368
    playerY = 500
    playerX_change = 0

    # Enemy of our game
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemy = 6

    for i in range(num_of_enemy):
        enemyImg.append(pygame.image.load("enemy.png"))
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(enemySpeed)
        enemyY_change.append(25)

    # Bullet of our game
    # ready --> You cant see the bullet on the screen
    # fire --> The bullet is correctly moving
    bulletImg = pygame.image.load("bullet1.png")
    bulletX = 0
    bulletY = 500
    # bulletX_change = 0
    bulletY_change = bulletSpeed
    bullet_state = 'ready'

    # Position of score on the screen
    score = 0
    scoreX = 10
    scoreY = 10

    # Displaying text/score on the screen
    font = pygame.font.Font("myfont.ttf", 36)

    def textScreen(x, y):
        text = font.render("SCORE : " + str(score), True, (255, 255, 255))
        screen.blit(text, (x, y))

    # Displaying text/gameover on the screen
    def player(x, y):
        screen.blit(playerImg, (x, y))

    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))

    def fire_bullet(x, y):
        nonlocal bullet_state
        bullet_state = 'fire'
        screen.blit(bulletImg, (x + 16, y + 10))

    def isCollision(enemyX, enemyY, bulletX, bulletY):
        dist = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
        if dist < 27:
            return True
        else:
            return False

    # Game Loop
    running = True
    while running:

        screen.fill((0, 0, 0))
        screen.blit(bgImg, (0, 0))

        # Events for game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Taking keystrokes
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = - playerSpeed
                if event.key == pygame.K_RIGHT:
                    playerX_change = playerSpeed
                if event.key == pygame.K_UP:
                    if bullet_state == 'ready':
                        bullet_sound = pygame.mixer.Sound("bullet.wav")
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # Boundry for our player
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy movement in x and y direction
        for i in range(num_of_enemy):

            # Game Over
            if enemyY[i] > 440:
                gameOver(score)
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = enemySpeed
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = - enemySpeed
                enemyY[i] += enemyY_change[i]

            # for Collison of bullet and enemy
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                exp_sound = pygame.mixer.Sound("exp.wav")
                exp_sound.play()
                bulletY = 500
                bullet_state = "ready"
                score += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)
            enemy(enemyX[i], enemyY[i], i)

        # Bullet movement in x and y direction
        if bulletY <= 0:
            bulletY = 500
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        textScreen(scoreX, scoreY)
        pygame.display.update()
    pygame.quit()
    quit()


def gameOver(score):
    pygame.mixer.music.load("gameover.mp3")
    pygame.mixer.music.play()
    running = True
    while running:

        screen.fill((0, 0, 0))
        goImg = pygame.image.load("go.jpg")
        screen.blit(goImg, (0, 0))
        font1 = pygame.font.Font("myfont.ttf", 48)
        text1 = font1.render("SCORE : " + str(score), True, (255, 200, 200))
        screen.blit(text1, (320, 470))

        # Events for game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            # Taking keystrokes
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load("back.mp3")
                    pygame.mixer.music.play(-1)
                    welcome()
        pygame.display.update()


welcome()
