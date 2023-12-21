import pygame as pg
#from pygame.locals import *
import random


pg.init()

WIDTH = 600
HEIGHT = 600
BACKGROUND_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
clock = pg.time.Clock()
fenetre = pg.display.set_mode((WIDTH, HEIGHT))
fenetre.fill(BACKGROUND_COLOR)
current_player = 1
game_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # Représentation du plateau de jeu
pg.display.set_caption("Tic Tac Toe")

#partie joueur contre IA
def check_gagnant():
    global game_board, current_player
    # Vérifier les lignes
    for i in range(3):
        if game_board[i][0] == game_board[i][1] == game_board[i][2] != 0: # Vérifier si les 3 cases de la ligne sont identiques et non vides # != 0 pour éviter les lignes vides
            dessin_ligne_victoire_horizontal(ligne=i, joueur=game_board[i][0])
            pg.display.flip()  # Mettre à jour l'écran une dernière fois
            pg.time.wait(500)  # Pause d'une demi-seconde 
            return game_board[i][0] # [i] = Ligne # [i][0] = 1ère case de la ligne # [i][1] = 2ème case de la ligne # [i][2] = 3ème case de la ligne 
    # Vérifier les colonnes
    for i in range(3):
        if game_board[0][i] == game_board[1][i] == game_board[2][i] != 0:
            dessin_ligne_victoire_vertical(colonne=i, joueur=game_board[0][i])
            pg.display.flip()  # Mettre à jour l'écran une dernière fois
            pg.time.wait(500)  
            return game_board[0][i]
    # Vérifier les diagonales
    if game_board[0][0] == game_board[1][1] == game_board[2][2] != 0:
        dessin_ligne_victoire_diagonale1(joueur=game_board[0][0])
        pg.display.flip()  
        pg.time.wait(500) 
        return game_board[0][0]
    if game_board[0][2] == game_board[1][1] == game_board[2][0] != 0:
        dessin_ligne_victoire_diagonale2(joueur=game_board[0][2])
        pg.display.flip()  
        pg.time.wait(500)  
        return game_board[0][2]
    return 0

def faire_mouvement():
    global game_board, current_player
    mouvement_possible = [(i, j) for i in range(3) for j in range(3) if game_board[i][j] == 0]

    if not mouvement_possible:
        return None
    
    for mouvement in mouvement_possible:
        game_board[mouvement[0]][mouvement[1]] = current_player
        if check_gagnant() == current_player:
            return mouvement
        game_board[mouvement[0]][mouvement[1]] = 0

    # Si tous les mouvements possibles sont occupés, l'IA choisit une case aléatoire parmi les cases libres
    while True:
        random_move = random.choice(mouvement_possible)
        if game_board[random_move[0]][random_move[1]] == 0:
            return random_move


def joueur_vs_ia():
    # Boucle de jeu
    global current_player
    fenetre.fill(BACKGROUND_COLOR)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if current_player == 1:  # Tour du joueur humain (Joueur 1)
                    x, y = pg.mouse.get_pos()
                    x //= 200
                    y //= 200
                    if game_board[y][x] == 0:  # Vérifier si la case est libre
                        placer_symbole(x, y)  # Placer le symbole du joueur

                        # Vérifier s'il y a un gagnant ou une partie nulle après le coup du joueur
                        if check_gagnant() != 0:
                            print("Victoire du joueur", check_gagnant())
                            afficher_victoire(check_gagnant())
                           
                            running = False
                            break
                        elif partie_nulle():
                            print("Partie nulle")
                            afficher_nulle()
                           
                            running = False
                            break

                        current_player = 2  # Changer pour le tour de l'IA (Joueur 2)

        if current_player == 2 and running:  # Tour de l'IA (Joueur 2)
            mouvement = faire_mouvement()  # Effectuer le mouvement de l'IA
            if mouvement:
                placer_symbole(mouvement[0], mouvement[1])  # Placer le symbole de l'IA
                
                # Vérifier s'il y a un gagnant ou une partie nulle après le coup de l'IA
                if check_gagnant() != 0:
                    print("Victoire de l'IA")
                    afficher_victoire(check_gagnant())
                    running = False
                elif partie_nulle():
                    print("Partie nulle")
                    afficher_nulle()
                    running = False

                current_player = 1  # Changer pour le tour du joueur humain (Joueur 1)
            else:
                print("Aucun mouvement possible")
                running = False

        # Mettre à jour l'affichage
        creation_grille()
        pg.display.flip()
        pg.display.update()
        clock.tick(60)
        
    # Quitter Pygame
    pg.quit()

