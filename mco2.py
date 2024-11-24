from pyswip import Prolog

def inferenceMachine(prolog):
    print() # not done yet
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
            if 0 <= adj_x < 5 and 0 <= adj_y < 5:
                grid[adj_x][adj_y] = "B"

def draw(grid):
    for i in range(5):
        for j in range(5):
            print(grid[i][j] + " ", end = "")
        print()



grid = [['.' for i in range(5)] for i in range(5)]
playerView = [['.' for i in range(5)] for i in range(5)]
golds = [['.' for i in range(5)] for i in range(5)]

# harcoded positions of pits gold home
pits = [(2, 1), (1, 2), (4, 3)]
home = (4, 0)
gold = [(0, 1), (1, 0), (0, 4), (3, 4)]
goldCount = 0

curX, curY = home[0], home[1]
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

putPit(grid)
putBreeze(grid)
putGold(grid)
prolog = Prolog()
prolog.assertz("breeze(-100, -100)")

prolog.assertz(f"home({home[0]}, {home[1]})")
playerView[home[0]][home[1]] = "A"

for dx, dy in directions:
    adj_x, adj_y = home[0] + dx, home[1] + dy
    if 0 <= adj_x < 5 and 0 <= adj_y < 5:
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
        prolog.assertz(f"breeze({curX}, {curY})")
    if golds[curX][curY] == 'G':
        print("agent detects: glitter")
    elif grid[curX][curY] == 'P':
        print("Mission failed! Player falls into a Pit")
        break
    
    print("gold count: " + str(goldCount))
    
    ui = input("u, d, l, r, g, leave: ")
    
    if ui == 'u' :
        if 0 <= curX - 1 < 5:
            # playerView[curX][curY] = 'S'
            curX -= 1
            playerView[curX][curY] = 'A'
    elif ui == 'd':
        if 0 <= curX + 1 < 5:
            # playerView[curX][curY] = 'S'
            curX += 1
            playerView[curX][curY] = 'A'
    elif ui == 'l':
        if 0 <= curY - 1 < 5:
            # playerView[curX][curY] = 'S'
            curY -= 1
            playerView[curX][curY] = 'A'
    elif ui == 'r':
        if 0 <= curY + 1 < 5:
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
            if 0 <= adj_x < 5 and 0 <= adj_y < 5 and not list(prolog.query(f"safe({adj_x}, {adj_y})")) and not list(prolog.query(f"breeze({adj_x}, {adj_y})")):
                prolog.assertz(f"safe({adj_x}, {adj_y})")
    if grid[curX][curY] != 'P':
        prolog.assertz(f"safe({curX}, {curY})")
    result = list(prolog.query("safe(X, Y)"))
    for r in result:
        x = r['X']
        y = r['Y']
        if not(curX == x and curY == y):
            playerView[x][y] = "S"
            if list(prolog.query(f"breeze({x}, {y})")):
                playerView[x][y] = "B"
        

    


print(result)

