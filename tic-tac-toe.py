import pygame as pg
import pygame_menu
#from pygame.locals import *

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

def menu():  
    main_menu = pygame_menu.Menu(width=400, height=300, title='Tic Tac Toe', theme=pygame_menu.themes.THEME_BLUE)
    main_menu.add.button('Joueur contre Joueur', jeux)
    main_menu.add.button('Joueur contre IA')
    main_menu.add.button('Quitter', pygame_menu.events.EXIT) 
    main_menu.mainloop(fenetre)

def retour_menu():
    global game_board, current_player
    game_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    current_player = 1
    menu() 

def jeux():
    # Boucle de jeu
    fenetre.fill(BACKGROUND_COLOR)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                if x < 200 and y < 200: # x = colonne, y = ligne # 1ère case en haut à gauche
                    placer_symbole(0, 0)
                elif x < 400 and y < 200: 
                    placer_symbole(1, 0)
                elif x < 600 and y < 200:
                    placer_symbole(2, 0)
                elif x < 200 and y < 400:
                    placer_symbole(0, 1)
                elif x < 400 and y < 400:
                    placer_symbole(1, 1)
                elif x < 600 and y < 400:
                    placer_symbole(2, 1)
                elif x < 200 and y < 600:
                    placer_symbole(0, 2)
                elif x < 400 and y < 600:
                    placer_symbole(1, 2)
                elif x < 600 and y < 600:
                    placer_symbole(2, 2)

        if victoire() != 0:
            print("Victoire du joueur", victoire())
            afficher_victoire(victoire())
            retour_menu()
            running = False
           
        elif partie_nulle():
            print("Partie nulle")
            afficher_nulle()
            retour_menu()
            running = False
        creation_grille()
        pg.display.flip() 
        pg.display.update() 
        clock.tick(60)
        pass
    pg.quit()

# Création de la grille
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

def victoire():
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


menu()