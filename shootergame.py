from pygame import *
from random import randint
from time import time as timer


win_w = 700
win_h = 500
window = display.set_mode((win_w, win_h))
display.set_caption("Shooter Game!")

font.init()
font = font.SysFont("Arial", 50)
win = font.render("You won!", True, (0, 200, 0))
lose = font.render("You lost ", True, (255, 0, 0))

fired = 0
score = 0
lost = 10
goal = 20
miss = 0

enemyimage = "ufo.png"
asteroidimage = "asteroid.png"
bulletimage = "bullet.png"

mixer.init()
mixer.music.load("space.ogg")
#mixer.music.play()



class Gamesprite(sprite.Sprite):
    def __init__(self, player_image, playerx, playery, sizex, sizey, playerspeed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (sizex, sizey))
        self.speed = playerspeed
        self.rect = self.image.get_rect()
        self.rect.x = playerx
        self.rect.y = playery

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Gamesprite):
    
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 625:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(bulletimage, self.rect.centerx, self.rect.top, 10 , 15 , -15)
        bullets.add(bullet)

class Enemy(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        global miss
        if self.rect.y > win_h:
            self.rect.x = randint(70, win_w - 70)
            self.rect.y = 0
            miss = miss + 1

ufos = sprite.Group()
asteroids = sprite.Group()
bullets = sprite.Group()


class Bullet(Gamesprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()            


for _ in range(3):
    ufo = Enemy(enemyimage, randint(70, win_w - 70), -40, 70, 40, randint(1, 3))
    ufos.add(ufo)

for _ in range(2):
    asteroid = Enemy(asteroidimage, randint(70, win_w - 70), -40, 70, 40, randint(1, 3))
    asteroids.add(asteroid)

        
background = transform.scale(image.load("galaxy.jpg"), (700,500))
rocket = Player("rocket.png", 100, 400, 60, 90, 6)


clock = time.Clock()
FPS = 60
run = True
finish = False
reloading = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if fired < 5 and reloading == False:
                    fired = fired + 1
                    rocket.shoot()

                if fired >=5 and reloading == False:
                    last_time = timer()
                    reloading = True   





                 


    if not finish: 
        window.blit(background,(0,0))

        ufos.update()
        bullets.update()
        asteroids.update()

        rocket.update()
        rocket.reset()

        ufos.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if reloading == True:
            current_time = timer()

            if current_time - last_time < 3:
                reloadtext = font.render("Reloading . . .", 1, (255, 255, 255))
                window.blit(reloadtext, (250, 400))
            else:
                fired = 0
                reloading = False


        collides = sprite.groupcollide(ufos, bullets, True, True)


        for c in collides:
            score = score + 1
            ufo = Enemy(enemyimage, randint(70, win_w - 70), -40, 70, 40, randint(1, 3))
            ufos.add(ufo)
    

        missed = font.render("Missed: " + str(miss), 1, (255,255,255))
        window.blit(missed, (10,50))

        scoretext = font.render("Score: " + str(score), 1, (255,255,255))
        window.blit(scoretext, (10, 10))

        if sprite.spritecollide(rocket, ufos, False) or miss >= lost:
            window.blit(lose, (250, 200))
            finish = True

        if sprite.spritecollide(rocket, asteroids, False):
            window.blit(lose, (250,200))
            finish = True

        if score >= goal:
            window.blit(win, (250, 200))
            finish = True



    display.update()
    clock.tick(FPS)
 

