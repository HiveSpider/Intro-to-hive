from hive_engine import *
from manim import *
from functools import reduce


class opening(MovingCameraScene):
    def construct(self):
        self.add_sound(".\\media\\narration\\Meet the Soldier p1.wav")
        width = 0.8 * self.camera.frame.get_width()
        self.camera.frame.set_width(width)
        self.camera.frame.move_to(DOWN*2)
        g = game(self, tile_size=1)
        g.make_moves('wP,wG1 wP-,bA1 /wP,bG1 wP\\,wQ -wP,bB1 wP/,wL wG1-,bQ wL-,bG2 bQ/,wS1 bG2/,wA1 bG2-,bA2 wQ/,bP -wQ,bS1 /wQ,wA2 wA1/,wA3 -wS1'.split(','))
        g.set_tile_positions()
        self.add(*g.get_live_tiles())
        lb= g.bugs['bL'].tile
        self.add(lb)
        lb.move_to(g.get_location('bG1\\'))
        lb.set_z_index(100)
        self.wait(1.5)
        tiles = VGroup(*g.get_live_tiles())
        lb.add_updater(lambda mob, dt: mob.rotate(dt*18*DEGREES/0.25*2/1.09))
        self.play(

            AnimationGroup(Succession(
            AnimationGroup(
                 Succession(
                     ScaleInPlace(lb, 1),
                     ScaleInPlace(lb,1.2),ScaleInPlace(lb, 1/1.2),
                     ScaleInPlace(lb,1.2),ScaleInPlace(lb, 1/1.2), run_time=1.1),
           
AnimationGroup(
            MoveAlongPath(tiles,Line(tiles.get_center(),tiles.get_center() + DOWN*3**0.5/2 + RIGHT/2)),
            self.camera.frame.animate.move_to(DOWN*3**0.5/2 + RIGHT/2+DOWN*2),
           run_time = 1
)), AnimationGroup(
                 Succession(
                     ScaleInPlace(lb,1.2),ScaleInPlace(lb, 1/1.2),
                     ScaleInPlace(lb,1.2),ScaleInPlace(lb, 1/1.2),
                     ScaleInPlace(lb,1.2),ScaleInPlace(lb, 1/1.2), run_time=1.1),
           
AnimationGroup(
            MoveAlongPath(tiles,Line(tiles.get_center() + DOWN*3**0.5/2 + RIGHT/2,tiles.get_center() + DOWN*3**0.5/2 + RIGHT/2 +  RIGHT)),
            self.camera.frame.animate.move_to(DOWN*3**0.5/2 + RIGHT/2 + RIGHT+DOWN*2),
            run_time = 1
)), AnimationGroup(
                 Succession(
                   ScaleInPlace(lb,1.3),ScaleInPlace(lb, 1/1.3), run_time=1.02),
           
AnimationGroup(
            MoveAlongPath(tiles,Line(tiles.get_center() + DOWN*3**0.5/2 + RIGHT/2 + RIGHT,tiles.get_center()  +  RIGHT*2)),
            self.camera.frame.animate.move_to(RIGHT*2+DOWN*2),
            run_time = 0.88
))
            ),
            ))
        
        lb.clear_updaters()
        lb.rotate(-PI/3)
        wA1 = g.bugs['wA1'].tile
        self.play(MoveAlongPath(wA1,CubicBezier(wA1.get_center(),wA1.get_center()+g.right_basis-g.up_basis,wA1.get_center()-g.up_basis*(5) - g.right_basis*2,wA1.get_center()-g.up_basis*(4) - g.right_basis*3)), rate_func=rate_functions.rush_into)

        self.wait(0.2)
        self.camera.frame.move_to(g.bugs['bB1'].tile.get_center()).set_width(self.camera.frame.get_width()*0.75)
        self.wait(0.1)

        bS1=g.bugs['bS2'].tile
        spot=g.bugs['bB1'].tile.get_center()+g.up_basis
        bS1.move_to(spot+4*UP)
        g.bugs['bS2'].svg_bug.rotate(-5*PI/6,about_point=spot+4*UP)
        line = Line(spot+4*UP, spot+8*UP)
        bS1.z_index=1
        
        wA3= g.bugs['wA3'].tile
        self.play(
            VGroup(bS1, line).animate.shift(DOWN*4))
        self.play(FadeOut(line), run_time=0.2)
        self.play(MoveAlongPath(wA3, Line(wA3.get_center(), wA3.get_center()-g.right_basis*2+g.up_basis), rate_func=rate_functions.rush_into, run_time=0.3))

        self.wait(0.2)
        self.camera.frame.move_to(g.bugs['bP'].tile.get_center()+g.up_basis -g.right_basis).set_width(self.camera.frame.get_width()*0.75)
        self.wait(0.2)
        
        bB2=g.bugs['bB2'].tile
        bB2.move_to(g.bugs['bP'].tile.get_center()+g.up_basis-g.right_basis)
        g.bugs['bB2'].svg_bug.rotate(-PI/3,about_point=bB2.get_center())
        self.play(FadeIn(bB2,scale=3, run_time=0.6))
        b2svg = g.bugs['bB2'].svg_bug
        self.play(LaggedStart(
        AnimationGroup(MoveAlongPath(b2svg,CubicBezier(b2svg.get_center(),b2svg.get_center()+RIGHT/7,b2svg.get_center()+RIGHT/7,b2svg.get_center())), run_time=0.4),
        AnimationGroup(MoveAlongPath(g.bugs['wA2'].tile,ArcBetweenPoints(g.bugs['wA2'].tile.get_center(),g.bugs['bB2'].tile.get_center()+g.up_basis,angle=TAU/2)),rate_func=rate_functions.rush_into, run_time=0.5),
        lag_ratio=0.3
        ))
        self.wait(0.3)
        self.play(FadeOut(Group(*self.mobjects),run_time=0.3))
        self.play(FadeIn(Text("Meet The Soldier (Ant)").move_to(self.camera.frame.get_center()).scale(0.7)))
        self.wait(4)

