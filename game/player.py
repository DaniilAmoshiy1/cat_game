import pygame


from constants import (
    INVISIBLE_COLOR,
    SCREEN_SIZE,
)


class Player(pygame.sprite.Sprite):

    def __init__(self, image_player: pygame.Surface):
        """
        This is function for initialisation, here happening
        init Sprite through library pygame, set selfs
        and player speed.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image_player = image_player
        self.image_player.set_colorkey(INVISIBLE_COLOR)
        self.rect: pygame.Rect = image_player.get_rect()
        self.y_speed = 0
        self.x_speed = 0
        self.rect.x = SCREEN_SIZE[0] // 2 - self.rect.width // 2
        self.rect.y = SCREEN_SIZE[1] // 2 - self.rect.height // 2
        print('Player created.')

    def apply_borders(self):
        self.rect.x = max(0, min(self.rect.x, SCREEN_SIZE[0] - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_SIZE[1] - self.rect.height))
