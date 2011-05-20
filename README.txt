Vanessa's Mahjong is a Mahjong-esque game written in Python (2.7) using PyGame (latest, as of 5/17/2011).

To run the game simply point python at run_game.py or run_game.pyw.

Currently, there is support for high-scores but no way to enter your name through the interface. At the time being use --player_name [name] at the command line to specify who will be playing.

Currently, there is support for toggling music on/off but no way to do this in game. To disable music use --nosound at the command line.

To run the level editor use --editor [filename] at the command line. If the filename does not exist it will be created in levels/. 

While in the editor, you can press 's' to save and 'u' to remove your previously placed tile. Left click to place tiles. Tiles should stack pretty intuitively and will snap to a grid. Lastly, while in the editor you may use keys 1-9 to change your cursor and tile placed. Currently, this does not affect the tile in the game (which are random), but can be used to help you keep track of z-levels while in the editor.

TODO as of 5/19/2011:
	Implement a method for users to input their name in-game.
	Enable mouse-clicking of all menu elements.
	Certain parts of the interface could be more intuitive, find an acceptable way to demonstrate them.
	Design/Implement settings window
		Allow resolution changes / full-screen toggle. This is a pretty complex one as it involves a lot of re-working.
		Allow sound toggle on/off and possibly volume control.
		Enable 'download levels from web'
	Speaking of, enable level downloads from the web.