class move_game_like_vgroup(Scene):
    def talk(self, tile, time, scale_value=1.1):
       self.play(ScaleInPlace(tile, scale_value, run_time = time / 2))
       self.play(ScaleInPlace(tile, 1/scale_value, run_time = time / 2))
    def construct(self):
        
        self.add_sound(".\\media\\narration\\Meet the Soldier p2.wav")
        g = hive_game(self, tile_size = 4)
        g.make_moves('bQ,bS1 bQ-,bA1 -bQ,bG1 bS1-,bB1 -bA1'.split(','))
        g.set_tile_positions()
        VGroup(*g.get_live_tiles()).to_edge(DOWN).shift(4*DOWN+2*RIGHT)
        ant_tile = g.bugs['wA1'].tile
        self.add(ant_tile)
        ant_tile.rotate(-2*PI/3)
        monologue_1 = [[0.35, 1.3],
                       [0.3],
                       [0.15],
                       [0.19],
                       [0.16],
                       [0.13],
                       [0.13],
                       [0.2],
                       [0.1],
                       [0.1],
                       [0.1],
                       [0.1],
                       [0.5,1.24],
                       [0.2],
                       [0.2],
                       [0.2],
                       [0.4, 1.5],
                       ]
        j = 0
        move_right_func = lambda mob, dt: mob.shift(dt * RIGHT)
        for i in monologue_1:
            j += 1
            if j == 2:
                ant_tile.add_updater(move_right_func)
            if j == len(monologue_1) - 1:
                ant_tile.remove_updater(move_right_func)
            self.talk(ant_tile, *i)

        self.wait(1)
        self.play(Rotate(ant_tile, -PI/2, run_time = 0.2))

        monologue_2 = [
            [0.2],
            [0.3],
            [0.18],
            [0.25],
            [0.3,1],
            [0.1, 1.04],
            [0.3, 1.13],
            [0.4],
            [0.16],
            [0.16],
            [0.16],
            [0.26, 1.23],
            [0.3],
            [0.22],
            [0.25],
            [0.32],
            [0.26],
            [0.19],
            [0.3,1],
            [0.3,1],
            [0.3],
            [0.4],
            [0.3],
            [0.2],
            [0.2],
            [0.2],
            [0.14],
            [0.14],
            [0.14],
            
        ]
        j = 0

        for i in monologue_2:
            j += 1
            if j == 19:
                self.play(MoveAlongPath(ant_tile, Line(ant_tile.get_center(), ant_tile.get_center() + DOWN)), run_time = i[0], rate_func = rate_functions.rush_from)
            elif j == 20:
                self.play(MoveAlongPath(ant_tile, Line(ant_tile.get_center(), ant_tile.get_center() + UP)), run_time = i[0], rate_func = rate_functions.rush_from)
            else:
                self.talk(ant_tile, *i)

        self.wait(0.1)
        self.play(Rotate(ant_tile, PI/3), run_time=0.2)

        monologue_3 = [
            [0.3],
            [0.2],
            [0.3],
            [0.25],
            [0.2, 1.3],
            [0.15],
            [0.14],
            [0.17],
            [0.18],
            [0.24, 1.2],
            [0.12],
            [0.16],
            [0.25],
            [0.23],
            [0.3, 1.26],
            [0.15],
            [0.12],
            [0.18],
            [0.2, 1.06],
            [0.18],
            [0.15, 1.2],
            [0.2],
        ]
        j = 0
        rotate_func = lambda mob, dt : mob.rotate(-dt*120*DEGREES/0.25)
        for i in monologue_3:
            j += 1
            if j==4:
                ant_tile.add_updater(rotate_func)
            elif j==5:
                ant_tile.remove_updater(rotate_func)
            self.talk(ant_tile, *i)
        self.wait(1)

