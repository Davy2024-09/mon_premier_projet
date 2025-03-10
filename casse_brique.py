import pygame
import sys

# Initialisation de pygame
pygame.init()

# Paramètres de la fenêtre
LARGEUR, HAUTEUR = 800, 600
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Casse-Briques")

# Couleurs
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)
VERT = (0, 255, 0)
NOIR = (0, 0, 0)
JAUNE = (255, 255, 0)

# Horloge pour contrôler le framerate
horloge = pygame.time.Clock()

# Paramètres de la raquette
LARGEUR_RAQUETTE = 300
HAUTEUR_RAQUETTE = 20
RAQUETTE_VITESSE = 10
raquette = pygame.Rect(LARGEUR // 2 - LARGEUR_RAQUETTE // 2, HAUTEUR - 50, LARGEUR_RAQUETTE, HAUTEUR_RAQUETTE)

# Paramètres de la balle
RAYON_BALLE = 10
balle = pygame.Rect(LARGEUR // 2 - RAYON_BALLE, HAUTEUR // 2 - RAYON_BALLE, RAYON_BALLE * 2, RAYON_BALLE * 2)
BALLE_VITESSE_X, BALLE_VITESSE_Y = 5, -5

# Score
score = 0
police = pygame.font.Font(None, 36)

# Niveaux
niveaux = [
    # Niveau 1
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    # Niveau 2
    [
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    ],
    # Niveau 3
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
]
niveau_actuel = 0
briques = []

# Fonction pour créer les briques du niveau actuel
def creer_briques():
    global briques
    briques = []
    for i in range(len(niveaux[niveau_actuel])):
        for j in range(len(niveaux[niveau_actuel][i])):
            if niveaux[niveau_actuel][i][j] == 1:
                brique = pygame.Rect(j * (LARGEUR_BRIQUE + ESPACEMENT) + ESPACEMENT, 
                                 i * (HAUTEUR_BRIQUE + ESPACEMENT) + ESPACEMENT, 
                                 LARGEUR_BRIQUE, HAUTEUR_BRIQUE)
                briques.append(brique)

# Créer les briques du premier niveau
LARGEUR_BRIQUE = 75
HAUTEUR_BRIQUE = 30
ESPACEMENT = 5
creer_briques()

# Menu de démarrage
def afficher_menu():
    fenetre.fill(NOIR)
    texte_titre = police.render("Casse-Briques", True, BLANC)
    texte_start = police.render("Appuyez sur ESPACE pour commencer", True, BLANC)
    fenetre.blit(texte_titre, (LARGEUR // 2 - texte_titre.get_width() // 2, HAUTEUR // 3))
    fenetre.blit(texte_start, (LARGEUR // 2 - texte_start.get_width() // 2, HAUTEUR // 2))
    pygame.display.flip()

# Fonction principale du jeu
def jeu():
    global BALLE_VITESSE_X, BALLE_VITESSE_Y, score, niveau_actuel

    en_jeu = False
    while True:
        if not en_jeu:
            afficher_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        en_jeu = True
            continue

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Déplacement de la raquette
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT] and raquette.left > 0:
            raquette.move_ip(-RAQUETTE_VITESSE, 0)
        if touches[pygame.K_RIGHT] and raquette.right < LARGEUR:
            raquette.move_ip(RAQUETTE_VITESSE, 0)

        # Déplacement de la balle
        balle.move_ip(BALLE_VITESSE_X, BALLE_VITESSE_Y)

        # Collisions avec les murs
        if balle.left <= 0 or balle.right >= LARGEUR:
            BALLE_VITESSE_X *= -1
        if balle.top <= 0:
            BALLE_VITESSE_Y *= -1
        if balle.bottom >= HAUTEUR:
            # Perdu : réinitialiser la balle et la raquette
            balle.x, balle.y = LARGEUR // 2 - RAYON_BALLE, HAUTEUR // 2 - RAYON_BALLE
            raquette.x = LARGEUR // 2 - LARGEUR_RAQUETTE // 2
            BALLE_VITESSE_X, BALLE_VITESSE_Y = 5, -5
            en_jeu = False
            score = 0
            niveau_actuel = 0
            creer_briques()

        # Collision avec la raquette
        if balle.colliderect(raquette):
            BALLE_VITESSE_Y *= -1

        # Collision avec les briques
        for brique in briques[:]:
            if balle.colliderect(brique):
                BALLE_VITESSE_Y *= -1
                briques.remove(brique)
                score += 10

        # Passer au niveau suivant si toutes les briques sont détruites
        if not briques:
            niveau_actuel += 1
            if niveau_actuel >= len(niveaux):
                niveau_actuel = 0
            creer_briques()
            balle.x, balle.y = LARGEUR // 2 - RAYON_BALLE, HAUTEUR // 2 - RAYON_BALLE
            raquette.x = LARGEUR // 2 - LARGEUR_RAQUETTE // 2
            BALLE_VITESSE_X, BALLE_VITESSE_Y = 5, -5

        # Affichage
        fenetre.fill(NOIR)
        pygame.draw.rect(fenetre, BLEU, raquette)
        pygame.draw.ellipse(fenetre, ROUGE, balle)
        for brique in briques:
            pygame.draw.rect(fenetre, VERT, brique)

        # Afficher le score
        texte_score = police.render(f"Score : {score}", True, BLANC)
        fenetre.blit(texte_score, (10, 10))

        # Afficher le niveau
        texte_niveau = police.render(f"Niveau : {niveau_actuel + 1}", True, BLANC)
        fenetre.blit(texte_niveau, (LARGEUR - texte_niveau.get_width() - 10, 10))

        # Mise à jour de l'affichage
        pygame.display.flip()
        horloge.tick(60)  # Limite à 60 FPS

# Lancer le jeu
jeu()
