import numpy as np
import math

class Vector():

    def __init__(self, elements=[]):
        self.v = np.array(elements)

    def __getitem__(self, i):
        return self.v[i]

    def magnitude(self):
        return math.sqrt(sum(self.v ** 2))

    def unit(self):
        mag = self.magnitude()
        if not mag == 0:
            return self.v / mag
        else:
            return self.v

    def proj_onto(self, other):
        dot_prod = self.v.dot(other.v)
        proj_length = dot_prod / other.magnitude
        return Vector(proj_length * other.unit())

    def dot_onto(self, other):
        dot_prod = self.v.dot(other.v)
        return Vector(dot_prod * other.unit())


