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

class Bird(pygame.sprite.Sprite):
  # bird should be controlled by the player.
   """Represents the bird controlled by the player.

    The bird is the 'hero' of this game.  The player can make it climb
    (ascend quickly), otherwise it sinks (descends more slowly).  It must
    pass through the space in between pipes (for every pipe passed, one
    point is scored); if it crashes into a pipe, the game ends.

    Attributes:
    x: The bird's X coordinate.
    y: The bird's Y coordinate.
    msec_to_climb: The number of milliseconds left to climb, where a
        complete climb lasts Bird.CLIMB_DURATION milliseconds.

    Constants:
    WIDTH: The width, in pixels, of the bird's image.
    HEIGHT: The height, in pixels, of the bird's image.
    SINK_SPEED: With which speed, in pixels per millisecond, the bird
        descends in one second while not climbing.
    CLIMB_SPEED: With which speed, in pixels per millisecond, the bird
        ascends in one second while climbing, on average.  See also the
        Bird.update docstring.
    CLIMB_DURATION: The number of milliseconds it takes the bird to
        execute a complete climb.
    """
    WIDTH = height = 32
    SINK_SPEED = 0.18
    CLIMB_SPEED = 0.32
    CLIMB_DURATION = 333.3

    def __init__(self, x, y, msec_to_climb, images):
      """Initialise a new Bird instance.

        Arguments:
        x: The bird's initial X coordinate.
        y: The bird's initial Y coordinate.
        msec_to_climb: The number of milliseconds left to climb, where a
            complete climb lasts Bird.CLIMB_DURATION milliseconds.  Use
            this if you want the bird to make a (small?) climb at the
            very beginning of the game.
        images: A tuple containing the images used by this bird.  It
            must contain the following images, in the following order:
                0. image of the bird with its wing pointing upward
                1. image of the bird with its wing pointing downward
        """
      super(Bird,self).__init__()
      self.x, self.y = x,y
      self.msec_to_climb = msec_to_climb
      self.img_wingup, self.img_wingdown = images
      self._mask_wingup = pygame.mask.from_surface(self._img_wingdown)
      self._mask_wingdown = pygame.mask.from_surface(self._img_wingdown)
      
      def mask(self):
        if pygame.time.get_ticks() % 500 >= 250:
          return self._mask_wingup
        else:
          return self._mask_wingdown

        """Get a bitmask for use in collision detection.

        The bitmask excludes all pixels in self.image with a
        transparency greater than 127."""


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