class battle1(MovingCameraScene):
    def construct(self):
        self.add_sound(".\\media\\narration\\Meet the Soldier p3.wav")
        g = hive_game(self)
        wA1=g.bugs['wA1'].tile
        self.add(g.bugs['wA1'].tile)
        wA1.rotate(-PI/6)
        wA1.scale(2)
        self.play(wA1.animate.shift(UP+LEFT/2).rotate(PI/5), run_time=0.2)
        self.play(wA1.animate.shift(DOWN+RIGHT/2).rotate(-PI/5), run_time=0.2)
        self.play(wA1.animate.shift(UP+RIGHT/2).rotate(-PI/5), run_time=0.2)
        self.play(wA1.animate.shift(DOWN+LEFT/2).rotate(PI/5), run_time=0.2)
        self.play(wA1.animate.shift(UP+LEFT/2).rotate(PI/5), run_time=0.2)
        self.play(wA1.animate.shift(DOWN+RIGHT/2).rotate(-PI/5), run_time=0.2)
        self.wait(0.2)
        self.play(Wiggle(wA1, 1.3, 0.03*TAU, n_wiggles=2), run_time=0.4)
        self.play(MoveAlongPath(wA1, CubicBezier(ORIGIN,ORIGIN + DOWN*3, ORIGIN + 3*UP, ORIGIN + 6*UP)), run_time=0.4)
        self.remove(*self.mobjects)
        wA1.scale(0.5)
        g.make_moves("wL,bL wL/,wQ -wL,bQ bL-,wP wQ\\,bS1 bQ-,wA1 /wQ".split(','))
        g.set_tile_positions()
        wA1.rotate(PI/6)
        wA1.shift(DOWN*3)
        self.play(AnimationGroup(AnimationGroup(wA1.animate.shift(UP*3), run_time=0.3),AnimationGroup(self.camera.frame.animate.scale(0.66).move_to(LEFT).set_phi(PI/7), run_time= 0.5)))
        bS1=g.bugs["bS1"].tile
        self.play(AnimationGroup(self.camera.frame.animate.move_to(UP).scale(1.1),Succession(Wait(0.3),MoveAlongPath(bS1,g.get_curve("bS1", "bQ/",-1)),MoveAlongPath(bS1,g.get_curve("bQ/", "bL/", -1)),MoveAlongPath(bS1,g.get_curve("bL/", "\\bL",-1)), run_time = 0.6)),rate_func=rate_functions.linear)
