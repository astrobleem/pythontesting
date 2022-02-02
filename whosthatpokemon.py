#chadpokemon
#speaking pokedex test change

#imports
import pokepy
import pygame
from pygame.locals import *
import inspect

import os.path
import os
import io
from pygame.version import ver
import requests
from urllib.request import urlopen
import random
from collections import Counter
import json
import requests
from requests.models import RequestEncodingMixin
from time import sleep
from os import system, name
import cv2
import pyttsx3


#constants



#variables
whichone = random.randrange(1,200)

#initalization stuff
engine = pyttsx3.init()
client = pokepy.V2Client()



#load pokemon class object
#get_pokemon
#get_move
#get_sprite
#get_ability
#get_game
#get_type
#get_egg

#create sprite url list object from api
mypokemon = client.get_pokemon(whichone)
abilities = client.get_ability(whichone)
species = client.get_pokemon_species(whichone)

sprites = mypokemon[0].sprites
image_str = urlopen(sprites.back_default).read()
image_file = io.BytesIO(image_str)

#load into pygame probably needs to be transformed to a fraction of the size of the screen
imageback = pygame.image.load(image_file)

image_str = urlopen(sprites.front_default).read()
image_file = io.BytesIO(image_str)
imagefront = pygame.image.load(image_file)


#copy image onto our surface upper left hand corner, will need to
# work out where it belongs based on p1 or p2 and if need to flip or not
#screen.blit(image, (0,0))


class Quadrants():
    def __init__(self,x,y):
        self.x, self.y = pygame.display.get_window_size()
        self.xr = self.x - (self.x / 4)
        self.xl = self.x / 4
        self.xh = self.x / 2
        self.yl =  self.y - (self.y / 4)
        self.yu = self.y / 4
        self.yh = self.y / 2
        self.lastx, self.lasty = screen_width, screen_height

    def recalc(self):
        self.lastx, self.lasty = self.x, self.y
        self.x, self.y = pygame.display.get_window_size()
        self.xr = self.x - (self.x / 4)
        self.xl = self.x / 4
        self.xh = self.x / 2
        self.yl =  self.y - (self.y / 4)
        self.yu = self.y / 4
        self.yh = self.y / 2


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def get_caller_info():
  # first get the full filename (including path and file extension)
  caller_frame = inspect.stack()[1]
  caller_filename_full = caller_frame.filename

  # now get rid of the directory (via basename)
  # then split filename and extension (via splitext)
  caller_filename_only = os.path.splitext(os.path.basename(caller_filename_full))[0]

  # return both filename versions as tuple
  return caller_filename_full, caller_filename_only


pygame.init()
filename,title = get_caller_info()
title = "Who's that Pokemon?"
clock = pygame.time.Clock()
fps = 30

#half the screen size minus a 5th of the screen size is the appropriate center for a window that is a third of the screen.
x = ((pygame.display.Info().current_w /2 ) - (pygame.display.Info().current_w /5))
y = ((pygame.display.Info().current_h /2 ) - (pygame.display.Info().current_h /5))
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
x = int((pygame.display.Info().current_w/3))
y = int((pygame.display.Info().current_h/3))
screen = pygame.display.set_mode((x,y), RESIZABLE)
pygame.display.set_caption(title)


# Count the joysticks the computer has
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    # No joysticks!
    print("Error, I didn't find any joysticks.")
    joysticks = None
else:
    # Use joystick #0 and initialize it
    my_joystick = pygame.joystick.Joystick(0)
    my_joystick.init()




#specials
#for i in range(0,10):
#    print(mypokemon[0].moves[i].move.name)
moves = mypokemon[0].moves
#print(Counter(moves))


def alphabinarization(abcopy):
    white = (255, 255, 255)
    black = (0, 0, 0)
    abcopy = abcopy.convert_alpha()
    blackcolormask = (0,0,0,1)
    whitecolormask = (255,255,255,1)
    transparentmask = (255,255,255,0)
    abwidth, abheight = abcopy.get_size()
    print("about to convert an image" + str((abwidth, abheight)))
    abpixelx = 0
    abpixely = 0

    for abpixelx in range(abwidth):
        for abpixely in range(abheight):
            
            #                                     0,1,2,3
            #if it's transparent, leave it alone (x,x,x,0)
            #if it's not transparent, make it black (0,0,0,1)
            whatshere = abcopy.get_at((abpixelx, abpixely))
            
            if whatshere[3] >= 0.1:
                #"changing other colored pixels to black"
                abcopy.set_at((abpixelx,abpixely),(0,0,0,255))
                
                
    
    #screen.blit(pygame.transform.scale(mypic, screen.get_size()), (0, 0))
    return abcopy 
            

