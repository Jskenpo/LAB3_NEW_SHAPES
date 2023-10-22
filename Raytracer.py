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
star_texture = Material(diffuse=(255,255,0), spec=64, ks=0.02, matType=OPAQUE)
Red_carpet = Material (diffuse=(255,0,0), spec =64, ks = 0.02, matType=OPAQUE)
cube_stand = Material(texture=pygame.image.load("imas/cube.png"), spec=64, ks=0.02, matType=OPAQUE)
sun = Material(texture=pygame.image.load("imas/sun.jpg"), spec=64, ks=0.02, matType=OPAQUE)
earth = Material(texture=pygame.image.load("imas/earth.png"), spec=64, ks=0.02, matType=OPAQUE)
mars = Material(texture=pygame.image.load("imas/mars.jpg"), spec=64, ks=0.02, matType=OPAQUE)
mercury = Material(texture=pygame.image.load("imas/mercury.jpg"), spec=64, ks=0.02, matType=OPAQUE)
venus = Material(texture=pygame.image.load("imas/venus.jpg"), spec=64, ks=0.02, matType=OPAQUE)


objetos = [
    # 3 esferas en corma de circulo
    Sphere(material=sun, position=(0, 2.5, -7), radius=0.6),
    Sphere(material=earth, position=(-2, 1, -7), radius=0.6),
    Sphere(material=mars, position=(2, 1, -7), radius=0.6),
    Sphere(material=espejo, position=(0, -3, -7), radius=0.6),
    Sphere(material=mercury, position=(-2, -1, -7), radius=0.6),
    Sphere(material=venus, position=(2, -1, -7), radius=0.6),

    # Plano debajo de esferas en forma de alfombra roja
    Plane(material=Red_carpet, position=(0, -3, -7), normal=(0, 5, 0.3), size=(4, 2)),

    #cubo centro de escena
    AABB(material=cube_stand, position=(0, -1, -7), size=(1, 1, 1)),

    #octaedro encima de cubo
    Star(material=star_texture, position=(0, 1.2, -11)),

    #triangulo en cada arista de octaedro
    Triangle(material=star_texture, position=(0, 1.2, 0), p0=(-0.5, 1.2, -11), p1=(0, 1.7, -11), p2=(0.5, 1.2, -11)),
    Triangle(material=star_texture, position=(0, 1.2, 0), p0= (-0.5, -1.2, -11), p1=(0, -1.7, -11), p2=(0.5, -1.2, -11)),
    Triangle(material=star_texture, position=(0, 1.2, 0), p0=(-0.5, 1.2, -11), p1=(-0.5, -1.2, -11), p2=(0, -1.7, -11)),
    Triangle(material=star_texture, position=(0, 1.2, 0), p0=(0.5, 1.2, -11), p1=(0.5, -1.2, -11), p2=(0, -1.7, -11)),

    #triangulo en cada esquina de la escena (transparente)
    Triangle(material= espejo , p0=(-0.5, -0.5, -0.5), p1=(0.5, -0.5, -0.5), p2=(0.5, 0.5, -0.5), position=(2.8, -2.8, -5)),
    Triangle(material= espejo , p0=(0.5, 0.5, 0.5), p1=(-0.5, 0.5, 0.5), p2=(-0.5, -0.5, 0.5), position=(-2.5, 2.1, -5)),

]

luces = [
    AmbientLight(intensity=0.5, color=(1, 0.8, 1)),
    DirectionalLight(direction=(0, 1, 0), intensity=0.5),
    PointLight(intensity=0.5, color=(1, 1, 1)),

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