#        self.play(Succession(*[g.move("bS1",path,) for path in "bQ/,bL/,\\bL".split(",")])))
        g.make_moves(["bS1 \\bL"])
        spots = ["wA1", "-wQ", "\\wQ","wQ/", "-bS1", "\\bS1"]
        self.play(AnimationGroup(Succession(
            *[MoveAlongPath(wA1, g.get_curve(spots[i],spots[i+1],1)) for i in range(len(spots)-1)],
            run_time= 0.6,
            rate_func=rate_functions.linear
            
        ),AnimationGroup(self.camera.frame.animate.move_to(UP*1.5+LEFT).scale(0.7).set_phi(-PI/11), run_time= 0.6)))
        g.make_moves(["wA1 \\bS1","wB1 wA1/","bG1 bL/"])
        g.set_tile_positions()
        wB1 = g.bugs["wB1"].tile
        wB1.rotate(PI)
        bG1= g.bugs["bG1"].tile
        wB1.shift(UP*5)
        bG1.shift(UP*4 + RIGHT*3)
        self.play(LaggedStart(bG1.animate.shift(DOWN*4 + LEFT*3),self.camera.frame.animate.scale(2.3),wB1.animate.shift(DOWN*5), lag_ratio = 0.3), run_time=0.9)
        self.play(LaggedStart(
            AnimationGroup(Succession(ScaleInPlace(bG1, 1.4), ScaleInPlace(bG1, 1/1.4), run_time = 1),MoveAlongPath(bG1, g.get_curve("bG1", "/wP"))),
            Succession(MoveAlongPath(wB1, g.get_curve("wB1", "wA1-",1))),
        run_time=0.4, lag_ratio = 0.3))
        self.play(Rotate(g.bugs["wB1"].svg_bug, -2*PI/3), run_time=0.2)
        g.make_moves(["bG1 /wP", "wB1 wA1-","bM -bG1"])
        g.set_tile_positions()
        bM = g.bugs["bM"].tile
        bM.shift(DOWN*2)
        self.play(LaggedStart(bM.animate.shift(UP*2),Succession(ScaleInPlace(wB1, 1.2), ScaleInPlace(wB1, 1/1.2),ScaleInPlace(wB1, 1.2), ScaleInPlace(wB1, 1/1.2), run_time=1), lag_ratio = 0.4), run_time = 0.6)
        spots = [spots[0]] + spots[:0:-1] + ["/wQ", "\\bM", "-bM"]
        self.play(AnimationGroup(Succession(
            *[MoveAlongPath(wA1, g.get_curve(spots[i],spots[i+1],-1)) for i in range(len(spots)-1)],
            run_time= 0.8,
            rate_func=rate_functions.linear
            
        ),AnimationGroup(self.camera.frame.animate.move_to(DOWN + 1.5*LEFT).scale(0.76), run_time= 0.5)))
        self.play(
            
            Succession(AnimationGroup(Rotate(g.bugs['wA1'].svg_bug,-PI*2/3), self.camera.frame.animate.move_to(wA1.get_center()).scale(0.6)),
                       ScaleInPlace(wA1, 1.2),ScaleInPlace(wA1, 1/1.2),
                       ScaleInPlace(wA1, 1.2),ScaleInPlace(wA1, 1/1.2),run_time = 1.2)
                       ,run_time = 0.8
        )
        g.make_moves(["wA1 -bM", "bP bQ-", "wG1 wL\\"])
        g.set_tile_positions()
        bP = g.bugs["bP"].tile
        wG1 = g.bugs["wG1"].tile
        self.remove(wG1)
        self.play(LaggedStart(self.camera.frame.animate.move_to(wG1.get_center()).scale(1.13),AnimationGroup(FadeIn(bP, shift = 4*LEFT)),
                          AnimationGroup(FadeIn(wG1, shift = 5*UP)), lag_ratio = 0.3
                             ), run_time = 1.1)
        self.play(Succession(Rotate(g.bugs["wG1"].svg_bug, -PI/3), ScaleInPlace(wG1, 1.15),ScaleInPlace(wG1, 1/1.15),ScaleInPlace(wG1, 1.15),ScaleInPlace(wG1, 1/1.15),Wait(0.2),ScaleInPlace(wG1, 1.15),ScaleInPlace(wG1, 1/1.15),ScaleInPlace(wG1, 1.15),ScaleInPlace(wG1, 1/1.15)), run_time = 1.4)
        g.make_moves(["bB1 bP\\"])
        g.set_tile_positions()
        bB1 = g.bugs["bB1"].tile
        self.play(FadeIn(bB1, shift=UP*3+LEFT*2), run_time = 0.6)
        self.wait(0.3)
        [wA2, wA3, wB2, wS1, wS2,wG2,wG3,wM] = [g.bugs[x].tile for x in ["wA2", "wA3", "wB2", "wS1", "wS2", "wG2","wG3","wM"]]
        self.add(wA3, wA2, wB2,  wS2,wS1,wG3, wG2, wM)
        wA3.move_to(DOWN*20)
        wA2.move_to(DOWN*20 + g.climb_basis)
        wB2.move_to(DOWN*20+g.right_basis)
        wM.move_to(DOWN*20+2*g.right_basis)
        wG3.move_to(DOWN*20+3*g.right_basis)
        wG2.move_to(DOWN*20+3*g.right_basis + g.climb_basis)
        wS2.move_to(DOWN*20+4*g.right_basis)
        wS1.move_to(DOWN*20+4*g.right_basis + g.climb_basis)
        self.camera.frame.move_to(wB2)
        self.wait(0.2)
        self.play(Rotate(wB2.submobjects[1],2*PI/3, about_point=wB2.get_center()), run_time = 0.5)
        self.play(Succession(ScaleInPlace(wB2, 1.2),ScaleInPlace(wB2, 1/1.2)), run_time = 0.37)
        self.play(LaggedStart(Succession(ScaleInPlace(wB2, 1.2),ScaleInPlace(wB2, 1/1.2)),MoveAlongPath(wA2, Line(wA2.get_center(), wA2.get_center()+ 4*UP)), lag_ratio=0.3), run_time = 0.47)
        self.play(LaggedStart(Succession(ScaleInPlace(wB2, 1.2),ScaleInPlace(wB2, 1/1.2)),MoveAlongPath(wA3, Line(wA3.get_center(), wA3.get_center()+ 4*UP)), lag_ratio=0.3), run_time = 0.47)
        # self.play()
        self.add(self.camera.frame)
        self.camera.frame.move_to(ORIGIN)
        #self.add_updater(lambda dt: self.camera.frame.set_phi(self.camera.frame.get_phi()+dt*DEGREES))
        g.make_moves(["wA2 \\wA1","bA1 bP/","wA3 wG1\\", "bG2 bP-"])
        (bA1, bG2) = (g.bugs[x].tile for x in ("bA1", "bG2"))
        g.set_tile_positions()
        self.play(AnimationGroup(AnimationGroup(ScaleInPlace(self.camera.frame, 4), rate_func=rate_functions.linear, run_time = 4), 
                                 LaggedStart(
                                     FadeIn(wA2,shift=4*RIGHT),
                                     FadeIn(bA1,shift=3*LEFT+2*DOWN),
                                     FadeIn(wA3,shift=3*UP+2*LEFT),
                                     FadeIn(bG2,shift=4*LEFT),lag_ratio=0.6)))
        
