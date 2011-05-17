import sys
import pygame
import time
import os.path

# my imports
from tile import *
from game import * 

class Editor(Game):
  def __init__(self):
    Game.__init__(self)
    self.cursor_tile = Tile(1,0,0,1)
    
  def select_cursor_tile(self, event):
    if event.key >= 49 and event.key <= 58:
      x,y = self.cursor_tile.x, self.cursor_tile.y
      self.cursor_tile = Tile(event.key-48,x,y,1)
    return
    
  def move_tile_cursor(self, event):
    self.cursor_tile.x = event.pos[0]
    self.cursor_tile.y = event.pos[1]
    return
    
  def draw_tile_cursor(self, screen):
      self.cursor_tile.draw(screen)
    
  def select_tile(self, event):
    return