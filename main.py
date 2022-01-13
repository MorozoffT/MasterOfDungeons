import os
import sys
import random
import time
from PIL import Image
from pygame.locals import *

import pygame
from pygame.locals import FULLSCREEN

pygame.init()
info_screen = pygame.display.Info()
WIDTH, HEIGHT = info_screen.current_w, info_screen.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN)
print(1536, 864)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f'Файл с изображением "{fullname}" не найден')
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image


class Player(pygame.sprite.Sprite):
    image = load_image('Player1.png')
    # image = pygame.transform.scale(image, (WIDTH, HEIGHT))

    def __init__(self, *group):
        super().__init__(*group)
        self.predelX = (0.5 * WIDTH // 1) - (0.5 * WIDTH * 6 / 7) // 1
        self.predelY = (0.5 * HEIGHT // 1) - (0.5 * HEIGHT * 3 / 4) // 1
        self.pos = 'right'
        self.karta = 0
        self.EZ = 0
        self.inerziaRIGHT = 0
        self.inerziaLEFT = 0
        self.inerziaUP = 0
        self.inerziaDOWN = 0
        self.image = Player.image
        self.image = pygame.transform.scale(self.image, (160, 132))
        self.rect = self.image.get_rect()
        self.rect.x = 0.5 * WIDTH // 1
        self.rect.y = 0.5 * HEIGHT // 1

    def up(self):
        if self.rect.y > self.predelY:
            self.inerziaUP = 15
            self.EZ += 1
            if self.pos == 'right':
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.pos == 'left':
                self.image = pygame.transform.rotate(self.image, 270)
            elif self.pos == 'up':
                pass
            elif self.pos == 'down':
                self.image = pygame.transform.rotate(self.image, 180)
            self.pos = 'up'
            if self.EZ % 10 == 0:
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.rect.move(0, -5)

    def down(self):
        if self.rect.y + 132 < HEIGHT - self.predelY:
            self.inerziaDOWN = 15
            self.EZ += 1
            if self.pos == 'right':
                self.image = pygame.transform.rotate(self.image, 270)
            elif self.pos == 'left':
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.pos == 'up':
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.pos == 'down':
                pass
            self.pos = 'down'
            if self.EZ % 10 == 0:
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.rect.move(0, 5)

    def right(self):
        if self.rect.x + 152 <= WIDTH - self.predelX:
            self.inerziaRIGHT = 15
            self.EZ += 1
            if self.pos == 'right':
                pass
            elif self.pos == 'left':
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.pos == 'up':
                self.image = pygame.transform.rotate(self.image, 270)
            elif self.pos == 'down':
                self.image = pygame.transform.rotate(self.image, 90)
            self.pos = 'right'
            if self.EZ % 10 == 0:
                self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.rect.move(5, 0)

    def left(self):
        if self.rect.x > self.predelX:
            self.inerziaLEFT = 15
            self.EZ += 1
            if self.pos == 'right':
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.pos == 'left':
                pass
            elif self.pos == 'up':
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.pos == 'down':
                self.image = pygame.transform.rotate(self.image, 270)
            self.pos = 'left'
            if self.EZ % 10 == 0:
                self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.rect.move(-5, 0)

    def inerzia(self):
        self.karta += 1
        if self.karta % 40 == 0:
            if self.inerziaUP != 0:
                self.rect = self.rect.move(0, -self.inerziaUP)
                self.inerziaUP -= 3
            if self.inerziaDOWN != 0:
                self.rect = self.rect.move(0, self.inerziaDOWN)
                self.inerziaDOWN -= 3
            if self.inerziaRIGHT != 0:
                self.rect = self.rect.move(self.inerziaRIGHT, 0)
                self.inerziaRIGHT -= 3
            if self.inerziaLEFT != 0:
                self.rect = self.rect.move(-self.inerziaLEFT, 0)
                self.inerziaLEFT -= 3

    def NEWcords(self, posX, posY):
        self.rect.x = posX
        self.rect.y = posY

    def GETcords(self):
        return self.rect.x, self.rect.y


player_sprite = pygame.sprite.Group()
ROOM1_sprites = pygame.sprite.Group()
ROOM2_sprites = pygame.sprite.Group()
ROOM3_sprites = pygame.sprite.Group()
ROOM4_sprites = pygame.sprite.Group()


player = Player(player_sprite)


class Door(pygame.sprite.Sprite):
    image = load_image('door1.png')
    doorZEL = load_image("door1GREEN.png")
    doorRED = load_image("door1RED.png")

    def __init__(self, group, room, cordX, cordY, ugol, perehod, prozent):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.room = room

        self.perehod = perehod
        self.ugol = ugol

        self.door = Door.image
        self.door = pygame.transform.rotate(self.door, ugol)
        self.door = pygame.transform.scale(self.door, (((213 * ((HEIGHT * 0.333) // 1) / 401) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))

        self.osnova = self.door

        self.doorZEL = Door.doorZEL
        self.doorZEL = pygame.transform.rotate(self.doorZEL, ugol)
        self.doorZEL = pygame.transform.scale(self.doorZEL, (((213 * ((HEIGHT * 0.333) // 1) / 401) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))

        self.doorRED = Door.doorRED
        self.doorRED = pygame.transform.rotate(self.doorRED, ugol)
        self.doorRED = pygame.transform.scale(self.doorRED, (((213 * ((HEIGHT * 0.333) // 1) / 401) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))

        self.rect = self.door.get_rect()
        self.rect.x = cordX
        self.rect.y = cordY

    def update(self, *args):
        if args == (0,):
            self.image = self.door
        elif args and args[0].type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(args[0].pos) and pygame.sprite.collide_mask(self, player):
                if self.ugol == 270:
                    return self.perehod, self.rect.x - (0.86 * WIDTH) // 1, (self.rect.y * 1.08) // 1, 1
                elif self.ugol == 90:
                    return self.perehod, self.rect.x + (0.84 * WIDTH) // 1, (self.rect.y * 1.08) // 1, 1
            else:
                return self.room, player.GETcords()[0], player.GETcords()[1], 0
        else:
            if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                    and not pygame.sprite.collide_mask(self, player):
                self.image = self.doorRED
            else:
                if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                        and pygame.sprite.collide_mask(self, player):
                    self.image = self.doorZEL
                else:
                    if args and self.rect.collidepoint(args[0].pos) is False:
                        self.image = self.osnova


class DoorWithKeyPurple(pygame.sprite.Sprite):
    image = load_image('doorPurple.png')
    # doorZEL = load_image("doorPurpleZEL.png")
    # doorRED = load_image("doorPurpleRED.png")

    def __init__(self, group, room, cordX, cordY, ugol, perehod, prozent):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.room = room

        self.perehod = perehod
        self.ugol = ugol

        self.door = DoorWithKeyPurple.image
        self.door = pygame.transform.rotate(self.door, ugol)
        self.door = pygame.transform.scale(self.door, (((207 * ((HEIGHT * 0.333) // 1) / 77) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))

        self.osnova = self.door

        # self.doorZEL = Door.doorZEL
        # self.doorZEL = pygame.transform.rotate(self.doorZEL, ugol)
        # self.doorZEL = pygame.transform.scale(self.doorZEL, (((213 * ((HEIGHT * 0.333) // 1) / 401) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))
        #
        # self.doorRED = Door.doorRED
        # self.doorRED = pygame.transform.rotate(self.doorRED, ugol)
        # self.doorRED = pygame.transform.scale(self.doorRED, (((213 * ((HEIGHT * 0.333) // 1) / 401) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))

        self.rect = self.door.get_rect()
        self.rect.x = cordX
        self.rect.y = cordY

    def updater(self, permission, *args):
        if permission == 9:
            self.image = self.door
        if permission == 1:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(args[0].pos) and pygame.sprite.collide_mask(self, player):
                    if self.ugol == 270:
                        return self.perehod, self.rect.x - (0.86 * WIDTH) // 1, (self.rect.y * 1.08) // 1, 1
                    elif self.ugol == 90:
                        return self.perehod, self.rect.x + (0.84 * WIDTH) // 1, (self.rect.y * 1.08) // 1, 1
                    elif self.ugol == 0:
                        return self.perehod, (self.rect.x * 1.13) // 1, HEIGHT - self.rect.height * 2.28, 1
                    elif self.ugol == 180:
                        print(1)
                        return self.perehod, (self.rect.x * 1.13) // 1, self.rect.height * 1.1, 1
                else:
                    return self.room, player.GETcords()[0], player.GETcords()[1], 0
            else:
                return 0, 0, 0, 0
        else:
            return self.room, player.GETcords()[0], player.GETcords()[1], 0
                # if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                #         and not pygame.sprite.collide_mask(self, player):
                #     self.image = self.doorRED
                # else:
                #     if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                #             and pygame.sprite.collide_mask(self, player):
                #         self.image = self.doorZEL
                #     else:
                #         if args and self.rect.collidepoint(args[0].pos) is False:
                #             self.image = self.osnova


class DoorWithKeyBlue(pygame.sprite.Sprite):
    image = load_image('doorBlue.png')
    # doorZEL = load_image("doorPurpleZEL.png")
    # doorRED = load_image("doorPurpleRED.png")

    def __init__(self, group, room, cordX, cordY, ugol, perehod, prozent):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.room = room

        self.perehod = perehod
        self.ugol = ugol

        self.door = DoorWithKeyBlue.image
        self.door = pygame.transform.rotate(self.door, ugol)
        self.door = pygame.transform.scale(self.door, (((207 * ((HEIGHT * 0.333) // 1) / 77) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))

        self.osnova = self.door

        # self.doorZEL = Door.doorZEL
        # self.doorZEL = pygame.transform.rotate(self.doorZEL, ugol)
        # self.doorZEL = pygame.transform.scale(self.doorZEL, (((213 * ((HEIGHT * 0.333) // 1) / 401) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))
        #
        # self.doorRED = Door.doorRED
        # self.doorRED = pygame.transform.rotate(self.doorRED, ugol)
        # self.doorRED = pygame.transform.scale(self.doorRED, (((213 * ((HEIGHT * 0.333) // 1) / 401) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))

        self.rect = self.door.get_rect()
        self.rect.x = cordX
        self.rect.y = cordY

    def updater(self, permission, *args):
        if permission == 9:
            self.image = self.door
        if permission == 1:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(args[0].pos) and pygame.sprite.collide_mask(self, player):
                    return 'end1'
                else:
                    return 1
            else:
                return 1
        else:
            return self.room, player.GETcords()[0], player.GETcords()[1], 0
                # if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                #         and not pygame.sprite.collide_mask(self, player):
                #     self.image = self.doorRED
                # else:
                #     if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                #             and pygame.sprite.collide_mask(self, player):
                #         self.image = self.doorZEL
                #     else:
                #         if args and self.rect.collidepoint(args[0].pos) is False:
                #             self.image = self.osnova


class Rat(pygame.sprite.Sprite):
    image = load_image('rat1.png')
    rat2 = load_image("rat2.png")

    def __init__(self, group, cordX, cordY, prozent):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)

        self.rat1 = Rat.image
        self.rat1 = pygame.transform.scale(self.rat1, ((103 * WIDTH / 1536) // 1, (75 * HEIGHT / 864) // 1))

        self.rat2 = Rat.rat2
        self.rat2 = pygame.transform.scale(self.rat2, (
            ((213 * ((HEIGHT * 0.333) // 1) / 401) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))

        self.rect = self.rat1.get_rect()
        self.rect.x = cordX
        self.rect.y = cordY

        self.predelX = (0.5 * WIDTH // 1) - (0.5 * WIDTH * 6 / 7) // 1

        self.key = [0, 0]
        self.N = 0

        self.pos = 'left'

    def updater(self):
        if self.N == 0:
            key = random.randint(1, 150)
            if key == 25:
                self.N = 1
                if random.randint(1, 2) == 1:
                    self.key = [1, 151]
                else:
                    self.key = [2, 151]
        elif self.N == 1:
            if self.key[1] == 1:
                self.N = 0

            if self.key[0] == 1:
                self.key[1] -= 1
                if self.pos == 'left':
                    pass
                elif self.pos == 'right':
                    self.pos = 'left'
                    self.image = pygame.transform.flip(self.image, True, False)
                if self.rect.x > self.predelX:
                    if self.key[1] % 2 == 0:
                        self.rect.x -= 3
            else:
                if self.key[0] == 2:
                    self.key[1] -= 1
                    if self.pos == 'right':
                        pass
                    elif self.pos == 'left':
                        self.pos = 'right'
                        self.image = pygame.transform.flip(self.image, True, False)
                    if self.rect.x + 152 <= WIDTH - self.predelX:
                        if self.key[1] % 2 == 0:
                            self.rect.x += 3

    def update_EZ(self, *args):
        if args == (0,):
            self.image = self.rat1


class KeyPurple(pygame.sprite.Sprite):
    image = load_image('keyPurple.png')

    def __init__(self, group, cordX, cordY, prozent):
        super().__init__(group)

        self.key = KeyPurple.image
        self.key = pygame.transform.scale(self.key, ((300 * WIDTH / 1536) // 1 * prozent, (372 * HEIGHT / 864) // 1 * prozent))

        self.rect = self.key.get_rect()
        self.rect.x = cordX
        self.rect.y = cordY

    def update_EZ(self, *args):
        if args == (0,):
            self.image = self.key

    def updater(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(args[0].pos) and pygame.sprite.collide_mask(self, player):
                self.image = pygame.transform.scale(self.image, (0, 0))
                return 1
            else:
                return 0
        else:
            return 0


class KeyBlue(pygame.sprite.Sprite):
    image = load_image('keyBlue.png')

    def __init__(self, group, cordX, cordY, prozent):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)

        self.key = KeyBlue.image
        self.key = pygame.transform.scale(self.key, ((300 * WIDTH / 1536) // 1 * prozent, (372 * HEIGHT / 864) // 1 * prozent))

        self.rect = self.key.get_rect()
        self.rect.x = cordX
        self.rect.y = cordY

    def update_EZ(self, *args):
        if args == (0,):
            self.image = self.key

    def updater(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(args[0].pos) and pygame.sprite.collide_mask(self, player):
                self.image = pygame.transform.scale(self.image, (0, 0))
                return 1
            else:
                return 0
        else:
            return 0


class Ded(pygame.sprite.Sprite):
    image = load_image('ded.png')
    dedPOSLANIE = load_image('dedPOSLANIE.png')

    def __init__(self, group, cordX, cordY, prozent):
        super().__init__(group)

        self.ded = Ded.image
        self.ded = pygame.transform.scale(self.ded, ((404 * WIDTH / 1536) // 1 * prozent, (618 * HEIGHT / 864) // 1 * prozent))
        self.ded = pygame.transform.flip(self.ded, True, False)

        self.dedPOSLANIE = Ded.dedPOSLANIE
        self.dedPOSLANIE = pygame.transform.scale(self.dedPOSLANIE, ((554 * WIDTH / 1536) // 1 * (prozent + 0.23), (398 * HEIGHT / 864) // 1 * (prozent + 0.23)))
        self.osnova = self.ded

        self.rect = self.ded.get_rect()
        self.rect.x = cordX
        self.rect.y = cordY

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos):
            self.image = self.dedPOSLANIE
        else:
            if args and self.rect.collidepoint(args[0].pos) is False:
                self.image = self.osnova

    def update_EZ(self, *args):
        if args == (0,):
            self.image = self.ded


def main():
    fps = 144
    clock = pygame.time.Clock()
    pygame.display.set_caption("Master of Dungeon")
    # sprite = pygame.sprite.Sprite()

    door = Door(ROOM1_sprites, 1, (WIDTH * 0.934 // 1), ((0.55 * HEIGHT) // 1), 270, 2, 0.8)
    door.update(0)

    door2 = Door(ROOM2_sprites, 2, (WIDTH * -0.01 // 1), ((0.55 * HEIGHT) // 1), 90, 1, 0.8)
    door2.update(0)

    door3 = Door(ROOM1_sprites, 1, (WIDTH * -0.01 // 1), ((0.3 * HEIGHT) // 1), 90, 3, 0.8)
    door3.update(0)

    door4 = Door(ROOM3_sprites, 3, (WIDTH * 0.934 // 1), ((0.3 * HEIGHT) // 1), 270, 1, 0.8)
    door4.update(0)

    doorPurple = DoorWithKeyPurple(ROOM1_sprites, 1, ((WIDTH * 0.4 // 1)), (0), 0, 4, 0.37)
    doorPurple.updater(9)

    doorPurple2 = DoorWithKeyPurple(ROOM4_sprites, 4, ((WIDTH * 0.4 // 1)), (HEIGHT - 100), 180, 1, 0.37)
    doorPurple2.updater(9)

    doorBlue = DoorWithKeyBlue(ROOM4_sprites, 4, ((WIDTH * 0.4 // 1)), (0), 0, 1, 0.37)
    doorBlue.updater(9)

    rat = Rat(ROOM1_sprites, 600, 120, 1)
    rat2 = Rat(ROOM1_sprites, 200, 210, 1)
    rat3 = Rat(ROOM1_sprites, 200, 670, 1)
    rat4 = Rat(ROOM2_sprites, 200, 670, 1)
    rat5 = Rat(ROOM4_sprites, 200, 560, 1)
    rat6 = Rat(ROOM3_sprites, 200, 120, 1)
    rat7 = Rat(ROOM3_sprites, 200, 210, 1)
    rat8 = Rat(ROOM3_sprites, 200, 560, 1)

    rat2.update_EZ(0)
    rat.update_EZ(0)
    rat3.update_EZ(0)
    rat4.update_EZ(0)
    rat5.update_EZ(0)
    rat6.update_EZ(0)
    rat7.update_EZ(0)
    rat8.update_EZ(0)

    ded = Ded(ROOM1_sprites, 140, 520, 0.37)
    ded.update_EZ(0)

    keyPurple = KeyPurple(ROOM2_sprites, 1275, 150, 0.3)
    keyPurple.update_EZ(0)

    keyBlue = KeyBlue(ROOM3_sprites, 150, 150, 0.3)
    keyBlue.update_EZ(0)

    FON = load_image('FON.png')
    FON = pygame.transform.scale(FON, (WIDTH, HEIGHT))

    NachFON = load_image('NachFON.png')
    NachFON = pygame.transform.scale(NachFON, (WIDTH, HEIGHT))
    running = True
    Nach = 0
    level = 1
    room = 1
    q = 0
    font = pygame.font.SysFont("Ubuntu Condensed", 90, bold=False, italic=False)
    font2 = pygame.font.SysFont("Ubuntu Condensed", 50, bold=False, italic=False)
    PurplePermission = 0
    BluePermission = 0
    while running:
        if Nach == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        Nach = 1
            screen.blit(NachFON, (0, 0))

            text1 = font.render("Master of Dungeon's", True, (50, 100, 255))
            screen.blit(text1, [(0.31 * WIDTH) // 1, (0.2 * HEIGHT) // 1])

            text2 = font2.render("Новая игра: N", True, (50, 150, 255))
            screen.blit(text2, [(0.4 * WIDTH) // 1, (0.4 * HEIGHT) // 1])

            text3 = font2.render("Продолжить: Space", True, (50, 150, 255))
            screen.blit(text3, [(0.4 * WIDTH) // 1, (0.5 * HEIGHT) // 1])

            text4 = font2.render("Выйти: Esc", True, (50, 150, 255))
            screen.blit(text4, [(0.4 * WIDTH) // 1, (0.6 * HEIGHT) // 1])

            pygame.display.flip()
        else:
            if level == 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEMOTION:
                        q = event
                        if room == 1:
                            door.update(event)
                            door3.update(event)
                            doorPurple.update(event)
                            ded.update(event)
                        elif room == 2:
                            door2.update(event)
                        elif room == 3:
                            door4.update(event)
                        elif room == 4:
                            doorPurple2.update(event)
                            doorBlue.update(event)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if PurplePermission == 0:
                            PurplePermission = keyPurple.updater(event)
                        if BluePermission == 0:
                            BluePermission = keyBlue.updater(event)
                        if room == 1:
                            room, posX, posY = 0, 0, 0
                            room, posX, posY, h = door.update(event)
                            if h == 0:
                                room, posX, posY, h = door3.update(event)
                            if h == 0:
                                room, posX, posY, h = doorPurple.updater(PurplePermission, event)
                            player.NEWcords(posX, posY)
                        elif room == 2:
                            room, posX, posY, h = door2.update(event)
                            player.NEWcords(posX, posY)
                        elif room == 3:
                            room, posX, posY, h = door4.update(event)
                            player.NEWcords(posX, posY)
                        elif room == 4:
                            room, posX, posY, h = doorPurple2.updater(1, event)
                            if h == 0:
                                level = doorBlue.updater(BluePermission, event)
                            player.NEWcords(posX, posY)
                    else:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_w] is True:
                            player.up()
                        if keys[pygame.K_a] is True:
                            player.left()
                        if keys[pygame.K_s] is True:
                            player.down()
                        if keys[pygame.K_d] is True:
                            player.right()
                        if keys[pygame.K_ESCAPE]:
                            running = False


                rat.updater()
                rat2.updater()
                rat3.updater()
                rat4.updater()
                rat5.updater()
                rat6.updater()
                rat7.updater()
                rat8.updater()

                player.inerzia()
                screen.blit(FON, (0, 0))


                door.update(q)
                door2.update(q)
                door3.update(q)
                door4.update(q)
                doorPurple.update(q)
                doorPurple2.update(q)
                doorBlue.update(q)

                # ded.update(q)


                if room == 1:
                    ROOM1_sprites.draw(screen)
                    ROOM1_sprites.update()
                elif room == 2:
                    ROOM2_sprites.draw(screen)
                    ROOM2_sprites.update()
                elif room == 3:
                    ROOM3_sprites.draw(screen)
                    ROOM3_sprites.update()
                elif room == 4:
                    ROOM4_sprites.draw(screen)
                    ROOM4_sprites.update()

                player_sprite.draw(screen)
                player_sprite.update()

                pygame.display.flip()
            elif level == 'end1':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            Nach = 1

                screen.fill((0, 0, 0))
                screen.blit(NachFON, (0, 0))

                text1 = font.render("Первый уровень пройден!", True, (50, 100, 255))
                screen.blit(text1, [(0.28 * WIDTH) // 1, (0.2 * HEIGHT) // 1])


                text3 = font2.render("Продолжить: Space", True, (50, 150, 255))
                screen.blit(text3, [(0.4 * WIDTH) // 1, (0.4 * HEIGHT) // 1])

                text4 = font2.render("Сохранить и выйти: Esc", True, (50, 150, 255))
                screen.blit(text4, [(0.4 * WIDTH) // 1, (0.5 * HEIGHT) // 1])

                pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()