class monologue2(MovingCameraScene):
    def talk(self, tile, time, scale_value=1.1):
       return Succession(ScaleInPlace(tile, scale_value),ScaleInPlace(tile, 1/scale_value), run_time = time)
    def construct(self):
        self.add_sound(".\\media\\narration\\Meet the Soldier p4.wav")
        g = hive_game(self, tile_size = 4)
        g.make_moves('bM,bS1 bM-,bA1 -bM,bG1 bS1-,bB1 -bA1'.split(','))
        g.set_tile_positions()
        VGroup(*g.get_live_tiles()).to_edge(DOWN).shift(4*DOWN+2*RIGHT)
        ant_tile = g.bugs['wA1'].tile
        self.add(ant_tile)
        ant_tile.rotate(PI/3)
        self.camera.frame.shift(LEFT*1.7+DOWN*0.4)
        monologue_1 = [[0.4],
                       [0.2],
                       [0.3],
                       [0.3],
                       [0.25,1.3],
                       [0.2],
                       [0.18],
                       [0.12],
                       [0.3],
                        [0.26, 1.2],
                       [0.14],
                        [0.2],
                        [0.17],
                        [0.13],
                        [0.11],
                        [0.2],
                        [0.2],
                        [0.4, 1.2],
                       ]
        j = 0
        for i in monologue_1:
            j += 1
            if j == 9:
                self.play(Rotate(ant_tile, PI/3,run_time=i[0]))
                continue
                #ant_tile.add_updater(move_right_func)
            self.play(self.talk(ant_tile, *i))

        self.play(Rotate(ant_tile, 2*PI/3, run_time = 0.2))
        self.play(self.talk(ant_tile, 0.2))
        self.play(self.talk(ant_tile, 0.25, 1.4))
        self.play(self.talk(ant_tile, 0.3))
        self.play(AnimationGroup(self.camera.frame.animate.shift(RIGHT*5+DOWN/4),Succession(*[Rotate(ant_tile, PI/20 * x) for x in [1,-2,2,-2,2,-1]], ScaleInPlace(ant_tile, 1.2), ScaleInPlace(ant_tile, 1/1.2), run_time = 0.9)))
        self.wait(0.12)
        self.play(Succession(*[self.talk(ant_tile, x) for x in [0.13, 0.24, 0.2, 0.2, 0.4]]))
        self.play(MoveAlongPath(ant_tile,CubicBezier(ORIGIN, RIGHT*4, RIGHT*4, ORIGIN)), run_time = 0.34)
        self.play(Succession(*[self.talk(ant_tile, x) for x in [0.13, 0.18]]))
        self.play(MoveAlongPath(ant_tile,CubicBezier(ORIGIN, RIGHT*4, RIGHT*4, ORIGIN)), run_time = 0.3)
        self.play(Succession(*[self.talk(ant_tile, x) for x in [0.11, 0.14]]))
        self.play(MoveAlongPath(ant_tile,CubicBezier(ORIGIN, RIGHT*4, RIGHT*4, ORIGIN)), run_time = 0.3)
        self.wait(1)

