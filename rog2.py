## imports

from ast import Not
from xml.etree.ElementTree import PI
import pygame as pg
import random
from random import randint
from itertools import product
import numpy as np
import secrets

## constantes

CIEL = (187, 210, 225)
CELADON = (131, 166, 151)
RED = (186, 0, 0)
GRIS = (175, 175, 175)
CERULEAN = (42, 82, 190)
SAPIN = (9, 82, 40)
SIZE = 25
PIXEL_SIZE = 30
    
class Game:
    """
    Initialise le jeu
    """
    def __init__(self):
        self.map = np.full((25,50), None)
        # |
        self.map[3:20, 14] = '|'
        self.map[3:20, 18] = '|'
        self.map[:8, 1] = '|'
        self.map[:8, 8] = '|'
        self.map[15:20, 1] = '|'
        self.map[15:20, 11] = '|'
        self.map[9:14, 9] = '|'
        self.map[9:14, 12] = '|'
        self.map[10:13, 1] = '|'
        self.map[10:13, 4] = '|'

        # - 
        self.map[0][1:9] = '-'
        self.map[7][1:9] = '-'
        self.map[10][1:5] = '-'
        self.map[12][1:5] = '-'
        self.map[15][1:12] = '-'
        self.map[19][1:12] = '-'
        self.map[3][14:19] = '-'
        self.map[19][14:19] = '-'
        self.map[7, 15:18] = '-'
        self.map[9, 9:13] = '-'
        self.map[13, 9:13] = '-'

        # sol
        self.map[1:7, 2:8] = '.'
        self.map[11, 2:4] = '.'
        self.map[16:19, 2:11] = '.'
        self.map[4:7, 15:18] = '.'
        self.map[8:19, 15:18] = '.'
        self.map[10:13, 10:12] = '.'


        # chemin
        self.map[8:11, 6] = '#'
        self.map[11, 5:8] = '#'
        self.map[11:15, 7] = '#'
        self.map[17, 12:14] = '#'
        self.map[2, 11:17] = '#'
        self.map[2:5, 11] = '#'
        self.map[4, 8:12] = '#'

        # porte
        self.map[7, 6] = '+'
        self.map[11, 4] = '+'
        self.map[15, 7] = '+'
        self.map[17, 14] = '+'
        self.map[3, 16] = '+'
        self.map[7,16] = '+'
        self.map[17, 11] = '+'
        self.map[4, 8] = '+'
        self.map = np.transpose(self.map)

        self.dots = np.full((25,25), None)
        for (i, j) in product(range(21), range(21)):    
            if self.map[i, j] in ['.','#'] :
                self.dots[i,j] = 1
        self.sac = {'taille' : 0, 'vie': 10, 'argent' : 0}
        self.taille_sac = 5
        self.mat_obj = np.full((25,25), None)
        self.names_obj = ['*','j','!','(','&','o']
        self.x_position = 2
        self.y_position = 5
        self.accessible_pos = ['.', '+', '#']
        self.colors = {'wall' : CELADON, 'floor': GRIS, 'empty': CIEL, 'road': GRIS}
        pg.init()
        self.clock = pg.time.Clock()
        self.screen= pg.display.set_mode((SIZE * PIXEL_SIZE, SIZE * PIXEL_SIZE))
        pg.display.flip()
        self.font = pg.font.SysFont('arial', 20)

    
    def draw_char(self,text, position, font, color=GRIS, background=GRIS):
        return font.render(text, False, color, background), position


    def placement_aleat(self):
        for k in range(10) :
            new_obj = secrets.choice(self.names_obj) # on choisit un objet au hasard
            i,j = randint(0, 24), randint(0, 24) #on choisit un triplet dans la liste de Tonio
            while self.dots[i,j] != 1 : #si la place est déjà occupée ou non accessible
                i,j = randint(0, 24), randint(0, 24)
            self.mat_obj[i,j] = new_obj
            self.dots[i,j] = 0 #La place est occupée
        
    
    def authorized_movement(self, mvmt):
        if mvmt == 'up':
            if self.y_position and map[self.x_position, self.y_position - 1] in self.accessible_pos:
                return True
            return False
        if mvmt == 'down':
            if self.y_position < SIZE - 1 and map[self.x_position, self.y_position + 1] in self.accessible_pos:
                return True
            return False
        if mvmt == 'left':
            if self.x_position and map[self.x_position - 1, self.y_position] in self.accessible_pos:
                return True
            return False
        if mvmt == 'right': 
            if self.x_position < SIZE - 1 and map[self.x_position + 1, self.y_position] in self.accessible_pos:
                return True
            return False
    

    def draw_rect(self,i, j,color):
        rect = pg.Rect(i*PIXEL_SIZE, j*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
        pg.draw.rect(self.screen, color, rect)
    

    def draw_set(self):
        for i, j in product(range(SIZE), range(SIZE)):
            if self.map[i, j] == '#':
                self.draw_rect(i, j, self.colors['road'])
            elif self.map[i, j] == '-' or self.map[i,j] == '|':
                self.draw_rect(i, j, self.colors['wall'])
            elif self.map[i, j] == '.' or self.map[i, j] == '+':
                self.draw_rect(i, j, self.colors['floor'])
    
class Objet :
    """prend un objet avec un nom (str affiché sur la map), un type (arme, armure...)
    """
    def __init__(self, name):
        self.name = name #un array d'une lettre
         #On rajoute un num ????

    def take(self, Prendre,game) : #Pour l'instant on prend les pièces une par une à voir comment on fait pour le nombre
        if game.sac['taille'] >= game.taille_sac:
            return None
        if self.name == '*':
            game.sac['argent']+=1
            game.mat_obj[game.x_position, game.y_position] = None
            game.dots[game.x_position, game.y_position] = 1
            #Modification de la matrice objet
            new_obj = secrets.choice(game.names_obj) # on choisit un objet au hasard
            i,j = randint(0, 24), randint(0, 24) #on choisit un triplet dans la liste de Tonio
            while game.dots[i,j] != 1 : #si la place est déjà occupée ou non accessible
                i,j = randint(0, 24), randint(0, 24)
            game.mat_obj[i,j] = new_obj
            game.dots[i,j] = 0 #La place est occupée
            
        if Prendre == True :
            if self.name == 'j': #potion magique qui remet la vie à 10 points
                game.sac['vie'] = 10
            elif self.name in game.sac :            
                game.sac[self.name] += 1
                game.sac['taille']+= 1
            else :
                game.sac[self.name] = 1
                game.sac['taille']+=1
            game.mat_obj[game.x_position, game.y_position] = None
            game.dots[game.x_position, game.y_position] = 1
            new_obj = secrets.choice(game.names_obj) # on choisit un objet au hasard
            i,j = randint(0, 24), randint(0, 24) #on choisit un triplet dans la liste de Tonio
            while game.dots[i,j] != 1 : #si la place est déjà occupée ou non accessible
                i,j = randint(0, 24), randint(0, 24)
            game.mat_obj[i,j] = new_obj
            game.dots[i,j] = 0 #La place est occupée

class Monstre :
    """
    args : power (1 or 2) whether it's a small (m) or big (M) monster
    """
    def __init__(self, power, x_pos, y_pos):
        if power == 1:
            self.proba = 0.5
            self.name = 'm'
        if power == 2:
            self.proba = 0.2
            self.name = 'M'
        self.x_pos = x_pos
        self.y_pos = y_pos

    def fight(self,game):
        succes = random.uniform(0, 1)
        if '!' in game.sac.keys() and game.sac['!'] >= 1:
            succes += 0.2
            game.sac['!'] -= 1
        if '(' in game.sac.keys() and game.sac['('] >= 1:
            succes += 0.1
            game.sac['('] -= 1
        if succes <= self.proba: #fight lost
            if '&' in game.sac.keys() and game.sac['&'] >= 1:
                game.sac['vie'] -= 3
                game.sac['&'] -= 1
            else:
                game.sac['vie'] -= 5
        else: #fight won
            game.sac['argent'] += 3
        x_pos, y_pos = np.random.randint(25), np.random.randint(25)
        while not(game.dots[x_pos, y_pos]) or (x_pos == game.x_position and y_pos == game.y_position):
            x_pos, y_pos = np.random.randint(25), np.random.randint(25)
        self.x_pos = x_pos
        self.y_pos = y_pos

    def authorized_movement_monster(self, mvmt, game):
        if mvmt == 'up':
            if self.y_pos and game.map[self.x_pos, self.y_pos - 1] in game.accessible_pos:
                return True
            return False
        if mvmt == 'down':
            if self.y_pos < SIZE - 1 and game.map[self.x_pos, self.y_pos + 1] in game.accessible_pos:
                return True
            return False
        if mvmt == 'left':
            if self.x_pos and game.map[self.x_pos - 1, self.y_pos] in game.accessible_pos:
                return True
            return False
        if mvmt == 'right': 
            if self.x_pos < SIZE - 1 and game.map[self.x_pos + 1, self.y_pos] in game.accessible_pos:
                return True
            return False

    def monster_moves(self, game):
        x = monster.x_pos
        y = monster.y_pos
        mvmt = np.random.choice(['up', 'down', 'left', 'right'])
        while not(self.authorized_movement_monster(mvmt,game)):
            mvmt = np.random.choice(['up', 'down', 'left', 'right'])
        if mvmt == 'up': 
            return x, y - 1
        if mvmt == 'down':
            return x, y + 1
        if mvmt == 'left':
            return x - 1, y
        if mvmt == 'right':
            return x + 1, y
            
## jeu

if __name__ == "__main__":

    running = True
    caption = 'Play ROG game'
    count = 0
    monsters = [Monstre(1, 3, 4), Monstre(1, 18, 5), Monstre(2, 14, 15)]
    game = Game()
    game.placement_aleat()
    while running:
        game.screen.fill(CIEL)
        game.clock.tick(4)
        # affichage plateau de jeu
        game.draw_set()
        for i, j in product(range(SIZE), range(SIZE)):
            if i == game.x_position and j == game.y_position:
                img, pos = game.draw_char('@', (i*PIXEL_SIZE, j*PIXEL_SIZE), game.font, color = RED)
                game.screen.blit(img, pos)
            elif game.mat_obj[i, j]:
                img, pos = game.draw_char(game.mat_obj[i,j], (i*PIXEL_SIZE, j*PIXEL_SIZE), game.font, color = SAPIN)
                game.screen.blit(img, pos)
            # elif MAP[i,j]:
            #     img, pos = draw_char(MAP[i, j], (i*PIXEL_SIZE, j*PIXEL_SIZE), font=font_arial)
            #     screen.blit(img, pos)
            # img, pos = draw_char('inventaire', (1*PIXEL_SIZE, 21*PIXEL_SIZE), font=font_arial, color = CELADON)
            # screen.blit(img, pos)
        for i, elements in enumerate(game.sac.keys()):
            img, pos = game.draw_char(f"{elements}:{game.sac[elements]}", (5*i*PIXEL_SIZE, 23*PIXEL_SIZE), game.font, color=CELADON)
            game.screen.blit(img, pos)
        # affichage messages
        if caption:
            pg.display.set_caption(caption)
        # itération sur tous les événements
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    running = False
                elif event.key == pg.K_UP:
                    # on reste dans le screen et on peut accéder à la case
                    if game.y_position and game.map[game.x_position, game.y_position - 1] in game.accessible_pos:
                        game.y_position -= 1
                elif event.key == pg.K_DOWN:
                    if game.y_position < SIZE - 1 and game.map[game.x_position, game.y_position + 1] in game.accessible_pos:
                        game.y_position += 1
                elif event.key == pg.K_LEFT:
                    if game.x_position and game.map[game.x_position - 1, game.y_position] in game.accessible_pos:
                        game.x_position -= 1
                elif event.key == pg.K_RIGHT:
                    if game.x_position and game.map[game.x_position + 1, game.y_position] in game.accessible_pos:
                        game.x_position += 1
            if game.mat_obj[game.x_position, game.y_position]:
                object = Objet(game.mat_obj[game.x_position, game.y_position])
                caption = "Prendre l'objet ? (press y)"
                pg.display.set_caption(caption)
                prendre = False
                if event.type == pg.KEYDOWN:
                    caption = "Play ROG game" 
                    pg.display.set_caption(caption)
                    if event.key == pg.K_y:
                        prendre = True
                object.take(prendre,game) 
            else:
                if (game.x_position == 10 or game.x_position == 11) and game.y_position <= 12 and game.y_position >= 10:
                    caption = "T'es piégé hahaha!"
                else:
                    caption = 'Play ROG game'
                pg.display.set_caption(caption)
            for monster in monsters:
                if monster.x_pos == game.x_position and monster.y_pos == game.y_position:
                    monster.fight(game)    
        for monster in monsters:
            img, pos = game.draw_char(monster.name, (monster.x_pos*PIXEL_SIZE, monster.y_pos*PIXEL_SIZE), game.font, color = CERULEAN)
            game.screen.blit(img, pos)
            if not(count % 3):
                x, y = monster.monster_moves(game)
                monster.x_pos = x
                monster.y_pos = y
        count += 1
        if (game.x_position, game.y_position) == (2, 1):
            game.x_position, game.y_position = 10, 10
            caption = "T'es piégé hahaha!"
            pg.display.set_caption(caption)
        if game.sac['vie'] <= 0:
            running = False
            print("You lost the game")
        pg.display.update()
    pg.quit()









