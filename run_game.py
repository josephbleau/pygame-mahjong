import argparse
import sys
import pygame
import time
import os.path

# my imports
from tile import *
from game import * 
from editor import *
    
def main():
  pygame.init()
  screen = pygame.display.set_mode((800,600))
  pygame.display.set_caption("Vanessa's Mahjong, v0.0")
  
  editor = False
  sound_on  = True
  
  if len(sys.argv) > 2 and '--editor' in sys.argv:
    editor = True
    pygame.mouse.set_visible(False)

    i = sys.argv.index('--editor') 
  if '--nosound' in sys.argv:
    sound_on = False
  
  if editor:
    level_arg = sys.argv[i+1]
    game = Editor(sound=sound_on, filename = level_arg)
  else:
    game = Game(sound=sound_on)
  
  while 1:
    screen.fill((255,255,255))
      
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return
      if event.type == pygame.MOUSEBUTTONDOWN:
        if editor:
          game.place_tile(event)
        else:
          game.handle_input(event)
      if event.type == pygame.MOUSEMOTION:
        if editor:
          game.move_tile_cursor(event)
      if event.type == pygame.KEYDOWN:
        game.handle_input(event)
        if editor:
          game.select_cursor_tile(event)
     
    game.render(screen)
  
    if editor:
      game.draw_tile_cursor(screen)  
      
    pygame.display.flip()
        
    time.sleep(.001)  
  return
  
if __name__ == "__main__":
  main()