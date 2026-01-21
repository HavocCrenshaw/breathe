# breathe.py
# personal breathing exercise utility
# prototype, half assed code, will be corrected in the future.

# Copyright (C) 2026 Havoc Crenshaw.
# Licensed under the MIT License. See LICENSE.

from enum import Enum

import numpy as np
import pygame as pg
import pygame.freetype
from pygame import gfxdraw

SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
CIRCLE_RADIUS = SCREEN_HEIGHT * 1/10
SMALL_CIRCLE_RADIUS = CIRCLE_RADIUS * 1/3
CIRCLE_Y = SCREEN_HEIGHT * 4/10

SECTION = 4 # seconds

COLOR_MAIN = (7, 89, 151)
COLOR_DARKER = (57, 122, 172)
COLOR_WHITE = (236, 242, 247)

# ripped from PyPong
def get_total_text_width(font: pygame.freetype.Font, text: str) -> int:
    metrics = font.get_metrics(text)

    total_width = 0
    for char_metrics in metrics:
        # Add the `horizontal_advance_x` of a single character
        total_width += char_metrics[4] 
    return total_width

class State(Enum):
    WAIT = 0
    BOX = 1
    CONTINUOUS = 2

class Step(Enum):
    BREATHE_OUT = 0
    BREATHE_IN = 1
    PAUSE_1 = 2
    PAUSE_2 = 3

