import sys
import pygame
import time
import re
from time import localtime
import os.path
import random
from random import shuffle

from tile import *

COLOR_BLACK = (0,0,0)
COLOR_WHITE = (255,255,255)

def render_black_bars(screen):
  pygame.draw.rect(screen,(0,0,0), (0,0,800,80))
  pygame.draw.rect(screen,(0,0,0), (0,520,800,80)) 
  
def get_string_surf(font, text, color=COLOR_BLACK):
  "Used in lazy-man text-writing :)"
  return font.render(text, True, color)
  
def render_text(screen, font, text, (x,y,w,h), color=COLOR_BLACK):
  "Lazy-man text-writing."
  screen.blit(get_string_surf(font, text, color=color), (x,y,w,h))

def load_level(filename, rnd=False, enforceTwo=False):
  "Loads a level from a text file. If the random flag is set to True \
   then all tiles are simply random, otherwise use the files data. "
   
  # If the file doesn't exist, create it for posterity.
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
  def __init__(self, editor=False, sound=True, filename=None):
  
    # If true, editor is running, if not then 
    # we begin in the menu like normal.
    if editor:  
      self.state = 'playing'
      self.filename = filename
      self.tiles = load_level(filename, rnd=(not editor))
      self.start_piece_count = len(self.tiles)
    else:
      self.state = 'menu' 
      
    self.pieces_removed = 0                         # Pieces removed in current level.
    self.selected = None                            # The tile currently selected 
    self.time_started = pygame.time.get_ticks()     # When our level started
    self.m_selector = 0                             # Menu Selector
    self.sound_on = sound                           # If sound is on
    self.editor = editor                            # If the editor is running
    
    # State-based render handling
    self.render_func = { 'playing'        : self.render_playing,         \
                         'menu'           : self.render_menu,            \
                         'level_select'   : self.render_level_select,    \
                         'paused'         : self.render_paused,          \
                         'level_complete' : self.render_level_complete,  \
                         'highscores'     : self.render_highscores }
    
    # State-based input handling
    self.input_handlers = { 'playing'        : self.handle_playing_input,       \
                            'menu'           : self.handle_menu_input,          \
                            'level_select'   : self.handle_level_select_input,  \
                            'paused'         : self.handle_paused_input,        \
                            'level_complete' : self.handle_level_complete_input, \
                            'highscores'     : self.handle_highscores_input }
    # If true then play sound
    if self.sound_on:
      pygame.mixer.music.load('res/bg.mp3')
      pygame.mixer.music.play(loops=-1)
    
    self.fontpath = os.path.abspath('res/ChopinScript.otf')   # Standard font resource location
    self.font = pygame.font.Font(self.fontpath, 42)           # Loaded standard font
     
  def write_score(self):
    "Writes player score to file for the current level they just completed. "
    scorepath = os.path.abspath('levels/scores/' + self.filename)
    scores = []
    
    try:
      fh = open(scorepath, 'r')
      scores = fh.read()
      scores = re.findall('[(](\w*),(\w*)[)]', scores)
      fh.close()
    except IOError:
      print "Score file doesn't yet exist, creating..."
      
    scores.append(('player',(pygame.time.get_ticks() - self.time_started)/1000))
    if scores:
      scores = sorted(scores, key=lambda s: int(s[01]))
      
    fh = open(scorepath, 'w')
    for score in scores:
      fh.write('('+str(score[0])+','+str(score[1])+')')

    fh.close()      
          
  def handle_input(self, event):
    "Based on the games current state, manage our mouse input."
    # The editor is a special case. It's not handled by a 
    # single function, as it's slightly more complex.
    if self.editor:
      if  event.type == pygame.MOUSEBUTTONDOWN:
        self.place_tile(event)
      elif event.type == pygame.MOUSEMOTION:
        self.move_tile_cursor(event)
      elif event.type == pygame.KEYDOWN:
        self.select_cursor_tile(event)
        
      return
    
    # If our state is valid, it should have an associated input handler,
    # but as with rendering, check to be sure. :)
    if self.state in self.input_handlers:
      self.input_handlers[self.state](event)
         
  def render(self, screen):
    "Based on the games state, call the appropriate drawing methods"
    # If our state is valid, it should have an associated rendering function
    # specified, but check here just to be sure.
    if self.state in self.render_func:     
      screen.fill((255,255,255))
      self.render_func[self.state](screen)
      
    if self.editor:
      self.draw_tile_cursor(screen)  
      
  def handle_menu_input(self, event):
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_DOWN:
        if self.m_selector == 3:
          self.m_selector = 0
        else:
          self.m_selector += 1
          
      if event.key == pygame.K_UP:
        if self.m_selector == 0:
          self.m_selector = 3
        else:
          self.m_selector -= 1
        
      if event.key == pygame.K_RETURN:
        if self.m_selector == 0:
          self.state = 'level_select'
          self.m_selector = 0
          
        if self.m_selector == 3:
          sys.exit()
        
      if event.key == pygame.K_ESCAPE:
        sys.exit()
          
  def handle_playing_input(self, event):
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        if not self.editor:
          self.state = 'level_select'
        else:
          sys.exit()
        return
      
    if event.type == pygame.MOUSEBUTTONDOWN:
      # Iterate through tiles seing if we've clicked above any of them.
      # If we have, and it's deemed selectable, then select it. If we have and
      # A tile is already selected elsewhere, compare the two to see if they're a match.
      # If they're a match, then remove the tiles and add to our tiles removed tally.
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
                  
                  # If we won!
                  if len(self.tiles) == 0:
                    self.state = 'level_complete'
                    self.score = str((pygame.time.get_ticks()-self.time_started)/1000)
                    pygame.event.clear()
                    
                    self.write_score()
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
   
  def handle_level_select_input(self, event):

    #List levels (as defined by basically any file in the levels/ directory.
    levels = os.listdir(os.path.abspath('levels/'))
    max = len(levels)-1 
    
    if 'scores' in levels:
      levels.remove('scores')
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        self.state = 'menu'
        return
      elif event.key == pygame.K_UP:
        if self.m_selector == 0:
          self.m_selector = max
        else:
          self.m_selector -= 1
      elif event.key == pygame.K_DOWN:
        if self.m_selector == max:
          self.m_selector = 0
        else:
          self.m_selector += 1  
      elif event.key == pygame.K_RETURN:
      
        # True if they selected enter while BACK was highlighted.
        if self.m_selector == max:
          self.state = 'menu'
          self.m_selector = 0
          return
          
        self.state = 'playing'     
        self.time_started = pygame.time.get_ticks()
        self.pieces_removed = 0
        self.tiles = load_level(filename=levels[self.m_selector], rnd=True)
        self.filename = levels[self.m_selector]
        self.start_piece_count = len(self.tiles)        
  
  def handle_level_complete_input(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      self.state = 'level_select'
      self.selected = None
  
  def handle_paused_input(self, event):
    pass
    
  def handle_highscores_input(self, event):
    pass
  
  def render_highscores(self, screen):
    pygame.draw.rect(screen,(0,0,0), (0,0,800,80))
    pygame.draw.rect(screen,(0,0,0), (0,520,800,80))   
    render_text(screen, self.font, "Vanessa's Mahjong", (300, 120, 300, 300))
    
  def render_level_complete(self, screen):
    rose = pygame.image.load('res/rose.jpg')
    roserect = (220,120,318,350)
    screen.blit(rose,roserect)
    render_black_bars(screen)

    render_text(screen, self.font,"Click for next level...", (450,540,200,100), color=(255,150,122))
    render_text(screen, self.font,  str(self.score) + " seconds, sweet!", (20,40,200,200), color=(255,150,122))
      
  def render_playing(self,screen):

    render_black_bars(screen)
    
    # True if we're currently in the editor. Just changes the labels
    # drawn to the screen.
    if self.editor:
      render_text(screen, self.font, "Level Editor", (20,20,300,300), color=(255,150,122))
      render_text(screen, self.font, "S = save, U = undo", (500,20,300,300), color=(255,150,122))
      render_text(screen, self.font, "Editing: " + self.filename, (20,520,200,100), color=(255,150,122))
      render_text(screen, self.font, "Pieces Placed: " + str(len(self.tiles)), (20,560,200,100), color=(255,255,255,))
    else:
      render_text(screen, self.font, "Vanessa's Mahjong", (20,20,300,300), color=(255,150,122))
      render_text(screen, self.font, "Pieces Removed: ", (20,540,200,100), color=(255,150,122))
      render_text(screen, self.font, str(self.pieces_removed) + ' of ' + str(self.start_piece_count), (300,540,200,50), color=(255,255,255))
      
    # Draw all of the tiles on the map.
    for tile in self.tiles:
      tile.draw(screen)
      if self.selected: 
        pygame.draw.rect(screen, (255,0,0), (self.selected.x - self.selected.z * 3, \
                                             self.selected.y - self.selected.z * 3, 40-2, 60-2),2)

  def render_menu(self, screen):
    pygame.draw.rect(screen,(0,0,0), (0,0,800,80))
    pygame.draw.rect(screen,(0,0,0), (0,520,800,80))   
    render_text(screen, self.font, "Vanessa's Mahjong", (20,20,300,300), color=(255,150,122))
    render_text(screen, self.font, "New Game", (310, 200, 300, 300))
    render_text(screen, self.font, "High Scores", (310, 250, 300, 300))
    render_text(screen, self.font, "Settings", (310, 300, 300, 300))
    render_text(screen, self.font, "Exit Game", (310, 350, 300, 300))
    render_text(screen, self.font, "->", (280, 200 + self.m_selector * 50, 300, 300))
    
  def render_level_select(self, screen):
    render_black_bars(screen)  
    render_text(screen, self.font, "Vanessa's Mahjong", (20,20,300,300), color=(255,150,122))
    render_text(screen, self.font, "Select a level...", (20,540,200,100), color=(255,150,122))
    i = 0
    levels = os.listdir(os.path.abspath('levels/'))
    for level in levels:
      if level == 'scores':
        continue
      level = level[:-4]
      render_text(screen, self.font, level, (310, 200 + i * 50, 300, 300))
      i += 1
    render_text(screen, self.font, "BACK", (310, 100, 300, 300))
    if self.m_selector == len(levels)-1:
      render_text(screen, self.font, "->", (280, 100, 300, 300 ))
    else:
      render_text(screen, self.font, "->", (280, 200 + self.m_selector * 50, 300, 300 ))
      
  def render_paused(screen):
    pass
    