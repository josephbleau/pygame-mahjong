import sys
import pygame
import time
import os.path

class Tile:
  def __init__(self, tileno, x, y, z):
    self.tileno = tileno
    self.imgpath    = os.path.abspath('res/tiles/' + str(self.tileno) + '.png')
    self.img = pygame.image.load(self.imgpath)
    
    self.x = x
    self.y = y
    self.z = z

  def draw(self, screen):
    "Draw a tile the the screen"
    if self.img:
      rect = (self.x - self.z * 3, self.y - self.z * 3, 40, 60)
      screen.blit(self.img, rect)
  
  def is_blocked(self,tiles):
    "A tile can compare itself to a list of tiles to find out whether or not it's being blocked. A tile  \
   being blocked is when it has both a tile on its direct left, and direct right. This is important in \
   Mahjong because you cannot remove a tile if it is blocked."
    left = False
    right = False
    
    for tile in tiles:
      # Check against pieces obscuring us above our tile.
      if (tile.z > self.z and tile.x + 20 == self.x and tile.y - 30 == self.y) or \
         (tile.z > self.z and tile.x - 20 == self.x and tile.y - 30 == self.y) or \
         (tile.z > self.z and tile.x + 20 == self.x and tile.y + 30 == self.y) or \
         (tile.z > self.z and tile.x - 20 == self.x and tile.y + 30 == self.y):
          return True
      
      if (tile.z > self.z and tile.x + 20 == self.x and tile.y == self.y)  or \
         (tile.z > self.z and tile.x - 20 == self.x and tile.y == self.y)  or \
         (tile.z > self.z and tile.x == self.x and tile.y == self.y)       or \
         (tile.z > self.z and tile.y + 30 == self.y and tile.x == self.x)  or \
         (tile.z > self.z and tile.y - 30 == self.y and tile.x == self.x):
        return True
        
      # Check against even-level touching pieces.
      if tile.z == self.z and tile.y == self.y:
        if self.x+40 == tile.x:
          right = True
        if tile.x + 40 == self.x:
          left = True
          
      if tile.z == self.z:
        if (tile.y == self.y - 30 and tile.x == self.x + 40) or \
           (tile.y == self.y + 30 and tile.x == self.x + 40):
          right = True
        if (tile.y == self.y - 30 and tile.x == self.x - 40) or \
           (tile.y == self.y + 30 and tile.x == self.x - 40):
          left = True

    return left and right
    
def byTopRight(tiles):
  "Helper function used to sort tiles."
  return (tiles.z, tiles.x, tiles.y)