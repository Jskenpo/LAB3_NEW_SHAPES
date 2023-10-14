import Mathematics as mate
from math import tan, pi, atan2, acos, sqrt


class Intercept(object):
    def __init__(self, distance, point, normal, texcoords, obj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texcoords = texcoords
        self.obj = obj


class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.material = material

    def ray_intersect(self, orig, dir):
        return None


class Sphere(Shape):
    def __init__(self, position, radius, material):
        self.radius = radius
        super().__init__(position, material)

    def ray_intersect(self, orig, direction):
        l = mate.sub(self.position, orig)
        lengthL = mate.norm(l)
        tca = mate.dot_product(l, direction)

        d = (lengthL ** 2 - tca ** 2) ** 0.5
        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        p = mate.add(orig, mate.multiply(t0, direction))
        normal = mate.sub(p, self.position)
        normal = mate.divTF(normal, mate.norm(normal))

        u = atan2(normal[2], normal[0]) / (2 * pi) + 0.5
        v = acos(normal[1]) / pi

        return Intercept(distance=t0,
                         point=p,
                         normal=normal,
                         texcoords=(u, v),
                         obj=self)


class Plane(Shape):
    def __init__(self, position, normal, material):
        self.normal = mate.divTF(normal, mate.norm(normal))
        super().__init__(position, material)

    def ray_intersect(self, orig, dir):
        denom = mate.dot_product(dir, self.normal)

        if abs(denom) <= 0.0001:
            return None

        num = mate.dot_product(mate.sub(self.position, orig), self.normal)
        t = num / denom

        if t < 0:
            return None

        P = mate.add(orig, mate.multiply(t, dir))

        return Intercept(distance=t,
                         point=P,
                         normal=self.normal,
                         texcoords=None,
                         obj=self)


class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        self.radius = radius
        super().__init__(position, normal, material)

    def ray_intersect(self, orig, dir):
        planeIntersect = super().ray_intersect(orig, dir)

        if planeIntersect is None:
            return None

        contactDist = mate.sub(planeIntersect.point, self.position)

        contactDist = mate.norm(contactDist)

        if contactDist > self.radius:
            return None

        return Intercept(distance=planeIntersect.distance,
                         point=planeIntersect.point,
                         normal=self.normal,
                         texcoords=None,
                         obj=self)


class AABB(Shape):
    def __init__(self, position, size, material):
        self.size = size
        super().__init__(position, material)

        self.planes = [Plane(mate.add(self.position, (-size[0] / 2, 0, 0)), (-1, 0, 0), material),
                       Plane(mate.add(self.position, (size[0] / 2, 0, 0)), (1, 0, 0), material),
                       Plane(mate.add(self.position, (0, -size[1] / 2, 0)), (0, -1, 0), material),
                       Plane(mate.add(self.position, (0, size[1] / 2, 0)), (0, 1, 0), material),
                       Plane(mate.add(self.position, (0, 0, -size[2] / 2)), (0, 0, -1), material),
                       Plane(mate.add(self.position, (0, 0, size[2] / 2)), (0, 0, 1), material)]

        # Bounds
        self.boundsMin = [0, 0, 0]
        self.boundsMax = [0, 0, 0]

        for i in range(3):
            self.boundsMin[i] = self.position[i] - (0.001 + size[i] / 2)
            self.boundsMax[i] = self.position[i] + (0.001 + size[i] / 2)

    def ray_intersect(self, orig, dir):
        # super().ray_intersect(orig, dir)
        intersect = None
        t = float('inf')

        u = 0
        v = 0

        for plane in self.planes:
            planeIntersect = plane.ray_intersect(orig, dir)
            if planeIntersect is not None:
                planePoint = planeIntersect.point
                if self.boundsMin[0] <= planePoint[0] < self.boundsMax[0]:
                    if self.boundsMin[1] <= planePoint[1] < self.boundsMax[1]:
                        if self.boundsMin[2] <= planePoint[2] < self.boundsMax[2]:
                            if planeIntersect.distance < t:
                                t = planeIntersect.distance
                                intersect = planeIntersect

                                if abs(plane.normal[0]) > 0:
                                    u = (planePoint[1] - self.boundsMin[1]) / (self.size[1] + 0.002)
                                    v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + 0.002)
                                elif abs(plane.normal[1]) > 0:
                                    u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + 0.002)
                                elif abs(plane.normal[2]) > 0:
                                    u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v = (planePoint[1] - self.boundsMin[1]) / (self.size[1] + 0.002)
        if intersect is None:
            return None

        return Intercept(distance=t,
                         point=intersect.point,
                         normal=intersect.normal,
                         texcoords=(u, v),
                         obj=self)


class Triangle(Shape):

    def __init__(self, p0, p1, p2, position, material):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2

        super().__init__(position, material)

    def ray_intersect(self, orig, dir):

        orig = mate.sub(orig, self.position)

        # encuentra vectores para dos lados del triángulo
        edge1 = mate.subtract(self.p1, self.p0)
        edge2 = mate.subtract(self.p2, self.p0)

        # producto cruz para obtener perpendicular
        pvec = mate.cross(dir, edge2)
        det = mate.dot_product(edge1, pvec)

        if abs(det) < 0.0001:
            return None

        # calcula distancia desde vertice 0 al rayo
        tvec = mate.subtract(orig, self.p0)
        u = mate.dot_product(tvec, pvec) / det
        if u < 0 or u > 1:
            return None

        # producto cruz para segundo perpendicular
        qvec = mate.cross(tvec, edge1)
        v = mate.dot_product(dir, qvec) / det
        if v < 0 or u + v > 1:
            return None

        t = mate.dot_product(edge2, qvec) / det
        if t < 0:
            return None

        # calcula normal del triángulo
        normal = mate.normalize(mate.cross(edge1, edge2))

        return Intercept(distance=t,
                         point=mate.add(orig, mate.multiply(t, dir)),
                         normal=normal,
                         texcoords=(u, v),
                            obj=self)