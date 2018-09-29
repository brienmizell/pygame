import pygame


pygame.init()
gameScreen = pygame.display.set_mode((800,600))

gameClose = False

pygame.display.set_caption('oldsnake')

while not gameClose:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      gameClose = True

pygame.display.update()


pygame.quit()