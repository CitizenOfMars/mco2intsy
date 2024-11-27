from pyautogui import Size
from pyswip import Prolog

def count_valid_adjacent(x, y, size):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
    valid_count = 0
    
    for dx, dy in directions:
        adj_x, adj_y = x + dx, y + dy
        if 0 <= adj_x < size and 0 <= adj_y < size:
            valid_count += 1
    
    return valid_count
def inferenceMachine(prolog):
    
    breezes = list(prolog.query("breeze(X, Y)"))
    
    for breeze in breezes:
        x = breeze['X']
        y = breeze['Y']
        result = list(prolog.query(f"count_safe_adjacent({x}, {y}, Count)"))
        print(result)
        if result[0]["Count"] == count_valid_adjacent(x, y, size) - 1:
            print("boom")
            for dx, dy in directions:
                adj_x, adj_y = x + dx, y + dy
                if 0 <= adj_x < size and 0 <= adj_y < size:
                    if not list(prolog.query(f"safe({adj_x}, {adj_y})")):
                        if not list(prolog.query(f"pit({adj_x}, {adj_y})")):
                            prolog.assertz(f"pit({adj_x}, {adj_y})")
                            break  

def putPit(grid):
    for px, py in pits:
        grid[px][py] = "P"

def putGold(grid):
    for gx, gy in gold:
        golds[gx][gy] = "G"
def putBreeze(grid):
    for px, py in pits:
        for dx, dy in directions:
            adj_x, adj_y = px + dx, py + dy
            if 0 <= adj_x < size and 0 <= adj_y < size:
                grid[adj_x][adj_y] = "B"

def draw(grid):
    for i in range(size):
        for j in range(size):
            print(grid[i][j] + " ", end = "")
        print()

# harcoded positions of pits gold home size
pits = [(2, 1), (1, 2), (4, 3)]
home = (4, 0)
gold = [(0, 1), (1, 0), (0, 4), (4, 4)]
size = 5

grid = [['.' for i in range(size)] for i in range(size)]
playerView = [['.' for i in range(size)] for i in range(size)]
golds = [['.' for i in range(size)] for i in range(size)]


goldCount = 0

curX, curY = home[0], home[1]
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

putPit(grid)
putBreeze(grid)
putGold(grid)
prolog = Prolog()
prolog.consult("adventure.pl")
prolog.assertz("breeze(-100, -100)")
prolog.assertz("pit(_, _) :- fail")

prolog.assertz(f"home({home[0]}, {home[1]})")
playerView[home[0]][home[1]] = "A"

for dx, dy in directions:
    adj_x, adj_y = home[0] + dx, home[1] + dy
    if 0 <= adj_x < size and 0 <= adj_y < size:
        prolog.assertz(f"safe({adj_x}, {adj_y})")



result = list(prolog.query("safe(X, Y)"))
for r in result:
    x = r['X']
    y = r['Y']
    playerView[x][y] = "S"

while(True):
    draw(playerView)
    if grid[curX][curY] == 'B':
        print("agent detects: breeze")
        if not list(prolog.query(f"breeze({curX}, {curY})")):
            prolog.assertz(f"breeze({curX}, {curY})")
    if golds[curX][curY] == 'G':
        print("agent detects: glitter")
    elif grid[curX][curY] == 'P':
        print("Mission failed! Player falls into a Pit")
        break
    
    print("gold count: " + str(goldCount))
    
    ui = input("u, d, l, r, g, leave: ")
    
    if ui == 'u' :
        if 0 <= curX - 1 < size:
            # playerView[curX][curY] = 'S'
            curX -= 1
            playerView[curX][curY] = 'A'
    elif ui == 'd':
        if 0 <= curX + 1 < size:
            # playerView[curX][curY] = 'S'
            curX += 1
            playerView[curX][curY] = 'A'
    elif ui == 'l':
        if 0 <= curY - 1 < size:
            # playerView[curX][curY] = 'S'
            curY -= 1
            playerView[curX][curY] = 'A'
    elif ui == 'r':
        if 0 <= curY + 1 < size:
            # playerView[curX][curY] = 'S'
            curY += 1
            playerView[curX][curY] = 'A'
    elif ui == 'g':
        if golds[curX][curY] == 'G':
            goldCount += 1
            golds[curX][curY] = '.'
    else:
        break

# prolog
    if grid[curX][curY] != 'B':
        for dx, dy in directions:
            adj_x, adj_y = curX + dx, curY + dy
            if 0 <= adj_x < size and 0 <= adj_y < size and not list(prolog.query(f"breeze({adj_x}, {adj_y})")):
                if not list(prolog.query(f"safe({adj_x}, {adj_y})")):
                    prolog.assertz(f"safe({adj_x}, {adj_y})")
    if grid[curX][curY] != 'P' and not list(prolog.query(f"safe({curX}, {curY})")):
        prolog.assertz(f"safe({curX}, {curY})")
    result = list(prolog.query("safe(X, Y)"))
    for r in result:
        x = r['X']
        y = r['Y']
        if not(curX == x and curY == y):
            playerView[x][y] = "S"
            if list(prolog.query(f"breeze({x}, {y})")):
                playerView[x][y] = "B"
    
    inferenceMachine(prolog)
    pitpos = list(prolog.query(f"pit(X, Y)"))
    for pit in pitpos:
        x = pit['X']
        y = pit['Y']
        playerView[x][y] = 'P'
        

    


print(result)

