from manimlib import *
import numpy as np

CYAN, MAGENTA = "#0BE3FB", "#C820E3"

# MathematRcal calculations needed
def norm(vec):
    sqSum = 0
    for n in vec:
        sqSum += n**2
    return np.math.sqrt(sqSum)

def normalize(vec) :
    return vec / norm(vec)

def angle_raw(dotO, dotA):
    return np.math.atan2((dotA-dotO)[1], (dotA-dotO)[0])

def angle_diff(dotO, dotA, dotB):
    return np.abs(angle_raw(dotO, dotA)-angle_raw(dotO, dotB))

def foot_point(d0, dl0, dl1):
    vecc = dl1-dl0
    vecs = d0-dl0
    projection = np.dot(vecc, vecs) / norm(vecc)
    vecdiff = projection*normalize(vecc)
    return dl0+vecdiff

def construct_arc(dotO, dotA, dotB, radius=0.5):
    return Arc(
        radius=radius, 
        arc_center=dotO, 
        start_angle=np.min([angle_raw(dotO, dotA), angle_raw(dotO, dotB)]), 
        angle=angle_diff(dotO, dotA, dotB)
        )

def outer_point(a,b,c):
    a1 = b[0] - a[0]
    b1 = b[1] - a[1]
    c1 = (a1*a1 + b1*b1)/2
    a2 = c[0] - a[0]
    b2 = c[1] - a[1]
    c2 = (a2*a2 + b2*b2)/2
    d = a1*b2 - a2*b1
    return np.array([a[0] + (c1*b2 - c2*b1)/d, a[1] + (a1*c2 -a2*c1)/d])