class battle2(MovingCameraScene):
    def construct(self):
        self.add_sound(".\\media\\narration\\Meet the Soldier p5.wav")
        moves_string = 'wL,bG1 -wL,wM wL-,bQ /bG1,wQ wL\\,bA1 \\bG1,wA1 \\wM,bP /bQ,wM -bA1,bS1 bP\\,wP /wQ,bA2 /bP,wA1 -bA2,bA3 \\bP,wM \\bA3,bS1 \\bA2,wA1 bA1/,bS1 \\wM,wA2 wL/,bM \\bA2,wA2 -bM,bA2 wQ-,wA3 wP\\,bA2 wA3\\,wG1 wA1-,wA2 \\bM,wG1 \\bA1,bM wQ-,wS1 /wP,bA2 wQ\\,wS1 bA2\\,bM /wA3,wS1 /bM,bA2 wQ-,wS2 /wS1,bS2 bA2-,wA1 bS2\\,bG2 \\bS2,wA1 bS2-,bL bP\\,wS2 /bL,bB1 bA2\\,wA2 bB1\\,bG2 bS2\\,wB1 -wS2,bB1 bA2,wB1 wS2,bG3 /bA3,wB1 bL,bG3 \\bQ,wS2 /wM,bQ bG1\\,wS2 \\bS1,bB1 wQ,wG2 /wB1,bB2 \\bS2,bQ bB1\\,bB2 \\bA2,wP \\bM,bQ bA2\\,wA2 bG2\\,bS2 wA1-,wA2 bS2\\,bB2 bA2,wA3 bQ\\,bB2 bB1\\,wG2 \\wP,wS1 wB1\\,wG2 /bA3,bM wS1\\,wG2 bA1/,bM bB2\\,wS1 /bM,bB2 bB1,wG1 bG1\\,bB2 \\bA2,wL bB2/,bB1 \\wQ,wG1 \\bB2,bB2 wQ,wA3 bS2/,bB2 /wQ,wP wB1\\,bB2 wQ,wA2 wA3\\,bB2 wQ\\,wA3 wL\\,bB2 wQ,wA3 wA1\\,bB2 wQ\\,wA1 wL\\,bB2 wQ,wL wA1\\,bB2 bG1\\,wL wQ\\,bB2 /wQ,wL bQ\\,bB2 bG1\\,wA1 -bS1,wA2 -wP'
        g = hive_game(self)
        g.make_moves(moves_string.split(','),no_animate=True)
        g.set_tile_positions()
        g.set_z_indices()
        spots = ["wA1", "-wS2", "\\wS2","wS2/", "wS2-", "bS1-","\\bA1","\\wG2","wG2/","wG2-","wG1/","wG1-","wG1\\","bA2/","bA2-"]
        wA1=g.bugs["wA1"].tile
        self.camera.frame.scale(0.6)
        self.play(AnimationGroup(Succession(
            *[MoveAlongPath(wA1, g.get_curve(spots[i],spots[i+1],1)) for i in range(len(spots)-1)],
            run_time= 1,
            rate_func=rate_functions.linear
            
        ),MoveAlongPath(self.camera.frame,CubicBezier(wA1.get_center(),wA1.get_center()+ 3*RIGHT +UP*4,g.bugs["bG2"].tile.get_center()+ 4*UP+2*LEFT,g.bugs["bG2"].tile.get_center())), run_time= 2.8))
        self.play(LaggedStart(MoveAlongPath(self.camera.frame, Line(self.camera.frame_center, g.bugs["bB2"].tile.get_center())),Rotate(g.bugs["bB2"].svg_bug,-PI/3),lag_ratio=0.4), run_time = 1)
        bB2=g.bugs["bB2"].tile
        self.play(Succession(ScaleInPlace(bB2,1.2, run_time = 3),ScaleInPlace(bB2,1/1.2),ScaleInPlace(bB2,1.2, run_time = 2),ScaleInPlace(bB2,1/1.2),ScaleInPlace(bB2,1.2),ScaleInPlace(bB2,1/1.2),ScaleInPlace(bB2,1.2),ScaleInPlace(bB2,1/1.2),ScaleInPlace(bB2,1.2),ScaleInPlace(bB2,1/1.2, run_time = 0.5)), run_time = 1.7)
        self.play(LaggedStart(g.move("bB2", "wQ"), MoveAlongPath(self.camera.frame, Line(self.camera.frame_center,self.camera.frame_center+DOWN*1.5+RIGHT)), lag_ratio=0.23))
        wA2=g.bugs["wA2"].tile
        spots = ["wA2","/wP","wP\\","wP-","\\wS1","\\bM"]
        self.play(Rotate(wA2.submobjects[1],-PI/3), run_time=0.4)
        self.play(Succession(
            *[MoveAlongPath(wA2, g.get_curve(spots[i],spots[i+1],1 if i>2 else -1)) for i in range(len(spots)-1)],
            run_time= 1.5,
            rate_func=rate_functions.linear
        ))
        self.wait(1.5)

