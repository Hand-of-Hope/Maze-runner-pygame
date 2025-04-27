import pygame
import os
import random
import sys


pygame.init()

TILE_SIZE = 64          
GRID_SIZE = 17          
SCREEN_SIZE = GRID_SIZE * TILE_SIZE

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Maze Runner: Big Adventure")



def load_and_scale(filename):
    img = pygame.image.load(os.path.join('assets', filename)).convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    return img

player_img = load_and_scale('player.png')
enemy_img = load_and_scale('enemy.png')
wall_img = load_and_scale('wall.png')
floor_img = load_and_scale('floor.png')
exit_img = load_and_scale('exit.png')



maze = [
    list("#################"),
    list("#P      #       #"),
    list("# ##### ####### #"),
    list("#     #         #"),
    list("### # ####### ###"),
    list("#   #       #   #"),
    list("# ##### ### ### #"),
    list("#     #   #     #"),
    list("### ### ### ### #"),
    list("#   #       #   #"),
    list("# ### ##### ### #"),
    list("#   #         # #"),
    list("# ### ####### # #"),
    list("#     #       # #"),
    list("# ### # ##### # #"),
    list("#   #     #   #E#"),
    list("#################")
]



player_pos = [1, 1]   
ai_pos = [15, 1]       
exit_pos = [15, 15]   


heatmap = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]



def draw_maze():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            screen.blit(floor_img, (x, y))  

            if maze[row][col] == '#':
                screen.blit(wall_img, (x, y))
            if [row, col] == exit_pos:
                screen.blit(exit_img, (x, y))

            if [row, col] == player_pos:
                screen.blit(player_img, (x, y))
            elif [row, col] == ai_pos:
                screen.blit(enemy_img, (x, y))

def move_player(keys):
    dx, dy = 0, 0
    if keys[pygame.K_w]:
        dx = -1
    if keys[pygame.K_s]:
        dx = 1
    if keys[pygame.K_a]:
        dy = -1
    if keys[pygame.K_d]:
        dy = 1

    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy

    if maze[new_x][new_y] != '#':
        player_pos[0], player_pos[1] = new_x, new_y
        heatmap[new_x][new_y] += 1

def move_ai():
    x, y = ai_pos
    possible_moves = []
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = x + dx, y + dy
        if maze[nx][ny] != '#':
            score = heatmap[nx][ny]
            dist = abs(player_pos[0] - nx) + abs(player_pos[1] - ny)
            weight = score - dist
            possible_moves.append(((nx, ny), weight))

    if possible_moves:
        possible_moves.sort(key=lambda x: x[1], reverse=True)
        ai_pos[0], ai_pos[1] = possible_moves[0][0]

def game_loop():
    clock = pygame.time.Clock()
    running = True
    move_counter = 0

    while running:
        clock.tick(10)  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        move_player(keys)

       
        move_counter += 1
        if move_counter % 5 == 0:
            move_ai()

        draw_maze()
        pygame.display.flip()

        if player_pos == exit_pos:
            print("You escaped the maze!")
            pygame.quit()
            sys.exit()

        if player_pos == ai_pos:
            print("You got caught by the AI!")
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    game_loop()
