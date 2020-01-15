import pygame
from pygame.locals import *
from classes import *
from constantes import *
import random as rand
import time

pygame.init()


fenetre = pygame.display.set_mode((cote_fenetre, cote_fenetre))
background = pygame.image.load(fond)

image_snake = pygame.image.load(tete).convert_alpha()
image_snake = pygame.transform.scale(image_snake, (taille, taille))

image_pomme = pygame.image.load(pomme).convert_alpha()
image_pomme = pygame.transform.scale(image_pomme, (taille, taille))

mange = pygame.mixer.Sound("sounds/eat.wav")
pygame.mixer.music.load("sounds/song.wav")

continuer = 1
fenetre_accueil = 1
continuer_jeu = 0
game_over = 0
#BOUCLE PRINCIPALE
#NEW
while continuer:
    pygame.mixer.music.play()
    snake = Snake(image_snake, 9, 9)
    snake_accueil = Snake(image_snake, 0, 0)
    for i in range(5) : snake_accueil.addCarre()
    score = Score()
#ENew

    pomme = Pomme(image_pomme, 30)

    fenetre.blit(background, (0, 0))

    direction = 'droite'

#NEW
    #FENETRE D'ACCUEIL
    while fenetre_accueil:
        pygame.time.Clock().tick(FPS)
        # Ecran accueil
        fenetre.blit(texte_accueil, texte_accueil_xy)
        fenetre.blit(texte_jouer, texte_jouer_xy)  # affichage de text_explicatif1
        fenetre.blit(texte_quitter, texte_quitter_xy)  # affichage de text_explicatif2

        snake_accueil.accueil()

        for event in pygame.event.get():
            if event.type == QUIT:
                fenetre_accueil = 0
                continuer = 0
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    score.reinitialisation()
                    continuer_jeu = 1
                    fenetre_accueil = 0
                if event.key == K_ESCAPE:
                    continuer = 0
                    fenetre_accueil = 0

        fenetre.blit(image_snake, (snake_accueil.x, snake_accueil.y))
        image_corps = pygame.image.load(corps).convert_alpha()
        for i in range(1, snake_accueil.nb_carres):
            image_corps = pygame.transform.scale(image_corps, (snake_accueil.carres[i].taille, snake_accueil.carres[i].taille))
            fenetre.blit(image_corps, (snake_accueil.carres[i].x, snake_accueil.carres[i].y))

        pygame.display.flip()  # permet un affichage dynamique dans cette fenêtre (on ne voit plus le serpent
        fenetre.blit(background, (0, 0))
#ENEW
    #BOUCLE DE JEU
    while continuer_jeu:
        print(snake.nb_carres)
        #limitation de vitesse de la boucle
        pygame.time.Clock().tick(FPS)
        for event in pygame.event.get():
            #Si l'utilisateur quitte, on met la variable qui continue le jeu
            #ET la variable générale à 0 pour fermer la fenêtre
            if event.type == QUIT:
                continuer_jeu = 0
                continuer = 0
            elif event.type == KEYDOWN:
                #SI l'utilisateur presse Echap ici, on revient seulement au menu
                if event.key == K_ESCAPE:
                    continuer_jeu = 0
                    continuer = 0
                #Touches de déplacement de Donkey Kong
                elif event.key == K_RIGHT and direction != 'gauche':
                    direction = 'droite'
                    break; #permet d'enlever le demi-tour immédiat
                elif event.key == K_LEFT and direction != 'droite':
                    direction = 'gauche'
                    break;
                elif event.key == K_UP and direction != 'bas':
                    direction = 'haut'
                    break;
                elif event.key == K_DOWN and direction != 'haut':
                    direction = 'bas'
                    break;
        snake.deplacer(direction)
        if snake.case_x == pomme.case_x and snake.case_y == pomme.case_y:
            mange.play()
            pomme.changement()
            snake.addCarre()
            # New
            score.ajoute()
            # ENew

        for i in range(snake.nb_carres-1, 1, -1):
            # vérifie si il est mort
            if snake.tete.x == snake.carres[i].x and snake.tete.y == snake.carres[i].y:
                snake.estMort = True



        #Affichage aux nouvelles positions
        fenetre.blit(background, (0,0))
        fenetre.blit(image_snake, (snake.x, snake.y))
        image_corps = pygame.image.load(corps).convert_alpha()
        for i in range(1, snake.nb_carres):
            image_corps = pygame.transform.scale(image_corps, (snake.carres[i].taille, snake.carres[i].taille))
            fenetre.blit(image_corps, (snake.carres[i].x, snake.carres[i].y))
        fenetre.blit(image_pomme, (pomme.x, pomme.y))

        if snake.estMort:
            snake.reinitialisation()
            continuer_jeu = 0
            game_over = 1

        pygame.display.flip()

    while game_over:
        pygame.mixer.music.stop()
        pygame.time.Clock().tick(FPS)

        texte_score = score.afficher()
        texte_score_rect = texte_score.get_rect()
        score_xy = (cote_fenetre / 2 - texte_score_rect.width / 2, cote_fenetre / 2 - texte_score_rect.width / 2)

        # Ecran fin
        fenetre.blit(text_GO, texte_go_xy)  # affichage de Game Over
        fenetre.blit(score.afficher(), score_xy)  # affichage du score
        fenetre.blit(text_explicatif1, texte_explicatif1_xy)  # affichage de text_explicatif1
        fenetre.blit(text_explicatif2, texte_explicatif2_xy)  # affichage de text_explicatif2

        for event in pygame.event.get():
            if event.type == QUIT:
                game_over = 0
                continuer = 0
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    score.reinitialisation()
                    continuer_jeu = 1
                    game_over = 0
                if event.key == K_ESCAPE:
                    score.reinitialisation()
                    game_over = 0
                    fenetre_accueil = 1
        pygame.display.flip()  # permet un affichage dynamique dans cette fenêtre (on ne voit plus le serpent

        fenetre.blit(background, (0, 0))
