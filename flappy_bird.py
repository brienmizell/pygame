import math
import os
from random import randint
from collections import deque

import pygame
from pygame.locals import *

# base variables

FPS = 60
ANIMATION_SPEED = 0.18
WIN_WIDTH = 284 * 2
WIN_HEIGHT = 512

class Bird(pygame.sprite.Sprite):
  '''Represents the bird controlled by the player.

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
  '''
  WIDTH = HEIGHT = 50
  SINK_SPEED = 0.18
  CLIMB_SPEED = 0.33
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
    super(Bird, self).__init__()
    self.x, self.y = x, y
    self.msec_to_climb = msec_to_climb
    self._img_wingup, self._img_wingdown = images
    self._mask_wingup = pygame.mask.from_surface(self._img_wingup)
    self._mask_wingdown = pygame.mask.from_surface(self._img_wingdown)

  def update(self, delta_frames = 1):
    """ delta_frame is number of frames elapsed
    
    this function will use the cosine function to acheive a smooth climb (flap)
    """
    if self.msec_to_climb > 0 :
      frac_climb_done = 1 - self.msec_to_climb / Bird.CLIMB_DURATION

      self.y -= (Bird.CLIMB_SPEED) * frames_to_msec(delta_frames) * (1 - math.cos(frac_climb_done * math.pi))

      self.msec_to_climb -= frames_to_msec(delta_frames)
    else:
      self.y += Bird.SINK_SPEED * frames_to_msec(delta_frames)
  
  @property
  def image(self):
    if pygame.time.get_ticks() % 500 >= 250:
      return self._img_wingup
    else:
      return self._img_wingdown

  @property
  def mask(self):
    if pygame.time.get_ticks() % 500 >= 250:
      return self._mask_wingup
    else:
      return self._mask_wingdown

    """Get a bitmask for use in collision detection.

    The bitmask excludes all pixels in self.image with a
    transparency greater than 127."""
  
  @property
  def rect(self):
    return Rect(self.x, self.y, Bird.WIDTH, Bird.HEIGHT)
  

class PipePair(pygame.sprite.Sprite):
  """
  Represents an obstacle.

  A PipePair has a top and a bottom pipe, and only between them can
  the bird pass -- if it collides with either part,the game is over.

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

  def __init__(self, pipe_end_img, pipe_body_img):

    self.x = float(WIN_WIDTH - 1)
    self.score_counted = False

    self.image = pygame.Surface((PipePair.WIDTH, WIN_HEIGHT), SRCALPHA)
    self.image.convert()
    self.image.fill((0, 0, 0, 0))

    total_pipe_body_pieces = int(
      (WIN_HEIGHT -
      3 * Bird.HEIGHT -
      3 * PipePair.PIECE_HEIGHT) / 
      PipePair.PIECE_HEIGHT
    )

    self.bottom_pieces = randint(1, total_pipe_body_pieces)
    self.top_pieces = total_pipe_body_pieces - self.bottom_pieces

    for i in range(1, self.bottom_pieces + 1):
      piece_pos = (0, WIN_HEIGHT - i * PipePair.PIECE_HEIGHT)
      self.image.blit(pipe_body_img, piece_pos)
    bottom_pipe_end_y = WIN_HEIGHT - self.bottom_height_px
    bottom_end_piece_pos = (0, bottom_pipe_end_y - PipePair.PIECE_HEIGHT)
    self.image.blit(pipe_end_img, bottom_end_piece_pos)

    for i in range(self.top_pieces):
      self.image.blit(pipe_body_img, (0, i * PipePair.PIECE_HEIGHT))
    top_pipe_end_y = self.top_height_px
    self.image.blit(pipe_end_img, (0, top_pipe_end_y))
    # total_pipe_end_x = self.top_height_px
    # self.image.blit(pipe_end_img, (o, total_pipe_end_x))

    self.top_pieces += 1
    self.bottom_pieces += 1

    self.mask = pygame.mask.from_surface(self.image)

  @property
  def top_height_px(self):
    return self.top_pieces * PipePair.PIECE_HEIGHT

  @property
  def bottom_height_px(self):
    return self.bottom_pieces * PipePair.PIECE_HEIGHT

  @ property
  def visible(self):
    return -PipePair.WIDTH < self.x < WIN_WIDTH

  @property
  def rect(self):
    return Rect(self.x, 0, PipePair.WIDTH, PipePair.PIECE_HEIGHT)

  def update(self, delta_frames = 1):
    self.x -= ANIMATION_SPEED * frames_to_msec(delta_frames)

    # self.x -= ANIMATION_SPEED * frame_clock(delta_frames)

  def collides_with(self, bird):
    return pygame.sprite.collide_mask(self, bird)

def load_images():
  """load images required by images and return dict of them
  1. background
  2. bird-wingp
  3. bird-wingwn
  4. pipe-end  5. pipe-body
  """
  def load_image(img_file_name):
    """ return the loaded pygame image with specified filename
    (.images/) """
    file_name = os.path.join(".", 'images', img_file_name)
    img = pygame.image.load(file_name)

    img.convert()
    return img
  return {'background' : load_image('background.png'),
      'pipe_end' : load_image('pipe_end.png'),
      'pipe_body' : load_image('pipe_body.png'),
      'bird_wingup' : load_image('bird_wingup.png'),
      'bird_wingdown' : load_image('bird_wingdown.png')}

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

  bird = Bird(50, int(WIN_HEIGHT / 2 - Bird.HEIGHT /2), 2,
        (images["bird_wingup"], images["bird_wingdown"]))
  pipes = deque()

  score = 0

  frame_clock = 0

  done = paused = False

  while not done:
    clock.tick(FPS)

    if not (paused or frame_clock % msec_to_frames(PipePair.ADD_INTERVAL)):
      pp = PipePair(images['pipe_end'], images['pipe_body'])
      pipes.append(pp)

    for e in pygame.event.get():
      if e.type == QUIT or (e.type == KEYUP and e.type == K_ESCAPE):
        done = True
        break
      elif e.type == KEYUP and e.key in (K_PAUSE, K_p):
        paused = not paused
      elif e.type == MOUSEBUTTONUP or (e.type == KEYUP and e.key in (K_UP, K_RETURN, K_SPACE)):
        bird.msec_to_climb = Bird.CLIMB_DURATION
    if paused:
      continue

    pipe_collision = any(p.collides_with(bird)for p in pipes)

    if pipe_collision or 0 >= bird.y or bird.y >= WIN_HEIGHT - Bird.HEIGHT:
      done = True
    
    for x in (0, WIN_WIDTH / 2):
      display_surface.blit(images['background'], (x, 0))

    while pipes and not pipes[0].visible:
      pipes.popleft()

    for p in pipes:
      p.update()
      display_surface.blit(p.image, p.rect)
    
    bird.update()
    display_surface.blit(bird.image, bird.rect)

    # update and show score
    for p in pipes:
      if p.x + PipePair.WIDTH < bird.x and not p.score_counted == True:
        score += 1
        p.score_counted = True

    score_surface = score_font.render(str(score), True, (255, 255, 255))
    score_x = WIN_WIDTH / 2 - score_surface.get_width() / 2
    display_surface.blit(score_surface,(score_x, PipePair.PIECE_HEIGHT))

    pygame.display.flip()
    frame_clock += 1
  print('Game over! Score: %i' % score)
  pygame.quit()

if __name__ == '__main__':
  main()