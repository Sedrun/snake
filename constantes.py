import pygame

pygame.init() #NEW

#Paramètre de la fenêtre
nombre_sprite_cote = 20
taille_sprite = 30
cote_fenetre = nombre_sprite_cote * taille_sprite
FPS = 30
hauteur_menu = 60


taille = 30
tete = "images/tetete.png"
corps = "images/tete2.png"
fond = "images/fond.png"
pomme = "images/pomme.png"
sound = "images/sound.png"
mute = "images/mute.png"


#New
fontTitre = pygame.font.Font(None,65) # font de gros titre
fontH2 = pygame.font.Font(None,40) # font de choses importantes mais pas gros titre

texte_accueil = fontTitre.render("Le jeu du Snake",1,(255,255,255))
texte_accueil_rect = texte_accueil.get_rect()

texte_jouer = fontH2.render("Espace pour commencer une partie",1,(255,255,255))
texte_jouer_rect = texte_jouer.get_rect()

texte_quitter = fontH2.render("Echap pour quitter",1,(255,255,255))
texte_quitter_rect = texte_quitter.get_rect()

text_GO = fontTitre.render("Game Over",1,(255,255,255))
text_GO_rect = text_GO.get_rect() #pour obtenir les dimensions du text

text_explicatif1 = fontH2.render("Espace pour rejouer",1,(255,255,255))
text_explicatif1_rect = text_explicatif1.get_rect()

text_explicatif2 = fontH2.render("Echap pour revenir au menu principal",1,(255,255,255))
text_explicatif2_rect = text_explicatif2.get_rect()


texte_accueil_xy = (cote_fenetre/2 - texte_accueil_rect.width/2,cote_fenetre/4 - texte_accueil_rect.height/2)

texte_go_xy = (cote_fenetre/2 - text_GO_rect.width/2,cote_fenetre/4 - text_GO_rect.height/2)
texte_jouer_xy = (cote_fenetre/2 - texte_jouer_rect.width/2, cote_fenetre/10*5 - texte_jouer_rect.height/2)
texte_quitter_xy = (cote_fenetre/2 - texte_quitter_rect.width/2, cote_fenetre/10*6 - texte_quitter_rect.height/2)
texte_explicatif1_xy = (cote_fenetre/2 - text_explicatif1_rect.width/2, cote_fenetre/10*6 - text_explicatif1_rect.height/2)
texte_explicatif2_xy = (cote_fenetre/2 - text_explicatif2_rect.width/2, cote_fenetre/10*7 - text_explicatif2_rect.height/2)

#ENEW