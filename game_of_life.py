import pygame
import random

pygame.init()

BLACK = (0,0,0)
GREY = (128,128,128)
YELLOW = (255,255,0)
WIDTH = 500
HEIGHT = 500
SQUARE_SIZE = 20
GRID_W = WIDTH // SQUARE_SIZE
GRID_H = HEIGHT // SQUARE_SIZE

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()


def get_neighbors(cell):
    x,y = cell  
    neighbors = list()
    for dx in [-1,0,1]:
        if dx +x <0 or dx+x > GRID_W:
            continue
        for dy in [-1,0,1]:
            if dy+y<0 or dy+y> GRID_H:
                continue
            if dx == 0 and dy==0:
                continue
            
            neighbors.append((dx +x, dy+y))

    return neighbors


def step(alive):

    new_alive = set()
    all_neighbors=set()

    for cell in alive:
        neighbors = get_neighbors(cell)
        all_neighbors.update(neighbors)

        # filters and keeps neighbors that are alive only
        neighbors = list(filter(lambda x:x in alive, neighbors))

        # which alive cells will stay alive next turn
        if len(neighbors) == 2 or len(neighbors) ==3:
            new_alive.add(cell)

    for cell in all_neighbors:
        neighbors = get_neighbors(cell)
        neighbors = list(filter(lambda x:x in alive, neighbors))
        if len(neighbors)==3:
            new_alive.add(cell)
    
    return new_alive
        

def gen(num):
    return set([(random.randrange(0,GRID_W), random.randrange(0,GRID_H)) for _ in range(num)])


def draw_grid(alive):
    for cell in alive:
        col, row = cell
        pygame.draw.rect(screen,YELLOW,(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE ))

    for row in range(GRID_H): #3rd and 4th arguments are coordinates of starting point and endpoint of line
        pygame.draw.line(screen,BLACK, (0,row*SQUARE_SIZE), (WIDTH, row*SQUARE_SIZE))
    for col in range(GRID_W):
        pygame.draw.line(screen, BLACK, (col*SQUARE_SIZE, 0), (col*SQUARE_SIZE, HEIGHT))

def main():
    running =  True
    playing = False
    alive = set()
    count = 0
    update_freq =120
    

    while running:

        if playing:
            count+=1
        
        if count >= update_freq:
            count = 0
            alive = step(alive)

        pygame.display.set_caption("Playing" if playing else "Paused")

        clock.tick(60)

        screen.fill(GREY)
        draw_grid(alive) 
        pygame.display.update()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                w = x//SQUARE_SIZE
                h = y //SQUARE_SIZE
                
                if (w,h) in alive:
                    alive.remove((w,h))
                else:
                    alive.add((w,h))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
                
                if event.key == pygame.K_c:
                    alive = set()
                    playing = False

                if event.key == pygame.K_g:
                    alive = gen(random.randrange(0,200))
    
        
if __name__ == "__main__":
    main()