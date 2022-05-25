import queue, sys, time, os
import keyboard
from copy import deepcopy
from art import tprint
import winsound
import pkg_resources

dependencies = [
    'keyboard>=0.13.5',
    'pip>=22.0.4',
    'click>=8.0.3',
    'art>=5.5'
]

try:
    pkg_resources.require(dependencies)
except:
    print(sys.exc_info())
    os.system(('pip install -r requirments.txt'))

maze1 = [
    ["#", "*", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", " ", " ", "#", " ", "#"],
    ["#", "#", "#", "#", "#", "X", "#"]
        ]

maze2 = [
    ["#", "#", "#", "#", "#", "#", "#", "*", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "X", "#", "#", "#", "#", "#", "#", "#"]
    ]

maze3 = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "*", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", "#", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", " ", " ", "#", "#"],
    ["#", "#", "#", "#", " ", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "X", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#"]
    ]

levels = {
    1: (maze1,(0,1)),
    2: (maze2,(0,7)),
    3: (maze3,(2,1))
          }

def clear():
    if (os.name == 'posix'):
        os.system('clear')
    else:
        os.system('cls')

def aprint(text):
    clear()
    tprint(text, 'tarty1')
    time.sleep(1)

def read_key():
    while True:
        key = keyboard.read_key(suppress=True)
        key = keyboard.read_key(suppress=True)
        if key[0] in 'lrud':
            return key[0].upper()
        if key in 'qQ':
            aprint('THANK YOU')
            sys.exit()
        if key in 'rs':
            return key

def printMaze(maze, path=""):
    for row in maze:
        for col in row:
            if col == '*':
                col = "\033[91m*\033[00m"
            print(col + " ", end="")
        print()
    print()
    print('q : Quit   r: Restart  s: Solution')


def validate(maze, start, path, cache):
    if path in cache:
        return 'skip'

    path_temp = path
    x_max = len(maze[0]) - 1
    y_max = len(maze) - 1
    y, x = cache.get(path[:-1],start)
    path = path[-1]

    for step in path:
        if step == 'L':
            x -= 1
        elif step == 'R':
            x += 1
        elif step == 'U':
            y -= 1
        else:
            y += 1

        if not (0 <= x <= x_max and 0 <= y <= y_max):
            return False
        if maze[y][x] == "#" or maze[y][x] == '*':
            return False
        if maze[y][x] == "X":
            winsound.Beep(440, 200)
            return 'win'
    cache[path_temp] = (y, x)
    return (y, x)

def update(maze, pos):
    maze[pos[0]][pos[1]] = "*"
    clear()
    printMaze(maze)

def skip(path, inp):
    if path and {path[-1],inp} in ({'U','D'},{'L','R'}):
        return True
    else:
        return False



def play(maze, start, cache):
    clear()
    printMaze(maze)
    path = ''
    while True:
        inp = read_key()
        if inp not in 'LRUD':
            return inp

        if skip(path, inp):
            continue

        pos = validate(maze, start, path + inp, cache)
        if pos == 'skip':
            continue
        if pos:
            if pos == 'win':
                path += path + inp
                return False
            else:
                path += inp
                update(maze, pos)
        else:
            winsound.Beep(440, 200)
            return 'r'



def find_solution(maze, start):
    que = queue.Queue()
    que.put('')
    cache = {}

    while not que.empty():
        path = que.get()
        for i in 'RLUD':
            if skip(path, i):
                continue
            pos = validate(maze, start, path + i, cache)
            if pos == 'skip':
                continue
            if pos:
                if pos == 'win':
                    path = path+i
                    que = queue.Queue()
                    break
                else:
                    que.put(path + i)
    return path, cache


def main():
    clear()
    aprint('MAZE')
    winsound.Beep(440, 200)
    time.sleep(1)
    for level, data in levels.items():
            cache = {}
            aprint(f'level {level}')
            result = play(deepcopy(data[0]), data[1], cache)
            while result:
                cache = {}
                if result == 'r':
                    aprint('TRY AGAIN')
                    aprint('RESTARTING...')
                    result = play(deepcopy(data[0]), data[1], cache)
                if result == 's':
                    aprint('FINDING \n   SOLUTION...')
                    sol,cache = find_solution(data[0], data[1])
                    new_data = deepcopy(data[0])
                    for i in range(1,len(sol)):
                        pos = cache[sol[:i]]
                        update(new_data, pos)
                        time.sleep(.5)
                    result = 'r'
    aprint('THANK YOU')


if __name__ == "__main__":
    main()