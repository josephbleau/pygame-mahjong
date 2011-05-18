import sys
import pygame
import time
import os.path

# my imports
from tile import *
from game import * 

class Editor(Game):
  def __init__(self,sound=True):
    Game.__init__(self,editor=True, sound=sound)
    self.cursor_tile = Tile(1,0,0,1)
    
  def save_level(self):
    "Writes the current tile list to file."
    fh = open('levels/' + self.filename, 'w')
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
    if event.unicode == 'u':
      try:
        self.tiles.pop()
      except IndexError, e:
        pass
    return
  
  def getNearestBelow(self, t):
    "Determines whether or not our tile 't' has a tile below it, and if it does,  \
     return the (nearest) tile below it. This is used in determining what z-level \
     our tile should be at when editing levels."
    x = t.x
    y = t.y
    z = t.z
    for tile in sorted(self.tiles, key=byTopRight, reverse=True):
      if (tile.x + 20 == x and tile.y - 30 == y) or \
         (tile.x - 20 == x and tile.y - 30 == y) or \
         (tile.x + 20 == x and tile.y + 30 == y) or \
         (tile.x - 20 == x and tile.y + 30 == y):
        return tile
      if tile.x == x and tile.y == y:
        return tile
      if tile.y == y and tile.x + 20 == x:
        return tile
      if tile.x == x and tile.y + 30 == y:
        return tile
      if tile.x == x and tile.y - 30 == y:
        return tile
      if tile.y == y and tile.x - 20 == x:
        return tile
    return None
    
  def manual_move_tile_cursor(self, x, y):
    "Take in mouse coordinates and move around our tile cursor."
    x = int(x/20) * 20
    y = int(y/30) * 30
    self.cursor_tile.x = x
    self.cursor_tile.y = y

    nearest_below = self.getNearestBelow(self.cursor_tile) 
    if nearest_below :
      self.cursor_tile.z = nearest_below.z + 1
    else:
      self.cursor_tile.z = 1
    
    return
    
  def move_tile_cursor(self, event):
    self.manual_move_tile_cursor( event.pos[0], event.pos[1] )
  
  
  def place_tile(self, event):
    if event.button == 1:
      no, x,y,z = self.cursor_tile.tileno, self.cursor_tile.x, self.cursor_tile.y, self.cursor_tile.z
      
    nearest_below = self.getNearestBelow(self.cursor_tile) 
    if nearest_below :
      self.cursor_tile.z = nearest_below.z + 1
    else:
      self.cursor_tile.z = 1

    self.tiles.append(Tile(no,x,y,z))
    self.manual_move_tile_cursor(self.cursor_tile.x, self.cursor_tile.y)
         
  def draw_tile_cursor(self, screen):
      self.cursor_tile.draw(screen)
    
  def select_tile(self, event):
    return