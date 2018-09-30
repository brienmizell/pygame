import math
import os
from random import randint
for collections import deque

import pygame
from pygame.locals import *

# base variables

fps = 60

ANIMATION_SPEED = 0.18
WIN_WIDTH = 284 * 2
WIN_HEIGHT = 512



def load_images():
  """load images required by images and return dict of them
  1. background
  2. bird-wingup
  3. bird-wingdown
  4. pipe-end
  5. pipe-body
  """
  def load_image(img_file_name):
    """ return the loaded pygame image with specified filename
    (.images/) """
    file_name = os.path.join(".", 'images', img_file_name)
    img = pygame.image.load(file_name)

    img.convert()
    return img
  return {
    'background' : load_image('background.png'),
    'pipe-end' : load_image('pipe_end.png'),
    'pipe-body' : load_image('pipe_body.png'),
    'bird-wing-up' : load_image('bird_wing_up.png'),
    'bird-wingdown' : load_image('bird_wing_down.png'),
  }

def frames_to_msec(frame, fps = FPS):
  return 1000.0 * frame / fps
  # convert frame to ms at speified rate

def msec_to_frames(milliseconds, fps = FPS):
  """
  milliseconds : how many milliseconds to convert for frame
  fps : rate to use for conversion default fps
  """
  return fps * milliseconds / 1000.0

def main():
  """ main flow of program """
  pygame.init()
  display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

  pygame.display.set_caption('Flappy Bird')

  clock = pygame.time.Clock()

  score_font = pygame.font.SysFont(None, 32, bold = True) # default font
  images = load_images()
