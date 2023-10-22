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
    # 3 esferas en corma de circulo
    Sphere(material=espejo, position=(0, 1.5, -6), radius=0.6),
    Sphere(material=espejo, position=(-2, 1, -6), radius=0.6),
    Sphere(material=espejo, position=(2, 1, -6), radius=0.6),

    # Estrella encima de cada esfera
    Star(material=espejo, position=(0, 2.5, -8)),
    Star(material=espejo, position=(-2, 2, -8)),
    Star(material=espejo, position=(2, 2, -8)),



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
