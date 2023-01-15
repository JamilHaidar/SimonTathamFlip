from utils import *
import random
class Grid:
    def __init__(self,n) -> None:
        self.n = n
        self.transition_matrix = generate_transition(n)
        self.reset_board()
    
    def reset_board(self):
        self.moves = 0
        self.winning_moves = self.moves
        self.apply_moves()

    def solve_game(self):
        M = []
        for i in range(self.n*self.n):
            M.append(self.transition_matrix[i]<<1 | (self.board>>(self.n*self.n-i-1))&1)
        M = solve_game(M,self.n)
        self.winning_moves = ravel(extract_matrix(M,start_column=self.n*self.n))
        return self.winning_moves

    def move(self,cell_index):
        self.moves = perform_move(self.moves,self.n,cell_index)
        self.apply_moves()

    def apply_moves(self):
        self.board = inner_mul(self.transition_matrix,[self.moves],self.n*self.n)[0]

    def randomize(self):
        for i in range(self.n*self.n):
            if random.random()>0.6:
                self.moves ^= 1<<i
        self.apply_moves()

    def __repr__(self) -> str:
        res = ''
        selection = ((1<<(self.n))-1)<<(self.n*(self.n-1))
        for i in range(self.n):
            res+= f'{((self.board&selection)>>(self.n*(self.n-i-1))):0{self.n}b}\n'
            selection = selection>>self.n
        return res

# grid = Grid(4)
# grid.randomize()
# print(grid)
# print_board(grid.moves,grid.n)

import pygame
import sys

RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255,255,255)
GREY = (180,180,180)
DARK_GREY = (120,120,120)
FPS=20

class GameController:
    def __init__(self,screen,n=5) -> None:
        self.screen = screen
        scale = min(screen.get_width(),screen.get_height())//(n+1)
        self.scale = scale
        self.clock = pygame.time.Clock()

        self.offset = scale//20
        self.ox = (screen.get_width()-n*scale)//2
        self.oy = (screen.get_height()-n*scale)//2
        self.solve_mode = False

        self.grid = Grid(n)
        self.grid.randomize()
        self.n = n
        self.winning_moves = self.grid.moves

    def draw_grid(self):
        self.screen.fill(GREY)
        selection = 1<<(self.n*self.n-1)
        for y in range(self.n):
            for x in range(self.n):
                if (self.grid.board&selection)==0:
                    if self.solve_mode:
                        pygame.draw.polygon(self.screen, WHITE,[(self.ox+x*self.scale,self.oy+y*self.scale),(self.ox+(x+1)*self.scale,self.oy+y*self.scale),(self.ox+(x+1)*self.scale,self.oy+(y+1)*self.scale),(self.ox+x*self.scale,self.oy+(y+1)*self.scale)])
                    else:
                        pygame.draw.polygon(self.screen, WHITE,[(self.ox+x*self.scale,self.oy+y*self.scale),(self.ox+(x+1)*self.scale,self.oy+y*self.scale),(self.ox+(x+1)*self.scale,self.oy+(y+1)*self.scale),(self.ox+x*self.scale,self.oy+(y+1)*self.scale)])
                else:
                    pygame.draw.polygon(self.screen, DARK_GREY,[(self.ox+x*self.scale,self.oy+y*self.scale),(self.ox+(x+1)*self.scale,self.oy+y*self.scale),(self.ox+(x+1)*self.scale,self.oy+(y+1)*self.scale),(self.ox+x*self.scale,self.oy+(y+1)*self.scale)])
                pygame.draw.polygon(self.screen, GREY,[(self.ox+x*self.scale,self.oy+y*self.scale),(self.ox+(x+1)*self.scale,self.oy+y*self.scale),(self.ox+(x+1)*self.scale,self.oy+(y+1)*self.scale),(self.ox+x*self.scale,self.oy+(y+1)*self.scale)],width=1)
                # if self.solve_mode:
                #     print(f'{self.winning_moves:0{self.n*self.n}b}')
                selection = selection>>1
        if self.solve_mode:
            selection = 1<<(self.n*self.n-1)
            for y in range(self.n):
                for x in range(self.n):
                    m=y*self.n+x
                    if (self.winning_moves&selection)>>(self.n*self.n-m-1)==1:
                        pygame.draw.polygon(self.screen, RED,[(self.ox+x*self.scale+self.offset,self.oy+y*self.scale+self.offset),(self.ox+(x+1)*self.scale-self.offset,self.oy+y*self.scale+self.offset),(self.ox+(x+1)*self.scale-self.offset,self.oy+(y+1)*self.scale-self.offset),(self.ox+x*self.scale+self.offset,self.oy+(y+1)*self.scale-self.offset)],width = self.offset)
                    selection = selection >> 1

    def update(self):
        self.clock.tick(FPS)
        self.draw_grid()
        pygame.display.update()
    
    def find_move(self,mouse_pos):
        if mouse_pos[0]<self.ox or mouse_pos[1]<self.oy:return -1
        if mouse_pos[0]>self.ox+self.scale*self.n or mouse_pos[1]>self.oy+self.scale*self.n: return -1
        x = ((mouse_pos[0]-self.ox)//self.scale) * self.scale + self.ox
        y = ((mouse_pos[1]-self.oy)//self.scale) * self.scale + self.oy
        if mouse_pos[0]-x<self.offset or mouse_pos[1]-y<self.offset:return -1
        if mouse_pos[0]-x>self.scale-self.offset or mouse_pos[1]-y>self.scale-self.offset:return -1
        return (y-self.oy)//self.scale * self.n + (x-self.ox)//self.scale + 1
        
    def handle_commands(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.unicode.isdigit():
                    return int(event.unicode)
                if event.key == pygame.K_n:
                    return self.n
                if event.key == pygame.K_s:
                    self.solve_mode = True
                    self.winning_moves = self.grid.solve_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                move = self.find_move(pygame.mouse.get_pos())
                if move!=-1:
                    if self.solve_mode:
                        self.winning_moves ^= (1<<(self.n*self.n-move))
                    self.grid.move(move)
                    if self.grid.board==0:self.solve_mode=False
        return 0