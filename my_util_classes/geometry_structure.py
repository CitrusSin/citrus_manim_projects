import math
from typing import Any, Dict, List, Optional, Tuple
from manimlib import *


def cmp_unordered(tuple1, tuple2):
    for x in tuple1:
        if x not in tuple2:
            return False
    for y in tuple2:
        if y not in tuple1:
            return False
    return True


class GeometryStructure(VGroup):
    def __init__(
                self, 
                point_dict: Dict[str, Any], 
                line_list: List, 
                label_pos_func=lambda p:UR, 
                color_index: Optional[Dict[str, int]] = None, 
                **kwargs
                ):
        super().__init__(**kwargs)

        self.__point_dict = {name: np.array(vertex) for name, vertex in point_dict.items()}
        self.__connections = [tuple(conn) for conn in line_list if len(conn) == 2]

        for i in range(len(self.__connections)):
            if isinstance(self.__connections[i], str):
                conn_str = self.__connections[i]
                self.__connections[i] = (conn_str[0], conn_str[1])
            elif not isinstance(self.__connections[i], tuple):
                conn = self.__connections[i]
                self.__connections[i] = tuple(conn)

        self.__dots = {name: Dot(vertex) for name, vertex in self.__point_dict.items()}
        self.__labels = {
            name: Tex(name).next_to(dot, label_pos_func(self.__point_dict[name])) 
            for name, dot in self.__dots.items()
        }
        self.__lines = {(a, b): Line(self.__point_dict[a], self.__point_dict[b]) for a, b in self.__connections}

        self.label_pos_func = label_pos_func

        self.add(*self.__dots.values())
        self.add(*self.__labels.values())
        self.add(*self.__lines.values())

        if color_index != None:
            for name, color in color_index.items():
                self.set_dot_color(name, color)

    def apply_points_function(self, func, about_point=None, about_edge=ORIGIN, works_on_bounding_box=False):
        super().apply_points_function(func, about_point, about_edge, works_on_bounding_box)

        if about_point is None and about_edge is not None:
            about_point = self.get_bounding_box_point(about_edge)

        for name, point in self.__point_dict.items():
            if about_point is None:
                self.__point_dict[name] = func(point)
            else:
                self.__point_dict[name] = func(point - about_point) + about_point
        
        return self

    def generate_delta_objects(self) -> Tuple[List[VMobject], List[VMobject]]:
        append_list = list()
        remove_list = list()

        for name, point in self.__point_dict.items():
            if name not in self.__dots:
                dot = Dot(point)
                label = Tex(name).next_to(dot, self.label_pos_func(self.__point_dict[name]))
                self.__dots[name] = dot
                self.__labels[name] = label
                append_list.append(dot)
                append_list.append(label)
        for name in self.__dots.keys():
            if name not in self.__point_dict:
                remove_list.append(self.__dots.pop(name))
                remove_list.append(self.__labels.pop(name))
                for conn in self.__connections:
                    if name in conn:
                        self.__connections.remove(conn)

        for conn in self.__connections:
            if conn not in self.__lines:
                line = Line(self.__point_dict[conn[0]], self.__point_dict[conn[1]])
                self.__lines[conn] = line
                append_list.append(line)
        for conn in self.__lines.keys():
            if conn not in self.__connections:
                remove_list.append(self.__lines.pop(conn))

        self.remove(*remove_list)
        self.add(*append_list)
        return append_list, remove_list

    def add_point(self, name:str, coord):
        co = np.array(coord)
        self.__point_dict[name] = co
        return self
        
    def connect(self, *conn_list):
        new_connections = [tuple(conn) for conn in conn_list if len(conn) == 2]

        for i in range(len(new_connections)):
            if isinstance(new_connections[i], str):
                conn_str = new_connections[i]
                new_connections[i] = (conn_str[0], conn_str[1])
            elif not isinstance(new_connections[i], tuple):
                conn = new_connections[i]
                new_connections[i] = tuple(conn)

        self.__connections.extend(new_connections)

    def get_dot(self, name):
        return self.__dots[name]

    def get_label(self, name):
        return self.__labels[name]

    def set_dot_color(self, name, color):
        self.get_dot(name).set_color(color)
        self.get_label(name).set_color(color)

class VertexPolygon(GeometryStructure):
    def __init__(self, *vertices, color_index=None, name_index='A', **kwargs):
        names = list()
        count = len(vertices)

        for i in range(count):
            names.append(chr(ord(name_index)+i))
        
        point_dict = {names[i]: vertices[i] for i in range(count)}
        line_list = [(names[i], names[i+1]) for i in range(count-1)]
        line_list.append((names[count-1], names[0]))

        color_dict = None
        if color_index != None:
            color_dict = {names[i]: color_index[i] for i in range(count)}

        self.vertices = np.array(vertices)

        def lpfunc(p):
            delta = p-self.get_grav_center()
            len = np.linalg.norm(delta)
            if len<0.05:
                delta = UR/math.sqrt(2)
            else:
                delta = delta / len
            return delta

        super().__init__(
            point_dict, line_list, 
            label_pos_func=lpfunc,
            color_index = color_dict
        )

    def apply_points_function(self, func, about_point=None, about_edge=ORIGIN, works_on_bounding_box=False):
        super().apply_points_function(func, about_point, about_edge, works_on_bounding_box)

        for vertex in self.vertices:
            if about_point is None:
                vertex[:] = func(vertex)
            else:
                vertex[:] = func(vertex - about_point) + about_point
        
    def get_grav_center(self):
        return np.sum(self.vertices, axis=0) / len(self.vertices)
