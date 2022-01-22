import math
from pydoc_data import topics
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

    def get_line(self, conn):
        if isinstance(conn, str):
            conn = (conn[0], conn[1])
        elif isinstance(conn, list):
            conn = tuple(conn[0:2])
        for conn2 in self.__lines.keys():
            if cmp_unordered(conn, conn2):
                return self.__lines[conn2]

    def set_line_color(self, name, color):
        self.get_line(name).set_color(color)

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
            delta = p-self.get_mass_center()
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
        
    def get_mass_center(self):
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
        #self.introduce_benz_theorem()
        #self.cross_introduce()
        #self.cross_properties()
        self.proof_benz_theorem()

    def proof_benz_theorem(self):
        tip1 = TexText("现在，让我们回到奔驰定理的证明上来。")
        self.play(Write(tip1))
        self.play(tip1.to_edge, UP)

        tri = VertexPolygon((1, 2, 0), (-2, -0.3, 0), (2, -1.3, 0), color_index=[RED, GREEN, BLUE]).center()
        self.play(ShowCreation(tri))

        tri.add_point('O', tri.get_mass_center() + 1.6*((np.random.rand(3)-0.8)*np.array([1,1,0])))
        tri.connect('OA', 'OB', 'OC')
        tri.set_line_color('OA', RED)
        tri.set_line_color('OB', GREEN)
        tri.set_line_color('OC', BLUE)
        tri.set_dot_color('O', PURPLE)
        tri.animate_changes(self)

        self.play(tri.to_edge, RIGHT)

        known_and_to_proof = VGroup(
            Tex(
                "\\textup{已知：}", "\\alpha\\overrightarrow{OA}+\\beta\\overrightarrow{OB}+\\gamma\\overrightarrow{OC}=\\overrightarrow{0}",
                tex_to_color_map = {
                    "\\overrightarrow{OA}": RED,
                    "\\overrightarrow{OB}": GREEN,
                    "\\overrightarrow{OC}": BLUE
                }
            ),
            Tex(
                "\\textup{求证：}S_{\\bigtriangleup OBC}:S_{\\bigtriangleup OCA}:S_{\\bigtriangleup OAB}=\\alpha : \\beta : \\gamma",
                tex_to_color_map = {
                    "S_{\\bigtriangleup OBC}": RED,
                    "S_{\\bigtriangleup OCA}": GREEN,
                    "S_{\\bigtriangleup OAB}": BLUE,
                    "\\alpha": RED,
                    "\\beta": GREEN,
                    "\\gamma": BLUE
                }
            )
        ).arrange(DOWN).next_to(tip1, DOWN).to_edge(LEFT)
        for t in known_and_to_proof.submobjects:
            t.to_edge(LEFT)
        
        self.play(Write(known_and_to_proof))

        formula = Tex(
            "\\alpha\\overrightarrow{OA}+\\beta\\overrightarrow{OB}+\\gamma\\overrightarrow{OC}=\\overrightarrow{0}",
            tex_to_color_map = {
                "\\overrightarrow{OA}": RED,
                "\\overrightarrow{OB}": GREEN,
                "\\overrightarrow{OC}": BLUE
            }
        ).move_to([0, -2, 0])

        self.play(TransformMatchingTex(known_and_to_proof[0].copy(), formula))
        self.wait(1)

        tip1 = TexText("现在，让我们开始利用“叉积”秒杀", tex_to_color_map={"秒杀": RED}).next_to(formula, DOWN)
        self.play(Write(tip1))
        self.wait(1)

        tip2 = TexText("不要眨眼！", color=RED).move_to(tip1)
        self.play(ReplacementTransform(tip1, tip2))
        self.wait(2)
        self.play(FadeOut(tip2))

        formula2 = Tex(
            "\\overrightarrow{OA} \\times (\\alpha\\overrightarrow{OA}+\\beta\\overrightarrow{OB}+\\gamma\\overrightarrow{OC})=0",
            isolate = ["(", ")"],
            tex_to_color_map = {
                "\\overrightarrow{OA}": RED,
                "\\overrightarrow{OB}": GREEN,
                "\\overrightarrow{OC}": BLUE
            }
        ).move_to(formula)

        formula3 = Tex(
            "\\alpha\\overrightarrow{OA}\\times\\overrightarrow{OA}+\\beta\\overrightarrow{OA}\\times\\overrightarrow{OB}+\\gamma\\overrightarrow{OA}\\times\\overrightarrow{OC}=0",
            tex_to_color_map = {
                "\\overrightarrow{OA}": RED,
                "\\overrightarrow{OB}": GREEN,
                "\\overrightarrow{OC}": BLUE
            }
        ).move_to(formula2)

        self.play(TransformMatchingTex(formula, formula2))
        self.wait(2)
        self.play(TransformMatchingTex(formula2, formula3))
        self.wait(2)

        formula3_center_pos = formula3.get_center()

        formula3_left = VGroup(formula3[:4])
        formula3_right = VGroup(formula3[4:])

        self.play(FadeOut(formula3_left, shift=DOWN), formula3_right.animate.move_to(formula3_center_pos))

        formula4 = Tex(
            "\\beta\\overrightarrow{OA}\\times\\overrightarrow{OB}+\\gamma\\overrightarrow{OA}\\times\\overrightarrow{OC}=0",
            tex_to_color_map = {
                "\\overrightarrow{OA}": RED,
                "\\overrightarrow{OB}": GREEN,
                "\\overrightarrow{OC}": BLUE
            }
        ).move_to(formula3)

        formula5 = Tex(
            "\\beta\\overrightarrow{OA}\\times\\overrightarrow{OB}=-\\gamma\\overrightarrow{OA}\\times\\overrightarrow{OC}",
            tex_to_color_map = {
                "\\overrightarrow{OA}": RED,
                "\\overrightarrow{OB}": GREEN,
                "\\overrightarrow{OC}": BLUE
            }
        ).move_to(formula3)

        formula6 = Tex(
            "\\beta\\overrightarrow{OA}\\times\\overrightarrow{OB}=\\gamma\\overrightarrow{OC}\\times\\overrightarrow{OA}",
            tex_to_color_map = {
                "\\overrightarrow{OA}": RED,
                "\\overrightarrow{OB}": GREEN,
                "\\overrightarrow{OC}": BLUE
            }
        ).move_to(formula3)

        self.play(TransformMatchingShapes(formula3_right, formula4))
        self.wait(2)
        self.play(TransformMatchingTex(formula4, formula5))
        self.wait(1)
        self.play(TransformMatchingTex(formula5, formula6))
        self.wait(2)

        color_map = {
            "\\alpha": RED,
            "\\beta": GREEN,
            "\\gamma": BLUE,
            "S_{\\bigtriangleup OBC}": RED,
            "S_{\\bigtriangleup OCA}": GREEN,
            "S_{\\bigtriangleup OAB}": BLUE
        }
        
        formula7 = Tex(
            "\\pm 2\\beta S_{\\bigtriangleup OAB}=\\pm 2\\gamma S_{\\bigtriangleup OCA}",
            isolate = ["2"],
            tex_to_color_map = color_map
        ).move_to(formula6)

        tip3 = TexText("注意：此时，由于两边都是逆时针乘向量，所以两边应该同号").scale(0.8).next_to(formula7, DOWN)
        tip4 = TexText("还记得“叉积”的绝对值代表什么么？").scale(0.8).next_to(formula7, DOWN)

        self.play(Write(tip3))
        self.wait(1)
        self.play(ReplacementTransform(tip3, tip4))
        self.wait(2)
        self.play(TransformMatchingTex(formula6, formula7))
        self.wait(1)
        self.play(Uncreate(tip4))

        formula8 = Tex(
            "\\beta S_{\\bigtriangleup OAB}=\\gamma S_{\\bigtriangleup OCA}",
            tex_to_color_map = color_map
        ).move_to(formula7)
        self.play(TransformMatchingTex(formula7, formula8))

        self.wait(1)

        self.play(formula8.animate.next_to(known_and_to_proof, DOWN).to_edge(LEFT))

        tip5 = TexText("同理可得：").next_to(formula8, DOWN).to_edge(LEFT)
        self.play(Write(tip5))

        popularize_formula = VGroup(
            Tex(
                "\\gamma S_{\\bigtriangleup OBC}=\\alpha S_{\\bigtriangleup OAB}",
                tex_to_color_map = color_map
            ),
            Tex(
                "\\alpha S_{\\bigtriangleup OCA}=\\beta S_{\\bigtriangleup OBC}",
                tex_to_color_map = color_map
            )
        ).arrange(DOWN).next_to(tip5, DOWN).to_edge(LEFT)
        for t in popularize_formula.submobjects:
            t.to_edge(LEFT)
        self.play(FadeIn(popularize_formula, shift=DOWN))

        self.embed()

    def introduce_benz_theorem(self):
        intro = VGroup(
            TexText("开头先讲一个定理：奔驰定理"),
            TexText("这个定理可以说是比较实用。"),
            TexText("先来看看奔驰定理说了些什么。")
        ).arrange(DOWN).center()

        self.play(Write(intro))
        self.wait(4)
        self.play(FadeOut(intro))


        title = TexText("奔驰定理：").to_corner(UL)
        self.play(Write(title))

        tri = VertexPolygon((1, 2, 0), (-2, -0.3, 0), (2, -1.3, 0), color_index=[RED, GREEN, BLUE]).to_corner(UR)
        
        self.play(ShowCreation(tri))

        tri.add_point('O', tri.get_mass_center() + 1.6*((np.random.rand(3)-0.8)*np.array([1,1,0])))
        tri.connect('OA', 'OB', 'OC')
        tri.set_line_color('OA', RED)
        tri.set_line_color('OB', GREEN)
        tri.set_line_color('OC', BLUE)
        tri.set_dot_color('O', PURPLE)
        tri.animate_changes(self)

        tip1 = VGroup(
            TexText("对于任意三角形$\\bigtriangleup ABC$，$O$是其中任意一点，"),
            Tex(
                "\\textup{若} \\alpha\\overrightarrow{OA}+\\beta\\overrightarrow{OB}+\\gamma\\overrightarrow{OC}=\\overrightarrow{0}",
                tex_to_color_map = {
                    "\\overrightarrow{OA}": RED,
                    "\\overrightarrow{OB}": GREEN,
                    "\\overrightarrow{OC}": BLUE
                }
            ),
            Tex(
                "\\textup{则} S_{\\bigtriangleup OBC}:S_{\\bigtriangleup OCA}:S_{\\bigtriangleup OAB}=\\alpha : \\beta : \\gamma",
                tex_to_color_map = {
                    "S_{\\bigtriangleup OBC}": RED,
                    "S_{\\bigtriangleup OCA}": GREEN,
                    "S_{\\bigtriangleup OAB}": BLUE,
                    "\\alpha": RED,
                    "\\beta": GREEN,
                    "\\gamma": BLUE
                }
            )
        ).arrange(DOWN).scale(0.8).next_to(title, DOWN).to_edge(LEFT)
        for t in tip1.submobjects:
            t.to_edge(LEFT)
        self.play(Write(tip1))

        triangles = VGroup(
            Polygon(tri.get_point('O'), tri.get_point('B'), tri.get_point('C'), stroke_width=0, color=RED, fill_color=RED, fill_opacity=0.5).scale(0.9),
            Polygon(tri.get_point('O'), tri.get_point('C'), tri.get_point('A'), stroke_width=0, color=GREEN, fill_color=GREEN, fill_opacity=0.5).scale(0.9),
            Polygon(tri.get_point('O'), tri.get_point('A'), tri.get_point('B'), stroke_width=0, color=BLUE, fill_color=BLUE, fill_opacity=0.5).scale(0.9),
        )
        self.play(ShowCreation(triangles))

        self.wait(4)

        self.play(Uncreate(triangles))

        question = TexText("怎么证明呢？", color=RED).next_to(tip1, DOWN).to_edge(LEFT)
        self.play(Write(question))
        self.wait(2)
        self.play(FadeOut(tip1), FadeOut(question))

        # Proof part

        proof_sign = TexText("证：").next_to(title, DOWN).to_edge(LEFT)
        self.play(Write(proof_sign))

        # Calculate alpha,beta,gamma using matrix to solve a set of equations.

        vecOA = tri.get_point('A')-tri.get_point('O')
        vecOB = tri.get_point('B')-tri.get_point('O')
        vecOC = tri.get_point('C')-tri.get_point('O')
        matrix: np.ndarray = -np.array([vecOB[0:2], vecOC[0:2]]).transpose()
        betagamma = np.linalg.inv(matrix) @ vecOA[0:2]
        abg: np.ndarray = np.array([1, betagamma[0], betagamma[1]])
        abg /= 1.5 * np.linalg.norm(abg)

        tri.add_point('D', tri.get_point('O') + abg[0]*vecOA)
        tri.add_point('E', tri.get_point('O') + abg[1]*vecOB)
        tri.add_point('F', tri.get_point('O') + abg[2]*vecOC)
        tri.set_dot_color('D', YELLOW)
        tri.set_dot_color('E', PINK)
        tri.set_dot_color('F', ORANGE)
        tri.connect('DE', 'EF', 'FD')
        tri.animate_changes(self)

        tri.generate_target()
        tri.target.scale(1.3).to_corner(UR)
        self.play(MoveToTarget(tri))

        proof_1 = Tex(
            "\\textup{作} \\overrightarrow{OD}=\\alpha\\overrightarrow{OA}, \\overrightarrow{OE}=\\beta\\overrightarrow{OB}, \\overrightarrow{OF}=\\gamma\\overrightarrow{OC}",
            tex_to_color_map={
                "\\overrightarrow{OA}": RED,
                "\\overrightarrow{OB}": GREEN,
                "\\overrightarrow{OC}": BLUE,
                "\\overrightarrow{OD}": YELLOW,
                "\\overrightarrow{OE}": PINK,
                "\\overrightarrow{OF}": ORANGE
            }
        ).scale(0.4).next_to(proof_sign, DOWN).to_edge(LEFT)
        self.play(Write(proof_1))

        proof_total = VGroup(
            TexText("我们可以很容易知道"),
            Tex("S_{\\bigtriangleup OAB}=\\frac{S_{\\bigtriangleup ODE}}{\\alpha \\beta}"),
            Tex("S_{\\bigtriangleup OBC}=\\frac{S_{\\bigtriangleup OEF}}{\\beta \\gamma}"),
            Tex("S_{\\bigtriangleup OCA}=\\frac{S_{\\bigtriangleup OFD}}{\\gamma \\alpha}"),
            TexText("而且因为$\\overrightarrow{OD}+\\overrightarrow{OE}+\\overrightarrow{OF}=\\overrightarrow{0}$，可以知道$O$是$\\bigtriangleup DEF$的重心"),
            Tex("\\textup{也就是说，} S_{\\bigtriangleup ODE}=S_{\\bigtriangleup OEF}=S_{\\bigtriangleup OFD}"),
            Tex("\\textup{这样一来，} \\alpha \\beta S_{\\bigtriangleup OAB} = \\beta \\gamma S_{\\bigtriangleup OBC} = \\gamma \\alpha S_{\\bigtriangleup OCA}"),
            TexText("三项均除以$\\alpha \\beta \\gamma $，得到表达式"),
            Tex("\\frac{S_{\\bigtriangleup OAB}}{\\gamma} = \\frac{S_{\\bigtriangleup OBC}}{\\alpha} = \\frac{S_{\\bigtriangleup OCA}}{\\beta}"),
            Tex("\\textup{即} S_{\\bigtriangleup OBC}:S_{\\bigtriangleup OCA}:S_{\\bigtriangleup OAB}=\\alpha : \\beta : \\gamma")
        ).arrange(DOWN).scale(0.4).next_to(proof_1, DOWN).to_edge(LEFT)
        for t in proof_total.submobjects:
            t.to_edge(LEFT)
        self.play(Write(proof_total), run_time=2)
        self.wait(1)

        tip2 = VGroup(
            TexText("稍等一下？我知道可能有些太快了，但这个视频的重点不是这种证法。"),
            TexText("这个视频要讲的，是一种利用平面向量的“叉积”迅速秒杀的证法。")
        ).arrange(DOWN).scale(0.8).next_to(proof_total, DOWN).to_edge(LEFT)
        for t in tip2.submobjects:
            t.to_edge(LEFT)
        self.play(Write(tip2))
        self.showCountdown(5)
        self.play(*[FadeOut(x) for x in self.mobjects if not isinstance(x, CameraFrame)])


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
            TransformMatchingShapes(title[0], title_replacement),
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

        self.play(FadeOut(tip4), FadeOut(tip2), TransformMatchingShapes(title_replacement, title0_backup))
        title0_backup.fix_in_frame()
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

        notice = TexText("注意：严格来讲，叉积的定义式应该是后者（坐标式），前者只是推论；但这两个命题等价，为方便理解，这里从三角函数开始定义。").fix_in_frame().scale(0.5).to_edge(DOWN)
        self.play(Write(notice))
        self.wait(5)
        self.play(FadeOut(notice))

        formula = tip7[2]
        tip7.remove(formula)
        self.play(Uncreate(tip7), Uncreate(tip6), Uncreate(tip5), Uncreate(vec0), Uncreate(vec1), Uncreate(area_num), Uncreate(poly), Uncreate(title[1]), Uncreate(title0_backup))
        
        formula.generate_target()
        formula.target.scale(2)

        append_text = TexText("接下来，我们用这个公式推导一些有关“叉积”的性质。").next_to(formula, DOWN, buff=0.5)
        group = VGroup(formula.target, append_text).center()
        self.play(MoveToTarget(formula), Write(append_text))

        self.showCountdown(5)
        self.play(FadeOut(group), FadeOut(formula))

    def cross_properties(self):
        tip1 = VGroup(
            TexText("第一性质："),
            TexText("向量自己叉乘自己，或叉乘平行于自己的向量，结果等于0"),
            TexText("这个很好理解，因为两个向量方向重合，"),
            TexText("张开的“平行四边形”就是一条直线。")
        ).fix_in_frame().arrange(DOWN).scale(0.8).to_corner(UL)
        for t in tip1.submobjects:
            t.to_edge(LEFT)
        self.play(Write(tip1))
        self.wait(2)

        formula = Tex(
            "\\overrightarrow{a}", "\\times", "\\overrightarrow{a}", "=",
            "x_1y_1-x_1y_1", "=0",
            tex_to_color_map = {"\\overrightarrow{a}": BLUE, "x_1y_1-x_1y_1": BLUE}
        ).fix_in_frame()
        self.play(Write(formula))
        self.wait(2)

        self.play(FadeOut(tip1), FadeOut(formula))

        tip2 = VGroup(
            TexText("第二性质："),
            TexText("叉乘具有反交换律"),
            TexText("所谓反交换律，就是减法交换运算数时的性质。"),
            TexText("也就是说：")
        ).fix_in_frame().arrange(DOWN).scale(0.8).to_corner(UL)
        for t in tip2.submobjects:
            t.to_edge(LEFT)
        self.play(Write(tip2))

        formula = Tex(
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
        formula2 = Tex(
            "\\overrightarrow{a}", "\\times", "\\overrightarrow{b}", "=",
            "-", "(", "x_2", "y_1", "-", "x_1", "y_2", ")",
            tex_to_color_map={
                "\\overrightarrow{a}": RED,
                "\\overrightarrow{b}": BLUE,
                "x_1": RED,
                "y_1": RED,
                "x_2": BLUE,
                "y_2": BLUE
            }
        )
        formula_addon = Tex(
            "=", "-", "\\overrightarrow{b}", "\\times", "\\overrightarrow{a}",
            tex_to_color_map={
                "\\overrightarrow{a}": RED,
                "\\overrightarrow{b}": BLUE,
            }
        ).next_to(formula2[3], DOWN, aligned_edge=LEFT)
        self.play(Write(formula))
        self.wait(1)
        self.play(TransformMatchingTex(formula, formula2))
        self.wait(1)
        self.play(Write(formula_addon))
        self.wait(3)

        self.play(FadeOut(formula2), FadeOut(formula_addon), Uncreate(tip2))
        tip3 = VGroup(
            TexText("第三性质："),
            TexText("叉乘具有分配律"),
            TexText("这就没有上面几个明显了。"),
            TexText("先从代数的角度推一遍：")
        ).fix_in_frame().arrange(DOWN).scale(0.8).to_corner(UL)
        for t in tip3.submobjects:
            t.to_edge(LEFT)
        self.play(Write(tip3))
        self.wait(1)

        color_map = {
            "\\overrightarrow{a}": RED,
            "\\overrightarrow{b}": GREEN,
            "\\overrightarrow{c}": BLUE,
            "x_1": RED,
            "y_1": RED,
            "x_2": GREEN,
            "y_2": GREEN,
            "x_3": BLUE,
            "y_3": BLUE
        }
        formula = VGroup(
            Tex(
                "\\overrightarrow{a}", "\\times",
                "(", "\\overrightarrow{b}", "+", "\\overrightarrow{c}", ")",
                tex_to_color_map = color_map
            ),
            Tex(
                "=", "x_1(y_2+y_3)-(x_2+x_3)y_1",
                isolate=["(", ")"], tex_to_color_map = color_map
            ),
            Tex(
                "=", "\\overrightarrow{a}\\times\\overrightarrow{b} + \\overrightarrow{a}\\times\\overrightarrow{c}",
                tex_to_color_map = color_map
            )
        ).arrange(DOWN)
        for t in formula.submobjects:
            t.to_edge(LEFT)
        formula[0].next_to(formula[1][1], UP, aligned_edge=LEFT)
        formula.move_to([0, -0.6, 0])

        self.play(Write(VGroup(formula[0], formula[1])))
        self.wait(2)

        formula1_trans = Tex(
            "=", "x_1y_2+x_1y_3-x_2y_1-x_3y_1",
            tex_to_color_map = color_map
        ).move_to(formula[1], aligned_edge=LEFT)

        formula1_trans2 = Tex(
            "=", "(x_1y_2-x_2y_1)+(x_1y_3-x_3y_1)",
            tex_to_color_map = color_map
        ).move_to(formula[1], aligned_edge=LEFT)

        self.play(TransformMatchingTex(formula[1], formula1_trans))
        self.wait(3)
        self.play(TransformMatchingTex(formula1_trans, formula1_trans2))
        self.wait(2)
        self.play(Write(formula[2]))
        self.wait(2)
        self.play(Uncreate(VGroup(formula[0], formula[2])), Uncreate(formula1_trans2), Uncreate(tip3[3]))
        
        tip3_1 = VGroup(
            TexText("也许你还没有反应过来，"),
            TexText("那没办法，代数真的太抽象了。"),
            TexText("接下来就通过几何，"),
            TexText("直观地证明一下。")
        ).fix_in_frame().arrange(DOWN).scale(0.8).next_to(tip3[2], DOWN)
        for t in tip3_1.submobjects:
            t.to_edge(LEFT)
        self.play(Write(tip3_1))

        self.camera.frame.move_to([-1, 0.5, 0])

        vecs = np.array([[2, -1, 0], [2, 1, 0], [0, 2, 0]])

        arrow1 = Arrow(ORIGIN, vecs[0], buff=0).set_color(RED)
        arrow2 = Arrow(vecs[0], vecs[0]+vecs[1], buff=0).set_color(GREEN)
        arrow3 = Arrow(ORIGIN, vecs[0]+vecs[1], buff=0).set_color(YELLOW)

        per_vec = Vector(vecs[2], buff=0).set_color(BLUE)

        poly1: Polygon = Polygon(
            ORIGIN, arrow1.get_end(), arrow1.get_end()+per_vec.get_end(), per_vec.get_end(),
            stroke_width=1, color=PINK, fill_color=PINK, fill_opacity=0.6
        )
        poly2: Polygon = Polygon(
            arrow1.get_end(), arrow2.get_end(), arrow2.get_end()+per_vec.get_end(), arrow1.get_end()+per_vec.get_end(),
            stroke_width=1, color=BLUE, fill_color=BLUE, fill_opacity=0.6
        )
        poly3: Polygon = Polygon( 
            ORIGIN, arrow2.get_end(), arrow2.get_end()+per_vec.get_end(), per_vec.get_end(),
            stroke_width=1, color=ORANGE, fill_color=ORANGE, fill_opacity=0.6
        )

        def arrow3_updater_func(m: Arrow, dt):
            m.put_start_and_end_on(ORIGIN, arrow2.get_end())
        arrow3.add_updater(arrow3_updater_func)

        def update_arrow2_func(m: Arrow, dt):
            m.put_start_and_end_on(arrow1.get_end(), arrow1.get_end()+vecs[1])
        arrow2.add_updater(update_arrow2_func)

        def update_polygons(vecs):
            poly1.target = Polygon(
                ORIGIN, vecs[0], vecs[0]+vecs[2], vecs[2],
                stroke_width=1, color=PINK, fill_color=PINK, fill_opacity=0.6
            )
            poly2.target = Polygon(
                vecs[0], vecs[0]+vecs[1], vecs[0]+vecs[1]+vecs[2], vecs[0]+vecs[2],
                stroke_width=1, color=BLUE, fill_color=BLUE, fill_opacity=0.6
            )
            poly3.target = Polygon( 
                ORIGIN, vecs[0]+vecs[1], vecs[0]+vecs[1]+vecs[2], vecs[2],
                stroke_width=1, color=ORANGE, fill_color=ORANGE, fill_opacity=0.6
            )

        geoTotal = VGroup(arrow1, arrow2, arrow3, per_vec, poly1, poly2, poly3)

        self.play(*[ShowCreation(x) for x in [poly1, poly2, poly3, arrow1, arrow2, arrow3, per_vec]])

        new_vec0 = np.array([3, -1, 0])
        arrow1.target = Arrow(ORIGIN, new_vec0, buff=0).set_color(RED)

        update_polygons([new_vec0, vecs[1], vecs[2]])
        self.play(MoveToTarget(arrow1), MoveToTarget(poly1), MoveToTarget(poly2), MoveToTarget(poly3), run_time=3)

        arrow2.remove_updater(update_arrow2_func)
        vecs[0] = new_vec0

        new_vec1 = np.array([1, 2.5, 0])
        arrow2.target = Arrow(vecs[0], vecs[0]+new_vec1, buff=0).set_color(GREEN)

        update_polygons([vecs[0], new_vec1, vecs[2]])
        self.play(MoveToTarget(arrow2), MoveToTarget(poly1), MoveToTarget(poly2), MoveToTarget(poly3), run_time=3)

        vecs[1] = new_vec1

        tip3_2 = VGroup(
            TexText("发现没有？"),
            TexText("粉红色区域", "的面积与", "蓝色区域", "的面积之和，"),
            TexText("始终等于", "橙色区域", "的面积。")
        ).fix_in_frame().arrange(DOWN).next_to(tip3_1, DOWN).to_edge(LEFT)
        for t in tip3_2.submobjects:
            t.to_edge(LEFT)
        tip3_2[1][0].set_color(PINK)
        tip3_2[1][2].set_color(BLUE)
        tip3_2[2][1].set_color(ORANGE)
        self.play(Write(tip3_2))

        tip3_3 = TexText("虽说还有种例外情况，").fix_in_frame().scale(0.8).next_to(tip3_2, DOWN).to_edge(LEFT)
        self.play(Write(tip3_3))

        new_vec1 = np.array([-0.5, 2.5, 0])
        arrow2.target = Arrow(vecs[0], vecs[0]+new_vec1, buff=0).set_color(GREEN)

        update_polygons([vecs[0], new_vec1, vecs[2]])
        self.play(MoveToTarget(arrow2), MoveToTarget(poly1), MoveToTarget(poly2), MoveToTarget(poly3), run_time=3)

        vecs[1] = new_vec1

        tip3_4 = TexText("但不要忘记叉积的正负自动摆平了这个问题。").fix_in_frame().scale(0.8).next_to(tip3_3, RIGHT)
        self.play(Write(tip3_4))
        self.play(Indicate(tip3_4))

        self.wait(5)

        self.play(Uncreate(geoTotal), FadeOut(VGroup(tip3, tip3_1, tip3_2, tip3_3, tip3_4)))
        self.camera.frame.to_default_state()

        tip4 = VGroup(
            TexText("第四性质："),
            TexText("单次叉乘与数乘间存在结合律"),
            TexText("鉴于这个特别好理解，这里就仅放公式证明。")
        ).fix_in_frame().arrange(DOWN).to_corner(UL)
        for t in tip4.submobjects:
            t.to_edge(LEFT)

        self.play(Write(tip4))
        self.wait(2)

        color_map = {
            "\\overrightarrow{a}": RED,
            "\\overrightarrow{b}": BLUE,
            "x_1": RED,
            "y_1": RED,
            "x_2": BLUE,
            "y_2": BLUE
        }
        formula4 = VGroup(
            Tex(
                "(k\\overrightarrow{a}) \\times \\overrightarrow{b}",
                isolate = ["(", ")"],
                tex_to_color_map = color_map
            ),
            Tex(
                "=", "(kx_1)y_2-x_2(ky_1)",
                isolate = ["(", ")"],
                tex_to_color_map = color_map
            ),
            Tex(
                "=", "\\overrightarrow{a} \\times (k\\overrightarrow{b})",
                isolate = ["(", ")"],
                tex_to_color_map = color_map
            )
        ).arrange(DOWN).to_edge(LEFT)
        for t in formula4.submobjects:
            t.to_edge(LEFT)
        formula4[0].move_to(formula4[1], aligned_edge=LEFT, coor_mask=np.array([1, 0, 0]))
        formula4.center()

        self.play(Write(formula4[0]))
        self.wait(1)
        self.play(Write(formula4[1]))
        self.wait(1)

        formula4_1_new = Tex(
            "=", "x_1(ky_2)-(kx_2)y_1",
            isolate = ["(", ")"],
            tex_to_color_map = color_map
        )
        self.play(TransformMatchingTex(formula4[1], formula4_1_new))
        self.wait(1)
        self.play(Write(formula4[2]))
        self.wait(3)

        self.play(*[FadeOut(x) for x in self.mobjects if not isinstance(x, CameraFrame)])
        self.camera.frame.to_default_state()

        chapter_ending = VGroup(
            TexText("希望你记住了这四个性质。"),
            TexText("接下来，这四个性质会被频繁使用，"),
            TexText("我也不会再特别说明。")
        ).arrange(DOWN)
        self.play(Write(chapter_ending))
        self.showCountdown(3)
        self.play(FadeOut(chapter_ending))


    def showCountdown(self, seconds):
        countDownObj = Tex(str(seconds), color=BLUE).to_corner(DR)

        self.play(Write(countDownObj))
        self.wait(0.25)

        for i in range(seconds-1, -1, -1):
            newObj = Tex(str(i), color=BLUE).to_corner(DR)
            self.play(Transform(countDownObj, newObj))
            self.wait(0.25)

        self.play(FadeOut(countDownObj))
        