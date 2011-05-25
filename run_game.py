#! /usr/bin/python

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
  player_name = 'Player'
  
  if len(sys.argv) > 2 and '--editor' in sys.argv:
    editor = True
    pygame.mouse.set_visible(False)
    i = sys.argv.index('--editor') 
        
    
  if len(sys.argv) > 2 and '--player_name' in sys.argv:
    pi = sys.argv.index('--player_name')+1
    player_name = sys.argv[pi]
    
  if '--nosound' in sys.argv:
    sound_on = False
  
  
  if editor:
    level_arg = sys.argv[i+1]
    game = Editor(sound=sound_on, filename = level_arg)
  else:
    game = Game(sound=sound_on, player_name=player_name)
  
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return

      game.handle_input(event)
     
    game.render(screen)
    pygame.display.flip()
        
    time.sleep(.001)  
  return
  
if __name__ == "__main__":
  main()
