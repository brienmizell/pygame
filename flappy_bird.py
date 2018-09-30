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
    WIDTH = HEIGHT = 32
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

  def update(self, delta_frame = 1):
    """ delta_frame is number of frames elapsed
    
    this function will use the cosine function to acheive a smooth climb (flap)
    """
    if self.msec_to_climb > 0 :
      frac_climb_done = 1 - self.msec_to_climb / Bird.CLIMB_DURATION

      self.y -= (bird.CLIMB_SPEED) * frames_to_msec(delta_frame) * (1-math.cos(frac_climb_done * math.pi))

      self.msec_to_climb -= frames_to_msec(delta_frame)
    else:
      self.y += Bird.SINK_SPEED * frames_to_msec(delta_frame)
  @property
  def image(self):
    if pygame.time.get_ticks() % 500 >= 250:
      return self._mask_wingdown
    else:
      return self._mask_wingup
  @property
  def rect(self):
    return rect(self.x, self.y, Bird.WIDTH, Bird.HEIGHT)

  def mask(self):
    if pygame.time.get_ticks() % 500 >= 250:
      return self._mask_wingup
    else:
      return self._mask_wingdown

    """Get a bitmask for use in collision detection.

    The bitmask excludes all pixels in self.image with a
    transparency greater than 127."""

class PipePair(pygame.sprite.Sprite):
  """Represents an obstacle.

    A PipePair has a top and a bottom pipe, and only between them can
    the bird pass -- if it collides with either part, the game is over.

    Attributes:
    x: The PipePair's X position.  This is a float, to make movement
        smoother.  Note that there is no y attribute, as it will only
        ever be 0.
    image: A pygame.Surface which can be blitted to the display surface
        to display the PipePair.
    mask: A bitmask which excludes all pixels in self.image with a
        transparency greater than 127.  This can be used for collision
        detection.
    top_pieces: The number of pieces, including the end piece, in the
        top pipe.
    bottom_pieces: The number of pieces, including the end piece, in
        the bottom pipe.

    Constants:
    WIDTH: The width, in pixels, of a pipe piece.  Because a pipe is
        only one piece wide, this is also the width of a PipePair's
        image.
    PIECE_HEIGHT: The height, in pixels, of a pipe piece.
    ADD_INTERVAL: The interval, in milliseconds, in between adding new
        pipes.
    """
  WIDTH = 80
  PIECE_HEIGHT = 32
  ADD_INTERVAL = 3000

  def __init__(self, pip_end_img, pipe_body_img):

    self.x - float(WIN_WIDTH -1)
    self.core_counted = False
    self.image = pygame((PipePair.WIDTH, WIN_HEIGHT), SRCALPHA)
    self.image.convert()
    self.image.fill((0, 0, 0))

    total_pipe_body_pieces = int(WIN_HEIGHT -
    3 * WIN_HEIGHT -
    3 * PipePair.PIECE_HEIGHT) /
    PipePair.PIECE_HEIGHT
    
    )
  self.bottom_pieces = randint(1, total_pipe_body_pieces)
  self.top_pieces = randint(1, total_pipe_body_pieces)

  for i in range(1, self.bottom_pieces):
    piece_pos = (0, WIN_HEIGHT - 1 * PipePair.PIECE_HEIGHT)
    self.image.blit(pipe_body_img, piece_pos)

  bottom_pipe_end_y = WIN_HEIGHT - self.bottom_height_px)
  bottom_end_pipe_pos = (0, bottom_pipe_end_y - PipePair.PIECE_HEIGHT)
  self.image.blit(pipe_end_img, bottom_end_pipe_pos)

  for in in range(self.top_pieces):
    self.image.blit(pipe_body_img, (0, i* PipePair.PIECE_HEIGHT))
  
  total_pipe_end_x = self.top_height_px
  self.image.blit(pipe_end_img, (o, total_pipe_end_x))

  self.top_pieces += 1
  self.bottom_pieces +=1

  self.mask = pygame.mask.from_surface(self.image)

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
