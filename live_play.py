from environment import *
from lmca import *
import pygame as pg
import sys

env = Environment(10, 0.2)
env.generate_level()

def generate_prompt():
    global env
    global prev_move
    global result

    state = env.to_state()
    prev_step = f"{str(prev_move)}, {result}"
    n_keys = str(env.nkeys)
    pos = str(env.agent_loc)

    return f"STATE: {state}\nPREV_STEP: {prev_step}\nNUMBER_KEYS: {n_keys}\nCURRENT_POS: {pos}"

user_control = False
colors = {0: (0,0,0),
          1: (255,255,255),
          2: (255,255,0),
          2: (255,255,0),
          3: (255,0,0),
          4: (0,0,255)}
screen_sz = 600
screen = pg.display.set_mode([screen_sz,screen_sz])
running = True
pg.init()

prev_move = "N/A"
result = "N/A"

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if user_control:
                if event.key in [pg.K_a, pg.K_LEFT]:
                    env.move_agent("left")
                elif event.key in [pg.K_d, pg.K_RIGHT]:
                    env.move_agent("right")
                elif event.key in [pg.K_w, pg.K_UP]:
                    env.move_agent("up")
                elif event.key in [pg.K_s, pg.K_DOWN]:
                    env.move_agent("down")

    screen.fill((0,0,0))
    for i in range(env.sz**2):
        sz = env.sz
        r, c = i // env.sz, i % env.sz
        val = env.level[r, c]
        pg.draw.rect(screen, colors[val], pg.Rect(c * screen_sz / env.sz, r * screen_sz / env.sz, screen_sz / env.sz, screen_sz / env.sz))

    if not user_control:
        prompt = generate_prompt()
        prev_move = lmca_move(prompt)
        result = env.move_agent(prev_move)

    pg.display.flip()

pg.quit()
