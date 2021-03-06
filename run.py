#! /usr/bin/python3
"""Startup file for the hackathon game.

Date: 2015-03-07
Authors: PythonJedi, jkwiedman"""

# stdlib imports
import time, os

# project imports
import src.gfx as gfx
import src.event as event
import res.res as res
from src.entity import Seed
from src.controller import Controller
from src.camera import Camera
from src.sprite import Group, Sheet
import lib.sdl2 as sdl2 # need event constants

FPS = 30.0

SPF = 1/FPS


def main():
    gfx.init()
    
    controller = Controller((sdl2.SDLK_w, sdl2.SDLK_s, sdl2.SDLK_a, sdl2.SDLK_d))

    win = gfx.Window("testing", (640, 480))
    ren = gfx.Renderer(win)
    sprite_rects = Sheet()
    
    lev, start, end, seeds, checkpoints = res.load_level("res\\Test-Level.txt", sprite_rects)
    
    cam = Camera(start.center, gfx.Texture(ren, "res\\game-tiles.bmp"), ren)
    
    world = Group()
    world.append(lev)
    world.append(seeds)
    world.append(checkpoints)
    if end:
        world.add(end)

    running = True
    e = event.Event()
    while running:
        start = time.time()
        while event.poll(e):
            if e.type == sdl2.SDL_QUIT:
                running = False
                break
            elif e.type in (sdl2.SDL_KEYDOWN, sdl2.SDL_KEYUP):
                controller.update(e)    
        cam.update(controller)
        world.update()
        ren.clear()
        cam.render_all(world)
        ren.present()
        end = time.time()
        diff = end-start
        if diff < SPF:
            time.sleep(SPF-diff)
        
        
    del(world)
    del(sprite_rects)
    del(ren)
    del(win)

    gfx.quit()
    
if __name__ == "__main__":
    main()