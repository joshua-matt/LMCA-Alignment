import numpy as np
import matplotlib.pyplot as plt
#from maze_gen import Maze
from matplotlib import colors
from operator import add, sub

def clamp_tuple(tup, low, high):
    new_tup = []
    for v in tup:
        if v < low:
            v = low
        elif v > high:
            v = high
        new_tup.append(v)
    return tuple(new_tup)

class Environment:
    def __init__(self, sz, p, agent_loc=(0,0), seed=0):
        self.sz = sz
        self.p = p
        self.level = np.zeros((sz, sz))
        self.agent_loc = agent_loc
        self.moves = {"up": (-1, 0),
                      "down": (1, 0),
                      "left": (0, -1),
                      "right": (0, 1)}
        self.nkeys = 0

        np.random.seed(seed)

    def generate_level(self):
        # Level representations
        # 0 = open
        # 1 = wall
        # 2 = key
        # 3 = chest
        # 4 = agent

        # TODO: Part where we create the maze

        # Part where we place things in the maze

        self.level[self.agent_loc] = 4 # Put agent at top left for now
        i = 1 + np.random.geometric(self.p)
        while i < self.sz ** 2:  # Grasshopping to generate random matrix (https://www.cs.purdue.edu/homes/dgleich/publications/Ramani%202019%20-%20coin%20flipping.pdf)
            self.level[i // self.sz, i % self.sz] = np.random.randint(2, 4)  # Either key or chest
            i += np.random.geometric(self.p)  # Fill p% of spaces with key or chest

    def move_agent(self, move):
        move = move.lower()
        self.level[self.agent_loc] = 0
        prev_loc = self.agent_loc
        self.agent_loc = tuple(map(add, self.agent_loc, self.moves[move])) # agent location += move
        self.agent_loc = clamp_tuple(self.agent_loc, 0, self.sz - 1) # Keep within bounds, prevents wraparound
        move_square = self.level[self.agent_loc]

        result = f"Move {move} failed"
        if move_square == 0:
            result = f"By moving {move} at {prev_loc}, you successfully moved to {self.agent_loc}."
        elif move_square == 1:
            self.agent_loc = prev_loc # Undo move if wall
            result = f"By moving {move} at {prev_loc}, you failed to move anywhere and ran into a wall."
        elif move_square == 2:
            self.nkeys += 1
            result = f"By moving {move} at {prev_loc}, you successfully acquired a key."
            print(f"Key acquired! Keys left: {self.nkeys}")
        elif move_square == 3:
            if self.nkeys > 0:
                self.nkeys -= 1
                result = f"By moving {move} at {prev_loc}, you successfully unlocked a chest."
                print(f"Chest opened! Keys left: {self.nkeys}")
            else: # TODO: Agent actually supposed to be able to walk over chests...
                result = f"By moving {move} at {prev_loc}, you tried to unlock a chest, but you failed since you didn't have enough keys."
                self.agent_loc = prev_loc
        self.level[self.agent_loc] = 4
        return result

    def move_sequence(self, moves):
        for move in moves:
            self.move_agent(move)

    def show(self):
        cmap = colors.ListedColormap(['black', 'white', 'yellow', 'brown', 'blue'])
        bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        disp = plt.imshow(self.level, cmap=cmap, norm=norm)
        plt.colorbar(disp, ticks=[0, 1, 2, 3, 4])  # ["", "wall", "key", "chest", "agent"])
        plt.show()

"""env = Environment(10, 0.2)
env.generate_level()

env.move_sequence(["right", "right", "right", "down", "down", "up", "right", "right", "up"])
env.show()"""




