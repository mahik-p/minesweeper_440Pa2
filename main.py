import pygame
import random
import os
import time

"""
     The Piece class
        mine = (True if the piece is a mine)
        visited = (True if the piece is visited by the algorithm)
        flagged = (True if the piece is visited by the algorithm)
        i = the (x,_) coordinate on the minefield of the piece
        j = the (_,y) coordinate on the minefield of the piece
        value = the number of mines around the piece
        total_neighbors = number of neighbors around the piece
        prob = (0 = safe, 1 = mine, anything in between is maybe)
    
"""


class Piece:

    def __init__(self, x, y, v):
        self.mine = False
        self.visited = False
        self.flagged = False
        self.i = x
        self.j = y
        self.value = v
        self.total_neighbors = 0
        self.prob = 0


"""
    This draws the grid on the pygame display
"""


def draw_grid(screen):
    distance = size // dim
    x = 0
    y = 0
    for i in range(dim):
        x += distance
        y += distance

        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, size))
        pygame.draw.line(screen, (255, 255, 255), (0, y), (size, y))


"""
    Used to start the pygame
"""


def initialize_game():
    # Initialize pygame
    pygame.init()

    # make a screen
    screen = pygame.display.set_mode((size, size))
    # Title of the window
    pygame.display.set_caption("Minesweeper")

    return screen


"""
    This loads all the images used for pygame to images
"""


