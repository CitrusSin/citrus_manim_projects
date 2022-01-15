import math
import numpy as np
from manimlib import *
from typing import Any, Dict, Tuple, List, Optional

from numpy.lib.function_base import iterable

### Util functions and classes BEGIN ##

# Content of my_util_classes/geometry_structure.py

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


### Util functions and classes END ##


def cross_vec2(a, b):
    return a[0]*b[1]-a[1]*b[0]


class Vec2Cross(Scene):
    def construct(self):
        self.cross_introduce()

    def cross_introduce(self):
        title = TexText("平面向量", "的“叉积”").scale(1.2)
        self.play(Write(title))
        self.wait(3)

        self.play(title.to_corner, UL)
        self.play(title[0].set_color, RED)

        self.wait(2)

        title_question = TexText("?", color=RED).scale(1.2)
        title[1].generate_target()
        title_question.next_to(title[0], RIGHT)
        title[1].target.next_to(title_question, RIGHT)
        self.play(MoveToTarget(title[1]), Write(title_question))

        tip1 = TexText("是不是有点陌生？").scale(0.8).next_to(title, DOWN).to_edge(LEFT)
        self.play(Write(tip1))
        self.wait(2)

        title_replacement = TexText("空间向量", color=BLUE).scale(1.2).move_to(title[0])
        tip1_2 = TexText("那这样呢？").scale(0.8).move_to(tip1).to_edge(LEFT)
        title[1].generate_target()
        title[1].target.next_to(title_replacement, RIGHT)

        title0_backup = title[0].copy()

        self.play(
            Transform(title[0], title_replacement),
            Transform(tip1, tip1_2),
            Uncreate(title_question),
            MoveToTarget(title[1])
        )

        tip2 = VGroup(
            TexText("想必大家对这也许有所耳闻，"),
            TexText("空间向量的叉积可以求出"),
            TexText("两个向量张成的平面的法向量，"),
            TexText("而利用法向量可以很快搞定"),
            TexText("诸如线面角，二面角之类的东西。")
        ).fix_in_frame().arrange(DOWN).scale(0.6).next_to(tip1, DOWN).to_edge(LEFT)
        
        for t in tip2.submobjects:
            t.to_edge(LEFT)
        self.play(Write(tip2))
        self.wait(2)

        tip2.generate_target()
        tip2.target.next_to(title, DOWN).to_edge(LEFT)
        self.play(FadeOut(tip1), MoveToTarget(tip2))

        formula = Tex("\\overrightarrow{S}", "=", "\\overrightarrow{a}", "\\times", "\\overrightarrow{b}")
        formula[0].set_color(GREEN)
        formula[2].set_color(RED)
        formula[4].set_color(BLUE)

        formula.fix_in_frame().next_to(tip2, DOWN)

        self.play(Write(formula))

        # Prepare to enter 3D

        title[0].fix_in_frame()
        title[1].fix_in_frame()
        title_replacement.fix_in_frame()
        tip1.fix_in_frame()
        tip1_2.fix_in_frame()

        # Enter 3D

        axe = ThreeDAxes((-3, 3), (-3, 3), (-3, 3))
        vecs = np.random.rand(3, 3) * 3 - 1.5
        vecs[2] = np.cross(vecs[0], vecs[1])

        vec_objs = VGroup(
            Vector(vecs[0]).set_color(RED),
            Vector(vecs[1]).set_color(BLUE),
            Vector(vecs[2]).set_color(GREEN)
        )

        poly = Polygon(ORIGIN, vecs[0], vecs[0]+vecs[1], vecs[1], stroke_width=1).set_color(GREEN).set_fill(GREEN, 0.6)

        # Configure camera

        camera_update_function = lambda m, dt: m.increment_theta(0.5*dt)
        self.camera.frame.set_euler_angles(theta=20, phi=20)
        self.camera.frame.add_updater(camera_update_function)
        
        self.play(ShowCreation(axe), ShowCreation(vec_objs), ShowCreation(poly))

        for i in range(3):
            vecs = np.random.rand(3, 3) * 3 - 1.5
            vecs[2] = np.cross(vecs[0], vecs[1])
            for i in range(3):
                vec_objs[i].target=Vector(vecs[i]).set_color(vec_objs[i].get_color())
            poly.target = Polygon(ORIGIN, vecs[0], vecs[0]+vecs[1], vecs[1], stroke_width=1).set_color(GREEN).set_fill(GREEN, 0.6)
            self.play(*[MoveToTarget(vec_objs[i]) for i in range(3)], MoveToTarget(poly))
            self.wait(2)

        tip3 = VGroup(
            TexText("但是，两个空间向量叉积"),
            TexText("不止包含方向信息，"), 
            TexText("它还有一个模长。")
        ).fix_in_frame().arrange(DOWN).scale(0.6).next_to(tip2, DOWN).to_edge(LEFT)

        for t in tip3.submobjects:
            t.to_edge(LEFT)
        self.play(FadeOut(formula), Write(tip3))
        self.wait(2)

        tip4 = VGroup(
            TexText("这个向量的模长，"),
            TexText("会刚好等于", "绿色平行四边形"),
            TexText("即两个向量所夹成的平行四边形的面积")
        ).fix_in_frame().arrange(DOWN).scale(0.6).next_to(tip2, DOWN).to_edge(LEFT)
        tip4[1][1].set_color(GREEN)

        for t in tip4.submobjects:
            t.to_edge(LEFT)
        self.play(ReplacementTransform(tip3, tip4))

        for i in range(2):
            vecs = np.random.rand(3, 3) * 3 - 1.5
            vecs[2] = np.cross(vecs[0], vecs[1])
            for i in range(3):
                vec_objs[i].target=Vector(vecs[i]).set_color(vec_objs[i].get_color())
            poly.target = Polygon(ORIGIN, vecs[0], vecs[0]+vecs[1], vecs[1], stroke_width=1).set_color(GREEN).set_fill(GREEN, 0.6)
            self.play(*[MoveToTarget(vec_objs[i]) for i in range(3)], MoveToTarget(poly))
            self.wait(2)

        self.camera.frame.remove_updater(camera_update_function)
        self.play(Uncreate(axe), Uncreate(vec_objs), Uncreate(poly))
        self.camera.frame.to_default_state()

        self.play(FadeOut(tip4), FadeOut(tip2), Transform(title[0], title0_backup))
        title[0].fix_in_frame()
        self.wait(1)

        self.camera.frame.reorient(45, 70, 0)

        tip5 = VGroup(
            TexText("虽说平面向量没有严格意义上的叉积，"),
            TexText("但这并不妨碍我们把叉积运算扩展到平面向量上。"),
        ).fix_in_frame().arrange(DOWN).scale(0.6).next_to(title, DOWN).to_edge(LEFT)
        for t in tip5.submobjects:
            t.to_edge(LEFT)
        self.play(Write(tip5))
        self.wait(2)

        vecs = VGroup(
            Vector([1, 0, 0]).set_color(RED),
            Vector([0, 1, 0]).set_color(BLUE),
            Vector(np.cross([1,0,0],[0,1,0])).set_color(GREEN)
        )
        poly = Polygon(ORIGIN, [1,0,0], [1,1,0], [0,1,0], stroke_width=1, color=GREEN).set_fill(GREEN, 0.6)
        self.play(ShowCreation(vecs), ShowCreation(poly))
        self.wait(1)
        self.play(UpdateFromAlphaFunc(self.camera.frame, lambda m, alpha: m.reorient(45-(45*alpha),70-(70*alpha), 0)))

        vec0 = vecs[0]
        vec1 = vecs[1]
        product = vecs[2]
        area_num = DecimalNumber(1, color=GREEN).move_to([-0.5, -0.5, 0])
        self.play(ReplacementTransform(product, area_num))
        self.wait(1)

        tip6 = VGroup(
            TexText("由于平面向量全都在一个平面内，"),
            TexText("所以不管怎么做叉积，结果都只有两个方向。"),
            TexText("为方便起见，这里直接使用实数代替结果向量，"),
            TexText("以正负来代表结果的两个向量，"),
            TexText("得到平面向量叉积如下的定义式："),
            Tex(
                "\\overrightarrow{a}", "\\times", "\\overrightarrow{b}", "=",
                "||", "\\overrightarrow{a}", "||\\cdot ||", "\\overrightarrow{b}",
                "||\\sin \\langle", "\\overrightarrow{a}", ",", "\\overrightarrow{b}",
                "\\rangle",
                tex_to_color_map={"\\overrightarrow{a}": RED, "\\overrightarrow{b}": BLUE}
            )
        ).fix_in_frame().arrange(DOWN).scale(0.6).next_to(tip5, DOWN).to_edge(LEFT)

        for t in tip6.submobjects:
            t.to_edge(LEFT)
            self.play(Write(t))

        vec0.generate_target()
        vec1.generate_target()
        vec0.target.put_start_and_end_on(ORIGIN, [1.5, 0, 0])
        vec1.target.put_start_and_end_on(ORIGIN, [0.5, -0.8, 0])
        
        poly.target = Polygon(ORIGIN, [1.5,0,0], [1.5,1,0], [0,1,0], stroke_width=1, color=GREEN).set_fill(GREEN, 0.6)
        
        self.play(
            MoveToTarget(vec0),
            UpdateFromFunc(area_num, lambda m: m.set_value(cross_vec2(vec0.get_end(), vec1.get_end())).set_color(GREEN)),
            MoveToTarget(poly)
        )

        poly.target = Polygon(ORIGIN, [1.5,0,0], [2,-0.8,0], [0.5,-0.8,0], stroke_width=1, color=GREEN).set_fill(GREEN, 0.6)

        self.play(
            MoveToTarget(vec1),
            UpdateFromFunc(area_num, lambda m: m.set_value(cross_vec2(vec0.get_end(), vec1.get_end())).set_color(GREEN)),
            MoveToTarget(poly)
        )

        tip7 = VGroup(
            TexText("利用正弦差角公式，我们不难推出，"),
            TexText("对于$\\overrightarrow{a}=\\begin{bmatrix} x_1 \\\\ y_1 \\end{bmatrix}, \\overrightarrow{b}=\\begin{bmatrix} x_2 \\\\ y_2 \\end{bmatrix}$，"),
            Tex(
                "\\overrightarrow{a}", "\\times", "\\overrightarrow{b}", "=",
                "x_1", "y_2", "-", "x_2", "y_1",
                tex_to_color_map={
                    "\\overrightarrow{a}": RED,
                    "\\overrightarrow{b}": BLUE,
                    "x_1": RED,
                    "y_1": RED,
                    "x_2": BLUE,
                    "y_2": BLUE
                }
            )
        ).fix_in_frame().arrange(DOWN).scale(0.6).next_to(tip6, DOWN).to_edge(LEFT)
        
        for t in tip7.submobjects:
            t.to_edge(LEFT)
            self.play(Write(t))

        self.wait(1)
        
        formula = tip7[2]
        tip7.remove(formula)
        self.play(Uncreate(tip7), Uncreate(tip6), Uncreate(tip5), Uncreate(vecs), Uncreate(area_num), Uncreate(poly), Uncreate(title))
        
        formula.generate_target()
        formula.target.scale(2)

        append_text = TexText("接下来，我们用这个公式推导一些有关“叉积”的性质。").next_to(formula, DOWN, buff=0.5)
        group = VGroup(formula.target, append_text).center()
        self.play(MoveToTarget(formula), Write(append_text))

        self.showCountdown(5)
        self.play(FadeOut(group))

    def showTriangle(self):
        tri = VertexPolygon((1.5, 3, 0), (-3, -0.5, 0), (3, -1.5, 0), color_index=[RED, GREEN, BLUE]).center()
        
        self.play(ShowCreation(tri))

        tri.add_point('O', tri.get_grav_center())
        tri.connect('OA', 'OB', 'OC')
        tri.set_dot_color('O', PURPLE)

        tri.animate_changes(self)

        tri.move_dot('C', [1, 0, 0])
        tri.move_dot('O', tri.get_grav_center())

        tri.animate_changes(self)

    def showCountdown(self, seconds):
        countDownObj = Tex(str(seconds), color=BLUE).to_corner(DR)

        self.play(Write(countDownObj))
        self.wait(0.25)

        for i in range(seconds-1, -1, -1):
            newObj = Tex(str(i), color=BLUE).to_corner(DR)
            self.play(Transform(countDownObj, newObj))
            self.wait(0.25)

        self.play(FadeOut(countDownObj))
        