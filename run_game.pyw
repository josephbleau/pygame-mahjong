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
  game = Game()
  
  if len(sys.argv) == 3 and sys.argv[1] == '--editor':
    editor = True
    pygame.mouse.set_visible(False)
    game = Editor()
    game.filename = sys.argv[2]
    game.tiles = load_level(sys.argv[2])
   
  while 1:
    if game.state == 'next_level':
      game = Game()
      
    if game.state == 'menu' or game.state == 'level_select':
      screen.fill((255,150,122))
    if game.state == 'playing':
      screen.fill((255,150,122))
    if game.state == 'level_complete':
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
        if game.state == 'menu' or game.state == 'level_select':
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