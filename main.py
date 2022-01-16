import os
import sys
import random

import pygame
from pygame.locals import FULLSCREEN

pygame.init()
info_screen = pygame.display.Info()
WIDTH, HEIGHT = info_screen.current_w, info_screen.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN)


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
    image = load_image('chel.png')

    def __init__(self, group, columns, rows, prozent):
        super().__init__(group)
        self.predelX = (0.5 * WIDTH // 1) - (0.5 * WIDTH * 8 / 9) // 1
        self.predelY = (0.5 * HEIGHT // 1) - (0.5 * HEIGHT * 7 / 8) // 1
        self.pos = 'right'
        self.karta = 0
        self.inerziaRIGHT = 0
        self.inerziaLEFT = 0
        self.inerziaUP = 0
        self.inerziaDOWN = 0
        self.frames = []
        self.cut_sheet(Player.image, columns, rows, prozent)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.EZ = 0
        self.prozent = prozent

    def cut_sheet(self, sheet, columns, rows, prozent):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

        self.frames[0] = pygame.transform.scale(self.frames[0], (222 / 1536 * WIDTH * prozent, 287 / 864 * HEIGHT * prozent))
        self.frames[1] = pygame.transform.scale(self.frames[1], (222 / 1536 * WIDTH * prozent, 287 / 864 * HEIGHT * prozent))
        self.frames[2] = pygame.transform.scale(self.frames[2], (222 / 1536 * WIDTH * prozent, 287 / 864 * HEIGHT * prozent))
        self.frames[3] = pygame.transform.scale(self.frames[3], (222 / 1536 * WIDTH * prozent, 287 / 864 * HEIGHT * prozent))

    def updates(self):
        if self.EZ == 6:
            self.EZ = 0
        self.EZ += 1
        if self.EZ == 5:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

    def up(self):
        if self.rect.y > self.predelY:
            self.inerziaUP = 15
            self.rect = self.rect.move(0, -5)

    def down(self):
        if self.rect.y + 280 / 864 * HEIGHT < HEIGHT - self.predelY:
            self.inerziaDOWN = 15
            self.rect = self.rect.move(0, 5)

    def right(self):
        if self.rect.x + 165 / 1536 * WIDTH <= WIDTH - self.predelX:
            self.inerziaRIGHT = 15
            if self.pos == 'right':
                pass
            elif self.pos == 'left':
                self.image = pygame.transform.flip(self.image, True, False)
                self.frames[0] = pygame.transform.flip(self.frames[0], True, False)
                self.frames[1] = pygame.transform.flip(self.frames[1], True, False)
                self.frames[2] = pygame.transform.flip(self.frames[2], True, False)
                self.frames[3] = pygame.transform.flip(self.frames[3], True, False)
            self.pos = 'right'
            self.rect = self.rect.move(5, 0)

    def left(self):
        if self.rect.x > self.predelX:
            self.inerziaLEFT = 15
            if self.pos == 'right':
                self.image = pygame.transform.flip(self.image, True, False)
                self.frames[0] = pygame.transform.flip(self.frames[0], True, False)
                self.frames[1] = pygame.transform.flip(self.frames[1], True, False)
                self.frames[2] = pygame.transform.flip(self.frames[2], True, False)
                self.frames[3] = pygame.transform.flip(self.frames[3], True, False)
            elif self.pos == 'left':
                pass
            self.pos = 'left'
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
level1_ROOM1_sprites = pygame.sprite.Group()
level1_ROOM2_sprites = pygame.sprite.Group()
level1_ROOM3_sprites = pygame.sprite.Group()
level1_ROOM4_sprites = pygame.sprite.Group()
level1_ROOM5_sprites = pygame.sprite.Group()

level2_ROOM1_sprites = pygame.sprite.Group()
level2_ROOM2_sprites = pygame.sprite.Group()
level2_ROOM3_sprites = pygame.sprite.Group()
level2_ROOM4_sprites = pygame.sprite.Group()

BatsRoom1 = pygame.sprite.Group()
BatsRoom2 = pygame.sprite.Group()
BatsRoom3 = pygame.sprite.Group()
BatsRoom4 = pygame.sprite.Group()
BatsRoom5 = pygame.sprite.Group()

player = Player(player_sprite, 4, 1, 0.75)
player.NEWcords(0.5 * WIDTH, 0.5 * HEIGHT)


class Door(pygame.sprite.Sprite):
    image = load_image('door1.png')
    doorZEL = load_image("door1GREEN.png")
    doorRED = load_image("door1RED.png")

    def __init__(self, group, room, cordX, cordY, ugol, perehod, prozent):
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
    doorZEL = load_image("doorPurplePer1.png")
    doorRED = load_image("doorPurplePer0.png")

    def __init__(self, group, room, cordX, cordY, ugol, perehod, prozent):
        super().__init__(group)
        self.room = room

        self.perehod = perehod
        self.ugol = ugol

        self.door = DoorWithKeyPurple.image
        self.door = pygame.transform.rotate(self.door, ugol)
        self.door = pygame.transform.scale(self.door, (((207 * ((HEIGHT * 0.333) // 1) / 77) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))

        self.doorRED = DoorWithKeyPurple.doorRED
        self.doorRED = pygame.transform.rotate(self.doorRED, ugol)
        self.doorRED = pygame.transform.scale(self.doorRED, (((207 * ((HEIGHT * 0.333) // 1) / 77) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))

        self.doorZEL = DoorWithKeyPurple.doorZEL
        self.doorZEL = pygame.transform.rotate(self.doorZEL, ugol)
        self.doorZEL = pygame.transform.scale(self.doorZEL, (((207 * ((HEIGHT * 0.333) // 1) / 77) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))

        self.osnova = self.door

        self.rect = self.door.get_rect()
        self.rect.x = cordX
        self.rect.y = cordY

    def updater(self, permission, *args):
        if args == (0,):
            pass
        elif args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                and not pygame.sprite.collide_mask(self, player):
            self.image = self.doorRED
        else:
            if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                    and pygame.sprite.collide_mask(self, player):
                if permission == 1:
                    self.image = self.doorZEL
                else:
                    self.image = self.doorRED
            else:
                if args and self.rect.collidepoint(args[0].pos) is False:
                    self.image = self.osnova
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
                        return self.perehod, (self.rect.x * 1.13) // 1, self.rect.height * 1.1, 1
                else:
                    return self.room, player.GETcords()[0], player.GETcords()[1], 0
            else:
                return 0, 0, 0, 0
        else:
            return self.room, player.GETcords()[0], player.GETcords()[1], 0


class DoorWithKeyBlue(pygame.sprite.Sprite):
    image = load_image('doorBlue.png')
    doorZEL = load_image("doorBluePer1.png")
    doorRED = load_image("doorBluePer0.png")

    def __init__(self, group, room, cordX, cordY, ugol, perehod, prozent):
        super().__init__(group)
        self.room = room

        self.perehod = perehod
        self.ugol = ugol

        self.door = DoorWithKeyBlue.image
        self.door = pygame.transform.rotate(self.door, ugol)
        self.door = pygame.transform.scale(self.door, (((207 * ((HEIGHT * 0.333) // 1) / 77) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))

        self.osnova = self.door

        self.doorZEL = DoorWithKeyBlue.doorZEL
        self.doorZEL = pygame.transform.rotate(self.doorZEL, ugol)
        self.doorZEL = pygame.transform.scale(self.doorZEL, (((207 * ((HEIGHT * 0.333) // 1) / 77) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))

        self.doorRED = DoorWithKeyBlue.doorRED
        self.doorRED = pygame.transform.rotate(self.doorRED, ugol)
        self.doorRED = pygame.transform.scale(self.doorRED, (((207 * ((HEIGHT * 0.333) // 1) / 77) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))

        self.rect = self.door.get_rect()
        self.rect.x = cordX
        self.rect.y = cordY

    def updater(self, permission, *args):
        if args == (0,):
            pass
        elif args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                and not pygame.sprite.collide_mask(self, player):
            self.image = self.doorRED
        else:
            if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                    and pygame.sprite.collide_mask(self, player):
                if permission == 1:
                    self.image = self.doorZEL
                else:
                    self.image = self.doorRED
            else:
                if args and self.rect.collidepoint(args[0].pos) is False:
                    self.image = self.osnova
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
            return 1


class DoorWithKeyGreen(pygame.sprite.Sprite):
    image = load_image('doorGreen.png')
    doorZEL = load_image("doorGreenPer1.png")
    doorRED = load_image("doorGreenPer0.png")

    def __init__(self, group, room, cordX, cordY, ugol, perehod, prozent):
        super().__init__(group)
        self.room = room

        self.perehod = perehod
        self.ugol = ugol

        self.door = DoorWithKeyGreen.image
        self.door = pygame.transform.rotate(self.door, ugol)
        self.door = pygame.transform.scale(self.door, (((207 * ((HEIGHT * 0.333) // 1) / 77) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))

        self.osnova = self.door

        self.doorZEL = DoorWithKeyGreen.doorZEL
        self.doorZEL = pygame.transform.rotate(self.doorZEL, ugol)
        self.doorZEL = pygame.transform.scale(self.doorZEL, (
        ((207 * ((HEIGHT * 0.333) // 1) / 77) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))

        self.doorRED = DoorWithKeyGreen.doorRED
        self.doorRED = pygame.transform.rotate(self.doorRED, ugol)
        self.doorRED = pygame.transform.scale(self.doorRED, (
        ((207 * ((HEIGHT * 0.333) // 1) / 77) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))

        self.rect = self.door.get_rect()
        self.rect.x = cordX
        self.rect.y = cordY

    def updater(self, permission, *args):
        if args == (0,):
            pass
        elif args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                and not pygame.sprite.collide_mask(self, player):
            self.image = self.doorRED
        else:
            if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                    and pygame.sprite.collide_mask(self, player):
                if permission == 1:
                    self.image = self.doorZEL
                else:
                    self.image = self.doorRED
            else:
                if args and self.rect.collidepoint(args[0].pos) is False:
                    self.image = self.osnova
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
                        return self.perehod, (self.rect.x * 1.13) // 1, self.rect.height * 1.1, 1
                else:
                    return self.room, player.GETcords()[0], player.GETcords()[1], 0
            else:
                return 0, 0, 0, 0
        else:
            return self.room, player.GETcords()[0], player.GETcords()[1], 0


class DoorWithKeyRed(pygame.sprite.Sprite):
    image = load_image('doorREDkey.png')
    doorZEL = load_image("doorREDkeyPer1.png")
    doorRED = load_image("doorREDkeyPer0.png")

    def __init__(self, group, room, cordX, cordY, ugol, perehod, prozent):
        super().__init__(group)
        self.room = room

        self.perehod = perehod
        self.ugol = ugol

        self.door = DoorWithKeyRed.image
        self.door = pygame.transform.rotate(self.door, ugol)
        self.door = pygame.transform.scale(self.door, (
        ((207 * ((HEIGHT * 0.333) // 1) / 77) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))

        self.osnova = self.door

        self.doorZEL = DoorWithKeyRed.doorZEL
        self.doorZEL = pygame.transform.rotate(self.doorZEL, ugol)
        self.doorZEL = pygame.transform.scale(self.doorZEL, (
        ((207 * ((HEIGHT * 0.333) // 1) / 77) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))

        self.doorRED = DoorWithKeyRed.doorRED
        self.doorRED = pygame.transform.rotate(self.doorRED, ugol)
        self.doorRED = pygame.transform.scale(self.doorRED, (
        ((207 * ((HEIGHT * 0.333) // 1) / 77) // 1) * prozent, ((HEIGHT * 0.333) // 1) * prozent))

        self.rect = self.door.get_rect()
        self.rect.x = cordX
        self.rect.y = cordY

    def updater(self, permission, *args):
        if args == (0,):
            pass
        elif args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                and not pygame.sprite.collide_mask(self, player):
            self.image = self.doorRED
        else:
            if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                    and pygame.sprite.collide_mask(self, player):
                if permission == 1:
                    self.image = self.doorZEL
                else:
                    self.image = self.doorRED
            else:
                if args and self.rect.collidepoint(args[0].pos) is False:
                    self.image = self.osnova
        if permission == 9:
            self.image = self.door
        if permission == 1:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(args[0].pos) and pygame.sprite.collide_mask(self, player):
                    return 'end2'
                else:
                    return 2
            else:
                return 2
        else:
            return 2


class Rat(pygame.sprite.Sprite):
    image = load_image('rat1.png')
    rat2 = load_image("rat2.png")
    rat3 = load_image("rat3.png")

    def __init__(self, group, cordX, cordY, prozent):
        super().__init__(group)

        self.rat1 = Rat.image
        self.rat1 = pygame.transform.scale(self.rat1, ((103 * WIDTH / 1536) // 1, (75 * HEIGHT / 864) // 1))

        self.rat2 = Rat.rat2
        self.rat2 = pygame.transform.scale(self.rat2, ((103 * WIDTH / 1536) // 1, (75 * HEIGHT / 864) // 1))

        self.rat3 = Rat.rat3
        self.rat3 = pygame.transform.scale(self.rat3, ((103 * WIDTH / 1536) // 1, (75 * HEIGHT / 864) // 1))

        self.rect = self.rat1.get_rect()
        self.rect.x = cordX
        self.rect.y = cordY

        self.predelX = (0.5 * WIDTH // 1) - (0.5 * WIDTH * 6 / 7) // 1

        self.key = [0, 0]
        self.N = 0

        self.pos = 'left'

        self.turn = 0
        self.hod = 0

    def updater(self):
        self.turn += 1
        if self.turn == 51:
            self.turn = 0
        if self.turn == 50:
            if self.hod == 4:
                self.hod = 0
            self.hod += 1
            if self.hod  == 1:
                self.image = self.rat3
            elif self.hod == 2:
                self.image = self.rat2
            elif self.hod  == 3:
                self.image = self.rat3
            elif self.hod == 4:
                self.image = self.rat1

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
                    self.rat1 = pygame.transform.flip(self.rat1, True, False)
                    self.rat2 = pygame.transform.flip(self.rat2, True, False)
                    self.rat3 = pygame.transform.flip(self.rat3, True, False)
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
                        self.rat1 = pygame.transform.flip(self.rat1, True, False)
                        self.rat2 = pygame.transform.flip(self.rat2, True, False)
                        self.rat3 = pygame.transform.flip(self.rat3, True, False)
                    if self.rect.x + 152 <= WIDTH - self.predelX:
                        if self.key[1] % 2 == 0:
                            self.rect.x += 3

    def update_EZ(self, *args):
        if args == (0,):
            self.image = self.rat1


class KeyPurple(pygame.sprite.Sprite):
    image = load_image('keyPurple.png')
    per0 = load_image('keyPurplePer0.png')
    per1 = load_image('keyPurplePer1.png')

    def __init__(self, group, cordX, cordY, prozent):
        super().__init__(group)

        self.key = KeyPurple.image
        self.key = pygame.transform.scale(self.key, ((300 * WIDTH / 1536) // 1 * prozent, (372 * HEIGHT / 864) // 1 * prozent))

        self.per0 = KeyPurple.per0
        self.per0 = pygame.transform.scale(self.per0, ((300 * WIDTH / 1536) // 1 * prozent, (372 * HEIGHT / 864) // 1 * prozent))

        self.per1 = KeyPurple.per1
        self.per1 = pygame.transform.scale(self.per1, ((300 * WIDTH / 1536) // 1 * prozent, (372 * HEIGHT / 864) // 1 * prozent))

        self.rect = self.key.get_rect()
        self.rect.x = cordX
        self.rect.y = cordY

    def update_EZ(self, *args):
        if args == (0,):
            self.image = self.key

    def updater(self, *args):
        if args == (0,):
            pass
        elif args and args[0].type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(args[0].pos) and pygame.sprite.collide_mask(self, player):
                self.image = pygame.transform.scale(self.image, (0, 0))
                self.per0 = pygame.transform.scale(self.per0, (0, 0))
                self.per1 = pygame.transform.scale(self.per1, (0, 0))
                self.key = pygame.transform.scale(self.key, (0, 0))
                return 1
            else:
                return 0
        else:
            if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                    and not pygame.sprite.collide_mask(self, player):
                self.image = self.per0
            else:
                if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                        and pygame.sprite.collide_mask(self, player):
                    self.image = self.per1
                else:
                    if args and self.rect.collidepoint(args[0].pos) is False:
                        self.image = self.key


class KeyBlue(pygame.sprite.Sprite):
    image = load_image('keyBlue.png')
    per0 = load_image('keyBluePer0.png')
    per1 = load_image('keyBluePer1.png')

    def __init__(self, group, cordX, cordY, prozent):
        super().__init__(group)

        self.key = KeyBlue.image
        self.key = pygame.transform.scale(self.key, ((300 * WIDTH / 1536) // 1 * prozent, (372 * HEIGHT / 864) // 1 * prozent))

        self.per0 = KeyBlue.per0
        self.per0 = pygame.transform.scale(self.per0,
                                           ((300 * WIDTH / 1536) // 1 * prozent, (372 * HEIGHT / 864) // 1 * prozent))

        self.per1 = KeyBlue.per1
        self.per1 = pygame.transform.scale(self.per1,
                                           ((300 * WIDTH / 1536) // 1 * prozent, (372 * HEIGHT / 864) // 1 * prozent))

        self.rect = self.key.get_rect()
        self.rect.x = cordX
        self.rect.y = cordY

    def update_EZ(self, *args):
        if args == (0,):
            self.image = self.key

    def updater(self, *args):
        if args == (0,):
            pass
        elif args and args[0].type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(args[0].pos) and pygame.sprite.collide_mask(self, player):
                self.image = pygame.transform.scale(self.image, (0, 0))
                self.per0 = pygame.transform.scale(self.per0, (0, 0))
                self.per1 = pygame.transform.scale(self.per1, (0, 0))
                self.key = pygame.transform.scale(self.key, (0, 0))
                return 1
            else:
                return 0
        else:
            if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                    and not pygame.sprite.collide_mask(self, player):
                self.image = self.per0
            else:
                if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                        and pygame.sprite.collide_mask(self, player):
                    self.image = self.per1
                else:
                    if args and self.rect.collidepoint(args[0].pos) is False:
                        self.image = self.key


class KeyGreen(pygame.sprite.Sprite):
    image = load_image('keyGreen.png')
    per0 = load_image('keyGreenPer0.png')
    per1 = load_image('keyGreenPer1.png')

    def __init__(self, group, cordX, cordY, prozent):
        super().__init__(group)

        self.key = KeyGreen.image
        self.key = pygame.transform.scale(self.key, ((300 * WIDTH / 1536) // 1 * prozent, (372 * HEIGHT / 864) // 1 * prozent))

        self.per0 = KeyGreen.per0
        self.per0 = pygame.transform.scale(self.per0,
                                           ((300 * WIDTH / 1536) // 1 * prozent, (372 * HEIGHT / 864) // 1 * prozent))

        self.per1 = KeyGreen.per1
        self.per1 = pygame.transform.scale(self.per1,
                                           ((300 * WIDTH / 1536) // 1 * prozent, (372 * HEIGHT / 864) // 1 * prozent))

        self.rect = self.key.get_rect()
        self.rect.x = cordX
        self.rect.y = cordY

    def update_EZ(self, *args):
        if args == (0,):
            self.image = self.key

    def updater(self, *args):
        if args == (0,):
            pass
        elif args and args[0].type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(args[0].pos) and pygame.sprite.collide_mask(self, player):
                self.image = pygame.transform.scale(self.image, (0, 0))
                self.per0 = pygame.transform.scale(self.per0, (0, 0))
                self.per1 = pygame.transform.scale(self.per1, (0, 0))
                self.key = pygame.transform.scale(self.key, (0, 0))
                return 1
            else:
                return 0
        else:
            if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                    and not pygame.sprite.collide_mask(self, player):
                self.image = self.per0
            else:
                if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                        and pygame.sprite.collide_mask(self, player):
                    self.image = self.per1
                else:
                    if args and self.rect.collidepoint(args[0].pos) is False:
                        self.image = self.key


class Ded2(pygame.sprite.Sprite):
    image = load_image('ded.png')
    dedPOSLANIE = load_image('dedPOSLANIE2.png')

    def __init__(self, group, cordX, cordY, prozent):
        super().__init__(group)

        self.ded = Ded2.image
        self.ded = pygame.transform.scale(self.ded, ((404 * WIDTH / 1536) // 1 * prozent, (618 * HEIGHT / 864) // 1 * prozent))
        self.ded = pygame.transform.flip(self.ded, True, False)

        self.dedPOSLANIE = Ded2.dedPOSLANIE
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


class Bat(pygame.sprite.Sprite):
    image = load_image('bat1.png')
    bat2 = load_image("bat2.png")

    def __init__(self, group, cordX, cordY, prozent):
        super().__init__(group)

        self.bat1 = Bat.image
        self.bat1 = pygame.transform.scale(self.bat1, ((464 * WIDTH / 1536) // 1 * prozent, (225 * HEIGHT / 864) // 1 * prozent))

        self.bat2 = Bat.bat2
        self.bat2 = pygame.transform.scale(self.bat2, ((464 * WIDTH / 1536) // 1 * prozent, (225 * HEIGHT / 864) // 1 * prozent))

        self.rect = self.bat1.get_rect()
        self.rect.x = cordX
        self.rect.y = cordY

        self.predelX = (0.5 * WIDTH // 1) - (0.5 * WIDTH * 6 / 7) // 1
        self.predelY = (0.5 * HEIGHT // 1) - (0.5 * HEIGHT * 3 / 4) // 1

        self.keyHORIZONTAL = [0, 0]
        self.keyVERTICAL = [0, 0]
        self.N = 0
        self.M = 0

        self.wing = 0
        self.permission = 0

    def updates(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(args[0].pos) and pygame.sprite.collide_mask(self, player):
                self.permission = 1
                self.image = pygame.transform.scale(self.image, (0, 0))

    def updater(self):
        if self.permission == 0:
            self.wing += 1
            if self.wing == 51:
                self.wing = 0
            if self.wing == 50:
                if self.image == self.bat1:
                    self.image = self.bat2
                elif self.image == self.bat2:
                    self.image = self.bat1

            if self.N == 0:
                key = random.randint(1, 150)
                if key == 25:
                    self.N = 1
                    if random.randint(1, 2) == 1:
                        self.keyHORIZONTAL = [1, 151]
                    else:
                        self.keyHORIZONTAL = [2, 151]

            elif self.N == 1:
                if self.keyHORIZONTAL[1] == 1:
                    self.N = 0

                if self.keyHORIZONTAL[0] == 1:
                    self.keyHORIZONTAL[1] -= 1
                    if self.rect.x > self.predelX:
                        if self.keyHORIZONTAL[1] % 2 == 0:
                            self.rect.x -= 3
                else:
                    if self.keyHORIZONTAL[0] == 2:
                        self.keyHORIZONTAL[1] -= 1
                        if self.rect.x + 152 <= WIDTH - self.predelX:
                            if self.keyHORIZONTAL[1] % 2 == 0:
                                self.rect.x += 3

            if self.M == 0:
                key = random.randint(1, 150)
                if key == 25:
                    self.M = 1
                    if random.randint(1, 2) == 1:
                        self.keyVERTICAL = [1, 151]
                    else:
                        self.keyVERTICAL = [2, 151]
            elif self.M == 1:
                if self.keyVERTICAL[1] == 1:
                    self.M = 0

                if self.keyVERTICAL[0] == 1:
                    self.keyVERTICAL[1] -= 1
                    if self.rect.y > self.predelY:
                        if self.keyVERTICAL[1] % 2 == 0:
                            self.rect.y -= 3
                else:
                    if self.keyVERTICAL[0] == 2:
                        self.keyVERTICAL[1] -= 1
                        if self.rect.y + 132 < HEIGHT - self.predelY:
                            if self.keyVERTICAL[1] % 2 == 0:
                                self.rect.y += 3



    def update_EZ(self, *args):
        if args == (0,):
            self.image = self.bat1


class BatWithKey(pygame.sprite.Sprite):
    image = load_image('bat1.png')
    bat2 = load_image("bat2.png")
    key = load_image("keyRed.png")
    per0 = load_image("keyRedPer0.png")
    per1 = load_image("keyRedPer1.png")

    def __init__(self, group, cordX, cordY, prozent):
        super().__init__(group)

        self.karta = 0

        self.move = -9

        self.keyRed = BatWithKey.key
        self.keyRed = pygame.transform.scale(self.keyRed, ((300 * WIDTH / 1536) // 1 * 0.3, (372 * HEIGHT / 864) // 1 * 0.3))

        self.per0 = BatWithKey.per0
        self.per0 = pygame.transform.scale(self.per0, ((300 * WIDTH / 1536) // 1 * 0.3, (372 * HEIGHT / 864) // 1 * 0.3))

        self.per1 = BatWithKey.per1
        self.per1 = pygame.transform.scale(self.per1, ((300 * WIDTH / 1536) // 1 * 0.3, (372 * HEIGHT / 864) // 1 * 0.3))

        self.bat1 = BatWithKey.image
        self.bat1 = pygame.transform.scale(self.bat1, ((464 * WIDTH / 1536) // 1 * prozent, (225 * HEIGHT / 864) // 1 * prozent))

        self.bat2 = BatWithKey.bat2
        self.bat2 = pygame.transform.scale(self.bat2, ((464 * WIDTH / 1536) // 1 * prozent, (225 * HEIGHT / 864) // 1 * prozent))

        self.rect = self.bat1.get_rect()
        self.rect.x = cordX
        self.rect.y = cordY

        self.predelX = (0.5 * WIDTH // 1) - (0.5 * WIDTH * 6 / 7) // 1
        self.predelY = (0.5 * HEIGHT // 1) - (0.5 * HEIGHT * 3 / 4) // 1

        self.keyHORIZONTAL = [0, 0]
        self.keyVERTICAL = [0, 0]
        self.N = 0
        self.M = 0

        self.wing = 0
        self.permission = 0

        self.EZ = 0

    def updates(self, *args):
        if args == (0,):
            pass
        elif args and args[0].type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(args[0].pos) and pygame.sprite.collide_mask(self, player):
                self.EZ += 1
                if self.EZ == 1:
                    self.permission = 1
                    x = self.rect.x
                    y = self.rect.y
                    self.image = self.keyRed
                    self.rect = self.keyRed.get_rect()
                    self.rect.y = y
                    self.rect.x = x
                    self.rect.y += 100
                    return 0
                elif self.EZ == 2:
                    self.image = pygame.transform.scale(self.image, (0, 0))
                    return 1
            else:
                return 0
        else:
            if self.EZ == 1:
                if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                        and not pygame.sprite.collide_mask(self, player):
                    self.image = self.per0
                else:
                    if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                            and pygame.sprite.collide_mask(self, player):
                        self.image = self.per1
                    else:
                        if args and self.rect.collidepoint(args[0].pos) is False:
                            self.image = self.keyRed


    def updater(self):
        if self.permission == 1:
            self.karta += 1
            if self.karta == 40:
                self.karta = 0
                if self.move != 18:
                    self.rect = self.rect.move(0, self.move)
                    self.move += 3
        elif self.permission == 0:
            self.wing += 1
            if self.wing == 51:
                self.wing = 0
            if self.wing == 50:
                if self.image == self.bat1:
                    self.image = self.bat2
                elif self.image == self.bat2:
                    self.image = self.bat1

            if self.N == 0:
                key = random.randint(1, 150)
                if key == 25:
                    self.N = 1
                    if random.randint(1, 2) == 1:
                        self.keyHORIZONTAL = [1, 151]
                    else:
                        self.keyHORIZONTAL = [2, 151]

            elif self.N == 1:
                if self.keyHORIZONTAL[1] == 1:
                    self.N = 0

                if self.keyHORIZONTAL[0] == 1:
                    self.keyHORIZONTAL[1] -= 1
                    if self.rect.x > self.predelX:
                        if self.keyHORIZONTAL[1] % 2 == 0:
                            self.rect.x -= 3
                else:
                    if self.keyHORIZONTAL[0] == 2:
                        self.keyHORIZONTAL[1] -= 1
                        if self.rect.x + 152 <= WIDTH - self.predelX:
                            if self.keyHORIZONTAL[1] % 2 == 0:
                                self.rect.x += 3

            if self.M == 0:
                key = random.randint(1, 150)
                if key == 25:
                    self.M = 1
                    if random.randint(1, 2) == 1:
                        self.keyVERTICAL = [1, 151]
                    else:
                        self.keyVERTICAL = [2, 151]
            elif self.M == 1:
                if self.keyVERTICAL[1] == 1:
                    self.M = 0

                if self.keyVERTICAL[0] == 1:
                    self.keyVERTICAL[1] -= 1
                    if self.rect.y > self.predelY:
                        if self.keyVERTICAL[1] % 2 == 0:
                            self.rect.y -= 3
                else:
                    if self.keyVERTICAL[0] == 2:
                        self.keyVERTICAL[1] -= 1
                        if self.rect.y + 132 < HEIGHT - self.predelY:
                            if self.keyVERTICAL[1] % 2 == 0:
                                self.rect.y += 3


    def update_EZ(self, *args):
        if args == (0,):
            self.image = self.bat1


class Plate1(pygame.sprite.Sprite):
    image = load_image('plate1.png')

    def __init__(self, group, cordX, cordY, prozent):
        super().__init__(group)

        self.plate = Plate1.image
        self.plate = pygame.transform.scale(self.plate, ((360 * WIDTH / 1536) // 1 * prozent, (450 * HEIGHT / 864) // 1 * prozent))

        self.rect = self.plate.get_rect()
        self.rect.x = cordX
        self.rect.y = cordY

    def update_EZ(self, *args):
        if args == (0,):
            self.image = self.plate


class Plate2(pygame.sprite.Sprite):
    image = load_image('plate2.png')

    def __init__(self, group, cordX, cordY, prozent):
        super().__init__(group)

        self.plate = Plate2.image
        self.plate = pygame.transform.scale(self.plate, ((360 * WIDTH / 1536) // 1 * prozent, (450 * HEIGHT / 864) // 1 * prozent))

        self.rect = self.plate.get_rect()
        self.rect.x = cordX
        self.rect.y = cordY

    def update_EZ(self, *args):
        if args == (0,):
            self.image = self.plate


class Kristall(pygame.sprite.Sprite):
    image = load_image('kristall.png')
    per0 = load_image('kristallRED.png')
    per1 = load_image('kristallZEL.png')

    def __init__(self, group, cordX, cordY, prozent):
        super().__init__(group)

        self.key = Kristall.image
        self.key = pygame.transform.scale(self.key, ((1240 * WIDTH / 1536) // 1 * prozent, (821 * HEIGHT / 864) // 1 * prozent))

        self.per0 = Kristall.per0
        self.per0 = pygame.transform.scale(self.per0, ((1240 * WIDTH / 1536) // 1 * prozent, (821 * HEIGHT / 864) // 1 * prozent))

        self.per1 = Kristall.per1
        self.per1 = pygame.transform.scale(self.per1, ((1240 * WIDTH / 1536) // 1 * prozent, (821 * HEIGHT / 864) // 1 * prozent))

        self.rect = self.key.get_rect()
        self.rect.x = cordX
        self.rect.y = cordY

    def update_EZ(self, *args):
        if args == (0,):
            self.image = self.key

    def updater(self, *args):
        if args == (0,):
            pass
        elif args and args[0].type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(args[0].pos) and pygame.sprite.collide_mask(self, player):
                self.image = pygame.transform.scale(self.image, (0, 0))
                self.per0 = pygame.transform.scale(self.per0, (0, 0))
                self.per1 = pygame.transform.scale(self.per1, (0, 0))
                self.key = pygame.transform.scale(self.key, (0, 0))
                return 1
            else:
                return 0
        else:
            if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                    and not pygame.sprite.collide_mask(self, player):
                self.image = self.per0
            else:
                if args and args[0].type == pygame.MOUSEMOTION and self.rect.collidepoint(args[0].pos) \
                        and pygame.sprite.collide_mask(self, player):
                    self.image = self.per1
                else:
                    if args and self.rect.collidepoint(args[0].pos) is False:
                        self.image = self.key


def main():
    pygame.display.set_caption("Master of Dungeon")
    secret = 0

    # ПЕРВЫЙ УРОВЕНЬ

    door = Door(level1_ROOM1_sprites, 1, (WIDTH * 0.934 // 1), ((0.55 * HEIGHT) // 1), 270, 2, 0.8)
    door.update(0)

    door2 = Door(level1_ROOM2_sprites, 2, (WIDTH * -0.01 // 1), ((0.55 * HEIGHT) // 1), 90, 1, 0.8)
    door2.update(0)

    door3 = Door(level1_ROOM1_sprites, 1, (WIDTH * -0.01 // 1), ((0.3 * HEIGHT) // 1), 90, 3, 0.8)
    door3.update(0)

    door4 = Door(level1_ROOM3_sprites, 3, (WIDTH * 0.934 // 1), ((0.3 * HEIGHT) // 1), 270, 1, 0.8)
    door4.update(0)

    door5 = Door(level1_ROOM4_sprites, 4, (WIDTH * -0.01 // 1), ((0.3 * HEIGHT) // 1), 90, 5, 0.8)
    door5.update(0)

    door6 = Door(level1_ROOM5_sprites, 5, (WIDTH * 0.934 // 1), ((0.3 * HEIGHT) // 1), 270, 4, 0.8)
    door6.update(0)

    doorPurple = DoorWithKeyPurple(level1_ROOM1_sprites, 1, ((WIDTH * 0.4 // 1)), (0), 0, 4, 0.37)
    doorPurple.updater(9)

    doorPurple2 = DoorWithKeyPurple(level1_ROOM4_sprites, 4, ((WIDTH * 0.4 // 1)), (HEIGHT - 100), 180, 1, 0.37)
    doorPurple2.updater(9)

    doorBlue = DoorWithKeyBlue(level1_ROOM4_sprites, 4, ((WIDTH * 0.4 // 1)), (0), 0, 1, 0.37)
    doorBlue.updater(9)

    rat = Rat(level1_ROOM1_sprites, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 1)
    rat2 = Rat(level1_ROOM1_sprites, 200 / 1536 * WIDTH, 210 / 864 * HEIGHT, 1)
    rat3 = Rat(level1_ROOM1_sprites, 200 / 1536 * WIDTH, 670 / 864 * HEIGHT, 1)
    rat4 = Rat(level1_ROOM2_sprites, 200 / 1536 * WIDTH, 670 / 864 * HEIGHT, 1)
    rat5 = Rat(level1_ROOM4_sprites, 200 / 1536 * WIDTH, 560 / 864 * HEIGHT, 1)
    rat6 = Rat(level1_ROOM3_sprites, 200 / 1536 * WIDTH, 120 / 864 * HEIGHT, 1)
    rat7 = Rat(level1_ROOM3_sprites, 200 / 1536 * WIDTH, 210 / 864 * HEIGHT, 1)
    rat8 = Rat(level1_ROOM3_sprites, 200 / 1536 * WIDTH, 560 / 864 * HEIGHT, 1)

    rat2.update_EZ(0)
    rat.update_EZ(0)
    rat3.update_EZ(0)
    rat4.update_EZ(0)
    rat5.update_EZ(0)
    rat6.update_EZ(0)
    rat7.update_EZ(0)
    rat8.update_EZ(0)

    ded = Ded(level1_ROOM1_sprites, 140 / 1536 * WIDTH, 520 / 864 * HEIGHT, 0.37)
    ded.update_EZ(0)

    keyPurple = KeyPurple(level1_ROOM2_sprites, 1275 / 1536 * WIDTH, 150 / 864 * HEIGHT, 0.3)
    keyPurple.update_EZ(0)

    keyBlue = KeyBlue(level1_ROOM3_sprites, 150 / 1536 * WIDTH, 150 / 864 * HEIGHT, 0.3)
    keyBlue.update_EZ(0)

    FON = load_image('FON.png')
    FON = pygame.transform.scale(FON, (WIDTH, HEIGHT))

    plate1 = Plate1(level1_ROOM1_sprites, 1260 / 1536 * WIDTH, 150 / 864 * HEIGHT, 0.35)
    plate1.update_EZ(0)

    plate2 = Plate2(level2_ROOM1_sprites, 1260 / 1536 * WIDTH, 580 / 864 * HEIGHT, 0.35)
    plate2.update_EZ(0)

    Kristall1 = Kristall(level1_ROOM1_sprites, 120 / 1536 * WIDTH, 125 / 864 * HEIGHT, 0.07)
    Kristall1.update_EZ(0)

    Kristall2 = Kristall(level1_ROOM5_sprites, 120 / 1536 * WIDTH, 680 / 864 * HEIGHT, 0.07)
    Kristall2.update_EZ(0)

    Kristall3 = Kristall(level2_ROOM1_sprites, 120 / 1536 * WIDTH, 680 / 864 * HEIGHT, 0.07)
    Kristall3.update_EZ(0)

    Kristall4 = Kristall(level2_ROOM2_sprites, 1350 / 1536 * WIDTH, 680 / 864 * HEIGHT, 0.07)
    Kristall4.update_EZ(0)

    Kristall5 = Kristall(level2_ROOM4_sprites, 1350 / 1536 * WIDTH, 680 / 864 * HEIGHT, 0.07)
    Kristall5.update_EZ(0)

    NachFON = load_image('NachFON.png')
    NachFON = pygame.transform.scale(NachFON, (WIDTH, HEIGHT))
    running = True
    Nach = 0
    room = 1
    q = 0
    font = pygame.font.SysFont("Ubuntu Condensed", 90, bold=False, italic=False)
    font2 = pygame.font.SysFont("Ubuntu Condensed", 50, bold=False, italic=False)
    PurplePermission = 0
    BluePermission = 0
    level = 1

    # ВТОРОЙ УРОВЕНЬ

    level2_door1 = Door(level2_ROOM1_sprites, 1, (WIDTH * -0.01 // 1), ((0.55 * HEIGHT) // 1), 90, 2, 0.8)
    level2_door1.update(0)

    level2_door2 = Door(level2_ROOM2_sprites, 2, (WIDTH * 0.934 // 1), ((0.55 * HEIGHT) // 1), 270, 1, 0.8)
    level2_door2.update(0)

    level2_door3 = Door(level2_ROOM3_sprites, 3, (WIDTH * 0.934 // 1), ((0.3 * HEIGHT) // 1), 270, 4, 0.8)
    level2_door3.update(0)

    level2_door4 = Door(level2_ROOM4_sprites, 4, (WIDTH * -0.01 // 1), ((0.3 * HEIGHT) // 1), 90, 3, 0.8)
    level2_door4.update(0)

    doorGreen = DoorWithKeyGreen(level2_ROOM1_sprites, 1, ((WIDTH * 0.4 // 1)), (0), 0, 3, 0.37)
    doorGreen.updater(9)

    doorGreen2 = DoorWithKeyGreen(level2_ROOM3_sprites, 3, ((WIDTH * 0.4 // 1)), (HEIGHT - 100), 180, 1, 0.37)
    doorGreen2.updater(9)

    keyGreen = KeyGreen(level2_ROOM2_sprites, 150 / 1536 * WIDTH, 150 / 864 * HEIGHT, 0.3)
    keyGreen.update_EZ(0)

    doorRed = DoorWithKeyRed(level2_ROOM3_sprites, 4, ((WIDTH * 0.4 // 1)), (0), 0, 1, 0.37)
    doorRed.updater(9)

    bat1 = Bat(BatsRoom1, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat1.update_EZ(0)
    bat2 = Bat(BatsRoom1, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat2.update_EZ(0)
    bat3 = Bat(BatsRoom1, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat3.update_EZ(0)
    bat4 = Bat(BatsRoom1, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat4.update_EZ(0)
    bat5 = Bat(BatsRoom1, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat5.update_EZ(0)
    bat6 = Bat(BatsRoom1, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat6.update_EZ(0)
    bat7 = Bat(BatsRoom1, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat7.update_EZ(0)

    bat21 = Bat(BatsRoom2, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat21.update_EZ(0)
    bat22 = Bat(BatsRoom2, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat22.update_EZ(0)
    bat23 = Bat(BatsRoom2, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat23.update_EZ(0)
    bat24 = Bat(BatsRoom2, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat24.update_EZ(0)
    bat25 = Bat(BatsRoom2, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat25.update_EZ(0)
    bat26 = Bat(BatsRoom2, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat26.update_EZ(0)
    bat27 = Bat(BatsRoom2, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat27.update_EZ(0)

    bat31 = BatWithKey(BatsRoom3, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat31.update_EZ(0)
    bat32 = Bat(BatsRoom3, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat32.update_EZ(0)
    bat33 = Bat(BatsRoom3, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat33.update_EZ(0)
    bat34 = Bat(BatsRoom3, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat34.update_EZ(0)
    bat35 = Bat(BatsRoom3, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat35.update_EZ(0)
    bat36 = Bat(BatsRoom3, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat36.update_EZ(0)
    bat37 = Bat(BatsRoom3, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat37.update_EZ(0)

    bat41 = Bat(BatsRoom4, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat41.update_EZ(0)
    bat42 = Bat(BatsRoom4, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat42.update_EZ(0)
    bat43 = Bat(BatsRoom4, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat43.update_EZ(0)
    bat44 = Bat(BatsRoom4, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat44.update_EZ(0)
    bat45 = Bat(BatsRoom4, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat45.update_EZ(0)
    bat46 = Bat(BatsRoom4, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat46.update_EZ(0)
    bat47 = Bat(BatsRoom4, 600 / 1536 * WIDTH, 120 / 864 * HEIGHT, 0.3)
    bat47.update_EZ(0)

    ded2 = Ded2(level2_ROOM1_sprites, 140 / 1536 * WIDTH, 100 / 864 * HEIGHT, 0.37)
    ded2.update_EZ(0)

    GreenPermission = 0
    RedPermission = 0

    while running:
        if Nach == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        f = open("progress.txt", 'w')
                        f.write('1')
                        f.close()
                        level = 1
                        Nach = 1
                    elif event.key == pygame.K_SPACE:
                        f = open("progress.txt", encoding="utf8")
                        for number, line in enumerate(f):
                            level = int(line)
                            if number > 1:
                                break
                        f.close()
                        if level != 0:
                            Nach  = 1
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
                            Kristall1.updater(event)
                            doorPurple.updater(PurplePermission, event)
                            door.update(event)
                            door3.update(event)
                            doorPurple.update(event)
                            ded.update(event)
                        elif room == 2:
                            keyPurple.updater(event)
                            door2.update(event)
                        elif room == 3:
                            keyBlue.updater(event)
                            door4.update(event)
                        elif room == 4:
                            door5.update(event)
                            doorPurple2.updater(1, event)
                            doorBlue.updater(BluePermission, event)
                        elif room == 5:
                            Kristall2.updater(event)
                            door6.update(event)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if room == 1:
                            secret += Kristall1.updater(event)
                            room, posX, posY, h = door.update(event)
                            if h == 0:
                                room, posX, posY, h = door3.update(event)
                            if h == 0:
                                room, posX, posY, h = doorPurple.updater(PurplePermission, event)
                            player.NEWcords(posX, posY)
                        elif room == 2:
                            if PurplePermission == 0:
                                PurplePermission = keyPurple.updater(event)
                            room, posX, posY, h = door2.update(event)
                            player.NEWcords(posX, posY)
                        elif room == 3:
                            if BluePermission == 0:
                                BluePermission = keyBlue.updater(event)
                            room, posX, posY, h = door4.update(event)
                            player.NEWcords(posX, posY)
                        elif room == 4:
                            room, posX, posY, h = doorPurple2.updater(1, event)
                            if h == 0:
                                room, posX, posY, h = door5.update(event)
                            if h == 0:
                                level = doorBlue.updater(BluePermission, event)
                            else:
                                player.NEWcords(posX, posY)
                        elif room == 5:
                            secret += Kristall2.updater(event)
                            room, posX, posY, h = door6.update(event)
                            player.NEWcords(posX, posY)
                    else:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_w] is True:
                            player.updates()
                            player.up()
                        if keys[pygame.K_a] is True:
                            player.updates()
                            player.left()
                        if keys[pygame.K_s] is True:
                            player.updates()
                            player.down()
                        if keys[pygame.K_d] is True:
                            player.updates()
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
                door5.update(q)
                door6.update(q)
                doorPurple.update(q)
                doorPurple2.update(q)
                doorBlue.update(q)

                doorPurple.updater(PurplePermission, q)
                doorPurple2.updater(PurplePermission, q)
                doorBlue.updater(BluePermission, q)

                keyPurple.updater(q)
                keyBlue.updater(q)

                Kristall1.updater(q)
                Kristall2.updater(q)

                if room == 1:
                    level1_ROOM1_sprites.draw(screen)
                    level1_ROOM1_sprites.update()
                elif room == 2:
                    level1_ROOM2_sprites.draw(screen)
                    level1_ROOM2_sprites.update()
                elif room == 3:
                    level1_ROOM3_sprites.draw(screen)
                    level1_ROOM3_sprites.update()
                elif room == 4:
                    level1_ROOM4_sprites.draw(screen)
                    level1_ROOM4_sprites.update()
                elif room == 5:
                    level1_ROOM5_sprites.draw(screen)
                    level1_ROOM5_sprites.update()

                player_sprite.draw(screen)
                player_sprite.update()

                pygame.display.flip()
            elif level == 'end1':
                f = open("progress.txt", 'w')
                f.write('2')
                f.close()
                player.NEWcords(0.5 * WIDTH // 1, 0.5 * HEIGHT // 1)
                room = 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            level = 2

                screen.fill((0, 0, 0))
                screen.blit(NachFON, (0, 0))

                text1 = font.render("Первый уровень пройден!", True, (50, 100, 255))
                screen.blit(text1, [(0.28 * WIDTH) // 1, (0.2 * HEIGHT) // 1])


                text3 = font2.render("Продолжить: Space", True, (50, 150, 255))
                screen.blit(text3, [(0.4 * WIDTH) // 1, (0.4 * HEIGHT) // 1])

                text4 = font2.render("Сохранить и выйти: Esc", True, (50, 150, 255))
                screen.blit(text4, [(0.4 * WIDTH) // 1, (0.5 * HEIGHT) // 1])

                pygame.display.flip()

            elif level == 2:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEMOTION:
                        q = event
                        if room == 1:
                            Kristall3.updater(event)
                            ded2.update(event)
                            level2_door1.update(event)
                            doorGreen.updater(GreenPermission, event)
                        elif room == 2:
                            Kristall4.updater(event)
                            level2_door2.update(event)
                            keyGreen.updater(event)
                        elif room == 3:
                            bat31.updates(event)
                            doorGreen2.updater(GreenPermission, event)
                            level2_door3.update(event)
                        elif room == 4:
                            Kristall5.updater(event)
                            level2_door4.update(event)
                            doorRed.updater(RedPermission, event)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if GreenPermission == 0:
                            GreenPermission = keyGreen.updater(event)
                        if room == 1:
                            secret += Kristall3.updater(event)
                            bat1.updates(event)
                            bat2.updates(event)
                            bat3.updates(event)
                            bat4.updates(event)
                            bat5.updates(event)
                            bat6.updates(event)
                            bat7.updates(event)
                            room, posX, posY, h = level2_door1.update(event)
                            if h == 0:
                                room, posX, posY, h = doorGreen.updater(GreenPermission, event)
                            player.NEWcords(posX, posY)
                        elif room == 2:
                            secret += Kristall4.updater(event)
                            bat21.updates(event)
                            bat22.updates(event)
                            bat23.updates(event)
                            bat24.updates(event)
                            bat25.updates(event)
                            bat26.updates(event)
                            bat27.updates(event)
                            room, posX, posY, h = level2_door2.update(event)
                            player.NEWcords(posX, posY)
                        elif room == 3:
                            if RedPermission == 0:
                                RedPermission = bat31.updates(event)
                            bat32.updates(event)
                            bat33.updates(event)
                            bat34.updates(event)
                            bat35.updates(event)
                            bat36.updates(event)
                            bat37.updates(event)
                            room, posX, posY, h = level2_door3.update(event)
                            if h == 0:
                                room, posX, posY, h = doorGreen2.updater(1, event)
                            if h == 0:
                                level = doorRed.updater(RedPermission, event)
                            else:
                                player.NEWcords(posX, posY)
                        elif room == 4:
                            secret += Kristall5.updater(event)
                            bat41.updates(event)
                            bat42.updates(event)
                            bat43.updates(event)
                            bat44.updates(event)
                            bat45.updates(event)
                            bat46.updates(event)
                            bat47.updates(event)
                            room, posX, posY, h = level2_door4.update(event)
                            player.NEWcords(posX, posY)
                    else:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_w] is True:
                            player.updates()
                            player.up()
                        if keys[pygame.K_a] is True:
                            player.updates()
                            player.left()
                        if keys[pygame.K_s] is True:
                            player.updates()
                            player.down()
                        if keys[pygame.K_d] is True:
                            player.updates()
                            player.right()
                        if keys[pygame.K_ESCAPE]:
                            running = False


                player.inerzia()
                screen.blit(FON, (0, 0))


                if room == 1:
                    level2_door1.update(q)
                    doorGreen.updater(GreenPermission, q)
                    level2_ROOM1_sprites.draw(screen)
                    level2_ROOM1_sprites.update()
                elif room == 2:
                    keyGreen.updater(q)
                    level2_door2.update(q)
                    level2_ROOM2_sprites.draw(screen)
                    level2_ROOM2_sprites.update()
                elif room == 3:
                    doorGreen2.updater(GreenPermission, q)
                    doorRed.updater(RedPermission, q)
                    level2_door3.update(q)
                    level2_ROOM3_sprites.draw(screen)
                    level2_ROOM3_sprites.update()
                elif room == 4:
                    level2_door4.update(q)
                    level2_ROOM4_sprites.draw(screen)
                    level2_ROOM4_sprites.update()

                bat31.updates(q)

                Kristall3.updater(q)
                Kristall4.updater(q)
                Kristall5.updater(q)

                player_sprite.draw(screen)
                player_sprite.update()

                if room == 1:
                    bat1.updater()
                    bat2.updater()
                    bat3.updater()
                    bat4.updater()
                    bat5.updater()
                    bat6.updater()
                    bat7.updater()
                    BatsRoom1.draw(screen)
                    BatsRoom1.update()
                elif room == 2:
                    bat21.updater()
                    bat22.updater()
                    bat23.updater()
                    bat24.updater()
                    bat25.updater()
                    bat26.updater()
                    bat27.updater()
                    BatsRoom2.draw(screen)
                    BatsRoom2.update()
                elif room == 3:
                    bat31.updater()
                    bat32.updater()
                    bat33.updater()
                    bat34.updater()
                    bat35.updater()
                    bat36.updater()
                    bat37.updater()
                    BatsRoom3.draw(screen)
                    BatsRoom3.update()
                elif room == 4:
                    bat41.updater()
                    bat42.updater()
                    bat43.updater()
                    bat44.updater()
                    bat45.updater()
                    bat46.updater()
                    bat47.updater()
                    BatsRoom4.draw(screen)
                    BatsRoom4.update()

                pygame.display.flip()

            elif level == 'end2':
                f = open("progress.txt", 'w')
                f.write('0')
                f.close()
                player.NEWcords(0.5 * WIDTH // 1, 0.5 * HEIGHT // 1)
                room = 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        running = False

                screen.fill((0, 0, 0))
                screen.blit(NachFON, (0, 0))

                text1 = font.render("Игра пройдена!", True, (50, 100, 255))
                screen.blit(text1, [(0.35 * WIDTH) // 1, (0.2 * HEIGHT) // 1])

                text7 = font2.render("Найдено " + str(secret) + " из 5 пасхалок", True, (50, 150, 255))
                screen.blit(text7, [(0.37 * WIDTH) // 1, (0.45 * HEIGHT) // 1])


                text3 = font2.render("Выйти: Esc", True, (50, 150, 255))
                screen.blit(text3, [(0.45 * WIDTH) // 1, (0.6 * HEIGHT) // 1])

                pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
