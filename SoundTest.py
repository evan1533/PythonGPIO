import pyglet
import threading
import time

def loop1_10():
    count = 0;
    player = pyglet.media.Player();
    neva = pyglet.media.load('NeverGonnaGiveYouUp.wav');
    player.queue(neva);
    player.play();
    while True:
        time.sleep(1)
        count = count + 1;
        if count>10:
            player.play();
        elif count > 5:
            player.pause();

threading.Thread(target=loop1_10).start()

import ServerTest
import TestClient

