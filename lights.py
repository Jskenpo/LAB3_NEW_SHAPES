
import Mathematics as mate
from math import acos, asin

def reflectVector(normal, direction):
    reflect = 2*mate.dot_product(normal, direction)
    reflect = mate.multiply(reflect, normal)
    reflect = mate.sub(reflect, direction)
    reflect = mate.divTF(reflect , mate.norm(reflect))
    
    return reflect

def totalInternalReflection(incident, normal, n1, n2):
    c1 = mate.dot_product(normal, incident)
    if c1 < 0:
        c1 = -c1
    else:
        normal = mate.multiply(-1, normal)
        n1, n2 = n2, n1
        
    if n1 < n2:
        return False
    
    theta1 = acos(c1)
    
    thetaC = asin(n2/n1)
    return theta1 >+ thetaC
    
def fresnel(normal, incident, n1, n2):
    c1 = mate.dot_product(normal, incident)

    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1

    s2 = (n1 * (1 - c1 ** 2) ** 0.5) / n2
    c2 = (1 - s2 ** 2) ** 0.5

    f1 = ((n2 * c1 - n1 * c2) / (n2 * c1 + n1 * c2)) ** 2
    f2 = ((n1 * c2 - n2 * c1) / (n1 * c2 + n2 * c1)) ** 2

    kr = (f1 + f2) / 2
    kt = 1 - kr

    return kr, kt

def refractVector(incident, normal ,n1, n2):
    c1 = mate.dot_product(normal, incident)
    if c1 < 0:
        c1 = -c1
    else:
        normal = mate.multiply(-1, normal)
        n1, n2 = n2, n1
    
    n = n1 / n2
    
    T = mate.add(mate.multiply(n, incident), normal)
    T = mate.multiply((n * c1 - (1 - n**2 * (1 - c1**2 )) ** 0.5), T)
    T = mate.divTF(T, mate.norm(T))
    
    return T

class Light(object):
    def __init__(self, intensity = 1, color = (1,1,1), lightType = "None"):
        self.intensity = intensity
        self.color = color
        self.lightType = lightType
    
    def getLightColor(self):
        return [self.color[0]*self.intensity,
                self.color[1]*self.intensity,
                self.color[2]*self.intensity]
    
    def getDiffuseColor(self, intercept):
        return None
    
    def getSpecularColor(self, intercept, viewPos):
        return None
    

class AmbientLight(Light):
    def __init__(self, intensity = 1, color = (1,0,0)):
        super().__init__(intensity,color,"Ambient")

class DirectionalLight(Light):
    def __init__(self, direction = (0,-1,0), intensity = 1, color = (1,1,1)):
        self.direction = mate.divTF(direction, mate.norm(direction))
        super().__init__(intensity,color,"Directional")
    
    def getDiffuseColor(self, intercept):
        
        dir =[(i*-1) for i in self.direction]
        
        intensity = mate.dot_product(intercept.normal, dir) * self.intensity
        intensity = max(0, min(1, intensity))
        intensity *= 1 - intercept.obj.material.ks
        
        diffuseColor = [(i*intensity) for i in self.color]
        
        return diffuseColor
    
    def getSpecularColor(self, intercept, viewPos):
        dir =[(i*-1) for i in self.direction]
        reflect = reflectVector(intercept.normal, dir)
        
        viewDir = mate.sub(viewPos,intercept.point)
        viewDir = mate.divTF(viewDir, mate.norm(viewDir))
                
        #Cambia dependiendo de la superficie
        specIntensity = max(0, mate.dot_product(viewDir, reflect))** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.ks
        specIntensity *= self.intensity
        
        specColor = [(i*specIntensity) for i in self.color]
        
        return specColor

class PointLight(Light):
    def __init__(self, point = (0,0,0), intensity = 1, color = (1,1,1)):
        self.point = point
        super().__init__(intensity, color, "Point")
        
    def getDiffuseColor(self, intercept):
        dir = mate.sub(self.point, intercept.point)
        R = mate.norm(dir)
        dir = mate.divTF(dir, R)
        
        intensity = mate.dot_product(intercept.normal, dir) * self.intensity
        intensity *= 1 - intercept.obj.material.ks
        
        #Ley de cuadrados inversos
        #If = intensity/R**2
        #R: distancia del punto intercepto a la luz punto.
        
        if R!=0:
            intensity /= R**2
        intensity = max(0, min(1, intensity))

        
        diffuseColor = [(i*intensity) for i in self.color]
        
        return diffuseColor
    
    def getSpecularColor(self, intercept, viewPos):
        dir = mate.sub(self.point, intercept.point)
        R = mate.norm(dir)
        dir = mate.divTF(dir, R)
        
        reflect = reflectVector(intercept.normal, dir)
        
        viewDir = mate.sub(viewPos,intercept.point)
        viewDir = mate.divTF(viewDir, mate.norm(viewDir))
        
        #Cambia dependiendo de la superficie
        specIntensity = max(0, mate.dot_product(viewDir, reflect))** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.ks
        specIntensity *= self.intensity
        
        if R!=0:
            specIntensity /= R**2
            
        specIntensity = max(0, min(1, specIntensity))
        
        specColor = [(i*specIntensity) for i in self.color]
        
        return specColor
        
        