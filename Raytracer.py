import pygame
from pygame.locals import *
from rt import Raytracer
from figures import *
from lights import *
from materials import *

width = 256
height = 256

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED)
screen.set_alpha(None)

raytracer = Raytracer(screen)
raytracer.envMap = pygame.image.load("imas/enviroment.jpg")
raytracer.rtClearColor(0.25, 0.25, 0.25)


opaco = Material(diffuse=(0,0,0))
espejo = Material(diffuse=(100,235, 224), spec =64, ks = 0.02, matType=REFLECTIVE)
transparente =  Material(diffuse=(100,255, 255), spec =64, ior = 1.5, ks = 0.02, matType=TRANSPARENT)


objetos = [
    # Esfera de cristal
    Triangle(material= transparente , p0=(-0.5, -0.5, -0.5), p1=(0.5, 0.9, -0.5), p2=(0.5, 0.5, -0.5), position=(-1.5, -1, -3)),
    Triangle(material= espejo , p0=(-0.5, -0.5, -0.5), p1=(0.5, -0.5, -0.5), p2=(0.5, 0.5, -0.5), position=(0, 0, 0)),
    Triangle(material= opaco , p0=(-0.5, -0.5, -0.5), p1=(0.5, -0.5, 0.5), p2=(0.5, 0.5, -0.5), position=(-1, 1, -3)),
]

luces = [
    AmbientLight(intensity=0.5, color=(1, 0.8, 1)),
]

for objeto in objetos:
    raytracer.scene.append(objeto)

for luz in luces:
    raytracer.lights.append(luz)

raytracer.rtClear()
raytracer.rtRender()

print("\nRender Time:", pygame.time.get_ticks() / 1000, "secs")

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False


pygame.quit()
