from manimlib import *

class ALGInequality(Scene):
    def construct(self):
        self.showTitle()
        text0 = TexText(
            """
            \\textup{先给出结论} \\\\
            \\textup{当} $a>0, b>0$ \\textup{时}
            """
        )
        text1 = Tex("\\sqrt{ab} \\le \\frac{a-b}{\\ln a -\\ln b} \\le \\frac{a+b}{2}", color=BLUE)
        text2 = TexText(
            """
            \\textup{当且仅当a=b时，等号成立（对数平均取极限）} \\\\
            \\textup{接下来将给出证明过程}
            """
        )
        text0.next_to(text1, UP)
        text2.next_to(text1, DOWN)
        text = VGroup(text0, text1, text2).center()

        self.play(Write(text))
        self.wait(2)
        self.play(Uncreate(text))
        self.wait()

        self.alProof()
        self.glProof()
        self.equalProof()

        tfw = TexText("\\textup{Thanks for watching!}")
        self.play(Write(tfw))
        self.wait(5)
        self.play(FadeOut(tfw))

    def showTitle(self):
        title0 = TexText("\\textup{对数平均不等式}")
        title1 = TexText("\\textup{A-L-G Inequality}")
        title1.next_to(title0, DOWN)
        titleGroup = VGroup(title0, title1)
        titleGroup.center()
        self.play(Write(titleGroup))
        self.wait()
        self.play(FadeOut(titleGroup))

    def alProof(self):
        title = TexText("\\textup{Part I. 对数均值与算术均值的大小关系}")
        title.to_corner(LEFT+UP)

        t0_0 = TexText("\\textup{先证明：当} $a>0, b>0$ \\textup{时，}")
        t0_1 = TexText("$\\frac{a-b}{\\ln a - \\ln b} < \\frac{a+b}{2}$", color=RED_A)
        t0_1.next_to(t0_0, RIGHT)
        t0 = VGroup(t0_0, t0_1)
        t0.next_to(title, DOWN).to_edge(LEFT)

        self.play(Write(title))
        self.play(Write(t0))
        self.wait()

        t1_0 = TexText("\\textup{当} $a \\ne b$ \\textup{时，不妨令}")
        t1_1 = TexText("$a>b>0$", color=GREEN_B)
        t1_1.next_to(t1_0, RIGHT)
        t1 = VGroup(t1_0, t1_1)
        t1.next_to(t0, DOWN).to_edge(LEFT)
        self.play(Write(t1))
        self.wait()

        tCenter_0 = Tex("\\frac{a-b}{\\ln a - \\ln b} < \\frac{a+b}{2}")
        tCenter_1 = Tex("\\frac{a-b}{\\ln a - \\ln b} < \\frac{a+b}{2}", color=BLUE_B)
        tCenter_1_L = TexText("\\textup{即证：}")
        tCenter_1.next_to(tCenter_0, DOWN)
        tCenter = VGroup(tCenter_0, tCenter_1)
        tCenter.center()

        tCenter_1_L.next_to(tCenter_1, LEFT, buff=1.5)
        tCenter_0_L = TexText("\\textup{要证：}").next_to(tCenter_0, LEFT, buff=1.5)
        tCenter.add(tCenter_1_L, tCenter_0_L)

        self.play(Write(tCenter))
        self.wait()

        tc1 = Tex("\\frac{a-b}{\\ln{\\frac{a}{b}}}} < \\frac{a+b}{2}", color=BLUE_B).move_to(tCenter_1)
        self.play(TransformMatchingShapes(tCenter_1, tc1))
        self.wait()

        tc2 = Tex("\\frac{\\frac{a}{b}-1}{\\ln{\\frac{a}{b}}} < \\frac{\\frac{a}{b}+1}{2}", color=BLUE_B).move_to(tc1)
        self.play(TransformMatchingShapes(tc1, tc2))
        self.wait()

        swapUnknown = TexText("\\textup{不妨设} $t=\\frac{a}{b}$ \\textup{，则有} $t>1$").next_to(tc2, DOWN)
        self.play(Write(swapUnknown))
        self.play(swapUnknown.scale, 0.6, swapUnknown.to_corner, LEFT+DOWN)
        self.wait()

        tc3 = TexText("$\\frac{t-1}{\\ln t} < \\frac{t+1}{2}$", color=BLUE_B).scale(1.5).move_to(tc2)

        self.play(TransformMatchingShapes(tc2, tc3))
        self.wait()

        tc3Supp = TexText("\\textup{此时，由于} $t=\\frac{a}{b}$ \\textup{且} $a>b>0$ \\textup{易得到：} $t>1, \\ln t > 0$")
        tc3Supp.next_to(tc3, DOWN)

        self.play(ShowCreation(tc3Supp))
        self.wait(2)
        self.play(FadeOut(tc3Supp))

        tc4 = Tex("\\frac{2(t-1)}{t+1}", "<", "\\ln t", color=BLUE_B).move_to(tc3)
        self.play(TransformMatchingShapes(tc3, tc4))

        tc5 = Tex("\\ln t", ">", "\\frac{2(t-1)}{t+1}", color=BLUE_B).move_to(tc4)
        self.play(TransformMatchingTex(tc4, tc5))

        tc6 = Tex("\\ln t", ">", "2", "-", "\\frac{4}{t+1}", color=BLUE_B).move_to(tc5)
        self.play(TransformMatchingTex(tc5, tc6))

        tc7 = Tex("\\ln t", "+", "\\frac{4}{t+1}" ">", "2", color=BLUE_B).move_to(tc6)
        self.play(TransformMatchingTex(tc6, tc7))

        self.play(FadeOut(t0), t1.next_to, title, DOWN, t1.to_edge, LEFT)

        tCenter_0.generate_target()
        tCenter_0.target.next_to(t1, DOWN)
        tCenter_0_L.generate_target()
        tCenter_0_L.target.next_to(tCenter_0.target, LEFT).to_edge(LEFT)
        tCenter_0.target.next_to(tCenter_0_L.target, RIGHT)
        tc7.generate_target()
        tc7.target.next_to(tCenter_0.target, DOWN)
        tCenter_1_L.generate_target()
        tCenter_1_L.target.next_to(tc7.target, LEFT).to_edge(LEFT)

        tc7.target.next_to(tCenter_1_L.target, RIGHT)

        self.play(
            MoveToTarget(tCenter_0_L),
            MoveToTarget(tCenter_1_L),
            MoveToTarget(tCenter_0),
            MoveToTarget(tc7)
        )

        gx_set = TexText("\\textup{设}")
        gx_formula = Tex("g(t)=\\ln t+\\frac{4}{t+1}", color=BLUE).next_to(gx_set, RIGHT)
        gx = VGroup(gx_set, gx_formula)
        gx.next_to(tc7, DOWN).to_edge(LEFT)

        self.play(Write(gx))

        gdx_set = TexText("\\textup{则}")
        gdx_formula = Tex("g'(t)=\\frac{1}{t}-\\frac{4}{(t+1)^2}", color=GREEN).next_to(gdx_set, RIGHT)
        gdx = VGroup(gdx_set, gdx_formula)
        gdx.next_to(gx, DOWN).to_edge(LEFT)

        self.play(Write(gdx))

        gdx_f_1 = Tex("g'(t)=\\frac{(t+1)^2-4t}{t(t+1)^2}", color=GREEN).next_to(gdx_set, RIGHT)
        gdx_f_2 = Tex("g'(t)=\\frac{(t-1)^2}{t(t+1)^2}", color=GREEN).next_to(gdx_set, RIGHT)

        self.play(TransformMatchingShapes(gdx_formula, gdx_f_1))
        self.play(TransformMatchingShapes(gdx_f_1, gdx_f_2))

        gdx_judge = Tex(">0", color=RED).next_to(gdx_f_2, RIGHT)

        self.play(Write(gdx_judge))
        self.wait()
        self.play(Transform(gdx_judge, TexText("\\textup{单调递增}", color=RED).next_to(gx, RIGHT)), FadeOut(gdx_set), FadeOut(gdx_f_2))

        g1c_0 = Tex("\\because g(1)=\\frac{4}{2}=2 \\therefore g(t)>2", color=BLUE).next_to(gx, DOWN)
        g1c_1 = TexText("$\\therefore$ \\textup{所证成立}").next_to(g1c_0, RIGHT)
        g1c = VGroup(g1c_0, g1c_1)
        g1c.to_edge(LEFT)
        self.play(Write(g1c))

        axes = Axes((-0.2,3), (-1,1.2))
        axes.scale(0.4)
        axes.add_coordinate_labels()
        
        axes.to_edge(RIGHT)

        self.play(Write(axes))

        gx_graph = axes.get_graph(
            lambda t: math.log(t) + (4/(t+1)) - 2,
            x_range=(0.05,3),
            color=BLUE
        )
        gx_label = axes.get_graph_label(gx_graph, "g(x)-2")

        self.play(ShowCreation(gx_graph), Write(gx_label))
        self.wait()
        self.play(
            FadeOut(title),
            FadeOut(t1),
            FadeOut(gx),
            FadeOut(gdx_judge),
            FadeOut(VGroup(tCenter_0, tCenter_0_L, tCenter_1_L, tc7)),
            FadeOut(axes),
            FadeOut(gx_graph),
            FadeOut(gx_label),
            FadeOut(g1c),
            FadeOut(swapUnknown)
        )

    def glProof(self):
        title = TexText("\\textup{Part II. 对数均值与几何均值的大小关系}")
        title.to_corner(LEFT+UP)

        proof0_L = TexText("\\textup{要证：}")
        proof0_R = Tex("\\sqrt{ab}", "<", "\\frac{a-b}{\\ln a - \\ln b}", color=GREEN).next_to(proof0_L, RIGHT)
        proof0 = VGroup(proof0_L, proof0_R).next_to(title, DOWN).to_edge(LEFT)

        self.play(Write(title))
        self.play(Write(proof0))

        proof1_L = TexText("\\textup{即证：}")
        proof1_R = Tex("\\sqrt{ab}", "<", "\\frac{a-b}{\\ln a - \\ln b}", color=RED_B).next_to(proof1_L, RIGHT)
        proof1 = VGroup(proof1_L, proof1_R).next_to(proof0, DOWN).to_edge(LEFT)

        self.play(Write(proof1))
        self.wait()

        supp0 = TexText("\\textup{照例，不妨设} $a>b>0$", color=BLUE_B).next_to(proof0, RIGHT)
        self.play(Write(supp0))
        self.wait()

        proof1_R_t1 = Tex("\\sqrt{ab}", "<", "\\frac{a-b}{\\ln{\\frac{a}{b}}}", color=RED_B).next_to(proof1_L, RIGHT)
        proof1_R_t2 = Tex("\\frac{\\sqrt{ab}}{b}", "<", "\\frac{\\frac{a}{b}-1}{\\ln{\\frac{a}{b}}}", color=RED_B).next_to(proof1_L, RIGHT)
        proof1_R_t3 = Tex("\\sqrt{\\frac{a}{b}}", "<", "\\frac{\\frac{a}{b}-1}{\\ln{\\frac{a}{b}}}", color=RED_B).next_to(proof1_L, RIGHT)

        self.play(TransformMatchingShapes(proof1_R, proof1_R_t1))
        self.play(TransformMatchingShapes(proof1_R_t1, proof1_R_t2))
        self.play(TransformMatchingShapes(proof1_R_t2, proof1_R_t3))
        self.wait()

        p1_supp = TexText("\\textup{设} $t=\\sqrt{\\frac{a}{b}}$ \\textup{，有} $t>1$", color=MAROON_C).next_to(proof1_R_t3, RIGHT).to_edge(RIGHT)
        self.play(Write(p1_supp))
        self.wait()

        proof1_R_t4 = Tex("t", "< ", "\\frac{t^2-1}{\\ln{t^2}}", color=RED_B).next_to(proof1_L, RIGHT)
        proof1_R_t5 = Tex("t", "< ", "\\frac{t^2-1}{2\\ln t}", color=RED_B).next_to(proof1_L, RIGHT)
        proof1_R_t6 = Tex("2t\\ln t", "< ", "t^2", "-", "1", color=RED_B).next_to(proof1_L, RIGHT)
        proof1_R_t7 = Tex("2t\\ln t", "-", "t^2", "+", "1", "< ", "0", color=RED_B).next_to(proof1_L, RIGHT)
        
        self.play(TransformMatchingShapes(proof1_R_t3, proof1_R_t4))
        self.play(TransformMatchingShapes(proof1_R_t4, proof1_R_t5))
        self.play(TransformMatchingTex(proof1_R_t5, proof1_R_t6))
        self.play(TransformMatchingTex(proof1_R_t6, proof1_R_t7))

        proof1.remove(proof1_R)
        proof1.add(proof1_R_t7)

        hx_L = TexText("\\textup{设}")
        hx_R = Tex("h(t)=2t\\ln t -t^2+1", color=BLUE_B).next_to(hx_L, RIGHT)
        hx = VGroup(hx_L, hx_R).next_to(proof1, DOWN).to_edge(LEFT)

        hdx_L = TexText("\\textup{则有}")
        hdx_R = Tex("h'(t)", "=", "2", "(", "\\ln t ", "+", "1", ")", "-", "2", "t", color=BLUE).next_to(hdx_L, RIGHT)
        hdx = VGroup(hdx_L, hdx_R).next_to(hx, DOWN).to_edge(LEFT)

        self.play(Write(hx))
        self.play(Write(hdx))

        hdx_R_t1 = Tex("h'(t)", "=", "2", "(", "\\ln t ", "-", "t", "+", "1", ")", color=BLUE).next_to(hdx_L, RIGHT)
        hdx_R_t2 = Tex("h'(t)", "=", "2", "[", "\\ln t ", "-", "(", "t", "-", "1", ")", "]", color=BLUE).next_to(hdx_L, RIGHT)

        self.play(TransformMatchingTex(hdx_R, hdx_R_t1))
        self.play(TransformMatchingTex(hdx_R_t1, hdx_R_t2))
        self.wait()

        hdx.remove(hdx_R)
        hdx.add(hdx_R_t2)

        we_know_L = TexText("\\textup{我们熟知，}")
        we_know_R = Tex("\\ln t \\le t-1", color=GREEN_C).next_to(we_know_L, RIGHT)
        we_know = VGroup(we_know_L, we_know_R).next_to(hdx, DOWN).to_edge(LEFT)
        we_know_D = TexText("\\textup{如右图：}").next_to(we_know_L, DOWN).to_edge(LEFT)
        we_know.add(we_know_D)

        self.play(Write(we_know))

        axes = Axes((0, 2), (-1, 2))
        axes.scale(0.4)
        axes.to_corner(RIGHT+DOWN)
        axes.add_coordinate_labels()

        self.play(Write(axes))

        axes_curve_log = axes.get_graph(
            lambda x: math.log(x),
            x_range=(0.3, 2),
            color=BLUE,
        )
        axes_curve_n = axes.get_graph(
            lambda x: x-1,
            #x_range=(-0.2, 2),
            color=RED
        )
        axes_curve_log_label = axes.get_graph_label(axes_curve_log, "\\ln t")
        axes_curve_n_label = axes.get_graph_label(axes_curve_n, "t-1")
        axes_curve_log_label.next_to(axes_curve_n_label, DOWN, buff=1)
        axes_curves = VGroup(axes_curve_log, axes_curve_n,  axes_curve_log_label, axes_curve_n_label)

        self.play(ShowCreation(axes_curves))
        self.wait()

        judgement = Tex("\\le 0", color=RED).next_to(hdx, RIGHT)
        self.play(Write(judgement))
        self.play(Transform(judgement, TexText("\\textup{单调递减}", color=RED).next_to(hx, RIGHT)))
        self.play(FadeOut(axes), FadeOut(axes_curves), FadeOut(we_know), FadeOut(hdx))

        conclusion_L = Tex("\\because h(1)=-1+1=0", color=BLUE)
        conclusion_R = Tex("\\therefore h(t)<0", color=GREEN).next_to(conclusion_L, RIGHT)
        conclusion = VGroup(conclusion_L, conclusion_R).next_to(hx, DOWN).to_edge(LEFT)

        self.play(Write(conclusion))

        end_text = TexText("\\textup{故原命题得证}").next_to(conclusion, DOWN).to_edge(LEFT)

        self.play(Write(end_text))

        axes2 = Axes((0, 3), (-2, 1))
        axes2.scale(0.5)
        axes2.to_corner(RIGHT+DOWN)
        axes2.add_coordinate_labels()

        axes2_h = axes2.get_graph(
            lambda t: 2*t*math.log(t)-(t**2)+1,
            x_range=(0.2, 3),
            color=BLUE
        )

        axes2_h_label = axes2.get_graph_label(axes2_h, "h(x)")

        self.play(Write(axes2))
        self.play(ShowCreation(axes2_h), Write(axes2_h_label))
        self.wait(3)

        self.play(FadeOut(axes2), FadeOut(axes2_h), FadeOut(axes2_h_label))
        self.play(FadeOut(end_text), FadeOut(conclusion), FadeOut(judgement), FadeOut(hx), FadeOut(title), FadeOut(proof0), FadeOut(proof1), FadeOut(supp0), FadeOut(p1_supp))

    def equalProof(self):
        title = TexText("\\textup{Part III. } $a=b$ \\textup{时的特殊情况}")
        title.to_corner(LEFT+UP)

        self.play(Write(title))

        ctx = TexText("\\textup{由于} \\\\ $\\lim_{a \\to x, b \\to x}{\\frac{a-b}{\\ln a - \\ln b}}=x$ \\\\ \\textup{故} $a=b$ \\textup{时两侧等号成立} \\\\ \\textup{所以当且仅当} $a=b$ \\textup{时，等号成立}")
        self.play(Write(ctx))
        self.wait(4)
        self.play(Uncreate(ctx))
        self.play(FadeOut(title))