class Pokemon():
    def __init__(self,name,kind,height,weight,speed,maxhp,attack,defense,spattack,spdefense,moves,abilities,spriteurls):
        #const
        self.x = 0
        self.y = 0
        self.scale = 6
        self.xp = 0
        self.level = 1
        self.potions = 3
        self.front = 0 #picture object
        self.back = 0 #picture object holder probably shouldnt be int, or does it matter? 

        #passed in
        self.name = name
        self.kind = kind
        
        self.height = height
        self.weight = weight
        self.speed = speed
        self.maxhp = maxhp       
        self.attack = attack
        self.defense = defense
        
        self.spattack = spattack
        self.spdefense = spdefense

        #object with list of moves in it
        self.moves = moves

        #object with sprite urls in it
        self.spriteurls = spriteurls

        self.abilites = abilities

        #transformed
        self.gender = 'male' #random?
        self.hp = self.maxhp
        self.maxpotions = self.potions

        self.imagefront = pygame.image.load(io.BytesIO(urlopen(spriteurls.front_default).read())).convert_alpha()
        self.imageback = pygame.image.load(io.BytesIO(urlopen(spriteurls.back_default).read())).convert_alpha()


    

    def getImages(self):
        self.imagefront = pygame.image.load(io.BytesIO(urlopen(self.spriteurls.front_default).read())).convert_alpha()
        self.imageback = pygame.image.load(io.BytesIO(urlopen(self.spriteurls.back_default).read())).convert_alpha()
        #this function will get the images
        #image_str = urlopen(self.spriteurls.back_default).read()
        #image_file = io.BytesIO(image_str)
        #load into pygame probably needs to be transformed to a fraction of the size of the screen
        #self.imageback = pygame.image.load(image_file)

        #image_str = urlopen(self.spriteurls.front_default).read()
        #image_file = io.BytesIO(image_str)
        #self.imagefront = pygame.image.load(image_file)
        #return imagefront
        #front = imagefront
        #back = imageback


    def fightMove(self):
        pass

    def printStats(self):
        clear()
        print(mypokemon[0].name + " the " + mypokemon[0].types[0].type.name + " type Pokemon.")
        print("height: " + str(mypokemon[0].height) + "in")
        print("weight:" + str(mypokemon[0].weight) + "lbs")
        print("*****")
        #hp
        print(mypokemon[0].stats[0].stat.name + " : " + str(mypokemon[0].stats[0].base_stat))
        #attack
        print(mypokemon[0].stats[1].stat.name + " : " + str(mypokemon[0].stats[1].base_stat))
        #defense
        print(mypokemon[0].stats[2].stat.name  + " : " + str(mypokemon[0].stats[2].base_stat))
        #special-attack
        print(mypokemon[0].stats[3].stat.name  + " : " + str(mypokemon[0].stats[3].base_stat))
        #special-defense
        print(mypokemon[0].stats[4].stat.name  + " : " + str(mypokemon[0].stats[4].base_stat))
        #speed
        print(mypokemon[0].stats[5].stat.name  + " : " + str(mypokemon[0].stats[5].base_stat))
        print("..")
        
        flavortexts = species[0].flavor_text_entries
        #sayit = mypokemon[0].name + " the " + mypokemon[0].types[0].type.name + " type Pokemon."
        running = True
        while running:
            which = random.randrange(len(flavortexts))
            #print(which)
            if flavortexts[which].language.name =='en':
                print (str(flavortexts[which].flavor_text.strip()))
                #sayit = str(flavortexts[which].flavor_text)
                running = False

        #for thestat in mypokemon[0].stats: 
        #    print(thestat.stat.name)
            
    def speakFlavor(self):
        flavortexts = species[0].flavor_text_entries
        #sayit = mypokemon[0].name + " the " + mypokemon[0].types[0].type.name + " type Pokemon."
        running = True
        while running:
            which = random.randrange(len(flavortexts))
            #print(which)
            if flavortexts[which].language.name =='en':
                sayit = str(flavortexts[which].flavor_text.strip().replace('/f','').replace('\n','').replace('.',' ').replace(',',' , ').replace('  ',' '))
                #sayit = str(flavortexts[which].flavor_text)
                running = False

        engine.say(sayit)
        engine.runAndWait()
       

    def listMoves(self):
        for fightmoves in self.moves:
            print(fightmoves)


        #specials
        #for i in range(0,10):
        #print(mypokemon[0].moves[i].move.name)
        #moves = mypokemon[0].moves
        #print(Counter(moves))
        pass


        
        


#requires name,kind,height,weight,speed,maxhp,attack,defense,spattack,spdefense,spriteurls
#armor class and character traits
#good or evil
#benefit or negative character trait
#resistance to poision
#3 positions for character traits
#one pos == nightvision, (more moves per turn hastening),
#one neg == colorblind  [also not cancel out]
#one from either list neg or pos [can not have already been using]
otherpokemon = Pokemon(
mypokemon[0].name, #name
mypokemon[0].types[0].type.name, #type
mypokemon[0].height, #height
mypokemon[0].weight, #weight,
mypokemon[0].stats[5].base_stat, #speed,
mypokemon[0].stats[0].base_stat, #maxhp,
mypokemon[0].stats[1].base_stat,#attack,
mypokemon[0].stats[2].base_stat,#defense,
mypokemon[0].stats[3].stat.name,#spattack,
mypokemon[0].stats[4].stat.name,#spdefense,
mypokemon[0].moves,
abilities,
mypokemon[0].sprites#spriteurls
)
print("the object:")
print(otherpokemon.name)
#print(otherpokemon.hp)