# Purely because Python is a fucking idiot about variables
class Owner:
    def __init__(self):
        self.current_state = State.WAIT
        self.current_step = Step.BREATHE_IN

        pg.init()
        pg.freetype.init()

        self.font = pg.freetype.SysFont("DejaVu Sans", 36)

        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("breathe")
        self.clock = pg.time.Clock()
        self.timer = 0.0
        self.dt = 0.0
        
    def flip_state(self):
        self.timer = 0.0
        if self.current_state == State.WAIT:
            self.current_state = State.BOX
        elif self.current_state == State.BOX:
            self.current_state = State.CONTINUOUS
        else:
            # Must be State.CONTINUOUS
            self.current_state = State.BOX

        self.current_step = Step.BREATHE_IN

    def change_step(self):
        self.timer = 0.0
        if self.current_state == State.BOX:
            if self.current_step == Step.BREATHE_IN:
                self.current_step = Step.PAUSE_1
            elif self.current_step == Step.PAUSE_1:
                self.current_step = Step.BREATHE_OUT
            elif self.current_step == Step.BREATHE_OUT:
                self.current_step = Step.PAUSE_2
            else:
                # Must be Step.PAUSE_2
                self.current_step = Step.BREATHE_IN
        else:
            # Must be State.CONTINUOUS
            if self.current_step == Step.BREATHE_OUT:
                self.current_step = Step.BREATHE_IN
            else:
                # Must be Step.BREATHE_IN
                self.current_step = Step.BREATHE_OUT

    def render(self):
        if self.current_state == State.WAIT:
            str_1 = "It's time to destress and breathe."
            center_x = get_total_text_width(self.font, str_1) / 2
            x = (SCREEN_WIDTH / 2) - center_x
            y = SCREEN_HEIGHT * 3/10
            str_2 = "Press space to switch between"
            str_3 = "continuous and box breathing."
            cx2 = get_total_text_width(self.font, str_2) / 2
            x2 = (SCREEN_WIDTH / 2) - cx2
            y2 = SCREEN_HEIGHT * 6/10
            cx3 = get_total_text_width(self.font, str_3) / 2
            x3 = (SCREEN_WIDTH / 2) - cx3
            y3 = SCREEN_HEIGHT * 13/20
            if self.timer < 1:
                norm = (self.timer / 1) # Range between 0-1 over 2 seconds
                color_rgba = COLOR_WHITE + (norm * 255,)
            else:
                color_rgba = COLOR_WHITE + (255,)
            self.font.render_to(self.screen, (x, y), str_1, color_rgba)
            self.font.render_to(self.screen, (x2, y2), str_2, color_rgba)
            self.font.render_to(self.screen, (x3, y3), str_3, color_rgba)
        else:
            # sort of a waste if on PAUSE_1 but eh
            # also this barely does aa lol i probably need something like tkinter
            # but idk tkinter (maybe if i rewrite for better)
            pg.gfxdraw.filled_circle(self.screen, int(SCREEN_WIDTH/2),
                                     int(CIRCLE_Y), int(CIRCLE_RADIUS),
                                     COLOR_DARKER)
            pg.gfxdraw.aacircle(self.screen, int(SCREEN_WIDTH/2),
                                int(CIRCLE_Y), int(CIRCLE_RADIUS),
                                COLOR_DARKER)
            # print current step # print "breathe" have it fade in and out with
            # the step like with quick fall off instead of linearly
            if self.current_step == Step.BREATHE_IN:
                string = "Breathe in."
                cx = get_total_text_width(self.font, string) / 2
                x = SCREEN_WIDTH / 2 - cx
                y = SCREEN_HEIGHT * 6/10
                if self.timer < 0.5:
                    norm = (self.timer / 0.5) # Range between 0-1 over 0.5 seconds
                    color_rgba = COLOR_WHITE + (norm * 255,)
                elif self.timer > 2.5 and self.timer < 3:
                    norm = ((self.timer - 2.5) / 0.5)
                    opp = 1 - norm
                    color_rgba = COLOR_WHITE + (opp * 255,)
                elif self.timer > 3:
                    color_rgba = COLOR_WHITE + (0,)
                else:
                    color_rgba = COLOR_WHITE + (255,)
                self.font.render_to(self.screen, (x, y), string, color_rgba)
                # btw i have no idea why the math needs to be like this this is
                # just what worked
                if self.timer == 0.0:
                    self.timer = 0.0000001 # No divisions by zero
                norm = (self.timer / SECTION) # Range between 0-1
                difference = (CIRCLE_RADIUS - SMALL_CIRCLE_RADIUS)
                current_radius = (difference * norm) + SMALL_CIRCLE_RADIUS
            elif self.current_step == Step.PAUSE_1:
                string = "Hold it."
                cx = get_total_text_width(self.font, string) / 2
                x = SCREEN_WIDTH / 2 - cx
                y = SCREEN_HEIGHT * 6/10
                if self.timer < 0.5:
                    norm = (self.timer / 0.5) # Range between 0-1 over 0.5 seconds
                    color_rgba = COLOR_WHITE + (norm * 255,)
                elif self.timer > 2.5 and self.timer < 3:
                    norm = ((self.timer - 2.5) / 0.5)
                    opp = 1 - norm
                    color_rgba = COLOR_WHITE + (opp * 255,)
                elif self.timer > 3:
                    color_rgba = COLOR_WHITE + (0,)
                else:
                    color_rgba = COLOR_WHITE + (255,)
                self.font.render_to(self.screen, (x, y), string, color_rgba)
                current_radius = CIRCLE_RADIUS
            elif self.current_step == Step.PAUSE_2:
                string = "Hold it."
                cx = get_total_text_width(self.font, string) / 2
                x = SCREEN_WIDTH / 2 - cx
                y = SCREEN_HEIGHT * 6/10
                if self.timer < 0.5:
                    norm = (self.timer / 0.5) # Range between 0-1 over 0.5 seconds
                    color_rgba = COLOR_WHITE + (norm * 255,)
                elif self.timer > 2.5 and self.timer < 3:
                    norm = ((self.timer - 2.5) / 0.5)
                    opp = 1 - norm
                    color_rgba = COLOR_WHITE + (opp * 255,)
                elif self.timer > 3:
                    color_rgba = COLOR_WHITE + (0,)
                else:
                    color_rgba = COLOR_WHITE + (255,)
                self.font.render_to(self.screen, (x, y), string, color_rgba)
                current_radius = SMALL_CIRCLE_RADIUS
            else:
                string = "Breathe out."
                cx = get_total_text_width(self.font, string) / 2
                x = SCREEN_WIDTH / 2 - cx
                y = SCREEN_HEIGHT * 6/10
                if self.timer < 0.5:
                    norm = (self.timer / 0.5) # Range between 0-1 over 0.5 seconds
                    color_rgba = COLOR_WHITE + (norm * 255,)
                elif self.timer > 2.5 and self.timer < 3:
                    norm = ((self.timer - 2.5) / 0.5)
                    opp = 1 - norm
                    color_rgba = COLOR_WHITE + (opp * 255,)
                elif self.timer > 3:
                    color_rgba = COLOR_WHITE + (0,)
                else:
                    color_rgba = COLOR_WHITE + (255,)
                self.font.render_to(self.screen, (x, y), string, color_rgba)
                # Must be Step.BREATHE_OUT
                if self.timer == 0.0:
                    self.timer = 0.0000001 # No divisions by zero
                norm = (self.timer / SECTION) # Range between 0-1
                opp = 1 - norm
                difference = (CIRCLE_RADIUS - SMALL_CIRCLE_RADIUS)
                current_radius = (difference * opp) + SMALL_CIRCLE_RADIUS

            pg.gfxdraw.filled_circle(self.screen, int(SCREEN_WIDTH/2),
                                     int(CIRCLE_Y), int(current_radius),
                                     COLOR_WHITE)
            pg.gfxdraw.aacircle(self.screen, int(SCREEN_WIDTH/2),
                                int(CIRCLE_Y), int(current_radius),
                                COLOR_WHITE)

    def do(self):
        self.timer += self.dt
        if self.current_state != State.WAIT:
            if self.timer >= SECTION:
                self.change_step()
        self.render()

owner = Owner()
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                owner.flip_state()
            if event.key == pg.K_ESCAPE:
                running = False

    owner.screen.fill(COLOR_MAIN)

    owner.do()

    pg.display.flip()

    owner.dt = owner.clock.tick() / 1000
