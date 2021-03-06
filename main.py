import pygame
from pygame.locals import *
import sys
import random
try:
    import android
except:
    android = None



def main():
    global i
    class Player:
        def __init__(self):
            self.animation = [pygame.image.load('helicopter/%i.1.png'%i) for i in range(1,4)]
            self.image = self.animation[1]
            self.speed = SPEED
            self.y = 200
        def update(self):
            self.image = self.animation[i%3]
            if started:
                if move:
                    if self.speed > -4 and i%4==0:
                        self.speed -= 1
                elif self.speed < 6 and i %3 == 0:
                    self.speed += 1
                self.y += self.speed
        def check_collide(self):
            """uses masks to see if non-transparent pixels overlap"""
            #check if the wall has collided:
            wall_mask = pygame.mask.from_surface(wall_image,50)
            prime_mask = pygame.mask.from_surface(wall_prime,50)
            helicopter_mask = pygame.mask.from_surface(helicopter.image,50)
            wall_offset_x = PLAYER_X - wall_image_x
            prime_offset_x = PLAYER_X - wall_prime_x
            offset_y = self.y
            wall_overlap = wall_mask.overlap(helicopter_mask,(wall_offset_x,offset_y))
            prime_overlap = prime_mask.overlap(helicopter_mask,(prime_offset_x,offset_y))
            if wall_overlap or prime_overlap:
                return True
            #check if the blocks have collided:
            for block in blocks:
                offset_x = PLAYER_X - block.x
                offset_y = self.y - block.y
                overlap = block.mask.overlap(helicopter_mask,(offset_x,offset_y))
                if overlap: return True

    class Block:
        def __init__(self):
            self.image = pygame.image.load('block.png')
            self.x = 701 #right out of view
            self.y = random.randint(50,400)
            self.mask = pygame.mask.from_surface(self.image,50)
            self.done = False
        def draw(self):
            screen.blit(self.image,(self.x,self.y))
        def update(self):
            self.x -= WALL_SPEED

    class Smoke(Block):
        def __init__(self):
            self.image = pygame.image.load('smoke.png')
            self.x = PLAYER_X
            self.y = helicopter.y + 4
            self.done = False


    def intro():
        global i
        screen.fill(pygame.Color('black'))
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    return
            screen.blit(helicopter.image,(PLAYER_X,helicopter.y))
            screen.blit(wall_image,(0,0))
            screen.blit(font.render('CLICK TO START',False,pygame.Color(78,195,230)),(300,200))
            screen.blit(small_font.render('BEST: %i'%highscore,False,pygame.Color(0,100,255)),(500,460))
            helicopter.update()
            clock.tick(FPS)
            pygame.display.update()
            i += 1




    pygame.init()
    if android:
        android.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 700,500
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    FPS = 60
    SPEED = 5
    WALL_SPEED = 7
    PLAYER_X = 200
    font = pygame.font.Font('digital-7 (italic).ttf',50)
    small_font = pygame.font.Font('digital-7 (italic).ttf',30)
    highscore = 0
    i = 0


    #load wall images
    wall_image = pygame.image.load('walls.png')
    wall_prime = pygame.image.load('walls.png') #used for looping the wall

    while True: #main loop
        if i > highscore:
            highscore = i
        i = 0
        wall_prime_x = -100000
        wall_image_x = 0
        main_wall = wall_image
        helicopter = Player()
        blocks = [Block()]
        smokes =[Smoke()]
        started = False
        intro()
        started = True
        game_over = False
        move = True
        restart = False

        while not restart: #game loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    move = True
                if event.type == MOUSEBUTTONUP:
                    move = False

            screen.fill(pygame.Color('black'))
            screen.blit(helicopter.image, (PLAYER_X,helicopter.y))

            #displaying the wall:
            if wall_image_x > -2100:
                screen.blit(wall_image, (wall_image_x,0))
                if not game_over: wall_image_x -= WALL_SPEED
            if wall_prime_x > -2100:
                screen.blit(wall_prime,(wall_prime_x,0))
                if not game_over: wall_prime_x -= WALL_SPEED
            if main_wall == wall_image:
                if wall_image_x <= -700:
                    main_wall = wall_prime
                    wall_prime_x = wall_image_x+1399
            elif main_wall == wall_prime:
                if wall_prime_x <= -700:
                    main_wall = wall_image
                    wall_image_x = wall_prime_x+1399

            #blocks:
            for block in blocks:
                block.draw()
                if not game_over: block.update()
                if not block.done and block.x < 100:
                    blocks.append(Block())
                    block.done = True
                if block.x < -50:
                    blocks = blocks[1:]
                #pygame.draw.rect(screen,pygame.Color(color),(block.x,block.y,block.image.get_rect()[2],block.image.get_rect()[3]),2)
            #smoke:
            for smoke in smokes:
                smoke.draw()
                smoke.update()
                if not smoke.done and smoke.x < PLAYER_X - random.randint(15,30):
                    smokes.append(Smoke())
                    smoke.done = True
                if smoke.x < -15:
                    smokes = smokes[1:]

            screen.blit(small_font.render('SCORE: %i'%i,False,pygame.Color(0,100,255)),(50,460))
            screen.blit(small_font.render('BEST: %i'%highscore,False,pygame.Color(0,100,255)),(500,460))

            helicopter.update()

            if helicopter.check_collide():
                pygame.draw.circle(screen, pygame.Color('red'), (PLAYER_X+39,helicopter.y+18), 60, 3)
                pygame.display.update()
                while not restart:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == MOUSEBUTTONDOWN:
                            restart = True


            pygame.display.update()
            clock.tick(FPS)
            i +=1

if __name__ == '__main__':
    main()
