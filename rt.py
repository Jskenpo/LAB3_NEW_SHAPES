
from math import tan, pi, atan2, acos
import random
from materials import *
from lights import *
import Mathematics as mate
import pygame

MAX_RECURSION_DEPTH = 3

class Raytracer(object):
    def __init__(self, screen):
        self.screen = screen
        _,_, self.width, self.height = screen.get_rect() 
        
        self.scene = []
        self.lights = []
        
        self.camPosition = [0,0,0]
        
        self.rtViewport(0, 0, self.width, self.height)
        self.rtProyection()
        
        self.rtClearColor(0,0,0)
        self.rtColor(1,1,1)
        self.rtClear()
        
        self.envMap = None
        
    
    def rtViewport(self,posX, posY, width, height):
        self.vpX = posX
        self.vpY = posY
        self.vpWidth = width
        self.vpHeight = height
    
    def rtProyection(self,fov=60,n=0.1):
        aspectRatio = self.vpWidth/self.vpHeight
        self.nearPlane = n
        self.topEdge = tan((fov*pi/180)/2)*self.nearPlane
        self.rightEdge = self.topEdge * aspectRatio
       
    def rtClearColor(self, r, g, b):
        self.clearColor = (r*255,g*255,b*255)
    
    def rtClear(self):
        self.screen.fill((self.clearColor))
    
    def rtColor(self,r,g,b):
        self.currentColor = (r*255,g*255,b*255)
    
    def rtPoint(self,x,y,color = None):
        y = self.height - y
        
        if (0<=x<self.width) and (0<=y<self.height):
            if color != None:
                color = (int(color[0]*255),
                         int(color[1]*255),
                         int(color[2]*255))
                
                self.screen.set_at((x,y), color)
            else:
                self.screen.set_at((x,y), self.currentColor)
    
    def rtCastRay(self,orig,dire,sceneObj = None, recursion = 0):
        if recursion >= MAX_RECURSION_DEPTH:
            return None
       
        depth = float('inf')
        intercept = None
        hit = None
        
        for obj in self.scene:
            if sceneObj != obj:
                intercept = obj.ray_intersect(orig, dire)
                if intercept != None:
                    if intercept.distance < depth:
                        hit = intercept
                        depth = intercept.distance
        return hit
    
    def rtRayColor(self, intercept, rayDirection, recursion = 0):
        if intercept == None:
            if self.envMap:
                x = (atan2(rayDirection[2], rayDirection[0]) / (2*pi) + 0.5) * self.envMap.get_width()
                y = acos(rayDirection[1]) / pi * self.envMap.get_height()
                
                envColor = self.envMap.get_at((int(x), int(y)))
                return [envColor[i] / 255 for i in range(3)]
            else:
                return None
        
        
        
            #Phong Reflection Model
            #LightColor = AmbientIntensity + DiffuseIntensity + SpecularIntensity
            #FinalColor = SurfaceColor * LightColor
            
        material = intercept.obj.material
        surfaceColor = material.diffuse
        if material.texture and intercept.texcoords:
            #intercept.texcoords = (min(1, intercept.texcoords[0]), min(1, intercept.texcoords[1]))   
            tX = intercept.texcoords[0] * material.texture.get_width() - 1
            tY = intercept.texcoords[1] * material.texture.get_height() - 1
            texColor = material.texture.get_at((int(tX), int(tY)))
            texColor = [i / 255 for i in texColor]
            surfaceColor = [surfaceColor[i] * texColor[i] for i in range(3)]
            
        
        finalColor = [0,0,0]
        ambientColor = [0,0,0]
        diffuseColor = [0,0,0]
        specularColor = [0,0,0]
        reflectColor = [0,0,0]
        refractColor = [0,0,0]
        
        if material.matType == OPAQUE:
            
            
            for light in self.lights:
                if light.lightType == "Ambient":
                    ambientColor = [(ambientColor[i]+light.getLightColor()[i]) for i in range(3)]
                
                else:
                    lightDir = None
                    if light.lightType == "Directional":
                        lightDir = [(i*-1) for i in light.direction]
                    elif light.lightType == "Point":
                        lightDir = mate.sub(light.point, intercept.point)
                        lightDir = mate.divTF(lightDir, mate.norm(lightDir))
                        
                    shadowIntersect = self.rtCastRay(intercept.point, lightDir, intercept.obj)
                    
                    if shadowIntersect==None:
                        diffuseColor = [(diffuseColor[i]+light.getDiffuseColor(intercept)[i]) for i in range(3)]
                        specularColor = [(specularColor[i]+light.getSpecularColor(intercept, self.camPosition)[i]) for i in range(3)]
            
        elif material.matType == REFLECTIVE:
            reflect = reflectVector(intercept.normal, mate.multiply(-1, rayDirection))
            reflectIntercept = self.rtCastRay(orig=intercept.point, dire=reflect, sceneObj=intercept.obj, recursion=recursion + 1)
            reflectColor = self.rtRayColor(intercept=reflectIntercept, rayDirection=reflect, recursion=recursion + 1)
            
            for light in self.lights:
                if light.lightType != "Ambient":
                    lightDir = None
                    if light.lightType == "Directional":
                        lightDir = [(i*-1) for i in light.direction]
                    elif light.lightType == "Point":
                        lightDir = mate.sub(light.point, intercept.point)
                        lightDir = mate.divTF(lightDir, mate.norm(lightDir))
                        
                    shadowIntersect = self.rtCastRay(orig=intercept.point, dire=lightDir, sceneObj=intercept.obj)
                    
                    if shadowIntersect==None:
                        specularColor = [(specularColor[i]+light.getSpecularColor(intercept, self.camPosition)[i]) for i in range(3)]
                        
        elif material.matType == TRANSPARENT:
            isOutside = mate.dot_product(rayDirection, intercept.normal) < 0
            factor = 0.001
            bias = [elemento * factor for elemento in intercept.normal]
            
            factor = -1
            negativeRayDirection = [elemento * factor for elemento in rayDirection]
            reflectRay = reflectVector(intercept.normal, negativeRayDirection)
            reflectOrigin = mate.add(intercept.point, bias) if isOutside else mate.sub(intercept.point, bias)
            reflectIntercept = self.rtCastRay(reflectOrigin, reflectRay, None, recursion + 1)
            reflectColor = self.rtRayColor(reflectIntercept, reflectRay, recursion + 1)

            for light in self.lights:
                if light.lightType != "Ambient":
                    shadowDirection = None
                    if light.lightType == "Directional":
                        shadowDirection = [i * -1 for i in light.direction]
                    if light.lightType == "Point":
                        lightDirection = mate.sub(light.point, intercept.point)
                        shadowDirection = mate.divTF(lightDirection, mate.norm(lightDirection))
                        
                    shadowIntersect = self.rtCastRay(intercept.point, shadowDirection, intercept.obj)

                    if shadowIntersect is None:
                        specColor = light.getSpecularColor(intercept, self.camPosition)
                        specularColor = [specularColor[i] + specColor[i] for i in range(3)]

            if not totalInternalReflection(intercept.normal, rayDirection, 1.0, intercept.obj.material.ior):
                refractRay = refractVector(intercept.normal, rayDirection, 1.0, intercept.obj.material.ior)
                refractOrigin = mate.sub(intercept.point, bias) if isOutside else mate.add(intercept.point, bias)
                refractIntercept = self.rtCastRay(refractOrigin, refractRay, None, recursion + 1)
                refractColor = self.rtRayColor(refractIntercept, refractRay, recursion + 1)

                kr, kt = fresnel(intercept.normal, rayDirection, 1.0, intercept.obj.material.ior)
                reflectColor = mate.multiply(kr, reflectColor)
                refractColor = mate.multiply(kt, refractColor)               

            
        lightColor = [(ambientColor[i]+diffuseColor[i]+specularColor[i] + reflectColor[i] + refractColor[i]) for i in range(3)]  
        finalColor = [min(1,surfaceColor[i]*lightColor[i])for i in range(3)]
        return finalColor     
            
    
    def rtRender(self):
        indexes = [(i, j) for i in range(self.vpWidth) for j in range(self.vpHeight)]
        random.shuffle(indexes)
        for i, j in indexes:
            x = i + self.vpX
            y = j + self.vpY
            if (0<=x<self.width) and (0<=y<self.height):
                pX = ((x+0.5-self.vpX)/self.vpWidth)*2-1
                pY = ((y+0.5-self.vpY)/self.vpHeight)*2-1
                
                pX*=self.rightEdge
                pY*=self.topEdge
                
                direction = (pX,pY,-self.nearPlane)
                direction = mate.divTF(direction, mate.norm(direction))
                
                intercept = self.rtCastRay(self.camPosition, direction)
                rayColor = self.rtRayColor(intercept, direction)
                
                if rayColor != None:   
                    self.rtPoint(x,y,rayColor)
                    pygame.display.flip() 
                    