def creation_grille():
    pg.draw.line(fenetre, LINE_COLOR, (200, 0), (200, 600), 15)
    pg.draw.line(fenetre, LINE_COLOR, (400, 0), (400, 600), 15)
    pg.draw.line(fenetre, LINE_COLOR, (0, 200), (600, 200), 15)
    pg.draw.line(fenetre, LINE_COLOR, (0, 400), (600, 400), 15)

def dessin_croix(x, y):
    pg.draw.line(fenetre, (66, 66, 66), (x*200+50, y*200+50), (x*200+150, y*200+150), 5)
    pg.draw.line(fenetre, (66, 66, 66), (x*200+50, y*200+150), (x*200+150, y*200+50), 5)

def dessin_rond(x, y):
    pg.draw.circle(fenetre, (239, 231, 200), (x*200+100, y*200+100), 50, 5)

def placer_symbole(x, y):
    global current_player
    while game_board[y][x] != 0 and current_player == 2:  # Vérifie si la case est occupée et si c'est le tour de l'IA
        mouvement = faire_mouvement()  # L'IA joue à nouveau
        if mouvement:
            x, y = mouvement  # Mettre à jour les coordonnées pour placer le symbole de l'IA
        else:
            print("Aucun mouvement possible pour l'IA")
            break

    if game_board[y][x] == 0:  # Vérifier si la case est libre
        if current_player == 1:
            dessin_croix(x, y)
            game_board[y][x] = 1  # Mettre à jour le plateau avec le symbole du joueur 1 (X)
            current_player = 2  # Changer de joueur pour le prochain tour
        else:
            dessin_rond(x, y)
            game_board[y][x] = 2  # Mettre à jour le plateau avec le symbole du joueur 2 (O)
            current_player = 1  # Changer de joueur pour le prochain tour
    else:
        print("Case occupée")

def dessin_ligne_victoire_vertical(colonne, joueur):
    posX = colonne * 200 + 100
    if joueur == 1:
        couleur = (255, 0, 0)
    else:
        couleur = (0, 0, 255)
    pg.draw.line(fenetre, couleur, (posX, 15), (posX, 585), 5)

def dessin_ligne_victoire_horizontal(ligne, joueur):
    posY = ligne * 200 + 100
    if joueur == 1:
        couleur = (255, 0, 0)
    else:
        couleur = (0, 0, 255)
    pg.draw.line(fenetre, couleur, (15, posY), (585, posY), 5)

def dessin_ligne_victoire_diagonale1(joueur):
    if joueur == 1:
        couleur = (255, 0, 0)
    elif joueur == 2:
        couleur = (0, 0, 255)
    pg.draw.line(fenetre, couleur, (15, 15), (585, 585), 5)

def dessin_ligne_victoire_diagonale2(joueur):
    if joueur == 1:
        couleur = (255, 0, 0)
    elif joueur == 2:
        couleur = (0, 0, 255)
    pg.draw.line(fenetre, couleur, (15, 585), (585, 15), 5)

def afficher_victoire(joueur):
    font = pg.font.Font(None, 36)  # Charge une police de taille 36 (vous pouvez changer cela)
    if joueur == 1:
        message = font.render("Victoire du joueur 1!", True, (255, 0, 0))  # Rouge pour le joueur 1
    else:
        message = font.render("Victoire du joueur 2!", True, (0, 0, 255))  # Bleu pour le joueur 2
    
    fenetre.fill(BACKGROUND_COLOR)  # Efface l'écran
    fenetre.blit(message, (150, 250))  # Affiche le message à une position spécifique
    
    pg.display.flip()  # Met à jour l'écran
        # Pause pendant 2 secondes
    temps_actuel = pg.time.get_ticks()  # Obtenez le temps écoulé depuis le début du jeu
    attente = True
    while attente:
        temps = pg.time.get_ticks() - temps_actuel
        if temps > 500:  # 2000 millisecondes (2 secondes)
            attente = False

def partie_nulle():
    for i in range(3):
        for j in range(3): 
            if game_board[i][j] == 0:
                return False
    return True

def afficher_nulle():
    font = pg.font.Font(None, 36)
    message = font.render("Partie nulle!", True, (0, 0, 0))
    fenetre.fill(BACKGROUND_COLOR)
    fenetre.blit(message, (150, 250))
    pg.display.flip()
    temps_actuel = pg.time.get_ticks()
    attente = True
    while attente:
        temps = pg.time.get_ticks() - temps_actuel
        if temps > 1000:
            attente = False


joueur_vs_ia()