import numpy as np
import matplotlib.pyplot as plt
import serial 
import curses

class OccupancyGrid:
    def __init__(self, size_x, size_y, initial_log_odds):
        self.size_x = size_x
        self.size_y = size_y
        self.log_odds = np.full((size_x, size_y), initial_log_odds)

    def update_grid(self, sensor_data, sensor_model):
        for x in range(self.size_x):
            for y in range(self.size_y):
                log_prior = self.log_odds[x, y]
                likelihood = sensor_model(sensor_data, x, y)
                log_odds_update = np.log(likelihood / (1 - likelihood))
                self.log_odds[x, y] = log_prior + log_odds_update

    def plot_map(self,directory,im):
        fig, ax = plt.subplots()
        ax.set_xticks(np.arange(-0.5, self.size_x, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, self.size_y, 1), minor=True)
        ax.grid(which="minor", color="black", linestyle='-', linewidth=1)

        self.log_odds = np.rot90(self.log_odds,3)
        self.log_odds = np.transpose(self.log_odds)
        for x in range(self.size_x):
            for y in range(self.size_y):
                prob_value = 1 / (1 + np.exp(-self.log_odds[x, y]))
                ax.text(y, x, f'{prob_value:.2f}', ha='center', va='center', color='black')
        self.log_odds = np.transpose(self.log_odds)
        self.log_odds = np.rot90(self.log_odds,1)   

        plt.xlabel('Grid Cell (X-axis)')
        plt.ylabel('Grid Cell (Y-axis)')
        plt.title('Occupancy Grid Map')
        plt.savefig(f"final_map.png")
        plt.show()


def get_dist(arduino):
    try:
        while True:
            line = arduino.readline().decode('utf-8').rstrip()
            print(line)
            dist = int(line) // 49
            print(dist)
            return dist 
    except KeyboardInterrupt:
        arduino.close() 


def sensor_model(sensor_data, x, y):
    occ = 0.8
    free = 0.1
    idk = 0.5

    if sensor_data[x][y] == 1:
        return occ
    if sensor_data[x][y] == idk:   
        return idk
    if sensor_data[x][y] == 0:
        return free



def update(x,y,dist,robot):
    intial_prob = 0.5 
    map = np.full((x,y),intial_prob)
    map[robot[0],robot[1]] = 0
    
    if robot[2] == 0: ##facing straight
        if dist == 0:
            map[robot[0] - 1 , robot[1]] = 1
        elif dist == 1:
            map[robot[0]:robot[0]-2:-1, robot[1]] = 0
            map[robot[0] - 2, robot[1]] = 1
        elif dist == 2:
            map[robot[0]:robot[0]-3:-1, robot[1]] = 0
            map[robot[0] - 3, robot[1]] = 1
        elif dist == 3:
            map[robot[0]:robot[0]-4:-1, robot[1]] = 0
            map[robot[0] - 4, robot[1]] = 1
        else:
            map[robot[0]:robot[0]-5:-1, robot[1]] = 0

    if robot[2] == 1: ##facing right
        if dist == 0:
            map[robot[0], robot[1] + 1] = 1
        elif dist == 1:
            map[robot[0], robot[1]:robot[1]+2] = 0
            map[robot[0], robot[1] + 2] = 1
        elif dist == 2:
            map[robot[0] , robot[1]:robot[1]+3] = 0
            map[robot[0], robot[1] + 3] = 1
        elif dist == 3:
            map[robot[0] , robot[1]:robot[1]+4] = 0
            map[robot[0] , robot[1] + 4] = 1
        else:
            map[robot[0] , robot[1]:robot[1]+5] = 0

    if robot[2] == 2: ##facing backwards
        if dist == 0:
            map[robot[0] + 1, robot[1]] = 1
        elif dist == 1:
            map[robot[0]:robot[0]+2, robot[1]] = 0
            map[robot[0] + 2 , robot[1]] = 1
        elif dist == 2:
            map[robot[0]:robot[0]+3, robot[1]] = 0
            map[robot[0] + 3 , robot[1]] = 1
        elif dist == 3:
            map[robot[0]:robot[0]+4, robot[1]] = 0
            map[robot[0] + 4, robot[1]] = 1
        else:
            map[robot[0]:robot[0]+5, robot[1]] = 0
    
    if robot[2] == 3: ##facing left
        if dist == 0:
            map[robot[0] , robot[1]-1] = 1
        elif dist == 1:
            map[robot[0] , robot[1]:robot[1]-2:-1] = 0
            map[robot[0] , robot[1]-2 ] = 1
        elif dist == 2:
            map[robot[0] , robot[1]:robot[1]-3:-1] = 0
            map[robot[0] , robot[1] - 3] = 1
        elif dist == 3:
            map[robot[0] , robot[1]:robot[1]-4:-1] = 0
            map[robot[0] , robot[1] - 4] = 1
        else:
            map[robot[0], robot[1]:robot[1]-5:-1] = 0
    
    return map

 

if __name__ == '__main__':
    intial_prob = 0.5
    map = np.full((5,5) , intial_prob)
    robot = [0,0,0] #the x-y coordinates and the direction it is facing.
    arduino = serial.Serial('/dev/ttyUSB0', 9600) 
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    grid_size_x = 5
    grid_size_y = 5
    initial_log_odds = 0.0
    occupancy_map_2d_log_odds = OccupancyGrid(grid_size_x, grid_size_y, initial_log_odds)
    directory = 'im'
    im = 0
    dist = 0

    try:
        while True:
            im += 1
            x = robot[0]
            y = robot[1]
            direc = robot[2]
            char = screen.getch()
            if char == ord('q'):
                break
            elif char == curses.KEY_UP:
                arduino.write(b'F') 
                if direc == 0:
                    x -= 1
                elif direc == 1:
                    y += 1
                elif direc == 2:
                    x += 1
                else:
                    y -= 1
                map[x,y] = 0
            elif char == curses.KEY_DOWN:
                arduino.write(b'B')
                if direc == 0:
                    x += 1
                    direc = 2
                elif direc == 1:
                    y -= 1
                    direc = 3
                elif direc == 2:
                    x -= 1
                    direc = 0
                else:
                    y += 1
                    direc = 1
                map[x,y] = 0
            elif char == curses.KEY_LEFT:
                arduino.write(b'L')
                if direc == 0:
                    direc = 3
                elif direc == 1:
                    direc = 0
                elif direc == 2:
                    direc = 1
                else:
                    direc = 2   
            elif char == curses.KEY_RIGHT:
                arduino.write(b'R')
                if direc == 0:
                    direc = 1
                elif direc == 1:
                    direc = 2
                elif direc == 2:
                    direc = 3
                else:
                    direc = 0
            elif char == ord('c'):
                occupancy_map_2d_log_odds.update_grid(map, sensor_model)
                occupancy_map_2d_log_odds.plot_map(directory,im)
            elif char == ord('w'):
                arduino.write(b'W')
            elif char == ord('a'):
                arduino.write(b'A')
            elif char == ord('d'):
                arduino.write(b'D')
            elif char == ord('o'):
                arduino.write(b'O')
                dist = get_dist(arduino)
                map = update(grid_size_x,grid_size_y,dist,robot)
            elif char == ord(' '):
                arduino.write(b'S')
            robot[0] = x
            robot[1] = y
            robot[2] = direc
            print(robot)
    finally:
        curses.nobreak()
        screen.keypad(False)
        curses.echo()
        curses.endwin()
        arduino.close()