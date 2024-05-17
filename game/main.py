import asyncio
import os
import sys

import pygame
from moviepy.editor import VideoFileClip
from PIL import Image

from player import Player
from constants import (
    SCREEN_SIZE,
    FPS,
    CURRENT_FOLDER,
    STEP_PIXELS,
    VIDEO_POSITION,
    BACKGROUND_POSITION,
    BLACK_FILL,
    SLEEPING_TIME_FOR_ASYNC
)

VIDEO_PATH = (os.path.join(CURRENT_FOLDER / 'assets/loading.mp4'))

print(f'{VIDEO_PATH = }')

BACKGROUND_PATH = (os.path.join(CURRENT_FOLDER / 'assets/roads.jpg'))
IMAGE_BACKGROUND = pygame.image.load(BACKGROUND_PATH)
IMAGE_PLAYER = (pygame.image.load(CURRENT_FOLDER / 'assets/cat.png'))


def quit_game():
    pygame.quit()
    sys.exit()
    pygame.mixer.quit()


async def main():
    """
    This is function mothing return.
    Need for start game and can start only from
    'main.py'.
    video_path - path to loading-video
    image_background - path to background image
    image_player - loading the player through pygame, since
    after that I sat the color which should be transparent.
    because
    """
    print('Start main()')
    player = Player(IMAGE_PLAYER)

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Window for play')
    clock = pygame.time.Clock()

    clip = VideoFileClip(VIDEO_PATH)

    # Start music
    pygame.mixer.init()
    current_music_index = 0
    music_files = [
        os.path.join(CURRENT_FOLDER / f'assets/track-{i}.mp3')
        for i in range(1, 6)
    ]

    pygame.mixer.music.load(music_files[current_music_index])
    pygame.mixer.music.play()

    must_play_loading_screen = True
    # video_started = False
    print('We are starting the main loop.')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Обработка события закрытия окна
                quit_game()

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                quit_game()

            if event.key not in (pygame.K_RIGHT, pygame.K_LEFT):
                continue
                shift = 1

            if event.key == pygame.K_LEFT:
                shift = -1
            current_music_index = (current_music_index + shift) % len(music_files)
            pygame.mixer.music.load(music_files[current_music_index])
            pygame.mixer.music.play()

        if must_play_loading_screen: # not video_started:
            frame = clip.get_frame(pygame.time.get_ticks() / 1000)
            pil_image = Image.fromarray(frame)
            image_bytes = pil_image.tobytes()
            frame_surface = pygame.image.fromstring(image_bytes, pil_image.size, pil_image.mode)
            screen.blit(frame_surface, VIDEO_POSITION)
            pygame.display.update()

            if pygame.time.get_ticks() / 1000 >= clip.duration:
                must_play_loading_screen = False

        else:
            # screen.blit(IMAGE_BACKGROUND, BACKGROUND_POSITION)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                if player.rect.y > 0:
                    player.rect.y -= STEP_PIXELS
            if keys[pygame.K_s]:
                if player.rect.y < SCREEN_SIZE[1] - player.rect.height:
                    player.rect.y += STEP_PIXELS
            if keys[pygame.K_d]:
                if player.rect.x < SCREEN_SIZE[0] - player.rect.width:
                    player.rect.x += STEP_PIXELS
            if keys[pygame.K_a]:
                if player.rect.x > 0:
                    player.rect.x -= STEP_PIXELS

            # Check borders:
            player.apply_borders()

            screen.fill(BLACK_FILL)
            screen.blit(IMAGE_BACKGROUND, BACKGROUND_POSITION)
            screen.blit(player.image_player, (player.rect.x, player.rect.y))
            pygame.display.update()

            if not pygame.mixer.music.get_busy():
                current_music_index = (current_music_index + 1) % len(music_files)
                pygame.mixer.music.load(music_files[current_music_index])
                pygame.mixer.music.play()

        clock.tick(FPS)
        await asyncio.sleep(SLEEPING_TIME_FOR_ASYNC)


if __name__ == '__main__':
    asyncio.run(main())
