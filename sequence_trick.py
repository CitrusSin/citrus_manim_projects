from manimlib import *


languageText = {
    "CH":{
        "title": "虚数在数列中的妙用",
        "questionPrev": "\\textup{开头先来思考一道题：}",
        "question": "\\textup{已知数列} $\\{a_{n}\\}$ \\textup{满足} \\\\ $a_{n+2}=2a_{n+1}-2a_{n},a_{1}=1,a_{2}=2$ \\textup{求} $\\{a_{n}\\}$ \\textup{通项公式}",
        "intro1": "\\textup{如你所见，这个数列乍一看就很怪。} \\\\ \\textup{若我们写出它的前十项，你会得到如下结果：}",
        "intro2": "\\textup{虽然这个数列的规律很好看出来，但要用通项公式描述并不容易。} \\\\ \\textup{这个数列不仅有正负交替，还时不时冒出个0，} \\\\ \\textup{即使你归纳出了它的通项公式，也很难严谨地证明它。}",
        "introAdd": "\\textup{试着去求一下它的通项公式！}",
        "solveMark": "\\textup{解：}",
        "expIsomor1": 
                    """
                    \\textup{这里我们可以同构来构造等比数列} \\\\
                    \\textup{思路和斐波那契数列通项推导过程相同}
                    """,
        "solve1Stuck": "\\textup{判别式小于0，我们碰到了死胡同（貌似？）}",
        "transition11": 
                    """
                    \\textup{我们才刚开始动笔，怎么可以退缩？！} \\\\
                    \\textup{既然题目向我们示威，我们也是时候拿起更高级的武器了！}
                    """,
        "transition12": "\\textup{若我们将目光投射到数轴之外的虚数上，} \\\\ \\textup{又会有什么收获呢？}",
        "solve2GetEquations": "\\textup{然后我们便得到了以下两个等式}",
        "getGeneralTerm": "\\textup{我们便得到了}$\\{a_{n}\\}$\\textup{的通项公式}",
        "transition21": 
                    """
                    \\textup{但是等等！} \\\\
                    \\textup{如你所见，刚才的通项公式中包含了虚数} \\\\
                    \\textup{但是，这个数列里面全都是实数，没有虚数！}
                    """,
        "transition22":
                    """
                    \\textup{其实，虽然通项公式中含有虚数，} \\\\
                    \\textup{但将它实际应用于计算时，无论n取何值，} \\\\
                    \\textup{最终答案的虚部都将消为0，也与递推关系不冲突。} \\\\
                    \\textup{那么，能否使用不含虚数的表达式表达它的通项公式呢？}
                    """,
        "simplifyTitle": "\\textup{通项公式的化简}",
        "simplifyText11": "\\textup{其实懂的人已经知道了，} \\\\ \\textup{这个东西和} $\\sin x$ \\textup{的欧拉公式表达式长得很像}",
        "simplifyText12": "\\textup{但为了照顾知识储备少的同学，} \\\\ \\textup{这里用不超过高中数学水平的方式来讲解一遍。}",
        "deMoivreTheorem1": 
                    """
                    \\textup{简单介绍一下棣莫弗定理} \\\\
                    \\textup{对于两个复数}
                    """,
        "deMoivreTheorem2": "\\textup{有}",
        "deMoivreTheoremExp": 
                    """
                    \\textup{翻译成人话就是} \\\\
                    \\textup{两个复数相乘，模长相乘，幅角相加} \\\\
                    """,
        "useTheorem1": 
                    """
                    \\textup{不难看出，若对一个复数取n次方，} \\\\
                    \\textup{模长也变为原来的n次方，} \\\\
                    \\textup{而幅角翻n倍。} \\\\
                    """,
        "meaning": "\\textup{这也就意味着}",
        "final": "\\textup{最终我们得到简洁的通项公式}",
        "thanksForWatching": "\\textup{感谢观看！}",
        "let": "\\textup{令}",
        "conclude": "\\textup{可以推出}",
        "obviously": "\\textup{显然}"
    },
    "EN":{
        "title": "A clever use of imaginary numbers in sequence",
        "questionPrev": "\\textup{Think about a question before the video: }",
        "question": "\\textup{A sequence} $\\{a_{n}\\}$ \\textup{satisfies} $a_{n+2}=2a_{n+1}-2a_{n},a_{1}=1,a_{2}=2$ \\\\ \\textup{Try to find the general term of } $\\{a_{n}\\}$",
        "intro1": "\\textup{As you see, this sequence looks weird.} \\\\ \\textup{If you write down it's first 10 terms}",
        "intro2": "\\textup{It's not easy to describe its pattern by a general term formula.} \\\\ \\textup{And it's even harder to prove it}",
        "introAdd": "\\textup{Let's try to find its general term formula!}",
        "solveMark": "\\textup{Solve：}",
        "expIsomor1": 
                    """
                    \\textup{We can construct a geometric series by isomorphism,} \\\\
                    \\textup{just as how the general term of Fibonacci sequence was found.}
                    """,
        "solve1Stuck": "\\textup{The discriminant is negative! What to do next?}",
        "transition11": 
                    """
                    \\textup{Try to use an advanced tool!}
                    """,
        "transition12": "\\textup{If we look at imaginary numbers,} \\\\ \\textup{What will we get?}",
        "solve2GetEquations": "\\textup{And we get these 2 equations below}",
        "getGeneralTerm": "\\textup{And we get the general term formula of }$\\{a_{n}\\}$",
        "transition21": 
                    """
                    \\textup{But wait!} \\\\
                    \\textup{As you see, there're imaginary numbers in the formula.} \\\\
                    \\textup{It's weird that all terms are real numbers} \\\\
                    \\textup{And imaginary numbers are in the formula.}
                    """,
        "transition22":
                    """
                    \\textup{In fact,} \\\\
                    \\textup{All these imaginary numbers get eliminated when calculating.} \\\\
                    \\textup{So, can we find a formula without imaginary numbers?}
                    """,
        "simplifyTitle": "\\textup{Simplification of the general term}",
        "simplifyText11": "\\textup{This formula looks so similar} \\\\ \\textup{to the imaginary expression of } $\\sin x$",
        "simplifyText12": "\\textup{But in consideration of those whose math is not good,} \\\\ \\textup{I'll explain it in a simpler way}",
        "deMoivreTheorem1": 
                    """
                    \\textup{Introduce De Moivre's formula briefly:} \\\\
                    \\textup{For two complex numbers}
                    """,
        "deMoivreTheorem2": "\\textup{We have}",
        "deMoivreTheoremExp": 
                    """
                    \\textup{In short,} \\\\
                    \\textup{Lengths multiply and arguments add} \\\\ \\textup{when two complex numbers multiply.} \\\\
                    """,
        "useTheorem1": 
                    """
                    \\textup{Obviously, if we get the n-th power of a complex number,} \\\\
                    \\textup{the length will be n-th powered too,} \\\\
                    \\textup{while the argument will be multiplied by n.} \\\\
                    """,
        "meaning": "\\textup{Which means}",
        "final": "\\textup{Finally, we get a simplified general term formula}",
        "thanksForWatching": "\\textup{Thanks for watching!}",
        "let": "\\textup{Let}",
        "conclude": "\\textup{We can conclude}",
        "obviously": "\\textup{Obviously, }"
    }
}


