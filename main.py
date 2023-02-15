from readchar import readkey, key
import time
from threading import Thread
from os import system
import cursor
from replit import db
from json import loads

cursor.hide()

alive = "⬜️"
dead = '  '
ind =  "░░"
hig =  "[]"

purple = "\033[0;35m"
normal = "\033[0;37m"

choice = 0

grid_size = 20
show = False
    
cells = {}
indicator = [0, 0]
    
pre_indicator = [-1, -1]
population = 0
    
for x in range(grid_size):
    for y in range(grid_size):
        cells[x, y] = dead
        
def reset():
    global grid_size
    global cells
    global indicator
    global pre_indicator
    
    cells = {}
    indicator = [0, 0]
    
    pre_indicator = [-1, -1]
    
    for x in range(grid_size):
        for y in range(grid_size):
            cells[x, y] = dead
    
def print_map():
    global population
    global pre_indicator
    global show
    
    final = ''
    population = 0

    for i in range(grid_size):
        final = final + '⎽⎽'

    final = final + '\n⎢'
    
    for x in range(grid_size):
        for y in range(grid_size):

            if indicator == [x, y] and True:
                if cells[x, y] == alive:
                    if pre_indicator != [x, y]:
                        final = final + f'{hig}'
                    else:
                        final = final + cells[x, y]
                else:
                    final = final + f'{ind}'
            else:
                if cells[x, y] == alive:
                    population += 1
                final = final + cells[x, y]

        final = final + '⎢\n⎢'

    for i in range(grid_size):
        final = final + '⎺⎺'

    if show is True:
        final = final + f'\nPopulation: {purple}{population}{normal}'
        
    print(final)

def play_sim():
    global cells

    ncells = {}
    for x in range(grid_size):
         for y in range(grid_size):

             left  = (x - 1) % grid_size
             right = (x + 1) % grid_size
             above = (y - 1) % grid_size
             below = (y + 1) % grid_size
 

             touching = 0
             if cells[(left, above)] == alive:
                 touching += 1 
             if cells[(x, above)] == alive:
                 touching += 1 
             if cells[(right, above)] == alive:
                 touching += 1 
             if cells[(left, y)] == alive:
                 touching += 1  
             if cells[(right, y)] == alive:
                 touching += 1  
             if cells[(left, below)] == alive:
                 touching += 1  
             if cells[(x, below)] == alive:
                 touching += 1  
             if cells[(right, below)] == alive:
                 touching += 1  
 

             if cells[(x, y)] == alive and (touching == 2
                 or touching == 3):

                     ncells[(x, y)] = alive
             elif cells[(x, y)] == dead and touching == 3:

                 ncells[(x, y)] = alive
             else:

                 ncells[(x, y)] = dead
    

    cells = ncells
                


    
def stop_sim():
    global stop
    
    while True:
        answer = readkey()

        if answer == key.SPACE:
            stop = True
            break

def save():
    db['alive'] = alive
    db['dead'] = dead
    db['ind'] = ind
    db['hig'] = hig
    db['choice'] = choice
    db['grid_size'] = grid_size
    db['show'] = show

    save_cells = []

    for i in cells:
        save_cells.append([i, cells[i]])
        
    db['cells'] = save_cells
    db['indicator'] = indicator
    db['pre_indicator'] = pre_indicator
    db['population'] = population

def load():
    global alive, dead, ind, hig, choice, grid_size, show, cells, indicator, pre_indicator, population

    alive = db['alive']
    dead = db['dead']
    ind = db['ind']
    hig = db['hig']
    choice = db['choice']
    grid_size = db['grid_size']
    show = db['show']

    load_cells = {}
    save_cells = loads(db.get_raw("cells"))

    for i in save_cells:
        load_cells[i[0]] = i[1]
        
    cells = load_cells
    indicator = db['indicator']
    pre_indicator = db['pre_indicator']
    population = db['population']
    
stop = False

while True:
    
    print("\033[1;1H", end="")
    print(end="", flush=True)
    print_map()

    pre_indicator = indicator

    answer = readkey()

    if answer == key.ENTER:
        if cells[(indicator[0], indicator[1])] == alive:
            cells[(indicator[0], indicator[1])] = dead
        else:
            cells[(indicator[0], indicator[1])] = alive

    if answer == key.UP or answer == 'w':
        indicator = [max(indicator[0] - 1, 0), indicator[1]]

    if answer == key.DOWN or answer == 's':
        indicator = [min(indicator[0] + 1, grid_size - 1), indicator[1]]

    if answer == key.RIGHT or answer == 'd':
        indicator = [indicator[0], min(indicator[1] + 1, grid_size - 1)]

    if answer == key.LEFT or answer == 'a':
        indicator = [indicator[0], max(indicator[1] - 1, 0)]

    if answer == key.SPACE:
        Thread(target=stop_sim).start()
        while stop is False:
            indicator = [-1, -1]
            
            print("\033[1;1H", end="")
            print(end="", flush=True)
            
            play_sim()
            print_map()
            time.sleep(0.3)

        stop = False
        indicator = [0, 0]

    if answer == 'x':
        indicator = [-1, -1]
            
        print("\033[1;1H", end="")
        print(end="", flush=True)
            
        play_sim()
        print_map()

        stop = False
        indicator = [0, 0]

    if answer == key.BACKSPACE:
        reset()

    if answer == key.TAB:

        pre_cells = cells
        pre_alive = alive
        pre_indicator2 = indicator
        
        choice += 1

        if choice > 6:
            choice = 0

        if choice == 0:
            alive = "⬜️"
            dead =  "  "
            ind =   "░░"

        if choice == 1:
            alive = "🟩"
            dead =  "⬛"
            ind =   "░░"

        if choice == 2:
            alive = "🟥"
            dead =  "⬛️"
            ind =   "░░"

        if choice == 3:
            alive = "⚪️"
            dead =  "  "
            ind =   "░░"

        if choice == 4:
            alive = "⬜️"
            dead =  "░░"
            ind =   "▓▓"

        if choice == 5:
            alive = "⬜️"
            dead =  "::"
            ind =   "▓▓"

            
        if choice == 6:
            alive = "{}"
            dead =  "  "
            ind =   "()"

        reset()

        indicator = pre_indicator2

        for i in pre_cells:
            if pre_cells[i] == pre_alive:
                cells[i] = alive
            else:
                cells[i] = dead

    if answer == "e":
        if show is True: show = False
        else: show = True
        system('clear')

    if answer == 'q':
        
        grid_size += 1
        system('clear')
        reset()

    #if answer == 'z':
        #save()