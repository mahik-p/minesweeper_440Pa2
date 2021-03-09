import pygame
import random
import os
import time


class Piece:

    def __init__(self, x, y, v):
        self.mine = False
        self.visited = False
        self.flagged = False
        self.i = x
        self.j = y
        self.value = v


def draw_grid(screen):
    distance = size // dim
    x = 0
    y = 0
    for i in range(dim):
        x += distance
        y += distance

        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, size))
        pygame.draw.line(screen, (255, 255, 255), (0, y), (size, y))

    pygame.display.update()


def initialize_game():
    # Initialize pygame
    pygame.init()

    # make a screen
    screen = pygame.display.set_mode((size, size))
    # Title of the window
    pygame.display.set_caption("Minesweeper")

    return screen


def loadImages():
    global images
    images = {}
    for fileName in os.listdir():
        if (fileName.endswith(".png")):
            image = pygame.image.load(fileName)
            image = pygame.transform.scale(image, (size // dim, size // dim))
            images[fileName.split(".")[0]] = image


def update_screen(screen):
    topLeft = (0, 0);
    for i in range(dim):
        for j in range(dim):

            # if its visited end update the screen else keep it blank
            if minefield[i][j].visited:

                if minefield[i][j].mine & minefield[i][j].flagged:
                    image = images["no_bomb"]
                elif minefield[i][j].mine:
                    image = images["explosion"]
                elif minefield[i][j].value == 0:
                    image = images["square"]
                elif minefield[i][j].value == 1:
                    image = images["one"]
                elif minefield[i][j].value == 2:
                    image = images["two"]
                elif minefield[i][j].value == 3:
                    image = images["three"]
                elif minefield[i][j].value == 4:
                    image = images["four"]
                elif minefield[i][j].value == 5:
                    image = images["five"]
                elif minefield[i][j].value == 6:
                    image = images["six"]
                elif minefield[i][j].value == 7:
                    image = images["seven"]
                elif minefield[i][j].value == 8:
                    image = images["eight"]
            else:
                image = images["square"]

            screen.blit(image, topLeft)

            topLeft = topLeft[0] + (size // dim), topLeft[1]
        topLeft = 0, topLeft[1] + (size // dim)


def num_visited():
    count = 0
    for i in range(dim):
        for j in range(dim):
            if minefield[i][j].visited:
                count += 1

    return count


def strategy_1():
    start_count = num_visited()

    for i in range(dim):
        for j in range(dim):
            if minefield[i][j].visited:
                num_mines = 0
                num_not_visited = 0
                # count the number of visited cells that are mines
                if (i - 1) >= 0:
                    if minefield[i - 1][j].mine & minefield[i - 1][j].visited:
                        num_mines += 1
                    if not minefield[i - 1][j].visited:
                        num_not_visited += 1
                if (j - 1) >= 0:
                    if minefield[i][j - 1].mine & minefield[i][j - 1].visited:
                        num_mines += 1
                    if not minefield[i][j - 1].visited:
                        num_not_visited += 1
                if (i + 1) < dim:
                    if minefield[i + 1][j].mine & minefield[i + 1][j].visited:
                        num_mines += 1
                    if not minefield[i + 1][j].visited:
                        num_not_visited += 1
                if (j + 1) < dim:
                    if minefield[i][j + 1].mine & minefield[i][j + 1].visited:
                        num_mines += 1
                    if not minefield[i][j + 1].visited:
                        num_not_visited += 1
                if ((i - 1) >= 0) & ((j - 1) >= 0):
                    if minefield[i - 1][j - 1].mine & minefield[i - 1][j - 1].visited:
                        num_mines += 1
                    if not minefield[i - 1][j - 1].visited:
                        num_not_visited += 1
                if ((i - 1) >= 0) & ((j + 1) < dim):
                    if minefield[i - 1][j + 1].mine & minefield[i - 1][j + 1].visited:
                        num_mines += 1
                    if not minefield[i - 1][j + 1].visited:
                        num_not_visited += 1
                if ((i + 1) < dim) & ((j - 1) >= 0):
                    if minefield[i + 1][j - 1].mine & minefield[i + 1][j - 1].visited:
                        num_mines += 1
                    if not minefield[i + 1][j - 1].visited:
                        num_not_visited += 1
                if ((i + 1) < dim) & ((j + 1) < dim):
                    if minefield[i + 1][j + 1].mine & minefield[i + 1][j + 1].mine:
                        num_mines += 1
                    if not minefield[i + 1][j + 1].visited:
                        num_not_visited += 1

                if num_mines == minefield[i][j].value:
                    # mark all neighbors as visited because they are all clear
                    if (i - 1) >= 0:
                        minefield[i - 1][j].visited = True
                    if (j - 1) >= 0:
                        minefield[i][j - 1].visited = True
                    if (i + 1) < dim:
                        minefield[i + 1][j].visited = True
                    if (j + 1) < dim:
                        minefield[i][j + 1].visited = True
                    if ((i - 1) >= 0) & ((j - 1) >= 0):
                        minefield[i - 1][j - 1].visited = True
                    if ((i - 1) >= 0) & ((j + 1) < dim):
                        minefield[i - 1][j + 1].visited = True
                    if ((i + 1) < dim) & ((j - 1) >= 0):
                        minefield[i + 1][j - 1].visited = True
                    if ((i + 1) < dim) & ((j + 1) < dim):
                        minefield[i + 1][j + 1].visited = True

                if (8 - minefield[i][j].value) == num_not_visited:
                    # mark all not visited as flagged bombs and visited
                    if (i - 1) >= 0:
                        if not minefield[i - 1][j].visited:
                            minefield[i - 1][j].falgged = True
                            minefield[i - 1][j].visited = True
                    if (j - 1) >= 0:
                        if not minefield[i][j - 1].visited:
                            minefield[i][j - 1].falgged = True
                            minefield[i][j - 1].visited = True
                    if (i + 1) < dim:
                        if not minefield[i + 1][j].visited:
                            minefield[i + 1][j].visited = True
                            minefield[i + 1][j].falgged = True
                    if (j + 1) < dim:
                        if not minefield[i][j + 1].visited:
                            minefield[i][j + 1].visited = True
                            minefield[i][j + 1].flagged = True
                    if ((i - 1) >= 0) & ((j - 1) >= 0):
                        if not minefield[i - 1][j - 1].visited:
                            minefield[i - 1][j - 1].visited = True
                            minefield[i - 1][j - 1].flagged = True
                    if ((i - 1) >= 0) & ((j + 1) < dim):
                        if not minefield[i - 1][j - 1].visited:
                            minefield[i - 1][j - 1].visited = True
                            minefield[i - 1][j - 1].flagged = True
                    if ((i + 1) < dim) & ((j - 1) >= 0):
                        if not minefield[i + 1][j - 1].visited:
                            minefield[i + 1][j - 1].visited = True
                            minefield[i + 1][j - 1].falgged = True
                    if ((i + 1) < dim) & ((j + 1) < dim):
                        if not minefield[i + 1][j + 1].visited:
                            minefield[i + 1][j + 1].visited = True
                            minefield[i + 1][j + 1].falgged = True

    end_count = num_visited()

    if start_count == end_count:
        # visit a random state

        rand_i = random.randint(0, dim - 1)
        rand_j = random.randint(0, dim - 1)

        if not minefield[rand_i][rand_j].visited:
            minefield[rand_i][rand_j].visited = True
            i += 1
        print("Stuck in strat")


def game_loop(screen):
    # game loop
    running = True
    while running:
        # background color RGB
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        strategy_1()

        update_screen(screen)
        draw_grid(screen)
        pygame.display.update()

        time.sleep(.5)
        print("Stuck in game")


def create_minefield():
    # initialze array
    arr = [[Piece(0, 0, 0) for i in range(dim)] for j in range(dim)]

    # place bombs
    i = 0
    while i < num_mines:

        rand_i = random.randint(0, dim - 1)
        rand_j = random.randint(0, dim - 1)

        if not arr[rand_i][rand_j].mine:
            arr[rand_i][rand_j].mine = True
            i += 1

    return arr


def assign_mine_values(arr):
    for i in range(dim):
        for j in range(dim):
            # assign correct i and j
            curr = arr[i][j]
            curr.i = i
            curr.j = j
            # get the piece value
            count = 0
            if (i - 1) >= 0:
                if arr[i - 1][j].mine:
                    count += 1
            if (j - 1) >= 0:
                if arr[i][j - 1].mine:
                    count += 1
            if (i + 1) < dim:
                if arr[i + 1][j].mine:
                    count += 1
            if (j + 1) < dim:
                if arr[i][j + 1].mine:
                    count += 1
            if ((i - 1) >= 0) & ((j - 1) >= 0):
                if arr[i - 1][j - 1].mine:
                    count += 1
            if ((i - 1) >= 0) & ((j + 1) < dim):
                if arr[i - 1][j + 1].mine:
                    count += 1
            if ((i + 1) < dim) & ((j - 1) >= 0):
                if arr[i + 1][j - 1].mine:
                    count += 1
            if ((i + 1) < dim) & ((j + 1) < dim):
                if arr[i + 1][j + 1].mine:
                    count += 1
            curr.value = count
    return arr


def initialize_minefield():
    arr = create_minefield()
    arr = assign_mine_values(arr)
    return arr


def main():
    global dim, num_mines, minefield, size

    # size of the screen
    size = 500

    dim = int(input("Enter the dimension of minefield: "))
    num_mines = int(input("Enter the number of mines:  "))

    # get all the sprites
    loadImages()

    minefield = initialize_minefield()

    screen = initialize_game()

    game_loop(screen)


main()