DSBLUE, HPINK, CRIMSON, ROYALBLUE = "#00BFFF", "#FF69B4", "#DC143C", "#4169E1"


class Mark(VGroup):
    def __init__(self, title, letObj, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.letMark = TexText(title).next_to(letObj, LEFT)
        self.add(self.letMark, letObj)


class SeqTrick(Scene):
    def construct(self):
        self.allowedWaiting = True
        self.language = languageText["EN"] # Switch the language by modifying here (CH, EN)
        self.title()
        self.showQuestion()
        self.introduction()
        self.solveGeneralTerm1()
        self.transition()
        self.solveGeneralTerm2()
        self.transition2()
        self.simplify()
        self.thanks()

    def title(self):
        text = TexText(self.language["title"])
        self.play(Write(text))
        self.wait(5)
        self.play(FadeOut(text))

    def thanks(self):
        text = TexText(self.language["thanksForWatching"])
        self.play(Write(text))
        self.wait(5)
        self.play(FadeOut(text))

    def simplify(self):
        simplifyTitle = TexText(self.language["simplifyTitle"]).to_corner(UL)
        self.play(Write(simplifyTitle))

        gtFormula = Tex("a_{n}=\\frac{(1+i)^{n}-(1-i)^{n}}{2i}", color=DSBLUE).scale(0.7).next_to(simplifyTitle, DOWN).to_edge(LEFT)
        self.play(Write(gtFormula))

        simText11 = TexText(self.language["simplifyText11"])
        sinEqu = Tex("\\sin x = \\frac{e^{ix}-e^{-ix}}{2i}", color=GREEN_B).next_to(simText11, DOWN)
        simText12 = TexText(self.language["simplifyText12"]).next_to(sinEqu, DOWN)
        simText1 = VGroup(simText11, sinEqu, simText12).center()
        
        self.play(Write(simText1))
        self.wait(5)
        self.play(Uncreate(simText1))
        self.wait(1)

        zColorMap = {
            "\\theta_{1}": DSBLUE,
            "\\theta_{2}": ORANGE,
            "r_{1}": DSBLUE,
            "r_{2}": ORANGE,
            "z_{1}": DSBLUE,
            "z_{2}": ORANGE
        }
        deMoivreTheorem1 = TexText(self.language["deMoivreTheorem1"])
        z1 = Tex("z_{1}=r_{1}(\\cos \\theta_{1} + i\\sin \\theta_{1})", tex_to_color_map=zColorMap).next_to(deMoivreTheorem1, DOWN)
        z2 = Tex("z_{2}=r_{2}(\\cos \\theta_{2} + i\\sin \\theta_{2})", tex_to_color_map=zColorMap).next_to(z1, DOWN)
        deMoivreTheorem2 = TexText(self.language["deMoivreTheorem2"]).next_to(z2, DOWN)
        z1z2 = Tex(
            "z_{1}z_{2}=r_{1}r_{2}(\\cos \\theta_{1} + i\\sin \\theta_{1})(\\cos \\theta_{2} + i\\sin \\theta_{2})",
            tex_to_color_map=zColorMap
        ).next_to(deMoivreTheorem2, DOWN)
        deMoivreTheorem = VGroup(deMoivreTheorem1, z1, z2, deMoivreTheorem2, z1z2).center()

        z1z2Second = Tex(
            "z_{1}z_{2}=r_{1}r_{2}[(\\cos \\theta_{1} \\cos \\theta_{2} - \\sin \\theta_{1} \\sin \\theta_{2})+i(\\sin \\theta_{1} \\cos \\theta_{2} + \\cos \\theta_{1} \\sin \\theta_{2})]",
            isolate={"(", ")", "[", "]"},
            tex_to_color_map=zColorMap
        ).scale(0.8).move_to(z1z2)
        z1z2Final = Tex(
            "z_{1} z_{2} = r_{1} r_{2} [ \\cos (\\theta_{1}+\\theta_{2}) + i \\sin (\\theta_{1}+\\theta_{2}) ]",
            isolate={"(", ")", "[", "]"},
            tex_to_color_map=zColorMap
        ).move_to(z1z2)

        deMoivreTheoremExp = TexText(self.language["deMoivreTheoremExp"])
        
        self.play(Write(deMoivreTheorem))
        self.wait(1)
        self.play(TransformMatchingTex(z1z2, z1z2Second))
        self.wait(1)
        self.play(TransformMatchingTex(z1z2Second, z1z2Final))

        deMoivreTheorem.remove(z1z2)
        deMoivreTheorem.add(z1z2Final)

        self.wait(5)
        self.play(FadeOut(deMoivreTheorem))
        self.play(FadeIn(deMoivreTheoremExp))
        self.wait(5)
        self.play(FadeOut(deMoivreTheoremExp))
        self.wait(1)

        useTheorem = TexText(self.language["useTheorem1"])
        self.play(FadeIn(useTheorem))
        self.wait(2)
        self.play(FadeOut(useTheorem))

        imTexColors = {
            "1+i": DSBLUE,
            "1-i": HPINK,
        }
        
        meaning = TexText(self.language["meaning"]).next_to(gtFormula, DOWN)
        self.play(Write(meaning))

        triEqu1 = Tex(
            "1+i=\\sqrt{2}(\\cos\\frac{\\pi}{4}+i\\sin\\frac{\\pi}{4})",
            isolate={"(", ")", "\\frac{\\pi}{4}"},
            tex_to_color_map=imTexColors
        )
        triEqu2 = Tex(
            "1-i=\\sqrt{2}(\\cos\\frac{\\pi}{4}-i\\sin\\frac{\\pi}{4})",
            isolate={"(", ")", "\\frac{\\pi}{4}"},
            tex_to_color_map=imTexColors
        ).next_to(triEqu1, DOWN)
        triEqu = VGroup(triEqu1, triEqu2).center()

        triEqu12 = Tex(
            "(1+i)", "^{n}", "=\\sqrt{2}", "^{n}", "(\\cos\\frac{\\pi}{4}+i\\sin\\frac{\\pi}{4})", "^{n}",
            isolate={"(", ")", "[", "]", "\\frac{\\pi}{4}"},
            tex_to_color_map=imTexColors
        ).move_to(triEqu1).set_color_by_tex("^{n}", ORANGE, substring=False)
        triEqu22 = Tex(
            "(1-i)", "^{n}", "=\\sqrt{2}", "^{n}", "(\\cos\\frac{\\pi}{4}-i\\sin\\frac{\\pi}{4})", "^{n}",
            isolate={"(", ")", "[", "]", "\\frac{\\pi}{4}"},
            tex_to_color_map=imTexColors
        ).move_to(triEqu2).set_color_by_tex("^{n}", ORANGE, substring=False)

        triEqu13 = Tex(
            "(1+i)", "^{n}", "=\\sqrt{2}", "^{n}", "[", "\\cos(\\frac{\\pi}{4}", "n", ")", "+i\\sin", "(", "\\frac{\\pi}{4}", "n", ")]",
            isolate={"(", ")", "[", "]", "\\frac{\\pi}{4}"},
            tex_to_color_map=imTexColors
        ).move_to(triEqu1).set_color_by_tex_to_color_map({"^{n}": ORANGE, "n": ORANGE}, substring=False)
        triEqu23 = Tex(
            "(1-i)", "^{n}", "=\\sqrt{2}", "^{n}", "[", "\\cos(\\frac{\\pi}{4}", "n", ")", "-i\\sin", "(", "\\frac{\\pi}{4}", "n", ")]",
            isolate={"(", ")", "[", "]", "\\frac{\\pi}{4}"},
            tex_to_color_map=imTexColors
        ).move_to(triEqu2).set_color_by_tex_to_color_map({"^{n}": ORANGE, "n": ORANGE}, substring=False)

        self.play(Write(triEqu))
        self.wait(2)
        self.play(TransformMatchingTex(triEqu1, triEqu12), TransformMatchingTex(triEqu2, triEqu22))
        self.wait(2)
        self.play(TransformMatchingTex(triEqu12, triEqu13), TransformMatchingTex(triEqu22, triEqu23))
        self.wait(2)

        triEquT3 = VGroup(triEqu13, triEqu23)
        triEquT3.generate_target()
        triEquT3.target.next_to(gtFormula, aligned_edge=UP)
        meaning.generate_target()
        meaning.target.set_color(RED)
        self.play(MoveToTarget(triEquT3), MoveToTarget(meaning))

        finalEqu = Tex(
            "2ia", "_{n}", "=\\sqrt{2}", "^{n}", "[\\cos(\\frac{\\pi}{4}", "n", ")+i\\sin(\\frac{\\pi}{4}", "n", ")-\\cos(\\frac{\\pi}{4}", "n", ")+i\\sin(\\frac{\\pi}{4}", "n", ")]",
            isolate={"(", ")", "[", "]", "\\frac{\\pi}{4}", "2i"}
        ).set_color_by_tex_to_color_map({"^{n}": ORANGE, "n": ORANGE, "_{n}": ORANGE}, substring=False)
        finalEqu2 = Tex(
            "2ia", "_{n}", "=2i\\sqrt{2}", "^{n}", "\\sin(\\frac{\\pi}{4}", "n", ")",
            isolate={"(", ")", "[", "]", "\\frac{\\pi}{4}", "2i"}
        ).set_color_by_tex_to_color_map({"^{n}": ORANGE, "n": ORANGE, "_{n}": ORANGE}, substring=False)
        finalEqu3 = Tex(
            "a", "_{n}", "=\\sqrt{2}", "^{n}", "\\sin(\\frac{\\pi}{4}", "n", ")",
            isolate={"(", ")", "[", "]", "\\frac{\\pi}{4}", "2i"}
        ).set_color_by_tex_to_color_map({"^{n}": ORANGE, "n": ORANGE, "_{n}": ORANGE}, substring=False)

        self.play(Write(finalEqu))
        self.wait(2)
        self.play(TransformMatchingTex(finalEqu, finalEqu2))
        self.wait(2)
        self.play(TransformMatchingTex(finalEqu2, finalEqu3))
        self.wait(2)

        actList = list()
        for obj in self.get_mobjects():
            if obj != finalEqu3:
                actList.append(FadeOut(obj))
        self.play(*actList)

        finalText = TexText(self.language["final"]).next_to(finalEqu3, UP)
        finalTextSet = VGroup(finalText, finalEqu3.generate_target()).center()

        self.play(MoveToTarget(finalEqu3), Write(finalText))
        self.showCountdown(5)
        self.clearScreenByFadingOut()

    def transition2(self):
        transi1 = TexText(self.language["transition21"])
        transi2 = TexText(self.language["transition22"])

        self.play(FadeIn(transi1))
        self.showCountdown(5)
        self.play(FadeOut(transi1))
        self.play(FadeIn(transi2))
        self.showCountdown(5)
        self.play(FadeOut(transi2))
        self.wait(1)

    def solveGeneralTerm2(self):
        isolateDict = {"a_{n+2}", "a_{n+1}", "a_{n}"}
        texColors = {
            "\\lambda": ORANGE,
            "(2-\\lambda)": GREEN,
            "\\frac{2}{2-\\lambda}": ORANGE,
            "1+i": DSBLUE,
            "1-i": HPINK,
            "p": ROYALBLUE,
            "q": CRIMSON
        }

        question = TexText(self.language["question"]).scale(0.5).to_corner(LEFT+UP)
        solveMark = TexText(self.language["solveMark"], color=RED_A).next_to(question, DOWN).to_edge(LEFT)
        equ = Tex("a_{n+2} - \\lambda a_{n+1} = (2-\\lambda)(a_{n+1}- \\frac{2}{2-\\lambda} a_{n})",
            isolate=isolateDict,
            tex_to_color_map=texColors
        ).next_to(solveMark, RIGHT)
        lamEqu = Tex("\\lambda^{2}-2\\lambda +2=0",
            isolate={"\\lambda"},
            tex_to_color_map=texColors
        ).next_to(equ, DOWN)

        self.play(Write(question), Write(solveMark), Write(equ), Write(lamEqu))
        self.wait(2)

        lambdaSolve = Tex("\\lambda_{1}=1-i,\\lambda_{2}=1+i", tex_to_color_map=texColors).next_to(lamEqu, DOWN)

        self.play(FadeIn(lambdaSolve, UP))
        self.wait(2)

        equExp = TexText(self.language["solve2GetEquations"]).next_to(lambdaSolve, DOWN)

        equ1 = Tex("a_{n+2}-(1-i)a_{n+1}=(1+i)[a_{n+1}-(1-i)a_{n}]", isolate=isolateDict, tex_to_color_map=texColors)
        equ2 = Tex("a_{n+2}-(1+i)a_{n+1}=(1-i)[a_{n+1}-(1+i)a_{n}]", isolate=isolateDict, tex_to_color_map=texColors).next_to(equ1, DOWN)
        totalEqu = VGroup(equ1, equ2).next_to(equExp, DOWN)

        self.play(Write(equExp))
        self.play(Write(totalEqu))
        self.wait(3)

        totalEqu.generate_target()
        totalEqu.target.scale(0.7).next_to(solveMark, RIGHT+DOWN)

        self.play(FadeOut(equ), FadeOut(lamEqu), FadeOut(lambdaSolve), FadeOut(equExp), MoveToTarget(totalEqu))
        self.wait(1)

        nseq1 = Tex("p_{n}=a_{n+1}-(1-i)a_{n}", isolate=isolateDict, tex_to_color_map=texColors)
        nseq2 = Tex("q_{n}=a_{n+1}-(1+i)a_{n}", isolate=isolateDict, tex_to_color_map=texColors).next_to(nseq1, DOWN)
        nseq = VGroup(nseq1, nseq2)

        letMark = Mark(self.language["let"], nseq).scale(0.7).next_to(totalEqu, RIGHT)

        self.play(Write(letMark))
        self.wait(2)

        nseqc1 = Tex("p_{n+1}=(1+i)p_{n},p_{1}=1+i", isolate=isolateDict, tex_to_color_map=texColors)
        nseqc2 = Tex("q_{n+1}=(1-i)q_{n},q_{1}=1-i", isolate=isolateDict, tex_to_color_map=texColors).next_to(nseqc1, DOWN)
        nseqc = VGroup(nseqc1, nseqc2)
        concludeMark = Mark(self.language["conclude"], nseqc).next_to(totalEqu, DOWN)

        self.play(Write(concludeMark))
        self.wait(2)

        nseqc1b = Tex("p_{n}=(1+i)^{n}", isolate=isolateDict, tex_to_color_map=texColors).move_to(nseqc1)
        nseqc2b = Tex("q_{n}=(1-i)^{n}", isolate=isolateDict, tex_to_color_map=texColors).move_to(nseqc2)

        self.play(Transform(nseqc1, nseqc1b), Transform(nseqc2, nseqc2b))
        self.wait(2)

        equMinus = Tex("p_{n}-q_{n}=2ia_{n}=(1+i)^{n}-(1-i)^{n}", isolate=isolateDict, tex_to_color_map=texColors)
        lastMark = Mark(self.language["obviously"], equMinus).next_to(concludeMark, DOWN, buff=0.6).to_edge(LEFT)

        equMinus2 = Tex("a_{n}=\\frac{(1+i)^{n}-(1-i)^{n}}{2i}", color=DSBLUE).next_to(lastMark.letMark, RIGHT)
        finalConclusion = TexText(self.language["getGeneralTerm"]).next_to(equMinus2, DOWN)

        self.play(Write(lastMark))
        self.wait(2)
        self.play(TransformMatchingTex(equMinus, equMinus2), Write(finalConclusion))
        self.showCountdown(5)
        act_list = list()
        for obj in self.get_mobjects():
            if obj != equMinus2 and obj != finalConclusion:
                act_list.append(Uncreate(obj))
        self.play(*act_list)

        equMinus2.generate_target()
        finalConclusion.generate_target()
        finalConclusion.target.next_to(equMinus2.target, UP)
        targetVG = VGroup(equMinus2.target, finalConclusion.target)
        targetVG.center()

        self.play(MoveToTarget(equMinus2), MoveToTarget(finalConclusion))
        self.wait(5)
        self.clearScreenByFadingOut()
        self.wait(1)

    def transition(self):
        transi1 = TexText(self.language["transition11"])
        tExpandingNum = Tex("\\mathbb{R} \\to \\mathbb{C}",
            tex_to_color_map={
                "\\mathbb{R}": ORANGE,
                "\\mathbb{C}": MAROON_B
            }
        ).scale(1.5).next_to(transi1, DOWN)
        transi2 = TexText(self.language["transition12"]).next_to(tExpandingNum, DOWN)

        textGroup = VGroup(transi1, tExpandingNum, transi2).center()

        self.play(Write(textGroup))
        self.wait(5)
        self.clearScreenByUncreate()

    def solveGeneralTerm1(self):
        question = TexText(self.language["question"]).scale(0.5).to_corner(LEFT+UP)
        self.play(Write(question))
        self.wait(1)

        solveMark = TexText(self.language["solveMark"], color=RED_A).next_to(question, DOWN).to_edge(LEFT)
        self.play(Write(solveMark))

        isolateDict = {"a_{n+2}", "a_{n+1}", "a_{n}"}
        lambdaTexColors = {
            "\\lambda": ORANGE,
            "(2-\\lambda)": GREEN,
            "\\frac{2}{2-\\lambda}": ORANGE
        }

        equ = Tex("a_{n+2}=2a_{n+1}-2a_{n}", isolate=isolateDict)
        equ2 = Tex("a_{n+2} - \\lambda a_{n+1} = (2-\\lambda)a_{n+1}-2a_{n}",
            isolate=isolateDict,
            tex_to_color_map=lambdaTexColors
        )
        equ3 = Tex("a_{n+2} - \\lambda a_{n+1} = (2-\\lambda)(a_{n+1}- \\frac{2}{2-\\lambda} a_{n})",
            isolate=isolateDict,
            tex_to_color_map=lambdaTexColors
        )
        exp1 = TexText(self.language["expIsomor1"]).next_to(equ, UP, buff=0.5)

        self.play(Write(exp1))
        self.wait(1)
        self.play(Write(equ))
        self.wait(2)
        self.play(TransformMatchingTex(equ, equ2))
        self.wait(2)
        self.play(TransformMatchingTex(equ2, equ3))
        self.wait(2)
        self.play(FadeOut(exp1))
        self.play(equ3.next_to, solveMark, RIGHT)

        lamEqu = Tex("\\lambda = \\frac{2}{2-\\lambda}", isolate={"\\lambda"}, tex_to_color_map=lambdaTexColors)
        let1 = Mark(self.language["let"], lamEqu).next_to(equ3, DOWN)

        lamEqu2 = Tex("2\\lambda - \\lambda^{2}=2",
            isolate={"\\lambda"},
            tex_to_color_map=lambdaTexColors
        ).next_to(let1.letMark, RIGHT)
        lamEqu3 = Tex("\\lambda^{2}-2\\lambda +2=0",
            isolate={"\\lambda"},
            tex_to_color_map=lambdaTexColors
        ).next_to(let1.letMark, RIGHT)
        deltaExp = Tex("\\Delta= -4", tex_to_color_map={"-4": RED}).next_to(lamEqu3, DOWN)

        solveStuck = TexText(self.language["solve1Stuck"], color=RED).next_to(deltaExp, DOWN)

        self.play(Write(let1))
        self.wait(2)
        self.play(TransformMatchingTex(lamEqu, lamEqu2))
        self.play(TransformMatchingTex(lamEqu2, lamEqu3))
        self.play(Write(deltaExp))
        self.wait(2)
        self.play(Write(solveStuck))

        self.wait(4)
        self.clearScreenByFadingOut()

    def showQuestion(self):
        questionText = TexText(self.language["question"])
        questionTextPrev = TexText(self.language["questionPrev"]).next_to(questionText, UP)
        VGroup(questionText, questionTextPrev).center()

        self.play(Write(questionTextPrev), Write(questionText))
        self.showCountdown(10)
        self.clearScreenByFadingOut()

    def introduction(self):
        nums = Tex("\\{1, 2, 2, 0, -4, -8, -8, 0, 16, 32\\}", color=BLUE)
        introText1 = TexText(self.language["intro1"]).next_to(nums, UP)
        introText2 = TexText(self.language["intro2"]).scale(0.7).next_to(nums, DOWN)
        introText = VGroup(introText1, nums, introText2)

        introText.generate_target()
        introTextAddition = TexText(self.language["introAdd"], color=RED_C).next_to(introText.target, DOWN)
        VGroup(introText.target, introTextAddition).center()

        self.play(FadeIn(introText))
        self.wait(5)
        self.play(MoveToTarget(introText))
        self.play(Write(introTextAddition))
        self.wait(1)
        self.clearScreenByFadingOut()

    def showCountdown(self, seconds):
        countDownObj = Tex(str(seconds), color=DSBLUE).to_corner(RIGHT+DOWN)

        self.play(Write(countDownObj))
        self.wait(0.25)

        for i in range(seconds-1, -1, -1):
            newObj = Tex(str(i), color=DSBLUE).to_corner(RIGHT+DOWN)
            self.play(Transform(countDownObj, newObj))
            self.wait(0.25)

        self.play(FadeOut(countDownObj))

    def clearScreenByFadingOut(self):
        act_list = list()
        for obj in self.get_mobjects():
            act_list.append(FadeOut(obj))
        self.play(*act_list)

    def clearScreenByUncreate(self):
        act_list = list()
        for obj in self.get_mobjects():
            act_list.append(Uncreate(obj))
        self.play(*act_list)

    def wait(self, duration=DEFAULT_WAIT_TIME, stop_condition=None):
        if self.allowedWaiting:
            return super().wait(duration, stop_condition)