class SineTheoremOptimizedTriangle(VGroup):
    def __init__(self, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        Ac, Bc, Cc = DOWN+2*LEFT, DOWN+2*RIGHT, UP*1.5+RIGHT
        Pc, Qc, Rc = foot_point(Cc, Ac, Bc), foot_point(Ac, Bc, Cc), foot_point(Bc, Ac, Cc)
        poly = Polygon(Ac,Bc,Cc)
        A,B,C,P, Q, R = Dot(Ac), Dot(Bc), Dot(Cc), Dot(Pc), Dot(Qc), Dot(Rc)
        CG, AH, BI = Line(Cc, Pc), Line(Ac, Qc), Line(Bc, Rc)
        ABCGHI = VGroup(A,B,C,P, Q, R)
        alpha = construct_arc(Ac, Bc, Cc, radius=0.5)
        beta = construct_arc(Bc, Ac, Cc, radius=0.3)
        gamma = construct_arc(Cc, Ac, Bc, radius=0.2)
        ABCGHI.set_color(RED)
        P.set_color(GREEN)
        Q.set_color(YELLOW)
        R.set_color(MAROON)
        CG.set_color(GREEN)
        AH.set_color(YELLOW)
        BI.set_color(MAROON)
        alpha.set_color(PURPLE)
        beta.set_color(ORANGE)
        gamma.set_color(CYAN)

        tagA, tagB, taPc = TexText("$A$"), TexText("$B$"), TexText("$C$")
        tagP, tagQ, tagR = TexText("$P$"), TexText("$Q$"), TexText("$R$")
        tagAlpha, tagBeta, tagGamma = TexText("$\\alpha$"), TexText("$\\beta$"), TexText("$\\gamma$")
        tagA.next_to(A, direction=DOWN)
        tagB.next_to(B, direction=DOWN)
        taPc.next_to(C, direction=UP)
        tagP.next_to(P, direction=DOWN)
        tagQ.next_to(Q, direction=RIGHT)
        tagR.next_to(R, direction=UP+0.1*LEFT)
        tagAlpha.next_to(alpha, direction=RIGHT)
        tagBeta.next_to(beta, direction=LEFT)
        tagGamma.next_to(gamma, direction=DOWN)
        tagA.set_color(RED)
        tagB.set_color(RED)
        taPc.set_color(RED)
        tagP.set_color(GREEN)
        tagQ.set_color(YELLOW)
        tagR.set_color(MAROON)
        tagAlpha.set_color(PURPLE)
        tagBeta.set_color(ORANGE)
        tagGamma.set_color(CYAN)
        self.add(ABCGHI, CG, AH, BI, alpha, beta, gamma, poly)
        self.add(tagA, tagB, taPc, tagP, tagQ, tagR, tagAlpha, tagBeta, tagGamma)


class SineTheorem(Scene):
    def construct(self):
        title = TexText("\\textup{正弦定理}")
        subtitle = Text("The Law of Sines")
        subtitle.next_to(title, direction=DOWN)
        titleGroup = VGroup(title, subtitle)
        titleGroup.center()
        self.play(Write(titleGroup))
        self.wait()
        self.play(FadeOut(titleGroup))

        tri = SineTheoremOptimizedTriangle()
        self.play(ShowCreation(tri))
        self.wait()
        self.play(ApplyMethod(tri.to_corner, LEFT+UP))
        explain1 = TexText("$|CP|=|AC|\\sin \\alpha$", color=GREEN)
        explain2 = TexText("$|AQ|=|AB|\\sin \\beta$", color=YELLOW)
        explain3 = TexText("$|BR|=|BC|\\sin \\gamma$", color=MAROON)
        explain1.next_to(tri, direction=DOWN)
        explain2.next_to(explain1, direction=DOWN)
        explain3.next_to(explain2, direction=DOWN)
        explainGroup = VGroup(explain1, explain2, explain3)
        self.play(Write(explainGroup))

        sqex = TexText(
            """
            \\begin{equation}
            \\begin{aligned}
            S_{\\Delta ABC} &=\\frac{1}{2}|AB||CP|\\\\
                            &=\\frac{1}{2}|BC||AQ|\\\\
                            &=\\frac{1}{2}|AC||BR|
            \\nonumber
            \\end{aligned}
            \\end{equation}
            """,
            color=WHITE
        )
        sqex.next_to(tri, direction=RIGHT)
        sqex2 = TexText(
            """
            \\begin{equation}
            \\begin{aligned}
            S_{\\Delta ABC} &=\\frac{1}{2}|AB||AC|\\sin \\alpha\\\\
                            &=\\frac{1}{2}|BC||AB|\\sin \\beta \\\\
                            &=\\frac{1}{2}|AC||BC|\\sin \\gamma
            \\nonumber
            \\end{aligned}
            \\end{equation}
            """,
            color=WHITE
        )
        sqex2.next_to(tri, direction=RIGHT)
        self.play(Write(sqex))
        self.wait()
        self.play(TransformMatchingShapes(sqex, sqex2))
        self.wait()

        chainEquality = TexText("$|AB||AC|\\sin \\alpha = |BC||AB|\\sin \\beta = |AC||BC| \\sin \\gamma$", color=WHITE)
        chainEquality.scale(0.7)
        chainEquality.next_to(tri, direction=RIGHT)
        self.play(TransformMatchingShapes(sqex2, chainEquality))
        self.wait()

        expChain = TexText("\\textup{将上述连等式除以}$|AB||AC||BC|$\\textup{，即得：}")
        halfCon = TexText("$\\frac{\\sin \\alpha}{|BC|} = \\frac{\\sin \\beta}{|AC|} = \\frac{\\sin \\gamma}{|AB|}$")
        expHalfCon = TexText("\\textup{此时对每一项取倒数，可得到}")
        sineTheoremEquality = TexText("$\\frac{|BC|}{\\sin \\alpha} = \\frac{|AC|}{\\sin \\beta} = \\frac{|AB|}{\\sin \\gamma}$")
        expChain.scale(0.8)
        expChain.next_to(chainEquality, direction=DOWN)
        halfCon.next_to(expChain, direction=DOWN)
        expHalfCon.scale(0.8)
        expHalfCon.next_to(halfCon, direction=DOWN)

        halfConclusionGroup = VGroup(chainEquality, expChain, halfCon, expHalfCon)
        sineTheoremEquality.next_to(expHalfCon, direction=DOWN)
        self.play(Write(expChain))
        self.play(Write(halfCon))
        self.play(Write(expHalfCon))
        self.play(Write(sineTheoremEquality))
        self.wait()
        conclusion = TexText("\\textup{正弦定理}")
        conclusionGroup = VGroup(conclusion, sineTheoremEquality)
        self.play(FadeOut(tri), FadeOut(explainGroup), FadeOut(halfConclusionGroup))
        self.play(sineTheoremEquality.center, sineTheoremEquality.scale, 2)
        self.play(Write(conclusion), sineTheoremEquality.next_to, conclusion, DOWN)
        self.play(conclusionGroup.center)

        self.wait(5)
        self.play(FadeOut(conclusionGroup))


class CosineTheoremOptimizedTriangle(VGroup):
    def __init__(self, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        Ac, Bc, Cc = DOWN+LEFT, 0.5*UP+1.5*RIGHT, UP
        Hc = foot_point(Cc, Ac, Bc)
        A, B, C, H = Dot(Ac), Dot(Bc), Dot(Cc), Dot(Hc)
        ABCH = VGroup(A, B, C, H)
        ABCH.set_color(RED_A)
        H.set_color(MAGENTA)

        CH = Line(Cc, Hc, color=MAGENTA)

        tagA, tagB, tagC, tagH = TexText("$A$"), TexText("$B$"), TexText("$C$"), TexText("$H$")
        tagA.next_to(A, direction=LEFT)
        tagB.next_to(B, direction=RIGHT)
        tagC.next_to(C, direction=UP)
        tagH.next_to(H, direction=DOWN)
        tags = VGroup(tagA, tagB, tagC, tagH)
        tags.set_color(RED_A)
        tagH.set_color(MAGENTA)

        AB = Line(Ac, Bc, color=BLUE)
        BC = Line(Bc, Cc, color=RED)
        AC = Line(Ac, Cc, color=GREEN)
        tagAB = TexText("$c$", color=BLUE)
        tagBC = TexText("$a$", color=RED)
        tagAC = TexText("$b$", color=GREEN)
        tagAB.next_to(AB, direction=(DOWN+RIGHT)/3, buff=-2)
        tagBC.next_to(BC, direction=UP, buff=0)
        tagAC.next_to(AC, direction=(LEFT+UP)/3, buff=-1)

        self.add(ABCH, CH, tags, AB, BC, AC, tagAB, tagBC, tagAC)

class CosineTheorem(Scene):
    def construct(self):
        title = TexText("\\textup{余弦定理}")
        subtitle = Text("The Law of Cosines")
        subtitle.next_to(title, direction=DOWN)
        titleGroup = VGroup(title, subtitle)
        titleGroup.center()
        self.play(Write(titleGroup))
        self.wait()
        self.play(FadeOut(titleGroup))

        tri = CosineTheoremOptimizedTriangle()
        self.play(ShowCreation(tri))
        self.play(tri.to_corner, LEFT+UP)

        tex1 = TexText("$|CH|=b\\sin A$", color=MAGENTA)
        tex2 = TexText(
            """
            \\begin{equation}
            \\begin{aligned}
            |BH|&=c-|AH| \\\\
                &=c-b\\cos A \\\\
            \\nonumber
            \\end{aligned}
            \\end{equation}
            """,
            color=BLUE
        )

        tex1.next_to(tri, DOWN)
        tex2.next_to(tex1, DOWN)
        
        self.play(Write(tex1))
        self.play(Write(tex2))

        rightExp1 = TexText(
            """
            \\begin{equation}
            \\begin{aligned}
            a^2 &=|BH|^2+|CH|^2 \\\\
                &=(c-b\\cos A)^2+b^2\\sin^2 A \\\\
                &=c^2+b^2\\cos^2 A -2bc\\cos A +b^2\\sin^2 A \\\\
                &=b^2+c^2-2bc\\cos A
            \\nonumber
            \\end{aligned}
            \\end{equation}
            """
        )
        rightExp1.next_to(tri, RIGHT)
        rightExp2 = TexText("$a^2=b^2+c^2-2bc\\cos A$", color=RED)
        rightText = TexText("\\textup{将上式变形：}")
        rightExp3 = TexText("$a^2=b^2+c^2-2bc\\cos A$", color=RED)
        rightExp3Replacement = TexText("$\\cos A = \\frac{b^2+c^2-a^2}{2bc}$", color=RED)
        rightExp2.next_to(rightExp1, DOWN)
        rightText.next_to(rightExp2, DOWN)
        rightExp3.next_to(rightText, DOWN)
        rightExp3Replacement.next_to(rightText, DOWN)
        
        self.play(Write(rightExp1))
        self.wait(6)
        self.play(Write(rightExp2))
        self.play(Write(rightText))
        self.play(ShowCreation(rightExp3))
        self.play(TransformMatchingShapes(rightExp3, rightExp3Replacement))
        self.wait()

        self.play(FadeOut(tri), FadeOut(tex1), FadeOut(tex2), FadeOut(rightExp1), FadeOut(rightText))

        round1A = rightExp2
        round1B = TexText("$b^2=a^2+c^2-2ac\\cos B$", color=GREEN)
        round1C = TexText("$c^2=a^2+b^2-2ab\\cos C$", color=BLUE)

        round2A = rightExp3Replacement
        round2B = TexText("$\\cos B = \\frac{a^2+c^2-b^2}{2ac}$", color=GREEN)
        round2C = TexText("$\\cos C = \\frac{a^2+b^2-c^2}{2ab}$", color=BLUE)

        round1A.generate_target()
        round2A.generate_target()

        swapText = TexText("\\textup{经过轮换后可以得到}").to_edge(UP)
        round1A.target.next_to(swapText, DOWN)
        round1B.next_to(round1A.target, DOWN)
        round1C.next_to(round1B, DOWN)
        round2A.target.next_to(round1C, DOWN)
        round2B.next_to(round2A.target, DOWN)
        round2C.next_to(round2B, DOWN)

        finalText = TexText("\\textup{以上为余弦定理公式}")
        finalText.next_to(round2C, DOWN)

        rounds = VGroup(swapText, round1A.target, round1B, round1C, round2A.target, round2B, round2C, finalText)
        rounds.center()
        rounds.remove(round1A.target, round2A.target)

        self.play(MoveToTarget(round1A), MoveToTarget(round2A))
        self.play(Write(rounds))
        rounds.add(round1A, round2A)
        self.wait(5)
        self.play(FadeOut(rounds))
        self.wait()
