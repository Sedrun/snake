import pygame
from pygame.locals import *
from constantes import *
import random as rand

class Carre:
    def __init__(self, image, x, y, taille):
        self.image = image
        self.x = x
        self.y = y
        self.taille = taille

class Pomme:
    def __init__(self, image, taille):
        self.case_x = rand.randint(0, nombre_sprite_cote-1)
        self.case_y = rand.randint(0, nombre_sprite_cote-1)
        self.x = self.case_x * taille_sprite
        self.y = self.case_y * taille_sprite
        self.taille = taille

    def changement(self):
        self.case_x = rand.randint(0, nombre_sprite_cote-1)
        self.case_y = rand.randint(0, nombre_sprite_cote-1)
        self.x = self.case_x * taille_sprite
        self.y = self.case_y * taille_sprite

class Snake:
    def __init__(self, image, case_x, case_y):
        #position du personnage en case et en pixel
        self.case_x = case_x
        self.case_y = case_y
        self.x = case_x * taille_sprite
        self.y = case_y * taille_sprite
        self.image = image
        #carres
        self.tete = Carre(self.image, self.case_x, self.case_y, taille)
        #NEW
        self.carres = [self.tete,Carre(self.image, self.x-taille_sprite, self.y, taille),Carre(self.image, self.x-2*taille_sprite, self.y, taille)]
        self.nb_carres = 3
        #ENEW
        #direction
        self.direction = "droite"
        #est-il mort ?
        self.estMort = False
    def addCarre(self):
        self.carres.append(Carre(self.image, self.x, self.y, taille))
        self.nb_carres += 1

    def initialisation(self):
        for i in range (self.nb_carres-1, 0, -1):
            self.carres.pop(i)
        #new
        self.estMort = False

    def deplacer(self, direction):
        self.direction = direction
        self.tete.x = self.x
        self.tete.y = self.y
        # Déplacement vers la droite
        if direction == 'droite':
            # Pour ne pas dépasser l'écran
            if self.case_x < (nombre_sprite_cote - 1):
                # Déplacement d'une case
                self.case_x += 1
                # Calcul de la position "réelle" en pixel
                self.x = self.case_x * taille_sprite
            else: self.estMort = True
        #Déplacement vers la gauche
        if direction == 'gauche':
            if self.case_x > 0:
                self.case_x -= 1
                self.x = self.case_x * taille_sprite
            else:
                self.estMort = True

        # Déplacement vers le haut
        if direction == 'haut':
            if self.case_y > 0:
                self.case_y -= 1
                self.y = self.case_y * taille_sprite
            else:
                self.estMort = True

        # Déplacement vers le bas
        if direction == 'bas':
            if self.case_y < (nombre_sprite_cote - 1):
                self.case_y += 1
                self.y = self.case_y * taille_sprite
            else:
                self.estMort = True
        #permet le déplacement de chaque partie du corps
        if self.estMort == False:
            for i in range(self.nb_carres - 1, 0, -1):
                self.carres[i].x = self.carres[i-1].x
                self.carres[i].y = self.carres[i-1].y
    # New
    def accueil(self):
        if self.case_y == 0 and self.case_x < 19:
            self.deplacer('droite')
        if self.case_x == 19 and self.case_y < 19:
            self.deplacer('bas')
        if self.case_y == 19 and self.case_x > 0:
            self.deplacer('gauche')
        if self.case_x == 0 and self.case_y > 0:
            self.deplacer('haut')
    # ENew

class Score:
    def __init__(self):
        self.total = 0

    def ajoute(self):
        if self.total < 40:
            self.total += 4
        if 40 <= self.total and self.total < 80:
            self.total += 8
        else:
            self.total += 16

    def reinitialisation(self):
        self.total = 0

    def afficher(self):
        return fontH2.render("score : " + str(self.total), 1, (255, 255, 255))  # récupération du score en string
