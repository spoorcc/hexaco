from Engine import GraphicsEngine
from Engine import GameEngine
from threading import Thread

import Tkinter 

root = Tkinter.Tk()

hexRadius = 30

gameEngine = GameEngine.GameEngine()
graphicsEngine = GraphicsEngine.GraphicsEngine(master=root)
graphicsEngine.hexRadius = hexRadius
gameEngine.gameObjectFactory.hexRadius = hexRadius

gameEngine.callback_for_new_object( graphicsEngine.add_component )

gameEngine.initialize_objects()

i = 0

print "Starting main game loop"
while 1:
	
	i += 1
	graphicsEngine.setTurnText( i )
	gameEngine.update()
	graphicsEngine.updateScreen()
