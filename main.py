import random
from turtle import Screen

import pygame
from sys import exit 
import sys

pygame.init()


#add background music 
pygame.mixer.init()
pygame.mixer.music.load("assets/song.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  

 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/him.png")
        self.rect = self.image.get_rect(midbottom=(100, 350))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 350:
            self.gravity = -12

    def apply_gravity(self):
        self.gravity += 0.5
        self.rect.y += self.gravity
        if self.rect.bottom > 350:
            self.rect.bottom = 350

    def update(self):
        self.player_input()
        self.apply_gravity()

class Target(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.start = random.randint(800, 1000)
        if type == "pencil":
            self.image = pygame.image.load("assets/pencil.png")
        elif type == "book":
            self.image = pygame.image.load("assets/book.png")
        else:
            self.image = pygame.image.load("assets/clipboard.png")

        self.rect = self.image.get_rect(midbottom=(self.start, 100))
    def update(self):
        self.rect.x -= 6
        self.destroy()
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
        

# obsticle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.start = random.randint(800, 2000)
        if type == "phone":
            self.image = pygame.image.load("assets/phone.png")
        elif type == "headphones":
            self.image = pygame.image.load("assets/headphones.png")
        else:
            self.image = pygame.image.load("assets/games.png")

        self.rect = self.image.get_rect(midbottom=(self.start, 350))

    def update(self):
           self.rect.x -= 6
           self.destroy()
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def check_collision():
    global score
    if player.sprite:
        collided_target = pygame.sprite.spritecollide(player.sprite, targets_group, True)
        if collided_target:
            score += 2

def check_collision2():
    global health
    if player.sprite:
        collided_target = pygame.sprite.spritecollide(player.sprite, obstacle_group, True)
        if collided_target:
            health -= 7
def display_score():
    score_surf = score_font.render("Score: " + str(score), True, (50, 50, 50))
    score_rect = score_surf.get_rect(center=(100, 50))
    screen.blit(score_surf, score_rect)




def display_health():
    health_surf = score_font.render("health: " + str(int(health)), True, (50, 50, 50))
    health_rect = health_surf.get_rect(center=(300, 50))
    screen.blit(health_surf, health_rect)


#initialize variables

score = 0
health = 30
score_font = pygame.font.Font(None, 30)
#start Screen
start_screen = pygame.image.load("assets/Start.png")

#Lose/win screen
lose_screen = pygame.image.load("assets/Lost.png")
win = pygame.image.load("assets/win.png")


player = pygame.sprite.GroupSingle()
player.add(Player())

#target group
targets_group = pygame.sprite.Group()

#obstacle group
obstacle_group = pygame.sprite.Group()

#create screen
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("The Detention Dodge")
clock = pygame.time.Clock()

grass = pygame.image.load("assets/grass.png").convert()
sky = pygame.image.load("assets/sky.png").convert()
game_screen = 0

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_screen = 1
                score = 0
                health = 30

        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_screen == 3 or game_screen == 2:
                    health = 30
                    score = 0
                    game_screen = 1

    

    if game_screen == 0:
        screen.blit(start_screen, (0, 0))
    
    
    elif game_screen == 1:
        #show background
        screen.blit(sky, (0, 0))
        screen.blit(grass, (0, 350))

        player.draw(screen)
        player.update()

        #targets
        targets_group.draw(screen)
        targets_group.update()
        if not targets_group:
            i = random.randint(0, 2)
            choices = ["pencil", "book", "clipboard"]
            targets_group.add(Target(choices[i]))

        #obstacle
        obstacle_group.draw(screen)
        obstacle_group.update()
        if not obstacle_group:
            i = random.randint(0, 2)
            choices = ["phone", "headphones", "games"]
            obstacle_group.add(Obstacle(choices[i]))
        check_collision()
        display_score()
        check_collision2()
        display_health()
        if health <= 0:
            game_screen = 3
        if score >= 50:
            game_screen = 2
    elif game_screen == 2:
        screen.blit(win, (0, 0))
    else:
        screen.blit(lose_screen, (0, 0))
        
   
    pygame.display.update()
    clock.tick(60)




