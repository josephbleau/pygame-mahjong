import sys
import pygame
import time
import os.path

# my imports
from tile import *
from game import * 

class Editor(Game):
  def __init__(self):
    Game.__init__(self,editor=True)
    self.cursor_tile = Tile(1,0,0,1)
    
  def save_level(self):
    "Writes the current tile list to file."
    fh = open('level.txt', 'w')
    if(fh):
      for tile in self.tiles:
        no = tile.tileno
        x,y,z = tile.x, tile.y, tile.z
        fh.write('('+str(no)+','+str(x)+','+str(y)+','+str(z)+')')
        
      print 'Saved.'
    
    fh.close()
        
  
  def select_cursor_tile(self, event):
    "Select which tile we're placing based on user input. Also, for no good reason \
     determine if the player pressed 's' for saving. "
    if event.key >= 49 and event.key <= 58:
      x,y = self.cursor_tile.x, self.cursor_tile.y
      self.cursor_tile = Tile(event.key-48,x,y,1)
    if event.unicode == 's':
      self.save_level()
    return
    
  def move_tile_cursor(self, event):
    "Take in mouse coordinates and move around our tile cursor."
    self.cursor_tile.x = int(event.pos[0] / 20) * 20
    self.cursor_tile.y = int(event.pos[1] / 30) * 30
    return
  
  
  def place_tile(self, event):
    if event.button == 1:
      no, x,y,z = self.cursor_tile.tileno, self.cursor_tile.x, self.cursor_tile.y, self.cursor_tile.z
      for tile in self.tiles:
        if tile.x == x and tile.y == y:
          z = tile.z + 1
        if tile.y == y and tile.x + 20 == x:
          z = tile.z + 1
        if tile.x == x and tile.y + 30 == y:
          z = tile.z + 1
        if tile.x == x and tile.y - 30 == y:
          z = tile.z + 1
        if tile.y == y and tile.x - 20 == x:
          z = tile.z + 1
      self.tiles.append(Tile(no,x,y,z))
      
    
  def draw_tile_cursor(self, screen):
      self.cursor_tile.draw(screen)
    
  def select_tile(self, event):
    return