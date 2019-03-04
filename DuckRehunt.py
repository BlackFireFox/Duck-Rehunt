"""
Copyright 2011 Michael Bachmann

This program is distributed under the terms of the GNU
General Public License
"""

import pygame, random
from datetime import datetime
pygame.init()

from DuckLib import *
#from WorldState import *



screen	 = pygame.display.set_mode((640,480))
screen_dim = screen.get_rect()

##class World():
##
##	def __init__(self):
##		self.TITLE = 1
##		self.

def main():

	pygame.display.set_caption("Duck Rehunt: Reckoning")
	pygame.mixer.init()
	pygame.mixer.Sound("Music.ogg").play(-1)

	background	 = pygame.Surface(screen.get_size())
	background.blit(pygame.image.load("Background.gif"), (0,0))
	screen.blit(background, (0,0))

	
	foreground	 = setPiece(pygame.image.load("Foreground.gif"), (0,301), 1 )
	hud			= setPiece(pygame.image.load("Hud.gif"), (22, 400), 3 )
	setSprites	 = pygame.sprite.LayeredUpdates( foreground , hud)

	dSprites.add(Dog())

	crosshair = pygame.sprite.Group(Crosshair())
						  
	keepGoing = True
	pause	 = 0
	delay	 = 60
	shotScore = 0
	global score, ducks

	time=30
	ammo=4
	nba=100

	scoreFont = pygame.font.Font("duckhunt.ttf",20)
	timeFont=pygame.font.Font("duckhunt.ttf",20)
	ammoFont=pygame.font.Font("duckhunt.ttf",20)
	scoreboard = scoreFont.render("%d" % score, 1, (255,255,255))
	timestamp=timeFont.render("%d" % time, 1, (255,255,255))
	ammoboard=timeFont.render("%d" % ammo, 1, (255,255,255))

	timel=30
	frt=datetime.now()
	clock = pygame.time.Clock()
	
	while keepGoing:

		clock.tick(60)
		time=timel-(datetime.now()-frt).seconds
		pygame.mouse.set_visible(False)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
					keepGoing = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				gunshot.play()
				ammo-=1
				flash.add(Flash())
				pointCollide = [sprite for sprite in dSprites.sprites() if sprite.rect.collidepoint(pygame.mouse.get_pos())]
				if pointCollide != []:
					for sprite in pointCollide:
						if not sprite.dog and not sprite.isDead:
							sprite.isDead = True
							sprite.pause = 0
							if sprite.enemy:
								shotScore -= 50
							else:
								frt=datetime.now()
								shotScore += 5
								ammo+=1
							sprite.setAnim()
					shotScore *= len(pointCollide)
					score += shotScore
					if score==nba:
						ammo+=1
						nba+=100
					shotScore = 0
					scoreboard = scoreFont.render("%d" % score, 1, (255,255,255))
		timestamp=timeFont.render("%d" % time, 1, (255,255,255))
		ammoboard=timeFont.render("%d" % ammo, 1, (255,255,255))

	
		#Garbage collection
		pause+= 1
		if pause >= delay:

			dSprites.remove([sprite for sprite in dSprites.sprites() if sprite.rect.centery >= 500])

		dSprites.clear(screen, background)
		crosshair.clear(screen, background)
		flash.clear(screen, background)

		dSprites.update()
		crosshair.update()
		flash.update()
		
		dSprites.draw(screen)
		setSprites.draw(screen)
		screen.blit(scoreboard, (530,410))
		screen.blit(timestamp,(290,410))
		screen.blit(ammoboard,(40,410))
		flash.draw(screen)
		crosshair.draw(screen)
		pygame.display.flip()
		if time<=0 or ammo<=0:
			pygame.draw.rect(screen,(255,255,255),(228,98,204,54))
			pygame.draw.rect(screen,(0,0,0),(230,100,200,50))
			screen.blit((pygame.font.Font("duckhunt.ttf",30)).render("GAME OVER",False,(255,255,255)),(240,100))
			pygame.display.flip()
			pygame.time.wait(1000)
			keepGoing=False

if __name__ == "__main__":
	main()

pygame.quit()