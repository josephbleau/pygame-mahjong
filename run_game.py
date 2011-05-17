import sys
import pygame
import time
import os.path

# my imports
from tile import *
from game import * 

def main():
  pygame.init()
  screen = pygame.display.set_mode((800,600))
  pygame.display.set_caption("Vanessa's Mahjong, v0.0")
  
  game = Game()
  
  while 1:
    if game.state == 'next_level':
      game = Game()
      
    screen.fill((255,255,255))
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return
      if event.type == pygame.MOUSEBUTTONDOWN:
        game.handle_input(event)
    
    game.render(screen)
    pygame.display.flip()
        
    time.sleep(.001)  
  return
  
if __name__ == "__main__":
  main()