class monologue_3(MovingCameraScene):
    def talk(self, tile, time, scale_value=1.1):
       return Succession(ScaleInPlace(tile, scale_value),ScaleInPlace(tile, 1/scale_value), run_time = time)

    def construct(self):
        self.add_sound(".\\media\\narration\\Meet the Soldier p6.wav")
        g = hive_game(self)
        g.make_moves('bM,bS1 bM-,bA1 -bM,bG1 bS1-,bB1 -bA1,bQ -bB1,bP bG1-,bL bP-,wQ bL-,wA3 -bQ'.split(','))
        g.bugs['wQ'].tile.rotate(PI/3)
        g.set_tile_positions()
        ant_tile = g.bugs['wA1'].tile
        ant_tile.shift(UP*1.1+RIGHT*0.5)
        self.add(ant_tile)
        ant_tile.rotate(PI/6*5)
        self.camera.frame.move_to(ant_tile).scale(1/4)

        ant_tile.shift(UP*0.5)
        ant_tile.submobjects[1].stretch(0.7, 1)

        self.play(Wiggle(ant_tile, scale_value = 1,n_wiggles=12,rotation_angle=13*DEGREES,rate_func=rate_functions.linear, run_time=2 ))

        self.play(AnimationGroup( 
                  Succession(ScaleInPlace(ant_tile.submobjects[0],1.2),ScaleInPlace(ant_tile.submobjects[0],1/1.2),run_time = 3), ant_tile.submobjects[1].animate.stretch(1/0.7, 1), run_time = 0.4))
        self.play(Succession(*[self.talk(ant_tile,x)for x in [0.3, 0.3, 0.2]]))
        self.play(ant_tile.animate.shift(DOWN/2), run_time=0.2)
        self.play(Succession(*[self.talk(ant_tile,x)for x in [0.12]*12]))
        self.play(Succession(*[self.talk(ant_tile,x)for x in [0.12, 0.12,0.2,0.2,0.2,0.24, 0.3]]))


        
        rotate_func = lambda mob, dt : mob.rotate(-dt*60*DEGREES).shift(dt*DOWN/3)
        ant_tile.add_updater(rotate_func)
        self.play(Succession(ScaleInPlace(ant_tile,1.4),ScaleInPlace(ant_tile,1/1.4)),run_time=0.5)
        ant_tile.remove_updater(rotate_func)
        ant_tile.rotate(30*DEGREES).shift(UP/6)
        self.wait(0.4)
        self.play(self.camera.frame.animate.scale(3), run_time=0.8)
        bM=g.bugs['bM'].svg_bug
        self.play(Wiggle(bM,scale_value= 1,rotation_angle=0.06*TAU),rate_func=rate_functions.smooth, run_time=0.8)
        self.play(Wiggle(bM,scale_value= 1,rotation_angle=0.06*TAU),rate_func=rate_functions.smooth, run_time=0.8)
        self.wait(2)
        
