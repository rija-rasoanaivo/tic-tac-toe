import pygame as pg

# Initialisation pygame
pg.init()

WIDTH = 600
HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (100, 100, 100)

fenetre = pg.display.set_mode((WIDTH, HEIGHT))
fenetre.fill(BACKGROUND_COLOR)
pg.display.set_caption("Tic Tac Toe")

# Création de la grille
def creation_grille():
    pg.draw.line(fenetre, LINE_COLOR, (200, 0), (200, 600), 5)
    pg.draw.line(fenetre, LINE_COLOR, (400, 0), (400, 600), 5)
    pg.draw.line(fenetre, LINE_COLOR, (0, 200), (600, 200), 5)
    pg.draw.line(fenetre, LINE_COLOR, (0, 400), (600, 400), 5)

def dessin_croix(x, y):
    pg.draw.line(fenetre, (255, 0, 0), (x*200+50, y*200+50), (x*200+150, y*200+150), 5)
    pg.draw.line(fenetre, (255, 0, 0), (x*200+50, y*200+150), (x*200+150, y*200+50), 5)

def dessin_rond(x, y):
    pg.draw.circle(fenetre, (0, 0, 255), (x*200+100, y*200+100), 50, 5)

current_player = 1
game_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # Représentation du plateau de jeu

def placer_symbole(x, y):
    global current_player
    if game_board[y][x] == 0:  # Vérifier si la case est libre
        if current_player == 1:
            dessin_croix(x, y)
            game_board[y][x] = 1  # Mettre à jour le plateau avec le symbole du joueur 1 (X)
            current_player = -1  # Changer de joueur pour le prochain tour
        else:
            dessin_rond(x, y)
            game_board[y][x] = -1  # Mettre à jour le plateau avec le symbole du joueur 2 (O)
            current_player = 1  # Changer de joueur pour le prochain tour
    else:
        print("Case occupée")

# Boucle de jeu
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            if x < 200 and y < 200:
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

    creation_grille()
    pg.display.flip()

pg.quit()
