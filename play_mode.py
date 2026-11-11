from pico2d import *
import game_world
import game_framework
from boy import Boy
from bird import Bird
from grass import Grass

boy = None
bird = None


def handle_events():


    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def init():
    global boy, bird

    bird = Bird()
    game_world.add_oject(bird)

    boy = Boy()
    game_world.add_oject(boy)

    grass = Grass()
    game_world.add_oject(grass, 0)


def pause():
    boy.pause()


def resume():
    pass


def finish():
    global boy, bird
    game_world.clear()
    boy = None
    bird = None


def update():
    game_world.update()

def render():
    clear_canvas()
    game_world.render()
    update_canvas()