class finale(MovingCameraScene):
    def construct(self):        
        self.add_sound(".\\media\\narration\\Meet the Soldier p7.wav")
        g = hive_game(self)
        self.wait(0.3)
        g.make_moves('wB1,wM -wB1,wQ -wM,wL -wQ,wG2 wB1-,wA2 wG2-,wS2 wA2-,wP wS2-'.split(','),no_animate=True)
        g.set_tile_positions()
        g.bugs["wP"].tile.rotate(-PI/3)
        self.camera.frame.move_to(g.bugs['wA2'].tile).scale(1/20).shift(UP/8+RIGHT/23)
        self.play(self.camera.frame.animate.scale(1.2).shift(LEFT*0.1+DOWN*0.03), rate_func=rate_functions.linear, run_time=0.63)
        self.camera.frame.scale(1.8)
        self.play(self.camera.frame.animate.scale(1.2).shift(LEFT*0.2+DOWN*0.1), rate_func=rate_functions.linear, run_time=0.63)
        self.camera.frame.scale(2.2)
        self.play(self.camera.frame.animate.scale(1.2).shift(LEFT*0.3+DOWN*0.3), rate_func=rate_functions.linear, run_time=0.63)
        self.camera.frame.scale(1.6).move_to(ORIGIN+RIGHT/2+DOWN)
        self.play(self.camera.frame.animate.scale(1.2), rate_func=rate_functions.linear, run_time=0.63)
        logo = SVGMobject(".\\media\\assets\\stacked_flat_dark.svg").shift(DOWN*2+RIGHT/2)
        self.play(DrawBorderThenFill(logo), run_time=1.2)
        self.wait(1)
        self.clear()
        g2 = hive_game(self)
        g2.make_moves('bM,bS1 bM-,bA1 -bM,bG1 bS1-,bB1 -bA1,bQ -bB1,bP bG1-,bL bP-,wQ bL-,wA3 -bQ'.split(','))
        g2.bugs['wQ'].tile.rotate(PI/3)
        g2.set_tile_positions()
        ant_tile = g2.bugs['wA1'].tile
        ant_tile.move_to(UP+3*LEFT).rotate(PI/6*5)
        self.add(ant_tile)
        bQ=g2.bugs["bQ"].svg_bug
        self.camera.frame.move_to(ant_tile.get_center()+RIGHT+DOWN/2).scale(0.5)
        self.play(AnimationGroup(Succession(ScaleInPlace(ant_tile, 1.1),ScaleInPlace(ant_tile, 1/1.1),ScaleInPlace(ant_tile, 1.1),ScaleInPlace(ant_tile, 1/1.1),ScaleInPlace(ant_tile, 1.1),ScaleInPlace(ant_tile, 1/1.1),ScaleInPlace(ant_tile, 1.1),ScaleInPlace(ant_tile, 1/1.1),ScaleInPlace(ant_tile, 1.1),ScaleInPlace(ant_tile, 1/1.1), run_time=1.3),
                                 Succession(Rotate(bQ,-PI/6),Wait(2),Rotate(bQ,PI/2),Wait(2),Rotate(bQ,-PI/2), run_time=0.8)))
        self.wait(2)

        
