import sys
import pygame
import time
from time import localtime
import os.path
import random

# my imports
from tile import *
  
def get_string_surf(font, text):
  return font.render(text, True, (0,0,0))
  
def render_text(screen, font, text, (x,y,w,h)):
  screen.blit(get_string_surf(font, text), (x,y,w,h))
  
class Game:
  def __init__(self):
    self.state = 'playing'
    self.selected = None
    self.time_started = localtime()
    pygame.mixer.music.load('res/bg.mp3')
    pygame.mixer.music.play(loops=-1)
    
    self.fontpath = os.path.abspath('res/ChopinScript.otf')
    self.font = pygame.font.Font(self.fontpath, 42)
    if self.font:
      self.game_title_text     = self.font.render("Vanessa Mahjong", True, (0,0,0))
      self.pieces_removed_text = self.font.render("Pieces Removed: ", True, (0,0,0)) 
      self.good_job_text       = self.font.render("Good job!", True, (0,0,0))
    
    #generate tiles, just for testing for now
    self.tiles = []
    self.pieces_removed = 0
    
    offset_x = 200
    offset_y = 200
    
    pieces = [n%8+1 for n in range(64)]
    
    for z in range(8):
      for x in range(4-z/2):
        for y in range(4-z/2):
          choice = random.choice(pieces)
          pieces.remove(choice)
          self.tiles.append(Tile(choice,offset_x + x*40,offset_y +  y*60,z))  
    
    print len(pieces)
  def handle_tile_click(self,event):
    for tile in sorted(self.tiles, key=byTopRight, reverse=True) :
        x,y = event.pos
        if x >= tile.x - tile.z * 3 and x <= tile.x + 40 - tile.z * 3 and \
           y >= tile.y - tile.z * 3 and y <= tile.y + 60 - tile.z * 3:
           if self.selected == tile: # Selecting the selected tile unselects it.
            self.selected = None
            return
           if self.selected: # We clicked on a tile, is a tile already selected?
            if self.selected.tileno == tile.tileno:     # Remove tiles if they're the same
              # But only if both tiles are not blocked on left & right
              if not tile.is_blocked(self.tiles) and not self.selected.is_blocked(self.tiles):
                self.tiles.remove(self.selected)
                self.tiles.remove(tile)
                self.pieces_removed += 2
                
                if len(self.tiles) == 0:
                  self.state = 'level_complete'
              self.selected = None
              return
            else:
              self.selected = None
              return
           else:
            if not tile.is_blocked(self.tiles):
              self.selected = tile        
           return
           
           
    self.selected = None
  
  def handle_input(self, event):
    "Based on the games current state, manage our mouse input."
    if self.state == 'playing':
      self.handle_tile_click(event)
    if self.state == 'level_complete':
      self.state == 'next_level'
      
  def render_menu(self, screen):
    "Draw the main menu"
    pass
    
  def render(self, screen):
    "Based on the games state, call the appropriate drawing methods"
    if self.state == 'menu':
      self.render_menu(screen)
      return
    elif self.state == 'playing':
      # Draw Title & Score
      if self.game_title_text:
        render_text(screen, self.font, "Vanessa Mahjong", (20,20,300,300))
      if self.pieces_removed_text:
        render_text(screen, self.font, "Pieces Removed: ", (500,500,200,100))
        render_text(screen, self.font, str(self.pieces_removed), (550,550,200,50))
      # Draw all of the tiles on the map.
      for tile in self.tiles:
        tile.draw(screen)
        if self.selected:
          pygame.draw.rect(screen, (255,0,0), (self.selected.x - self.selected.z * 3, \
                                               self.selected.y - self.selected.z * 3, 40-2, 60-2),2)   
    elif self.state == 'level_complete':
      render_text(screen, self.font, "Sweet!", (325,250,200,100))
      render_text(screen, self.font, "(Click for next level!)", (20,120,100,100))
      rose = pygame.image.load('res/rose.jpg')
      roserect = [(0,200,318,350),(800-318,100,318,350)]
      screen.blit(rose,roserect[0])
      screen.blit(rose,roserect[1])
      pygame.draw.rect(screen,(0,0,0), (0,0,800,100))
      pygame.draw.rect(screen,(0,0,0), (0,500,800,100))
      
    return