#otherpokemon.printStats()
#otherpokemon.listMoves()

#set icon 
pygame.display.set_icon(imagefront)

print("converting....")
pic = alphabinarization(imagefront)
screen.fill((255, 255, 255))
screen.blit(pygame.transform.scale(pic, screen.get_size()), (0, 0))
pygame.display.update()


whosthatpokemonsound = pygame.mixer.music.load("whoisthat.wav")
itssound = pygame.mixer.Sound('its.wav')

pygame.mixer.music.play()

#main loop
running = True
while running:
    
    #pygame.display.update()
    clock.tick(fps)
    
    pygame.event.pump()
    event = pygame.event.wait()
    if event.type == QUIT:
        running = False
    elif event.type == VIDEORESIZE:
        screen.blit(pygame.transform.scale(pic, event.dict['size']), (0, 0))
        newsize = screen.get_size()
        print(newsize)
        screen_width,screen_height = pygame.display.get_window_size()
        cardinals = Quadrants(screen_width,screen_height)
        pygame.display.update()
    elif event.type == VIDEOEXPOSE:  # handles window minimising/maximising
        screen.fill((255, 255, 255))
        screen.blit(pygame.transform.scale(pic, screen.get_size()), (0, 0))
        screen_width,screen_height = pygame.display.get_window_size()
        cardinals = Quadrants(screen_width,screen_height)
        pygame.display.update()
    if event.type == pygame.KEYDOWN:
        pass
    if event.type == pygame.KEYUP
        pass

    if event.type == pygame.JOYBUTTONDOWN:
        print("Joystick button pressed.")
        whichone = pygame.joystick.Joystick(0).get_button
        if whichone(0):
            print("button 0")
            pygame.display.update()
            
        if whichone(1):
            pic = otherpokemon.imagefront
            screen.fill((255, 255, 255))
            screen.blit(pygame.transform.scale(pic, screen.get_size()), (0, 0))
            pygame.display.update()
            #pass #print("button 1")
            
        if whichone(2):
            print(otherpokemon.name)
            #pickone = random.randrange(1,200)
            #load pokemon object
            #mypokemon = client.get_pokemon(pickone)
            #abilities = client.get_ability(pickone)
            #otherpokemon = Pokemon(mypokemon[0].name,mypokemon[0].types[0].type.name,mypokemon[0].height,mypokemon[0].weight,mypokemon[0].stats[5].base_stat,mypokemon[0].stats[0].base_stat,mypokemon[0].stats[1].base_stat,mypokemon[0].stats[2].base_stat,mypokemon[0].stats[3].stat.name,mypokemon[0].stats[4].stat.name,mypokemon[0].moves,abilities,mypokemon[0].sprites)
            #otherpokemon.getImages()
            #pic = otherpokemon.imagefront
            #screen.fill((255, 255, 255))
            #screen.blit(pygame.transform.scale(pic, screen.get_size()), (0, 0))
            
            #pic = alphabinarization(imagefront)
            #screen.fill((255, 255, 255))
            #screen.blit(pygame.transform.scale(pic, screen.get_size()), (0, 0))
            
            #pygame.display.update()
            #print("button 2")
            #print(otherpokemon.name)
            #new pokemon loaded u need to mask him again

        if whichone(3):
            pass #print("button 3")
        imagefront = otherpokemon.imagefront
        pic = imagefront
        screen.blit(pygame.transform.scale(pic, screen.get_size()), (0, 0))
        itssound.play()
        sleep(1)
        pygame.display.update()
        sayit = mypokemon[0].name + " ... " + mypokemon[0].name + " the " + mypokemon[0].types[0].type.name + " type Pokemon."
        engine.say(sayit)
        engine.runAndWait()
        sleep(1)
        
        otherpokemon.speakFlavor()
        
        otherpokemon.printStats()

            


    if event.type == pygame.JOYBUTTONUP:
        whichone = pygame.joystick.Joystick(0).get_button
        #print("Joystick button released.")
        if whichone(0):
            pass 
        if whichone(1):
            pass 
        if whichone(2):
            pass 
        if whichone(3):
            pass 

    if joystick_count != 0: 
        # This gets the position of the axis on the game controller
        # It returns a number between -1.0 and +1.0
        horiz_axis_pos = my_joystick.get_axis(0)
        vert_axis_pos = my_joystick.get_axis(1)
        
        if horiz_axis_pos < -0.08:
            pass #print (horiz_axis_pos, vert_axis_pos)
            print ("left") # decrement pokemon
        
        if horiz_axis_pos > 0.09:
            pass #print (horiz_axis_pos, vert_axis_pos)
            print ("right") #increment pokemon

        

    
    pygame.display.update()