def loadImages():
    global images
    images = {}
    for fileName in os.listdir():
        if (fileName.endswith(".png")):
            image = pygame.image.load(fileName)
            image = pygame.transform.scale(image, (size // dim, size // dim))
            images[fileName.split(".")[0]] = image


"""
    Everytime this is called the screen in pygame updates to the 
    visited pieces visited
"""


def update_screen(screen):
    screen.fill((255, 255, 255))
    topLeft = (0, 0);
    for i in range(dim):
        for j in range(dim):

            # if its visited end update the screen else keep it blank
            if minefield[i][j].visited:

                if minefield[i][j].mine and minefield[i][j].flagged:
                    image = images["no_bomb"]
                elif minefield[i][j].mine:
                    image = images["explosion"]
                elif minefield[i][j].value == 0:
                    image = images["clear"]
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

    draw_grid(screen)
    pygame.display.update()
    time.sleep(time_sleep)


"""
    This returns the number of visited pieces in the minefield
"""


def num_visited():
    count = 0
    for i in range(dim):
        for j in range(dim):
            if minefield[i][j].visited:
                count += 1

    return count


"""
    This return the number of visited mines in the minefield
"""


def num_visited_mines():
    count = 0
    for i in range(dim):
        for j in range(dim):
            if minefield[i][j].visited and minefield[i][j].mine:
                count += 1
    return count


"""
    This returns and array of not visited pieces 
"""


def get_all_not_visited():
    arr = []
    for i in range(dim):
        for j in range(dim):
            if not minefield[i][j].visited:
                arr.append(minefield[i][j])
    return arr


"""
    This marks all the not visited pieces as mines
"""


def mark_not_visited_as_mines():
    for i in range(dim):
        for j in range(dim):
            if not minefield[i][j].visited:
                minefield[i][j].visited = True
                if minefield[i][j].mine:
                    minefield[i][j].flagged = True


"""
    The basic method only follows two rules
        1) get a start count of visited neighbors
        2) for every visited piece
            2.1) check if the number of discovered mines around it equals it's value. If so then every 
                 unknown neighbor is safe
            2.2) check if the number of total neighbors -visited safe neighbors = its value, then 
                 every unknown neighbors is a mine
        3) get end count of visited pieces 
            3.3 if start count == end count and endcount < dim*dim, then pick a random unknown piece        
"""


def basic():
    start_count = num_visited()

    for i in range(dim):
        for j in range(dim):
            if minefield[i][j].visited and minefield[i][j].mine == False:
                num_mines = 0
                num_safe = 0
                # count the number of visited cells that are mines & the number of visited safe cells
                if (i - 1) >= 0:
                    if minefield[i - 1][j].mine and minefield[i - 1][j].visited:
                        num_mines += 1
                    if minefield[i - 1][j].visited and (minefield[i - 1][j].mine == False):
                        num_safe += 1
                if (j - 1) >= 0:
                    if minefield[i][j - 1].mine and minefield[i][j - 1].visited:
                        num_mines += 1
                    if minefield[i][j - 1].visited and (minefield[i][j - 1].mine == False):
                        num_safe += 1
                if (i + 1) < dim:
                    if minefield[i + 1][j].mine and minefield[i + 1][j].visited:
                        num_mines += 1
                    if minefield[i + 1][j].visited and (minefield[i + 1][j].mine == False):
                        num_safe += 1
                if (j + 1) < dim:
                    if minefield[i][j + 1].mine and minefield[i][j + 1].visited:
                        num_mines += 1
                    if minefield[i][j + 1].visited and (minefield[i][j + 1].mine == False):
                        num_safe += 1
                if ((i - 1) >= 0) and ((j - 1) >= 0):
                    if minefield[i - 1][j - 1].mine and minefield[i - 1][j - 1].visited:
                        num_mines += 1
                    if minefield[i - 1][j - 1].visited and (minefield[i - 1][j - 1].mine == False):
                        num_safe += 1
                if ((i - 1) >= 0) and ((j + 1) < dim):
                    if minefield[i - 1][j + 1].mine and minefield[i - 1][j + 1].visited:
                        num_mines += 1
                    if minefield[i - 1][j + 1].visited and (minefield[i - 1][j + 1].mine == False):
                        num_safe += 1
                if ((i + 1) < dim) and ((j - 1) >= 0):
                    if minefield[i + 1][j - 1].mine and minefield[i + 1][j - 1].visited:
                        num_mines += 1
                    if minefield[i + 1][j - 1].visited and (minefield[i + 1][j - 1].mine == False):
                        num_safe += 1
                if ((i + 1) < dim) and ((j + 1) < dim):
                    if minefield[i + 1][j + 1].mine and minefield[i + 1][j + 1].mine:
                        num_mines += 1
                    if minefield[i + 1][j + 1].visited and (minefield[i + 1][j + 1].mine == False):
                        num_safe += 1
                if minefield[i][j].value == num_mines:
                    # all other not visited neighbors are safe to visit
                    if (i - 1) >= 0:
                        minefield[i - 1][j].visited = True
                    if (j - 1) >= 0:
                        minefield[i][j - 1].visited = True
                    if (i + 1) < dim:
                        minefield[i + 1][j].visited = True
                    if (j + 1) < dim:
                        minefield[i][j + 1].visited = True
                    if ((i - 1) >= 0) and ((j - 1) >= 0):
                        minefield[i - 1][j - 1].visited = True
                    if ((i - 1) >= 0) and ((j + 1) < dim):
                        minefield[i - 1][j + 1].visited = True
                    if ((i + 1) < dim) and ((j - 1) >= 0):
                        minefield[i + 1][j - 1].visited = True
                    if ((i + 1) < dim) and ((j + 1) < dim):
                        minefield[i + 1][j + 1].visited = True

                if minefield[i][j].total_neighbors - num_safe == minefield[i][j].value:
                    # all other not visited neighbors are mines -> flag them
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
                    if ((i - 1) >= 0) and ((j - 1) >= 0):
                        if not minefield[i - 1][j - 1].visited:
                            minefield[i - 1][j - 1].visited = True
                            minefield[i - 1][j - 1].flagged = True
                    if ((i - 1) >= 0) and ((j + 1) < dim):
                        if not minefield[i - 1][j - 1].visited:
                            minefield[i - 1][j - 1].visited = True
                            minefield[i - 1][j - 1].flagged = True
                    if ((i + 1) < dim) and ((j - 1) >= 0):
                        if not minefield[i + 1][j - 1].visited:
                            minefield[i + 1][j - 1].visited = True
                            minefield[i + 1][j - 1].falgged = True
                    if ((i + 1) < dim) and ((j + 1) < dim):
                        if not minefield[i + 1][j + 1].visited:
                            minefield[i + 1][j + 1].visited = True
                            minefield[i + 1][j + 1].falgged = True

    end_count = num_visited()

    if start_count == end_count:
        # visit a random state
        arr = get_all_not_visited()
        if len(arr) != 0:
            rand = random.randint(0, len(arr) - 1)
            arr[rand].visited = True

    # indite when to stop
    if end_count == (dim * dim):
        return False
    else:
        return True


"""
    get_neighbors()
        
        parameter: a piece on the minefield
        
        returns: all the neighbors of the input in an array
"""


def get_neighbors(point):
    arr = []

    if (point.i - 1) >= 0:
        if minefield[point.i - 1][point.j].visited:
            arr.append(minefield[point.i - 1][point.j])
    if (point.j - 1) >= 0:
        if minefield[point.i][point.j - 1].visited:
            arr.append(minefield[point.i][point.j - 1])
    if (point.i + 1) < dim:
        if minefield[point.i + 1][point.j].visited:
            arr.append(minefield[point.i + 1][point.j])
    if (point.j + 1) < dim:
        if minefield[point.i][point.j + 1].visited:
            arr.append(minefield[point.i][point.j + 1])
    if ((point.i - 1) >= 0) and ((point.j - 1) >= 0):
        if minefield[point.i - 1][point.j - 1].visited:
            arr.append(minefield[point.i - 1][point.j - 1])
    if ((point.i - 1) >= 0) and ((point.j + 1) < dim):
        if minefield[point.i - 1][point.j + 1].visited:
            arr.append(minefield[point.i - 1][point.j + 1])
    if ((point.i + 1) < dim) and ((point.j - 1) >= 0):
        if minefield[point.i + 1][point.j - 1].visited:
            arr.append(minefield[point.i + 1][point.j - 1])
    if ((point.i + 1) < dim) and ((point.j + 1) < dim):
        if minefield[point.i + 1][point.j + 1].visited:
            arr.append(minefield[point.i + 1][point.j + 1])

    return arr


"""
    get_number_of_not_visited_neighbors()
    
        parameter: a piece on the minefield
        
        returns: the number of not visited neighbors around the input
"""


def get_number_of_not_visited_neighbors(point):
    count = 0
    if (point.i - 1) >= 0:
        if not minefield[point.i - 1][point.j].visited:
            count += 1
    if (point.j - 1) >= 0:
        if not minefield[point.i][point.j - 1].visited:
            count += 1
    if (point.i + 1) < dim:
        if not minefield[point.i + 1][point.j].visited:
            count += 1
    if (point.j + 1) < dim:
        if not minefield[point.i][point.j + 1].visited:
            count += 1
    if ((point.i - 1) >= 0) and ((point.j - 1) >= 0):
        if not minefield[point.i - 1][point.j - 1].visited:
            count += 1
    if ((point.i - 1) >= 0) and ((point.j + 1) < dim):
        if not minefield[point.i - 1][point.j + 1].visited:
            count += 1
    if ((point.i + 1) < dim) and ((point.j - 1) >= 0):
        if not minefield[point.i + 1][point.j - 1].visited:
            count += 1
    if ((point.i + 1) < dim) and ((point.j + 1) < dim):
        if not minefield[point.i + 1][point.j + 1].visited:
            count += 1

    return count


"""
    get_number_of_visited_neighbor_mines()
    
        parameter: a piece on the minefield
        
        returns: the number of visited mines around the input
"""


def get_number_of_visited_neighbor_mines(point):
    count = 0
    if (point.i - 1) >= 0:
        if minefield[point.i - 1][point.j].visited and minefield[point.i - 1][point.j].mine:
            count += 1
    if (point.j - 1) >= 0:
        if minefield[point.i][point.j - 1].visited and minefield[point.i][point.j - 1].mine:
            count += 1
    if (point.i + 1) < dim:
        if minefield[point.i + 1][point.j].visited and minefield[point.i + 1][point.j].mine:
            count += 1
    if (point.j + 1) < dim:
        if minefield[point.i][point.j + 1].visited and minefield[point.i][point.j + 1].mine:
            count += 1
    if ((point.i - 1) >= 0) and ((point.j - 1) >= 0):
        if minefield[point.i - 1][point.j - 1].visited and minefield[point.i - 1][point.j - 1].mine:
            count += 1
    if ((point.i - 1) >= 0) and ((point.j + 1) < dim):
        if minefield[point.i - 1][point.j + 1].visited and minefield[point.i - 1][point.j + 1].mine:
            count += 1
    if ((point.i + 1) < dim) and ((point.j - 1) >= 0):
        if minefield[point.i + 1][point.j - 1].visited and minefield[point.i + 1][point.j - 1].mine:
            count += 1
    if ((point.i + 1) < dim) and ((point.j + 1) < dim):
        if minefield[point.i + 1][point.j + 1].visited and minefield[point.i + 1][point.j + 1].mine:
            count += 1

    return count


"""
    calculate_prob():
    
        input: a piece on the minefield
        
        returns the prob of the piece being a mine
        
    This looks at the inputs visited neighbors and calculates the probability that it self is a mine
    based on the neighbors value and the neighbors unknown neighbors
"""


def calculate_prob(point):
    neighbors = get_neighbors(point)

    prob = 0.0
    count = 0

    for i in neighbors:

        # if the neighbor is a mine do not use it for calculation
        if not i.mine:
            num_of_mines_left = i.value - get_number_of_visited_neighbor_mines(i)
            num_of_not_visited_neighbors = get_number_of_not_visited_neighbors(i)

            if num_of_mines_left == 0:
                # this is a safe neighbor
                return 0
            if num_of_mines_left == num_of_not_visited_neighbors:
                # this is a mine for sure
                return 1

            prob += num_of_mines_left / num_of_not_visited_neighbors
            count += 1

    if count == 0:
        # unkown cell prob will be 0.5 without global info
        # this is for regular advanced algo
        if strat == 2:
            return 0.5

        # This takes in account of global info
        # This is for extra credit. (Allowed to access the total number of mines)
        prob = (num_mines - num_visited_mines()) / len(get_all_not_visited())
        return prob

    else:
        return prob / count


"""
    strat2()
    
    input: the pygame screen
    
    strata 2 calculates the probability of all unknown pieces,
        if the prob is 0 it visits it, if 1 then it flags it
    if the start count of visted pieces == end count of visited pieces then it picks the piece with 
    the lowest probability
"""


def strat2(screen):
    start_count = num_visited()

    # for each cell not visited calculate its probability
    for i in range(dim):
        for j in range(dim):

            if not minefield[i][j].visited:
                prob = calculate_prob(minefield[i][j])
                if prob == 0:
                    # safe cell, mark it as visited
                    minefield[i][j].visited = True

                if prob == 1:
                    # mine 100% for flag it
                    minefield[i][j].visited = True
                    minefield[i][j].flagged = True

            update_screen(screen)

    end_count = num_visited()

    # if end = star, # pick the one with the min prob
    if end_count < dim * dim:
        # if total mines - number of mines discovered = empty blocks then all of them are mines
        if num_mines - num_visited_mines() == len(get_all_not_visited()):
            # every not visited block is a mine
            mark_not_visited_as_mines()

        if start_count == end_count:

            # pick a point with the min prob
            min_prob = 1
            x = 0
            y = 0
            for i in range(dim):
                for j in range(dim):
                    if (minefield[i][j].prob < min_prob) and (minefield[i][j].visited == False):
                        min_prob = minefield[i][j].prob
                        x = i
                        y = j

            minefield[x][y].visited = True
            update_screen(screen)

            # true so keep going
            return True

    # searched all so u can stop now
    if end_count == (dim * dim):
        return False

    return True


"""
    game_loop()
    
    runs until the algoritim visits all the pieces on the minefield
    and updates the screen
"""


def game_loop(screen):
    # game loop
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if strat == 1:
            if not basic():
                break
        else:
            if not strat2(screen):
                break

        update_screen(screen)


"""
    create_minefield():
    
    creates a arr[dim][dim] of pieces
"""


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


"""
    assign_mine_values(arr)
    
    input: minefield
    
    returns: minefield
    
    assigns the proper i, j, total_neighbors, and value of the Piece
"""


def assign_mine_values(arr):
    for i in range(dim):
        for j in range(dim):
            # assign correct i and j
            curr = arr[i][j]
            curr.i = i
            curr.j = j
            # get the piece value
            count = 0
            count_neighbors = 0
            if (i - 1) >= 0:
                count_neighbors += 1
                if arr[i - 1][j].mine:
                    count += 1
            if (j - 1) >= 0:
                count_neighbors += 1
                if arr[i][j - 1].mine:
                    count += 1
            if (i + 1) < dim:
                count_neighbors += 1
                if arr[i + 1][j].mine:
                    count += 1
            if (j + 1) < dim:
                count_neighbors += 1
                if arr[i][j + 1].mine:
                    count += 1
            if ((i - 1) >= 0) and ((j - 1) >= 0):
                count_neighbors += 1
                if arr[i - 1][j - 1].mine:
                    count += 1
            if ((i - 1) >= 0) and ((j + 1) < dim):
                count_neighbors += 1
                if arr[i - 1][j + 1].mine:
                    count += 1
            if ((i + 1) < dim) and ((j - 1) >= 0):
                count_neighbors += 1
                if arr[i + 1][j - 1].mine:
                    count += 1
            if ((i + 1) < dim) and ((j + 1) < dim):
                count_neighbors += 1
                if arr[i + 1][j + 1].mine:
                    count += 1
            curr.value = count
            curr.total_neighbors = count_neighbors

    return arr


"""
    initialize_minefield():
    creates the minefield
"""


def initialize_minefield():
    arr = create_minefield()
    arr = assign_mine_values(arr)
    return arr


"""
    get_flagged_count():
    
    returns the number of flagged pieces in the minefield
"""


def get_flagged_count():
    count = 0
    for i in range(dim):
        for j in range(dim):
            if minefield[i][j].mine and minefield[i][j].flagged:
                count += 1
    return count


def main():
    global dim, num_mines, minefield, size, time_sleep, strat

    time_sleep = 0.1

    # size of the screen
    size = 1000

    dim = int(input("Enter the dimension of minefield: "))
    num_mines = int(input("Enter the number of mines:  "))
    strat = int(input(
        "Strat 1 (basic) or Strat 2 (smart) or Strat 3 (Extra credit. Strat 2 with global info). Enter 1 or 2 or 3"))

    if (strat == 1):
        time_sleep = 1
    if (strat == 2 and dim > 10):
        time_sleep = 3
    # get all the sprites10
    loadImages()

    minefield = initialize_minefield()

    screen = initialize_game()

    # pick a random point to be visited first
    rand_i = random.randint(0, dim - 1)
    rand_j = random.randint(0, dim - 1)
    minefield[rand_i][rand_j].visited = True

    game_loop(screen)

    print("There were " + str(num_mines) + " and " + str(get_flagged_count()) + " were flagged")
    print("success rate: " + str(get_flagged_count() / num_mines))


main()


"""
    This was just used for testing disregard the bottom
"""


def testing_main():
    global dim, num_mines, minefield, size, time_sleep, strat

    time_sleep = 0.0

    # size of the screen
    size = 1000

    dim = 10
    num_mines = 90
    strat = 2

    # get all the sprites10
    loadImages()

    minefield = initialize_minefield()

    screen = initialize_game()

    # pick a random point to be visited first
    rand_i = random.randint(0, dim - 1)
    rand_j = random.randint(0, dim - 1)
    minefield[rand_i][rand_j].visited = True

    game_loop(screen)

    print("There were " + str(num_mines) + " and " + str(get_flagged_count()) + " were flagged")
    print("success rate: " + str(get_flagged_count() / num_mines))

    return get_flagged_count() / num_mines


def test():
    total = 0
    for i in range(3):
        total += testing_main()
    print(str(total / 3))

# test()
