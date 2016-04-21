#!/usr/bin/env python3

from PyMata.pymata import PyMata
from enum import Enum
import subprocess
from collections import deque
import random
from time import sleep

class State(Enum):
    stop = 0
    play_normal = 1
    play_end = 2
    play_stopped = 3
    stop_stopped = 4
    stop_playing = 5



board = PyMata(bluetooth=False)
board.set_pin_mode(1, board.INPUT, board.ANALOG)
state = State.stop
lugemite_arv = 1
lugemid = deque(maxlen=lugemite_arv)
    
end_sound = "tsiktsikaa.wav"

end_sounds = ("tsiktsikaa.wav", "potter.wav")

sound = ("walkthedinosaur.wav", 
         "gangstersparadise.wav",
         "offspring.wav",
         "scatman.wav",
         "frog.wav")

player = None

last_played_song = "potter.wav"

def get_end_song():
    return "tsiktsikaa.wav"
    global last_played_song
    if last_played_song == "potter.wav":
        last_played_song = "tsiktsikaa.wav"
        return "tsiktsikaa.wav"
    else:
        last_played_song = "potter.wav"
        return "potter.wav"

def print_vals():
    vals = ["distance:", int(distance),
          "state:", state,
          "player:",player,
          ]

    if player:
        vals.extend(["returncode:", player.returncode])

    
    print(*vals, flush=True)


while True:
    value = board.analog_read(1)
    sleep(0.1)
    try:
        distance = 6762 / (value -9) -4
    except:
        distance = 9001
    lugemid.append(distance)

    distance = sum(lugemid) / len(lugemid)
    if distance < 0 :
        distance  = - distance

    if distance < 40:
        if state not in (State.play_normal, State.play_end, State.play_stopped):
            state = State.play_normal
            print_vals()
    if distance > 60:
        if state not in (State.stop, State.stop_playing, State.stop_stopped):
            state = State.stop
            print_vals()

    if player:
        player.poll()

    if state == State.play_normal and not player:
        player = subprocess.Popen(["aplay", "-q", random.choice(sound)])

    if state == State.play_normal and player and player.returncode == 0:
        state = State.play_end
        player = subprocess.Popen(["aplay", "-q", end_sound])

    if state == State.play_end and player and player.returncode == 0:
        player = None
        state = State.play_stopped

    if state == State.stop:
        if player and player.returncode != 0:
            player.terminate()
            player = None
        player = subprocess.Popen(["aplay", "-q", get_end_song()])
        state = State.stop_playing


    if state == State.stop_playing and player and player.returncode == 0:
        player = None
        state = State.stop_stopped



    print_vals()

