import sys
import pygame
import time
import re
from time import localtime
import os.path
import random
from random import shuffle

# my imports
from tile import *
  
def get_string_surf(font, text, color=(0,0,0)):
  "Used in lazy-man text-writing :)"
  return font.render(text, True, color)
  
def render_text(screen, font, text, (x,y,w,h), color=(0,0,0)):
  "Lazy-man text-writing."
  screen.blit(get_string_surf(font, text, color=color), (x,y,w,h))

def load_level(filename, rnd=False, enforceTwo=False):
  "Loads a level from a text file. If the random flag is set to True \
   then all tiles are simply random, otherwise use the files tileno's "
  try:
    fh = open(os.path.abspath('levels/' + filename), 'r')
  except IOError, e:
    open(os.path.abspath('levels/' + filename), 'a')
  
  fh = open(os.path.abspath('levels/' + filename), 'r')
  if fh:
    text = fh.read()
    tiles = []
    for no,x,y,z in re.findall('[(](\d+),(\d+),(\d+),(\d+)[))]', text):
     tiles.append(Tile(int(no),int(x),int(y),int(z)))
    
    if enforceTwo and len(tiles) % 2 == 0:
      print 'You are enforcing divisible by two tile rule, and there are an uneven amount of tiles.'
      return []
    
    if rnd:
      random.seed()
      for tile in range(0,len(tiles)-1,2):
        no = random.choice(range(1,9,1))
        tiles[tile] = Tile(no, tiles[tile].x, tiles[tile].y, tiles[tile].z)
        tiles[tile+1] = Tile(no, tiles[tile+1].x, tiles[tile+1].y, tiles[tile+1].z)
        
        
    return tiles
      
  return []
  
class Game:    
  def __init__(self, editor=False, sound=True):
    if editor:
      self.state = 'playing'
    else:
      self.state = 'menu'
    
    self.selected = None
    self.time_started = localtime()
    self.m_selector = 0 # menu selector
    self.sound = sound
    self.editor = editor
    
    # Background Music
    if self.sound:
      pygame.mixer.music.load('res/bg.mp3')
      pygame.mixer.music.play(loops=-1)
    
    # Font
    self.fontpath = os.path.abspath('res/ChopinScript.otf')
    self.font = pygame.font.Font(self.fontpath, 42)
    
    # Load tiles
    self.pieces_removed = 0
    self.tiles = load_level('turtle.txt', rnd=(not editor))
    self.start_piece_count = len(self.tiles)
   #generate tiles, just for testing for now    
   # offset_x = 200
   # offset_y = 200
   # pieces = [n%8+1 for n in range(64)] 
   # for z in range(8):
   #   for x in range(4-z/2):
   #     for y in range(4-z/2):
   #       choice = random.choice(pieces)
   #       pieces.remove(choice)
   #       self.tiles.append(Tile(choice,offset_x + x*40,offset_y +  y*60,z))  
    
  def handle_tile_click(self,event):
    "Send mouse click events to us. We handle selected / unselecting tiles, \
     match-pairing, and whether or not the matches were valid. This function also handles \
     state-changing when all tiles are missing. "
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
                  pygame.event.clear()
                  return
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
    if self.state == 'menu':
      
      if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
        if self.m_selector == 3:
          self.m_selector = 0
        else:
          self.m_selector += 1
      if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
        if self.m_selector == 0:
          self.m_selector = 3
        else:
          self.m_selector -= 1
          
      # When the user makes a selection
      if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        if self.m_selector == 0:
          self.state = 'level_select'
          self.m_selector = 0
          return
        if self.m_selector == 3:
          sys.exit()
          
      if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        sys.exit()
          
    if self.state == 'level_select':
      if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        self.state = 'menu'
        return
        
      max = len(os.listdir(os.path.abspath('levels/')))-1
      if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
        if self.m_selector == 0:
          self.m_selector = max+1
        else:
          self.m_selector -= 1
      if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
        if self.m_selector == max+1:
          self.m_selector = 0
        else:
          self.m_selector += 1
          
      if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        if self.m_selector == max+1: #back button pressed
          self.state = 'menu'
          self.m_selector = 0
          return
          
        levels = os.listdir(os.path.abspath('levels/'))
        self.state = 'playing'      
        self.pieces_removed = 0
        self.tiles = load_level(filename=levels[self.m_selector], rnd=True)
        self.start_piece_count = len(self.tiles)             
      return
    elif self.state == 'playing':
      self.handle_tile_click(event) 
    elif self.state == 'level_complete':
      print '?'
      if event.type == pygame.MOUSEBUTTONDOWN:
        self.state = 'level_select'
      
  def render_menu(self, screen):
    "Draw the main menu"
    pass
    
  def render(self, screen):
    "Based on the games state, call the appropriate drawing methods"
    if self.state == 'menu':
      self.render_menu(screen)
      pygame.draw.rect(screen,(0,0,0), (0,0,800,80))
      pygame.draw.rect(screen,(0,0,0), (0,520,800,80))   
      render_text(screen, self.font, "Vanessa's Mahjong", (300, 120, 300, 300))
      render_text(screen, self.font, "New Game", (380, 200, 300, 300))
      render_text(screen, self.font, "High Scores", (380, 250, 300, 300))
      render_text(screen, self.font, "Settings", (380, 300, 300, 300))
      render_text(screen, self.font, "Exit Game", (380, 350, 300, 300))
      
      render_text(screen, self.font, "->", (350, 200 + self.m_selector * 50, 300, 300))
      
      return
    elif self.state == 'level_select':
      pygame.draw.rect(screen,(0,0,0), (0,0,800,80))
      pygame.draw.rect(screen,(0,0,0), (0,520,800,80))   
      render_text(screen, self.font, "Vanessa's Mahjong", (300, 120, 300, 300))
      render_text(screen, self.font, "Select a level:", (380, 200, 300, 300))
      i = 0
      for level in os.listdir(os.path.abspath('levels/')):
        level = level[:-4]
        render_text(screen, self.font, level, (410, 250 + i * 50, 300, 300))
        i += 1
      render_text(screen, self.font, "BACK", (410, 250 + i * 50, 300, 300))
      render_text(screen, self.font, "->", (370, 250 + self.m_selector * 50, 300, 300 ))
      return
    elif self.state == 'playing':
      #Bars
      pygame.draw.rect(screen,(0,0,0), (0,0,800,80))
      pygame.draw.rect(screen,(0,0,0), (0,520,800,80))      
      
      # Draw Title & Score

      if not self.editor:
        render_text(screen, self.font, "Vanessa's Mahjong", (20,20,300,300), color=(255,150,122))
        render_text(screen, self.font, "Pieces Removed: ", (20,540,200,100), color=(255,150,122))
        render_text(screen, self.font, str(self.pieces_removed) + ' of ' + str(self.start_piece_count), (300,540,200,50), color=(255,255,255))
      else:
        render_text(screen, self.font, "Level Editor", (20,20,300,300), color=(255,150,122))
        render_text(screen, self.font, "S = save, U = undo", (500,20,300,300), color=(255,150,122))
        render_text(screen, self.font, "Editing: " + self.filename, (20,520,200,100), color=(255,150,122))
        render_text(screen, self.font, "Pieces Placed: " + str(len(self.tiles)), (20,560,200,100), color=(255,255,255,))
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