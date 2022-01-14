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
    __vmobjects_append: List[VMobject] = list()
    __vmobjects_remove: List[VMobject] = list()
    __vmobjects_targeted: List[VMobject] = list()
    __point_dict: Dict[str, np.ndarray]
    __dots: Dict[str, Dot]
    __labels: Dict[str, Tex]
    __lines: Dict[Tuple[str, str], Line]

    label_pos_func = lambda p:UR

    def __init__(
                self, 
                point_dict: Dict[str, Any], 
                conn_list: List, 
                label_pos_func=lambda p:UR, 
                color_index: Optional[Dict[str, int]] = None, 
                **kwargs
                ):
        super().__init__(**kwargs)

        self.__point_dict = {name: np.array(vertex) for name, vertex in point_dict.items()}
        self.__dots = {name: Dot(vertex) for name, vertex in self.__point_dict.items()}
        self.__labels = {
            name: Tex(name).next_to(dot, label_pos_func(self.__point_dict[name])) 
            for name, dot in self.__dots.items()
        }

        connections = list()

        for conn in conn_list:
            if isinstance(conn, str):
                connections.append((conn[0], conn[1]))
            elif isinstance(conn, list):
                connections.append(tuple(conn[0:2]))
            elif isinstance(conn, tuple):
                connections.append(conn)

        self.__lines = {(a, b): Line(self.__point_dict[a], self.__point_dict[b]) for a, b in connections}

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

    def animate_changes(self, scene: Scene, **kwargs):
        list_append, list_remove, list_targeted = self.apply_changes()

        animations = list()
        animations.extend([ShowCreation(x) for x in list_append])
        animations.extend([Uncreate(x) for x in list_remove])
        animations.extend([MoveToTarget(x) for x in list_targeted])

        scene.play(*animations, **kwargs)

    def apply_changes(self) -> Tuple[List[VMobject], List[VMobject], List[VMobject]]:
        list_append = self.__vmobjects_append
        list_remove = self.__vmobjects_remove
        list_targeted = self.__vmobjects_targeted
        self.__vmobjects_append = list()
        self.__vmobjects_remove = list()
        self.__vmobjects_targeted = list()

        self.remove(*list_remove)
        self.add(*list_append)

        return list_append, list_remove, list_targeted

    def add_point(self, name:str, coord):
        co = np.array(coord)
        self.__point_dict[name] = co

        dot = Dot(co)
        self.__dots[name] = dot
        self.__vmobjects_append.append(dot)

        label = Tex(name).next_to(dot, self.label_pos_func(co))
        self.__labels[name] = label
        self.__vmobjects_append.append(label)
        return self
        
    def connect(self, *conn_list):
        new_connections = list()

        for conn in conn_list:
            if isinstance(conn, str):
                new_connections.append((conn[0], conn[1]))
            elif isinstance(conn, list):
                new_connections.append(tuple(conn[0:2]))
            elif isinstance(conn, tuple):
                new_connections.append(conn)

        #self.__connections.extend(new_connections)

        for conn in new_connections:
            line = Line(self.__point_dict[conn[0]], self.__point_dict[conn[1]])
            self.__lines[conn] = line
            self.__vmobjects_append.append(line)

    def disconnect(self, *disconn_list):
        normalized_list = list()

        for conn in disconn_list:
            if isinstance(conn, str):
                normalized_list.append((conn[0], conn[1]))
            elif isinstance(conn, list):
                normalized_list.append(tuple(conn[0:2]))
            elif isinstance(conn, tuple):
                normalized_list.append(conn)

        keys_to_remove = list()
        for conn_tbd in normalized_list:
            for conn in self.__lines.keys():
                if cmp_unordered(conn_tbd, conn):
                    keys_to_remove.append(conn)
        for key in keys_to_remove:
            self.__vmobjects_remove.append(self.__lines.pop(key))

    def remove_point(self, name:str):
        self.__point_dict.pop(name)
        self.__vmobjects_remove.append(self.__dots.pop(name))
        
        keys_to_remove = list()
        for conn in self.__lines.keys():
            if name in conn:
                keys_to_remove.append(conn)
        for key in keys_to_remove:
            self.__vmobjects_remove.append(self.__lines.pop(key))

        self.__vmobjects_remove.append(self.__labels.pop(name))

    def move_dot(self, name, point):
        if name in self.__point_dict:
            if not isinstance(point, np.ndarray):
                point = np.array(point)

            dot = self.__dots[name]
            label = self.__labels[name]
            
            if dot not in self.__vmobjects_targeted:
                dot.generate_target()
                self.__vmobjects_targeted.append(dot)
            if label not in self.__vmobjects_targeted:
                label.generate_target()
                self.__vmobjects_targeted.append(label)
            
            self.__point_dict[name] = point
            dot.target.move_to(point)
            label.target.next_to(dot.target, self.label_pos_func(point))
            
            for conn, line in self.__lines.items():
                if name in conn:
                    if line not in self.__vmobjects_targeted:
                        self.__vmobjects_targeted.append(line)
                    line.target = Line(self.__point_dict[conn[0]], self.__point_dict[conn[1]])

    def get_dot(self, name):
        return self.__dots[name]

    def get_label(self, name):
        return self.__labels[name]

    def get_point(self, name):
        return self.__point_dict[name]

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
        self.__vertex_names = names

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
        for vertex in self.vertices:
            if about_point is None:
                vertex[:] = func(vertex)
            else:
                vertex[:] = func(vertex - about_point) + about_point

        return super().apply_points_function(func, about_point, about_edge, works_on_bounding_box)
        
    def get_grav_center(self):
        return np.sum(self.vertices, axis=0) / len(self.vertices)

    def move_dot(self, name, point):
        for i, n in enumerate(self.__vertex_names):
            if n == name:
                self.vertices[i] = point
                break
        return super().move_dot(name, point)

