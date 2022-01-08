import os
import sys
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
    image = load_image('Player1.png')
    # image = pygame.transform.scale(image, (WIDTH, HEIGHT))

    def __init__(self, *group):
        super().__init__(*group)
        self.predelX = (0.5 * WIDTH // 1) - (0.5 * WIDTH * 5 / 7) // 1
        self.predelY = (0.5 * HEIGHT // 1) - (0.5 * HEIGHT * 2 / 3) // 1
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
        self.rect.x = 190 + 100
        self.rect.y = 10 + 200

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
        if self.rect.x + 160 <= WIDTH - self.predelX:
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

def main():
    fps = 144
    clock = pygame.time.Clock()
    pygame.display.set_caption("Master of Dungeon")
    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    player = Player(all_sprites)
    FON = load_image('Fon.jpeg')
    FON = pygame.transform.scale(FON, (WIDTH, HEIGHT))
    screen.blit(FON, (0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                pass
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
        player.inerzia()
        screen.blit(FON, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()