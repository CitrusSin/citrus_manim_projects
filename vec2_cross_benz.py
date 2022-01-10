import numpy as np
from manimlib import *

class VertexPolygon(VGroup):
    def __init__(self, *vertices, starting_point='A', color_index=None, **kwargs):
        super().__init__(**kwargs)

        self.vertices = vertices
        self.dots = list()
        self.labels = list()
        self.polygon = Polygon(*vertices)
        self.starting_point = starting_point

        center = np.array((0.0,0.0,0.0))
        for vertice in vertices:
            center += vertice
        center = center / len(vertices)

        for i in range(len(vertices)):
            vertex = np.array(vertices[i])
            dot = Dot(vertex)
            directionVec = (vertex - center)/np.linalg.norm(vertex)
            label = Tex(chr(ord(starting_point) + i)).next_to(dot, directionVec)
            self.dots.append(dot)
            self.labels.append(label)

        self.add(self.polygon)
        self.add(*self.dots)
        self.add(*self.labels)

        if isinstance(color_index, list):
            for i in range(len(color_index)):
                self.set_vertex_color(i, color_index[i])

    def get_vertex_dot(self, name):
        index = name
        if isinstance(name, str):
            index = ord(name) - ord(self.starting_point)
        if not isinstance(index, int):
            raise TypeError("Index not a number or a string")
        return self.dots[index]

    def get_vertex_label(self, name):
        index = name
        if isinstance(name, str):
            index = ord(name) - ord(self.starting_point)
        if not isinstance(index, int):
            raise TypeError("Index not a number or a string")
        return self.labels[index]

    def set_vertex_color(self, name, color):
        self.get_vertex_dot(name).set_color(color)
        self.get_vertex_label(name).set_color(color)


class Vec2Cross(Scene):
    def construct(self):
        tri = VertexPolygon((1.5, 3, 0), (-3, -1.5, 0), (3, -1.5, 0), color_index=[RED, GREEN, BLUE]).center()
        self.play(ShowCreation(tri))
        pass