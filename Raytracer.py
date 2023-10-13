import pygame
from pygame.locals import *
from rt import Raytracer
from figures import *
from lights import *
from materials import *

width = 256
height = 256 

pygame.init()

screen = pygame.display.set_mode((width,height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED)
screen.set_alpha(None)

raytracer = Raytracer(screen)
skyTexture = pygame.image.load("imas/hell.jpg")
raytracer.rtClearColor(0.25,0.25,0.25)

blanco = Material(diffuse=(255,255,255), spec = 10, ks = 0.02)
rojo = Material(diffuse=(255,0,0), spec = 10, ks = 0.02) 
azul = Material(diffuse=(0,0,255), spec = 10, ks = 0.02)
verde = Material(diffuse=(0,255,0), spec = 10, ks = 0.02)
celeste = Material(diffuse=(95,75,139), spec = 32, ks = 0.1)
espejo = Material(diffuse=(200,200, 200), spec =64, ks = 0.02, matType=REFLECTIVE)
cielo = Material(spec=64, ks=0.1, texture=skyTexture, matType=REFLECTIVE)
cesped = Material(diffuse=(100,225,100), spec = 46, ks = 0.05)
black = Material(diffuse=(0,0,0), spec = 46, ks = 0.05, matType=OPAQUE)
amarillo = Material(diffuse=(255,255,0), spec = 46, ks = 0.05, matType=OPAQUE)


objetos = [
  Plane(position=(0,-2,0), normal=(0,1,-0.02), material=blanco), 
  Plane(position=(0,5,0), normal=(0,1,0.2), material=amarillo),
  Plane(position=(4,0,0), normal=(1,0,0.2), material=azul), 
  Plane(position=(-4,0,0), normal=(1,0,-0.2), material=rojo),
  Plane(position=(0,2,0), normal=(0,-1,0), material=verde),
  Disk(position=(0.2,0.05,-5), normal=(0,0.05,3), radius=0.5, material=espejo),
  AABB(position=(-1,-1,-3), size=(0.5,0.5,0.5), material=amarillo),
  AABB(position=(1,-1,-3), size=(0.5,0.5,0.5), material=black),
]

luces = [
  AmbientLight(intensity=0.5, color=(1,0.8,1)),
]

for objeto in objetos:
  raytracer.scene.append(objeto)

for luz in luces:
  raytracer.lights.append(luz)
  
raytracer.rtClear()
raytracer.rtRender()

print("\nRender Time:",pygame.time.get_ticks()/1000, "secs")

isRunning = True
while isRunning:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      isRunning = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        isRunning=False
      
        
pygame.quit()