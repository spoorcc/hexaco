from Engine import GraphicsEngine
from Engine import GameEngine
from Engine import GameObjectFactory

import Tkinter 

root = Tkinter.Tk()

gameFact = GameObjectFactory.GameObjectFactory(None)
gameEngine = GameEngine.GameEngine()
graphicsEngine = GraphicsEngine.GraphicsEngine(master=root)

i = 0

graphicsEngine.add_component( gameFact.create_tile() )

print "Starting main game loop"
while 1:
	
	i += 1
	graphicsEngine.setTurnText( i )
	gameEngine.update()
	graphicsEngine.updateScreen()
