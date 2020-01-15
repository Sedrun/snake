"""
    Reproduction du jeu Snake que l'on retrouvait sur les premiers téléphones portables :

    composition :
    - une tête (serpent) qui mange ce qui est à sa portée
    - une queue (Queue) qui suit la tête, elle est composée de carrés
        - carrés qui composent la queue :
         ils suivent le principe des vertèbres d'un serpent :
             au temps j, deux vertèbres a, b et une tête t ont des coordonnées
            b : b_x b_y,
            a : a_x,a_y,
            t : t_x,t_y
            au temps j+1 les coordonnées des vertèbres seront :
            b : a_x,a_y
            a : t_x,t_y
            t : déterminées par le joueur

    défauts :
    - parfois la pomme n'est plus au bon endroit
    - si l'on change vite de déplacement on peut parfois retourner sur nos pas



"""

import pygame
import time
import random as rand

successes, failures = pygame.init()
print("Initializing pygame: {0} successes and {1} failures.".format(successes, failures))

# Initialisation
    # variables
score = 0
gameover = 0
largeur = 480
longueur = 480
screen = pygame.display.set_mode((largeur, longueur))
clock = pygame.time.Clock()
FPS = 4
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLOR = BLACK
pygame.mixer.music.load('1114.wav')


    # méthodes
def scoreUpdate(score):
    if score < 40:
        score += 4
    if 40 <= score and score < 80:
        score += 8
    if score > 80:
        score += 16
    return score


    #classes
class Vertebre():
    def __init__(self, vert_x, vert_y):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill(WHITE)
        self.x = vert_x
        self.y = vert_y
        self.rect = self.image.get_rect()
        self.rect.move_ip(vert_x, vert_y)

    def show(self):
        screen.blit(self.image, self.image.get_rect())


class Queue(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.nbVerts = 2
        self.vertebres = [Vertebre(32*6-16, 32*6),Vertebre(32*6-32, 32*6)]

    def show(self):
        for x in self.vertebres:
            x.show()

    # update : met à jour la queue quand on a mangé
    def update(self, newVertebre, ate):
        if ate:
            self.nbVerts += 1
        for i in range(1, self.nbVerts-1):
            self.vertebres[i] = self.vertebres[i + 1]
        self.vertebres.insert(self.nbVerts-1, Vertebre(32*6-16, 32*6))


class Serpent(pygame.sprite.Sprite):
    def __init__(self, q):
        super().__init__()
        self.head = pygame.Surface((32, 32))
        self.image = self.head
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = 32 * 6
        self.y = 32 * 6
        self.velocity = [32, 0]
        self.queue = q
        self.ate = False

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.rect.move_ip(*self.velocity)
        nv = Vertebre(self.x, self.y)
        self.queue.update(nv,self.ate)
        self.ate = False

    def eat(self):
        pygame.mixer.music.play()
        self.ate = True

# variables plus courtes pour une meilleure compréhension
p_coords = [0, 0, 16, 16]
p_x = 0
p_y = 0

class Pomme(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        serpent.rect.move_ip(32 * 6, 32 * 6)
        self.alive = False
        self.growing = 0
        self.x = 0
        self.y = 0
        self.coords = [0, 0, 16, 16]

    def eaten(self):
        self.alive = False
        self.growing = 0
        self.image.fill(BLACK)
        self.rect.move_ip(-self.x, -self.y)
        self.x = 16 * rand.randint(0, (largeur / 16))-16
        self.y = 16 * rand.randint(0, (longueur / 16))-16

    def update(self):
        if self.growing < 11:
            self.growing += 1
        if self.growing == 10:
            self.x = 16 * rand.randint(0, (largeur / 16))-16
            self.y = 16 * rand.randint(0, (longueur / 16))-16
            self.rect.move_ip(self.x, self.y)
            self.image.fill(WHITE)
            self.alive = True


queue = Queue()
serpent = Serpent(queue)
s_x = 32 * 6
s_y = 32 * 6
# serpent.rect.move_ip(s_x, s_y)

pomme = Pomme()

pressed = ''


# thread du jeu
running = True


while running:
    dt = clock.tick(FPS) / 1000  # Returns milliseconds
    screen.fill(BLACK)

    # interactions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and pressed != 's':
                serpent.velocity[1] = -32
                serpent.velocity[0] = 0
                pressed = 'w'
            elif event.key == pygame.K_s and pressed != 'w':
                serpent.velocity[1] = 32
                serpent.velocity[0] = 0
                pressed = 's'
            elif event.key == pygame.K_a and pressed != 'd':
                serpent.velocity[0] = -32
                serpent.velocity[1] = 0
                pressed = 'a'
            elif event.key == pygame.K_d and pressed != 'a':
                serpent.velocity[0] = 32
                serpent.velocity[1] = 0
                pressed = 'd'
            elif event.key == pygame.K_ESCAPE:
                exit()

    # joueur

    # on prend juste un nom plus court pour faciliter la compréhension des calculs
    s_x = serpent.x
    s_y = serpent.y
    # si le joueur dépasse du cadre
    if s_x > largeur or s_y > longueur or s_y < 0 or s_x < 0:
        if gameover == 0:
            gameover = 1

    # serpent a mangé ou non :
    p_x = pomme.x
    p_y = pomme.y
        # cas où le serpent a mangé
    if (s_x > p_x - 32 and s_y > p_y - 32) and (s_x < p_x + 16 and s_y < p_y + 16):
        serpent.eat()
        pomme.eaten()
        score = scoreUpdate(score)


    # Totalité des actions ingame
    if gameover == 0:
        serpent.update()
        pomme.update()
        # Engrenage du jeu
        # graphique jeu
        screen.blit(serpent.image, serpent.rect)
        screen.blit(pomme.image, pomme.rect)

        #test 1

        print(serpent.queue.vertebres[1].x)
        serpent.queue.vertebres[0].x = s_x-16
        serpent.queue.vertebres[0].y = s_y-16
        for i in range(1,serpent.queue.nbVerts):
            serpent.queue.vertebres[i]=serpent.queue.vertebres[i-1]
        serpent.queue.vertebres[0]=Vertebre(s_x,s_y)
        for x in serpent.queue.vertebres:
            screen.blit(x.image, x.rect)
        #fin tests 1
        


        pygame.display.update()

    if gameover >= 1:
        pygame.display.update()  # # le jeu est updated mais pas les objets
        gameover = gameover + 1
        # simplement pour avoir une fin moins rude
        if gameover == 7:
            print("game over \nscore : "+str(score))
            exit()

print("Exited the game loop")
quit()  # Not actually necessary since the script will exit anyway.
