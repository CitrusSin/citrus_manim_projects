from typing import Literal
from manimlib import *


languageText = {
    "CH":{
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
        "let": "\\textup{令}",
        "conclude": "\\textup{可以推出}",
        "obviously": "\\textup{显然}"
    },
    "EN":{
        "questionPrev": "\\textup{Think about a question before the video: }",
        "question": "\\textup{A sequence} $\\{a_{n}\\}$ \\textup{satisfies} $a_{n+2}=2a_{n+1}-2a_{n},a_{1}=1,a_{2}=2$ \\\\ \\textup{Try to find the general term of } $\\{a_{n}\\}$",
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
        self.language = languageText["CH"] # Switch the language by modifying here (CH, EN)
        #self.showQuestion()
        #self.introduction()
        #self.solveGeneralTerm1()
        #self.transition()
        self.solveGeneralTerm2()

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
        equ = Tex("a_{n+2} - \\lambda a_{n+1} = (2-\\lambda)(a_{n+1}+ \\frac{2}{2-\\lambda} a_{n})",
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
        finalConclusion = TexText(self.language["getGeneralTerm"]).next_to(equMinus2, RIGHT)

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

        equ = Tex("a_{n+2}=2a_{n+1}+2a_{n}", isolate=isolateDict)
        equ2 = Tex("a_{n+2} - \\lambda a_{n+1} = (2-\\lambda)a_{n+1}+2a_{n}",
            isolate=isolateDict,
            tex_to_color_map=lambdaTexColors
        )
        equ3 = Tex("a_{n+2} - \\lambda a_{n+1} = (2-\\lambda)(a_{n+1}+ \\frac{2}{2-\\lambda} a_{n})",
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
        countDownObj = Tex(str(seconds), color=RED).to_corner(RIGHT+DOWN)

        self.play(Write(countDownObj))
        self.wait(1)

        for i in range(seconds-1, -1, -1):
            newObj = Tex(str(i), color=RED).to_corner(RIGHT+DOWN)
            self.play(Transform(countDownObj, newObj))
            self.wait(0.5)

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
