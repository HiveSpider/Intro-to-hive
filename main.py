from manim import *
from hive import bug, game, assetPathOfficial
from Dice import create_dice
import json
from math import sin

class full_movie(Scene):
    def construct(self):
        opening.play_scene(self)
        strategy_game.play_scene(self)
        tiles.play_scene(self)
        queen_command.play_scene(self)
        spawn.play_scene(self)
        freedom_of_movement.play_scene(self)

        

class beetle_demo(Scene):
    def construct(self):
        demo_game = game(self)
        self.play((demo_game.display(run_time=0.1)))
        (demo_game.move("wA1", ""))
        (demo_game.move("bB1", "wA1-"))
        (demo_game.move("wB1", "wA1/"))
        demo_game.make_moves(["bB2 \\wA1", "wB2 -wA1", "bM /wA1", "wM wA1\\"])
        self.play(LaggedStart(*demo_game.move_to_current_position().animations,lag_ratio=0.15))
        self.play(Wait(1))

        (demo_game.move("wB1", "wA1"))
        (demo_game.move("bM","wB1"))
        (demo_game.move("wB2","bM"))
        (demo_game.move("bB1","wB2"))
        (demo_game.move("wM","bB1"))
        (demo_game.move("bB2","wM"))
        anim = LaggedStart(*demo_game.move_to_current_position().animations, lag_ratio = 0.33)
        self.play(anim)
        self.play(Wait(1))
        self.play(demo_game.reveal_stacks())
        self.play(Wait(1))
        self.play(demo_game.collapse_stacks())
        
class better_spider(Scene):
    def construct(self):
        demo_game = game(self)
        up = demo_game.up_basis
        right = demo_game.right_basis
        n = UP * 0.5
        m = -n
        a = rotate_vector(n, -PI/3)
        f = rotate_vector(n, PI/3)
        line = CubicBezier(-up, -up + 0.33*rotate_vector(-right + up, PI/2), -right + 0.33*rotate_vector(-right + up, PI/2),-right)
        line.add_cubic_bezier_curve(-right, -right + 0.33*rotate_vector(up, PI/2), -right + up + 0.33*rotate_vector(up, PI/2),-right+up)
        line.add_cubic_bezier_curve(-right+up, -right +up + 0.33*rotate_vector(right, PI/2), up + 0.33*rotate_vector(right, PI/2),up)
        wS1 = demo_game.bugs["wS1"].tile
        self.play((demo_game.display(run_time=0.1)))
        self.play(demo_game.move("wA1",""))
        self.play(demo_game.move("bS1", "wA1-"))
        self.play(demo_game.move("wS1", "/wA1"))
        self.play(demo_game.move("bQ", "bS1-"))
        self.play(AnimationGroup(MoveAlongPath(wS1, line, rate_func=rate_functions.ease_in_out_sine), run_time=2))
        self.play(Wait(3))

class better_queen(Scene):
    def construct(self):
        demo_game = game(self)
        up = demo_game.up_basis
        right = demo_game.right_basis
        n = UP * 0.5
        m = -n
        a = rotate_vector(n, -PI/3)
        f = rotate_vector(n, PI/3)
        line = CubicBezier(ORIGIN, up*0.866 - right/2, up*0.866 - right/2,up)
        line = CubicBezier(ORIGIN, ORIGIN + n, up -a,up)
        wA1 = demo_game.bugs["wA1"].tile
        self.play((demo_game.display(run_time=0.1)))
        self.play(demo_game.move("wA1",""))
        self.play(demo_game.move("bS1", "wA1-"))
        self.play(demo_game.move("wS1", "-wA1"))
        self.play(demo_game.move("bS2", "/wA1"))
        self.play(demo_game.move("wS2", "wA1\\"))
        self.play(AnimationGroup(MoveAlongPath(wA1, line), run_time=1))
        self.play(Wait(3))


class better_grasshopper(Scene):
    def construct(self):
        line = Line(ORIGIN, RIGHT*2)
        demo_game = game(self)
        wG1 = demo_game.bugs["wG1"].tile
        self.play((demo_game.display(run_time=0.1)))
        self.play(demo_game.move("wG1",""))
        self.play(demo_game.move("bS1", "wG1-"))
        #self.bring_to_front(wG1)
        self.play(AnimationGroup(Succession(ScaleInPlace(wG1, 1.2, run_time = 0.5), ScaleInPlace(wG1, 1/1.2, run_time = 0.5)), MoveAlongPath(wG1, line)))

        #self.play(demo_game.move("wG1", "bS1-"))

class bugs_playing(Scene):
    def construct(self):
        bugs_playing.play_scene(self)
    def play_scene(s):
        backing_game = game(s)
        spider = backing_game.bugs["wS1"].tile
        grasshopper = backing_game.bugs["bG1"].tile
        spider.rotate((-PI/3 * 2))
        grasshopper.rotate((-PI/3 * 2))
        backing_game.make_moves([
            "wA1",
            "wS1 wA1-",
            "bG1 wS1-",
            "wB1 -wA1",
            "wA1 -wB1",
            "bB1 /wA1",
            "wB2 -wA1",
            "bB2 -wA1\\",
            "bP wB1\\",
            "wP bP\\",
            "bP wP-",
            "bM wP\\",
            "bB2 wA1\\",
            "wM wA1/",
        ])
        #self.play(backing_game.move_to_current_position())
        backing_game.set_tile_positions()
        s.play(*[GrowFromCenter(x) for x in backing_game.get_live_tiles()])
        up = backing_game.up_basis
        right = backing_game.right_basis
        spider.generate_target()
        line = CubicBezier(right,right + rotate_vector(up, PI/2)/3,right+up+rotate_vector(up, PI/2)/3,right + up)
        line2 = CubicBezier(right+up,right + up + rotate_vector(right, PI/2)/3,2*right+up+rotate_vector(right, PI/2)/3,2*right + up)
        line3 = CubicBezier(2*right+up, 2*right+up+ rotate_vector(right-up, PI/2)/3,3*right+rotate_vector(right-up,PI/2)/3, 3*right)
      
        s.play(
            LaggedStart(Succession(MoveAlongPath(spider,line),MoveAlongPath(spider,line2),MoveAlongPath(spider,line3), run_time = 1.5),

            Succession(
            LaggedStart(Rotate(backing_game.bugs["wP"].tile ,angle=TAU, axis=UP),
            backing_game.move("bP", "wP")),

            LaggedStart(Rotate(backing_game.bugs["wP"].tile ,angle=TAU, axis=rotate_vector(UP,PI/3)),
            backing_game.move("bP", "/wP") ),run_time=1.5
            
            ),
             lag_ratio=0.05), Succession(backing_game.move("wB1","wA1"), backing_game.move("bB1","wB1"),backing_game.move("wB2","bB1"), run_time = 2))
        s.play(LaggedStart(
            AnimationGroup(Succession(ScaleInPlace(grasshopper,1.25, run_time = 0.5),ScaleInPlace(grasshopper,0.8,run_time = 0.5)), MoveAlongPath(grasshopper,Line(2*RIGHT,4*RIGHT)) ),
            Succession(
            LaggedStart(Rotate(backing_game.bugs["bM"].tile ,angle=TAU, axis=rotate_vector(UP,-PI/3)),
            backing_game.move("wP", "bM")),

            LaggedStart(Rotate(backing_game.bugs["bM"].tile ,angle=TAU, axis=rotate_vector(UP,PI/3)),
            backing_game.move("wP", "/bM")), run_time=1.5),
            Succession(backing_game.move("bB2","wB2"), backing_game.move("wM","bB2"),backing_game.reveal_stacks(), run_time = 2), lag_ratio=0.05))
        
        for i in backing_game.get_live_bugs():
            i.tile.generate_target()
            if i.color == "white":
                i.tile.target.set_x(-9)
            else:
                i.tile.target.set_x(9)
        s.play(AnimationGroup(AnimationGroup([Rotate(x.tile, PI/3 if x.color == "white" else -2*PI/3) for x in backing_game.get_live_bugs() ])))
        s.play(AnimationGroup([MoveToTarget(x) for x in backing_game.get_live_tiles()]))

class zoom_out_game(Scene):
    def construct(self):
        zoom_out_game.play_scene(self)
    def play_scene(s):
        analysis_file = ".\\media\\analysis_files\\analysis_02-Jun-2025_22_49_52.json"
        with open(analysis_file, 'r') as file:
                data = json.load(file)
        demo_game = game(s, data, tile_size=1.2)
        # for x in demo_game.black_bugs:
        #     x.tile.set_x(-9)
        # for x in demo_game.white_bugs:
        #     x.tile.set_x(9)
        # for i in range(4)
        moves = demo_game.next_n_moves(4)
        for i in demo_game.get_live_bugs():
            x = i.tile.target.get_x()
            y = i.tile.target.get_y()
            i.tile.set_x(x).set_y(y)
            #self.play(DrawBorderThenFill(i.svg_t))
            #self.play(DrawBorderThenFill(i.svg_bug))
            #self.play(AnimationGroup(DrawBorderThenFill(i.svg_bug), DrawBorderThenFill(i.svg_t)))
        s.remove(*[t for t in demo_game.get_live_tiles()])
        
        s.play(LaggedStart([Succession(GrowFromCenter(i.svg_t), DrawBorderThenFill(i.svg_bug), run_time = 0.8) for i in demo_game.get_live_bugs()], lag_ratio = 0.8))

        n = 0
        for i in demo_game.black_bugs:
            if i.game_coordinate == None:
                s.add(i.tile)
                i.tile.set_y(-7)
                i.tile.set_x((n - 5.5)*1.2)
                n += 1
        n = 0
        for i in demo_game.white_bugs:
            if i.game_coordinate == None:
                #print(i)
                i.tile.set_y(7)
                i.tile.set_x((n - 5.5)*1.2)
                s.add(i.tile)
                n += 1
        
        #self.play(ScaleInPlace(VGroup([x.tile for x in demo_game.bugs.values() if x.game_coordinate != None]),0.5))
        #self.play(ScaleInPlace(VGroup([x.tile for x in demo_game.bugs.values()]),0.5, about_point = ORIGIN))
        s.play(ScaleInPlace(VGroup(demo_game.all_tiles), 0.5))
        #v = VGroup(demo_game.all_tiles).scale(0.5).move_to(ORIGIN)
        # self.play(Transform(VGroup(demo_game.all_tiles), v))
        demo_game.tile_size = demo_game.tile_size * 0.5
        demo_game.right_basis = demo_game.right_basis *0.5
        demo_game.up_basis = demo_game.up_basis *0.5
        demo_game.climb_basis = demo_game.climb_basis * 0.5
        for i in range(19):
            s.play(demo_game.next_move(run_time=1-(i/30)**0.3 - .05))
        for i in range(19):
            s.play(demo_game.next_move(run_time=1-((25-i)/30)**0.5- .05))
        s.play(Succession(Wait(0.3),demo_game.next_move()))
        s.play(Wait(0.2))
        s.play(ShrinkToCenter(VGroup([b.tile for b in sorted(demo_game.bugs.values(),key = lambda x: x.z_index)])))
        #self.play(Succession(*[DrawBorderThenFill(i.svg_t) for i in demo_game.get_live_bugs()]))
        #self.play(LaggedStart([i.draw() for i in demo_game.get_live_bugs()]))
        # for i in moves[:6]:
        #     self.play(i.set_run_time(0.75))
        # ScaleInPlace(VGroup(*demo_game.all_tiles), 1.0/3)
        # demo_game.tile_size = 0.6

        # for i in moves[6:10]:
        #     self.play(i.set_run_time(0.6))
            
        # for i in moves[10:30]:
        #     self.play(i.set_run_time(0.4))
        # for i in moves[30:37]:
        #     self.play(i.set_run_time(0.6))
        # for i in moves[37:]:
        #     self.play(i.set_run_time(0.75))
        # self.play(Succession(*moves[:4]).set_run_time(6))
        # self.play(Succession(*moves[4:21]).set_run_time(6))
        # self.play(Succession(*moves[22:38]).set_run_time(6))
        # self.play(Succession(*moves[39:]).set_run_time(2))
        

        #self.play(moves[21])
        #self.play(Succession(*moves).set_run_time(10))


class game_demo(Scene):
    def construct(self):

        # a = SVGMobject(assetPathOfficial + "white.svg").set_x(0.2)
        # b = SVGMobject(assetPathOfficial + "black.svg").set_x(-0.2)

        # self.play(DrawBorderThenFill(a), DrawBorderThenFill(b))
        # self.wait(2)
        # a.set_z(3)
        # a.set_z_index(3)
        # a.generate_target()
        # a.target.set_z(3)
        # a.set_z_index(3)
        # self.play(MoveToTarget(a))
        # self.play(Wait(2))

        #Initialize from downloaded analysis file
        analysis_file = ".\\media\\analysis_files\\analysis_31-May-2025_15_51_12.json"
        with open(analysis_file, 'r') as file:
            data = json.load(file)
        demo_game = game(self, data, tile_size=0.6)
        self.play(demo_game.display())

        #Custom movement of the inventory
        for i in range(len(demo_game.white_bugs)):
            b = demo_game.white_bugs[i].tile
            b.generate_target()
            b.target.set_x(-5 - (i%3)*0.67)
            b.target.set_y(2 -(i//3))
        for i in range(len(demo_game.black_bugs)):
            b = demo_game.black_bugs[i].tile
            b.generate_target()
            b.target.set_x(5 + (i%3)*0.67)
            b.target.set_y(2 -(i//3))

        #play through all the moves, with faster and faster speed
        self.play(LaggedStart(*[MoveToTarget(x.tile) for x in demo_game.bugs.values()]))
        a = 1
        i = 1
        while a != None:
            a = demo_game.next_move(run_time = 0.2 + 1.0/i)
            if(a):
                pass
                self.play(a)
            i+=1

class demo(Scene):
    def construct(self):
        a = Square()
        a.center
        #tile = SVGMobject(assetPathOfficial + "white.svg",True,height=1)#.rotate(-PI/6)
        #s = SVGMobject(assetPathOfficial + "Spider.svg",height=0.666).set_x(-0.02)
        #s = SVGMobject(assetPathOfficial + "Ant.svg",height=0.666).rotate(-PI/6).set_x(-0.02).rotate(PI/6)
        # self.play(DrawBorderThenFill(tile), DrawBorderThenFill(s))
        # t = Group(tile, s)
        # self.wait(1)
        # self.play(ScaleInPlace(t, 3))
        # self.play(Rotate(t, -PI/6))
        b = bug("Spider","white")
        #b.draw(self)
        #self.play(ScaleInPlace(b.tile, 3))
        bugs = ["Ant", "Beetle", "Grasshopper", "Ladybug", "Mosquito", "Pillbug", "Queen", "Spider"]
        tiles = []
        for i in range(len(bugs)):
            w = bug(bugs[i], "white")
            b = bug(bugs[i], "black")
            w.tile.set_x(i-3.5)
            w.tile.set_y(0.6)
            b.tile.set_x(i-3.5)
            b.tile.set_y(-0.6)
            tiles.append(w)
            tiles.append(b)
            w.tile.generate_target()
            w.tile.target.shift(UP*2)
            b.tile.generate_target()
            b.tile.target.shift(DOWN*2)



        self.play(LaggedStart(*[x.draw() for x in tiles]))
        self.play(LaggedStart(*[MoveToTarget(x.tile) for x in tiles[::-1]]))
        self.play(LaggedStart(*[Rotate(x.tile, 5*PI/6) for x in tiles[::2]]), LaggedStart(*[Rotate(x.tile, -PI/6) for x in tiles[1::2]]))

        title = Text("Welcome to HiveGame.com")
        self.play(Write(title))
        self.play(Wait(2))
        self.play(FadeOut(title))
        all = Group(*[x.tile for x in tiles])
        self.play(Rotate(all, PI/2))
        self.play(*[MoveAlongPath(x.tile, Line(x.tile.get_center(), x.tile.get_center()+LEFT*4)) for x in tiles[::2]], *[MoveAlongPath(x.tile, Line(x.tile.get_center(), x.tile.get_center()+RIGHT*4)) for x in tiles[1::2]])
        # self.play()
        tiles[6].tile.generate_target()
        tiles[6].tile.target.move_to(ORIGIN + LEFT/2)
        spawn_text = Text("Spawn your pieces...").set_y(-3)
        self.play(MoveToTarget(tiles[6].tile),FadeIn(spawn_text))
        tiles[7].tile.generate_target()
        tiles[7].tile.target.move_to(ORIGIN + RIGHT/2)
        self.play(MoveToTarget(tiles[7].tile))
        tiles[8].tile.generate_target()
        tiles[8].tile.target.move_to(ORIGIN + LEFT*3/2)
        self.play(FadeOut(spawn_text), MoveToTarget(tiles[8].tile))
        queen_text = Text("Surround the enemy queen").set_y(-3)
        tiles[13].tile.generate_target()
        tiles[13].tile.target.move_to(ORIGIN + RIGHT + UP*0.866)

        self.play(FadeIn(queen_text), MoveToTarget(tiles[13].tile))
        tiles[12].tile.generate_target()
        tiles[12].tile.target.move_to(ORIGIN + LEFT + UP*0.866)
        self.play(MoveToTarget(tiles[12].tile))
        tiles[11].tile.generate_target()
        tiles[11].tile.target.move_to(ORIGIN + RIGHT*1.5 + UP*2*0.866)
        self.play(FadeOut(queen_text),MoveToTarget(tiles[11].tile))
        tiles[0].tile.generate_target()
        tiles[0].tile.target.move_to(ORIGIN + LEFT + DOWN*0.866)
        self.play(MoveToTarget(tiles[0].tile))

        self.play(Wait(2))


class opening(Scene):
    # do bugs_playing followed by 
    def construct(self):
        opening.play_scene(self)
    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 45.m4a")
        bugs_playing.play_scene(s)
        zoom_out_game.play_scene(s)
        pass

class strategy_game(Scene):
    def board(a, b, n = 8,stroke = None):
        return VGroup([Square(stroke_color = stroke,fill_opacity=1,side_length=1,color=(a, b)[(i+i//n)%2]).set_x(i//n).set_y(i%n) for i in range(n*n)])
    def construct(self):
        strategy_game.play_scene(self)
    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 47.m4a")
        text = Tex('2 player pure strategy game').set_y(2)
        dice = VGroup(create_dice(3, 1, .2).set_x(-0.6), create_dice(6, 1, 0.2).set_x(0.6))
        x = VGroup(Line(2*LEFT +DOWN, 2*RIGHT+UP,stroke_width=8,stroke_color=RED),Line(2*LEFT +UP, 2*RIGHT+DOWN,stroke_width=8,stroke_color=RED)).scale(0.9)
        ace=VGroup(
                    RoundedRectangle(height=2, width=1.5, corner_radius=0.3, color=WHITE, fill_opacity=1),
                    Text('A', color=RED).scale(0.5).set_y(0.7).set_x(-0.52),
                    SVGMobject('media/images/Heart.svg').scale(0.11).set_opacity(0.8).set_y(0.3).set_x(-0.52)
                   ).set_x(-0.2)
        hidden_card = VGroup(
            RoundedRectangle(height=2, width=1.5, corner_radius=0.3, color=BLUE, fill_opacity=1),
            RoundedRectangle(height = 1.8, width = 1.3, corner_radius = 0.3)
        ).set_x(0.2)
        cards = VGroup(ace, hidden_card)
        x2 = VGroup(Line(2*LEFT +DOWN, 2*RIGHT+UP,stroke_width=8,stroke_color=RED),Line(2*LEFT +UP, 2*RIGHT+DOWN,stroke_width=8,stroke_color=RED)).set_y(-2).scale(0.9)
        dice.set_x(-2.5).set_y(-1)
        x.set_x(-2.5).set_y(-1)
        cards.set_y(-1).set_x(2.5)
        x2.set_x(2.5).set_y(-1)
        s.play(Write(text))
        s.play(GrowFromEdge(dice,DOWN))
        s.play(Write(x))
        s.play(GrowFromCenter(cards))
        s.play(Write(x2))
        s.play(Wait(2))
        s.play(FadeOut(cards,dice,text,x,x2,run_time=0.3))
        chess = VGroup(
        strategy_game.board(GREEN,DARK_BROWN).scale(1.11).set_x(0.1).set_y(0), SVGMobject('./media/images/Chess_Pieces_Sprite.svg')
        ).scale(0.33).set_y(2).set_x(2)
        checkers = VGroup(
            strategy_game.board(DARK_GRAY,RED),
            VGroup([Circle(radius = 0.3, fill_opacity=1, color= RED if i < 12 else BLACK).set_x(2*(i%4) +((i//4)%2)).set_y(i//4 + (2 if i >=12 else 0)) for i in range(24)])
        ).scale(0.33).set_y(2).set_x(-2)
        go = VGroup(Square(side_length = 20, color=LIGHT_BROWN, fill_opacity=1).set_x(8.5).set_y(8.5),
                    strategy_game.board(LIGHT_BROWN, LIGHT_BROWN, 18, BLACK),
                    Circle(fill_opacity=1, color = WHITE, radius = 0.4).set_x(2.5).set_y(2.5),
                    Circle(fill_opacity=1, color = BLACK, radius = 0.4).set_x(14.5).set_y(2.5),
                    Circle(fill_opacity=1, color = BLACK, radius = 0.4).set_x(2.5).set_y(14.5),
                    Circle(fill_opacity=1, color = WHITE, radius = 0.4).set_x(14.5).set_y(14.5)
            ).scale(0.2).set_y(-2).set_x(-2)
        connect4 = VGroup(
            [Circle(radius = 0.3,fill_opacity = 1, color = GREY_BROWN if i >= 30 else (RED, YELLOW)[(i + i//14)%2]).set_x(i%7).set_y(i//7) for i in range(42)]
        ).scale(0.4).set_x(2).set_y(-2)
        s.play(GrowFromEdge(checkers, RIGHT))
        s.play(GrowFromEdge(chess, LEFT))
        s.play(GrowFromEdge(go, RIGHT))
        s.play(GrowFromEdge(connect4, LEFT))
        s.play(Wait(1))
        s.play(LaggedStart(*[i.animate.shift(20*RIGHT) for i in (connect4,chess,checkers, go)]))
        s.play(Wait(0.7))

class tiles(Scene):
    def construct(self):
        tiles.play_scene(self)
    def play_scene(s):
        
        s.add_sound(".\\media\\narration\\New Recording 50.m4a")
        g = game(s, rotate_by_dot=False, tile_size=0.66)
        s.play(AnimationGroup(LaggedStart(*[MoveAlongPath(g.white_bugs[13-x].tile,CubicBezier(10*LEFT,8*LEFT+2*UP,3*UP+7*LEFT, 2*UP+6*LEFT).add_cubic_bezier_curve_to(UP+6*LEFT,RIGHT*(8.3-x*0.66 - 4), RIGHT*(8.27-x*0.66-4)+UP)) for x in range(14)]),
               LaggedStart(*[MoveAlongPath(g.black_bugs[x].tile,CubicBezier(10*RIGHT,8*RIGHT+2*DOWN,3*DOWN+7*RIGHT, 2*DOWN+6*RIGHT).add_cubic_bezier_curve_to(DOWN+6*RIGHT,LEFT*(8.3-x*0.66 - 4), LEFT*(8.27-x*0.66-4)+DOWN)) for x in range(14)])))
        s.play(Wait(1.5))
        s.play(AnimationGroup([Wiggle(g.bugs[x].tile, scale_value=1.3, run_time=1, n_wiggles=4) for x in ["wA1","wA2","wQ","wA3","wS1","wS2","bA1","bA2","bQ","bA3","bS1","bS2",]]))
        s.play(AnimationGroup([Wiggle(g.bugs[x].tile, scale_value=1.3, run_time=1, n_wiggles=4) for x in ["wG1","wG2","wG3","bG1","bG2","bG3"]]))
        s.play(AnimationGroup([Wiggle(g.bugs[x].tile, scale_value=1.3, run_time=1, n_wiggles=4) for x in ["wB1","wB2","wL","bB1","bB2","bL"]]))
        # s.play(AnimationGroup(VGroup([x.tile for x in g.white_bugs]).animate.shift(UP*2),
        # VGroup([x.tile for x in g.black_bugs]).animate.shift(DOWN*2)))
        s.play(Wait(2))
        s.play(AnimationGroup(LaggedStart(*[MoveAlongPath(g.white_bugs[x].tile,Line(g.white_bugs[x].tile.get_x() * RIGHT + g.white_bugs[13-x].tile.get_y() * UP,RIGHT*4.5 + RIGHT*0.66*(x%3) + DOWN * (0.66*(x//3) - 1.33))) for x in range(14)][::-1], lag_ratio = 0.02),
                              LaggedStart(*[MoveAlongPath(g.black_bugs[x].tile,Line(g.black_bugs[x].tile.get_x() * RIGHT + g.black_bugs[x].tile.get_y() * UP,LEFT*4.5 + LEFT*0.66*(x%3) + DOWN * (0.66*(x//3) - 1.33))) for x in range(14)], lag_ratio = 0.02)))
        s.play(Wait(0.5))
        s.play(AnimationGroup(*[Rotate(x.tile, PI/3) for x in g.white_bugs], *[Rotate(x.tile, -2*PI/3) for x in g.black_bugs]))
        g.center = RIGHT * 0.33
        t = 0.6
        spawn_text = Tex("Spawn new piece").set_y(3)
        move_text = Tex("Move spawned piece").set_y(3)

        s.play(AnimationGroup(g.move("wG1", ""),Write(spawn_text),run_time=t))
        s.play(g.move("bL","-wG1", run_time=t))
        s.play(g.move("wQ","wG1/", run_time=t))
        s.play(g.move("bQ","/bL", run_time=t))
        s.play(Wait(1))
        s.play(AnimationGroup(g.move("wQ","bL/"), 
        spawn_text.animate.become(move_text)))
        s.play(g.move("bQ","/wG1"))
        win_text = Tex("Win by surrounding enemy queen").set_y(-2)
        win_subtext = Tex("(color of surrounding tiles don't matter)").set_y(-3)
        
        s.play(LaggedStart(FadeOut(spawn_text), Write(win_text),Write(win_subtext), [*g.make_moves(["bA1 -wQ", "bA2 \\wQ", "bA3 wQ/", "bS1 wQ-"], )]))
        s.play(AnimationGroup(        
            Rotate(g.bugs["bA2"].tile,-PI/3),
        Rotate(g.bugs["bA3"].tile,-PI*2/3),
        Rotate(g.bugs["bS1"].tile, PI),
        Rotate(g.bugs["bL"].tile,PI/3),))
        s.play(Wait(0.5))
        s.play(AnimationGroup(*g.make_moves(["wA1 bQ-", "wA2 bQ\\", "wA3 /bQ", "wS1 -bQ"]), ))
        s.play(AnimationGroup(        
            Rotate(g.bugs["wA2"].tile,-PI/3),
        Rotate(g.bugs["wA3"].tile,-PI*2/3),
        Rotate(g.bugs["wS1"].tile, PI),
        Rotate(g.bugs["wG1"].tile,PI/3),))
        s.play(Wait(1))
        s.play(LaggedStart(Unwrite(VGroup(win_text, win_subtext)), LaggedStart(*[FadeOut(x.tile) for x in g.bugs.values()]), run_time=1))

class queen_command(Scene):
    def set_to_target(tile):
        tile.set_x(tile.target.get_x()).set_y(tile.target.get_y())
    def construct(self):
        queen_command.play_scene(self)
    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 49.m4a")
        m_center = 3.5*LEFT + 2*DOWN
        m = bug("Mosquito", "black").tile.rotate(-PI/6).move_to(m_center)
        b1_center = 3*RIGHT
        b1= bug("Beetle", "black").tile.move_to(b1_center).rotate(-2*PI/3)
        b2_center = 4*RIGHT
        b2= bug("Beetle", "black").tile.move_to(b2_center).rotate(PI/3)
        s_center=3.5*LEFT+3.5*UP
        s1 = bug("Spider", "black").tile.move_to(s_center).rotate(PI*5/6)
        web = Line(s_center, s_center+3*UP)
        s.play(*[GrowFromCenter(x) for x in [m,b1, b2,s1]])
        s.add(web)
        s.play(AnimationGroup(
            Succession(
                Rotate(m, about_point=m_center+LEFT, angle=TAU,rate_func=linear),
                Rotate(m, about_point=m_center+RIGHT, angle=-TAU,rate_func=linear), run_time=3)),
            Succession(
                LaggedStart(MoveAlongPath(b1,CubicBezier(b1_center,b1_center+LEFT,b1_center+LEFT,b1_center),rate_func=rush_into),
                MoveAlongPath(b2,CubicBezier(b2_center,b2_center+RIGHT/3,b2_center+RIGHT/3,b2_center),rate_func=linear,run_time=0.3), lag_ratio=1.02), Wait(0.4),
                LaggedStart(MoveAlongPath(b2,CubicBezier(b2_center,b2_center-LEFT,b2_center-LEFT,b2_center),rate_func=rush_into),
                MoveAlongPath(b1,CubicBezier(b1_center,b1_center-RIGHT/3,b1_center-RIGHT/3,b1_center),rate_func=linear,run_time=0.3), lag_ratio=1.02),
            ),
            VGroup(web, s1).animate.shift(DOWN * 2),
            run_time=5)
        s.play(Wait(0.5))
        q = bug("Queen", "black", off_y=-0.08, off_x=0.04).tile.rotate(-PI/6)
        s.play(
            Succession(FadeIn(q, scale=2.5),
            AnimationGroup(
                Rotate(m,angle=-PI/3), 
                Rotate(s1,angle=PI/3), 
                Rotate(b1, angle=PI))))
        s.play(Wait(0.2))
        s.play(Rotate(q, PI/3), run_time=0.2)
        s.play(Wait(0.1))
        s.play(
                Rotate(s1,2*PI/3),
                 run_time=0.2)
        s.play(
                VGroup(web, s1).animate.shift(UP*3)
            , run_time=0.25)
        s.play(Rotate(q, -5*PI/6), run_time=0.2)
        s.play(AnimationGroup(Rotate(b1, PI), Rotate(b2, -PI), run_time=0.2))
        for i in range(3):
            s.play(b2.animate.shift(RIGHT*2), run_time=0.13)
            s.play(b1.animate.shift(RIGHT*2), run_time=0.13)
        s.play(Rotate(q, -PI*5/6, run_time=0.2))
        s.play(Rotate(m,-PI,about_point=DOWN*3.5+1.7*LEFT))
        s.play(Rotate(q, -2*PI/3, run_time=0.5))
        g2 = game(s, center=3*RIGHT + 2*UP, tile_size=0.6)
        g2.make_moves(["wG1","bL -wG1", "wQ wG1/", "bQ -bL"])        
        g2q=g2.bugs["bQ"].tile
        g2o = ("wG1", "bL", "wQ" )
        g2ob=(g2.bugs[x].tile for x in g2o)
        g3 = game(s, center=3*RIGHT, tile_size=0.6)
        g3.make_moves(["wG1","bL -wG1", "wQ wG1/", "wM wG1-", "bA1 -bL", "bQ \\bL"])
        g3q=g3.bugs["bQ"].tile
        g3o = ("wG1", "bL", "wQ" ,"wM", "bA1")
        g3ob=(g3.bugs[x].tile for x in g3o)
        g4 = game(s, center=3*RIGHT + 2*DOWN, tile_size=0.6)
        g4.make_moves(["wG1","bL -wG1", "wQ wG1/", "wM wG1-", "bA1 -bL", "wB1 wQ-", "bS1 /bL","bQ \\bL"])
        g4q=g4.bugs["bQ"].tile
        g4o = ("wG1", "bL", "wQ" ,"wM", "bA1", "wB1", "bS1")
        g4ob=(g4.bugs[x].tile for x in g4o)


        queen_command.set_to_target(g2q)
        queen_command.set_to_target(g3q)
        queen_command.set_to_target(g4q)
        s.remove(*g2.get_live_tiles(),*g3.get_live_tiles(),*g4.get_live_tiles())
        for x in g2o:
            queen_command.set_to_target(g2.bugs[x].tile)
        for x in g3o:
            queen_command.set_to_target(g3.bugs[x].tile)
        for x in g4o:
            queen_command.set_to_target(g4.bugs[x].tile)
        s.play(LaggedStart(q.animate.shift(LEFT*3)))
        s.play(LaggedStart(
            LaggedStart(
                FadeIn(VGroup(g2ob)),
                TransformFromCopy(q, g2q), lag_ratio=1.7),
            LaggedStart(
                FadeIn(VGroup(g3ob)),
                TransformFromCopy(q, g3q), lag_ratio=1.7),
            LaggedStart(
                FadeIn(VGroup(g4ob)),
                TransformFromCopy(q, g4q), lag_ratio=1.7),
            lag_ratio=0.3))
        
        s.play(FadeOut(*s.mobjects))

class spawn(Scene):
    def construct(self):
        spawn.play_scene(self)
    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 23.m4a")
        analysis_file = ".\\media\\analysis_files\\analysis_07-Jun-2025_11_17_09.json"
        #analysis_file = ".\\media\\analysis_files\\analysis_31-May-2025_15_51_12.json"
        with open(analysis_file, 'r') as file:
            data = json.load(file)
        backing_game=game(s,analysis_json=data)
        backing_game.next_n_moves(10)
        backing_game.set_tiles_to_target()
        spots = [backing_game.hex_at_position(p) for p in(
            'wQ-', 'wQ/','\\wQ','-wQ', '-wM','-wS1','-wP','/wP', 'wP\\', 'wP-', 'wS1-')]
        #s.add(*spots)
        s.play([DrawBorderThenFill(x) for x in backing_game.get_live_tiles()])
        s.play(LaggedStart(*[SpiralIn(x) for x in spots]))
        s.play([Wiggle(x) for x in spots])
        s.play(*[FadeToColor(x, RED) for x in  spots[:2]+spots[-2:]], *[FadeToColor(x, GREEN) for x in spots[2:-2]])
        good_spots = VGroup(spots[2:-2])
        s.play(Succession(LaggedStart(*[ShrinkToCenter(x) for x in spots[-2:]+spots[:2]], lag_ratio = 0.6) ,Succession(ScaleInPlace(good_spots, 1.25), ScaleInPlace(good_spots, 0.8), run_time=0.7)))
        s.play(Wait(0.5))
        s.play(LaggedStart(FadeOut(x, shift=DOWN, scale=0.5) for x in spots[::-1] + backing_game.get_live_tiles()))

class freedom_of_movement(Scene):
    rules = [Tex('Freedom of Movement').set_x(-3).set_y(3),
             Tex('One Hive').set_x(-4.4).set_y(2)]
    pointer= Triangle(color=WHITE, fill_opacity=1).rotate(-PI/2).scale(0.1).next_to(rules[0],LEFT)

    def construct(self):
        freedom_of_movement.play_scene(self)
    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 48.m4a")
        rules = freedom_of_movement.rules
        s.play(LaggedStart(*[Write(rule) for rule in freedom_of_movement.rules], lag_ratio=0.9))
        pointer = freedom_of_movement.pointer
        s.play(Wait(1))
        s.play(ApplyMethod(rules[1].set_opacity, 0.3), FadeIn(pointer,shift=UP))
        s.play
        
        g = game(s, center=RIGHT*2 + DOWN)
        g.make_moves(['wS1', 'bS1 wS1/', 'wQ -wS1', 'bQ \\bS1', 'wA1 /wQ', 'bA1 bQ/'])
        g.set_tiles_to_target()
        #ss.play(DrawBorderThenFill(g.bugs['wS1'].tile))
        s.remove(*g.all_tiles)
        s.play(LaggedStart(*[DrawBorderThenFill(i) for i in g.get_live_tiles()]))
        # s.play(g.move('wQ', 'bQ-',curve_dir=-1))
        # s.play(g.move('wQ', 'bQ/',curve_dir=-1))
        # s.play(Succession(g.move('wQ', '\\bQ',curve_dir=-1),
        #                   g.move('wQ', '-bQ',curve_dir=-1),g.move('wQ', '/bQ',curve_dir=-1)))
        s.play(Wait(2))
        s.play(g.move('bA1','\\bQ',curve_dir=-1))
        s.play(g.move('bA1','-bQ',curve_dir=-1))
        s.play(g.move('bA1','\\bQ',curve_dir=1))
        s.play(g.move('bA1','bQ/',curve_dir=1))
        s.play(g.move('wA1','-wQ',curve_dir=1))
        s.play(g.move('wA1','\\wQ',curve_dir=1))
        s.play(g.move('wA1','-wQ',curve_dir=-1))
        s.play(g.move('wA1','/wQ',curve_dir=-1))
        s.play(g.move('bA1','\\bQ',curve_dir=-1))
        s.play(g.move('bA1','-bQ',curve_dir=-1))
        s.play(g.move('bA1','/bQ',curve_dir=-1))
        check = Tex("\checkmark").set_color(GREEN).shift(LEFT)
        x = VGroup(Line(UP+RIGHT, DOWN+LEFT),Line(UP+LEFT,DOWN+RIGHT)).set_color(RED).scale(0.3).shift(LEFT)
        s.play(Write(check))
        s.play(g.move('bA1','-bQ',curve_dir=1))
        s.play(g.move('wA1','-wQ',curve_dir=1))
        s.play(g.move('wA1','\\wQ',curve_dir=1))
        s.play(g.move('wA1','-bA1',curve_dir=1))
        s.play(g.move('wA1','\\wQ',curve_dir=-1))
        wA1=g.bugs["wA1"].tile
        start_pos=wA1.get_center()
        end_pos= start_pos+g.right_basis
        wQ=g.bugs["wQ"].tile
        bA1=g.bugs["bA1"].tile
        s.play(LaggedStart([MoveAlongPath(wA1,CubicBezier(start_pos, start_pos+ LEFT, end_pos+LEFT, end_pos)),AnimationGroup(wQ.animate.shift(DOWN*0.4), bA1.animate.shift(UP*0.4),Transform(check,x), rate_func=rush_from)], lag_ratio=0.5))
        s.pause(1)
        s.play(FadeOut(check,*g.get_live_tiles()))

class one_hive_rule(Scene):
    def construct(self):
        one_hive_rule.play_scene(self)
    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 52.m4a")
        rules= freedom_of_movement.rules
        rules[1].set_opacity(0.3)
        pointer = freedom_of_movement.pointer
        s.add(*rules, pointer)
        s.play(Transform(pointer,pointer.copy().next_to(rules[1], direction=LEFT)), ApplyMethod(rules[0].set_opacity,0.3), ApplyMethod(rules[1].set_opacity,1))
        analysis_file='./media/analysis_files/analysis_08-Jun-2025_22_59_31.json'
        with open(analysis_file, 'r') as file:
            data = json.load(file)
        backing_game=game(s,analysis_json=data, center = 2*RIGHT + DOWN)
        backing_game.next_n_moves(12)
        backing_game.set_tiles_to_target()
        s.remove(*backing_game.get_live_tiles())
        s.play(*[DrawBorderThenFill(i) for i in backing_game.get_live_tiles()])
        s.play(Wait(1))
        wA = backing_game.bugs["wA1"].tile
        s.play(backing_game.move("bA1", "bG1-", curve_dir=-1))
        group1=('bG1', 'bS1', 'bA1')
        group2=('bP','bQ','bL','wL','wQ','wM','wA1','wS1','wG1')
        g1=VGroup(backing_game.bugs[i].tile for i in group1)
        g2=VGroup(backing_game.bugs[i].tile for i in group2)
        g3=VGroup([backing_game.bugs[i].tile for i in ("wS1","wG1")])
        big_x = VGroup(Line(LEFT+UP, RIGHT +DOWN, color=RED),Line(LEFT-UP,RIGHT -DOWN,color=RED)).scale(2).move_to(g2.get_center())
        s.play(LaggedStart(Wiggle(g1), Wiggle(g2),Write(big_x), lag_ratio=0.4))
        s.play(Wait(1))
        s.play(LaggedStart(Unwrite(big_x),backing_game.move("bA1", "bG1\\", curve_dir=1),lag_ratio=0.6))
        s.play(Wait(0.5))
        s.play(ScaleInPlace(wA,0.01))
        s.play(Wait(1))
        s.play(Wiggle(g3))
        s.play(ScaleInPlace(wA,100))
        s.play(Wait(0.5))
        s.play(backing_game.move("wA1", "wG1\\", curve_dir=-1))
        small_x=VGroup(Line(LEFT+UP,RIGHT+DOWN, color=RED),Line(LEFT+DOWN, RIGHT+UP, color=RED)).move_to(wA.get_center()).scale(0.5)
        s.play(Write(small_x))
        s.wait()
        s.play(Unwrite(small_x))
        s.play(backing_game.move("wA1",'wS1\\', curve_dir=1))
        s.wait(0.4)
        s.play(LaggedStart(*[Wiggle(backing_game.bugs[i].tile) for i in ('wS1','wA1','wL','bL','bA1','bG1')],lag_ratio=0.3))
        s.play(LaggedStart(FadeOut(*backing_game.get_live_tiles(), VGroup(*rules, pointer))))



class piece_rules(Scene):
    def construct(self):
        piece_rules.play_scene(self)
    def get_pieces(s):
        bg = game(s)
        bugs = [bg.bugs[i].tile for i in ('wQ', 'wA1', 'wS1', 'wG1', 'wB1', 'wM', 'wL', 'wP')]
        for i in range(len(bugs)):
            bugs[i].rotate(-PI/6).to_edge().set_y(3.5-i)
        instructions = ['Crawl one space', 'Crawl any distance', 'Crawl 3 spaces', 'Jump in line to empty spot','Move 1 or Climb','Copy adjacent bug','Crawl 2 on top, then 1 down','Move 1 or warp adjacent bug']
        text = [Text(instructions[i],font_size = 30).next_to(bugs[i]) for i in range(len(instructions))]
        analysis_file='./media/analysis_files/analysis_11-Jun-2025_17_38_23.json'
        with open(analysis_file, 'r') as file:
            data = json.load(file)
        backing_game=game(s, tile_size=0.75,analysis_json=data, center=2*RIGHT + 0.75*0.5*rotate_vector(LEFT, -PI/3))
        backing_game.next_n_moves(18)
        backing_game.set_tile_positions()
        return bugs, text, backing_game

    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 61.m4a")


        pieces, text, backing_game = piece_rules.get_pieces(s)
        #s.add(*text)
        s.remove(*backing_game.get_live_tiles())
        s.play(LaggedStart([FadeIn(i, shift=RIGHT) for i in pieces]))
        s.play(LaggedStart([DrawBorderThenFill(i) for i in backing_game.get_live_tiles()]))

        #s.add(*backing_game.get_live_tiles())
        s.play(Wait(1))
        moves = [
            [["wQ \\wL", "bQ bL\\", "wQ -wL", 'bQ bL-', "wQ \\wL", "bQ bL\\",'wQ wL/', 'bQ /bL'], [-1,-1,-1,-1,1,1,1,1], 0.8],
            [['wA1 wB1-', 'wA1 wG1-', 'wA1 bL-', 'wA1 bQ-', 'wA1 bM-', 'wA1 bP-','wA1 bP\\','wA1 /bP','bA1 -bB1', 'bA1 -bG1', 'bA1 -wL', 'bA1 -wQ', 'bA1 -wM', 'bA1 -wP','bA1 \\wP','bA1 wP/', 
              'wA1 bP\\', 'wA1 bP-', 'wA1 bM-', 'wA1 bQ-', 'wA1 bL-', 'wA1 wG1-', 'wA1 wB1-', 'wA1 wM-', 'bA1 \\wP', 'bA1 -wP', 'bA1 -wM', 'bA1 -wQ', 'bA1 -wL', 'bA1 -bG1', 'bA1 -bB1', 'bA1 -bM'
              ], [1]*16+[-1]*16, 0.2],
            [['wS1 wA1-', 'wS1 wB1-', 'wS1 wG1-', 'bS1 -bA1', 'bS1 -bB1', 'bS1 -bG1', 'wS1 bL-', 'wS1 bQ-', 'wS1 bM-',
              'bS1 -wL','bS1 -wQ','bS1 -wM','wS1 bQ-','wS1 bL-', 'wS1 wG1-','bS1 -wQ','bS1 -wL','bS1 -bG1','wS1 wB1-','wS1 wA1-', 'wS1 wP-', 'bS1 -bB1','bS1 -bA1', 'bS1 -bP'], [1]*12 + [-1]*12, 0.4]
        ]

        for i in range(len(moves)):
            if i == 1:
                s.add_sound(".\\media\\narration\\New Recording 62.m4a", 0.5)
                s.play(Wait(1))
            elif i == 2:
                s.add_sound(".\\media\\narration\\New Recording 6.m4a")
                s.play(Wait(0.5))
            s.play(AddTextLetterByLetter(text[i]))
            for m in range(len(moves[i][0])):
                move = moves[i][0][m].split(' ')
                s.play(backing_game.move(move[0], move[1], curve_dir=moves[i][1][m]),run_time=moves[i][2])
        s.play(Wait(6))
        # for i in ('wL\\','/bA1','bA1\\'):
        #     s.play(backing_game.move('wS1', i, curve_dir=-1), run_time=0.4)
        # s.play(MoveAlongPath(backing_game.bugs['bS1'].tile, backing_game.get_multi_path('\\bQ','\\bL','wA1/','\\wA1', curve_dir=-1),rate_func=linear, run_time=1.2))

class piece_rules_2(Scene):
    def construct(self):
        piece_rules_2.play_scene(self)
    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 27.m4a")
        pieces, text, backing_game = piece_rules.get_pieces(s)
        s.add(*pieces, *backing_game.get_live_tiles(), *text[0:3])
        s.play(Wait(0.5))
        s.play(AddTextLetterByLetter(text[3]))
        s.play(Wait(0.5))
        moves = ['wG1 -wL', 'bG1 bL-', 'wG1 wL-', 'bG1 -bL', 'wG1 /bP', 'bG1 wP/', 'wG1 wL-', 'bG1 -bL', 'wG1 wS1/', 'bG1 /bS1', 'wG1 wL-', 'bG1 -bL',]
        for move in moves:
            bug, pos = move.split(' ')
            tile = backing_game.bugs[bug].tile
            rt = 1.25
            s.play(AnimationGroup(Succession(ScaleInPlace(tile, 5/4, run_time=rt/2),ScaleInPlace(tile, 4/5, run_time=rt/2)), AnimationGroup(backing_game.move(bug,pos,curve_dir=0.0001, run_time=rt), run_time=rt)))
        s.play(Wait(1))

class piece_rules_3(Scene):
    def construct(self):
        piece_rules_3.play_scene(self)
    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 28.m4a")
        pieces, text, backing_game = piece_rules.get_pieces(s)
        s.add(*pieces, *backing_game.get_live_tiles(), *text[0:4])
        s.play(AddTextLetterByLetter(text[4][:5]))
        moves = ['wB1 wG1-', 'bB1 -bG1','wB1 bL-','bB1 -wL','wB1 bQ-', 'bB1 -wQ','wB1 bQ', 'bB1 wQ','wB1 bG1', 'bB1 wG1','wB1 bL', 'bB1 wL']
        for m in range(len(moves)):
            if m == 6:
                s.play(AddTextLetterByLetter(text[4][5:]))
            bug, pos = moves[m].split(' ')
            s.play(backing_game.move(bug,pos, curve_dir=(1 if m < 6 else -1 if m == 11 else 0), run_time=1 if m < 6 else 1.5))
        hexes = (backing_game.hex_at_position('-wL').set_stroke(GRAY),backing_game.hex_at_position('bL-').set_stroke(WHITE))
        s.play(Wait(5))
        s.play(GrowFromPoint(hexes[0],hexes[0].get_center()+rotate_vector(DOWN/2,PI/3)), GrowFromPoint(hexes[1], hexes[1].get_center()+rotate_vector(UP/2,PI/3)))
        s.play(Wait(3))
        resetMoves = ['wB1 wG1', 'bB1 bG1', 'wB1 wQ-', 'bB1 -bQ']
        for m in range(len(resetMoves)):
            bug, pos = resetMoves[m].split(' ')
            animations = [backing_game.move(bug, pos, curve_dir=-1 if m == 0 else 0)]
            if m < 2:
                animations.append(ShrinkToCenter(hexes[1-m], rate_func=rush_from))
            s.play(AnimationGroup(animations), run_time=1.5)

class piece_rules_4(Scene):
    def construct(self):
        piece_rules_4.play_scene(self)
    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 29.m4a")
        pieces, text, backing_game = piece_rules.get_pieces(s)
        s.add(*pieces, *backing_game.get_live_tiles(), *text[0:5])
        s.play(AddTextLetterByLetter(text[5]))
        s.wait(1)
        bM=backing_game.bugs['bM']
        backing_game.move('bA2','bA1-')
        backing_game.set_tile_positions()
        bA = backing_game.bugs['bA2']
        bA.tile.rotate(2*PI/3)
        bA.svg_t.rotate(-PI/3)
        s.remove(bA.tile)
        s.play(Succession(Wiggle(bM.tile, run_time=2),Rotate(bM.svg_bug,PI/3,about_point=bM.svg_t.get_center()), AnimationGroup(FadeOut(bM.svg_bug),FadeIn(bA.svg_bug))))
        s.wait(0.67)
        s.remove(bM.svg_t)
        s.add(bA.tile)
        moves = ['bA2 bP-','bA2 bP\\', 'bA2 /bP', 'bA2 /bS1', 'bA2 -bS1', 'bA2 \\bS1', 'bA2 -bB1','bA2 -bG1']
        for m in moves:
            s.play(backing_game.move(*m.split(' '), curve_dir=1), run_time=0.2)
        s.play(Wait(0.5))
        backing_game.move('bM', '-bG1')
        backing_game.set_tile_positions()
        s.add(bM.tile)
        s.bring_to_front(bA.tile)
        s.play(FadeOut(bA.tile))
        s.remove(bA.svg_t)
        s.add(bM.tile)
        s.play(Rotate(bM.svg_bug, -PI/3, about_point=bM.svg_t.get_center()))
        wM = backing_game.bugs['wM']
        backing_game.move('wB2', '-wA1')
        wB = backing_game.bugs['wB2']
        wB.tile.rotate(-2*PI/3)
        s.remove(wB.tile)
        s.play(Rotate(wM.svg_bug,-PI, about_point=wM.svg_t.get_center()))
        backing_game.set_tile_positions()
        s.play(AnimationGroup(FadeIn(wB.svg_bug), FadeOut(wM.svg_bug)))
        s.remove(wM.svg_t)
        s.play(backing_game.move('wB2', 'wP'))
        backing_game.move('wM','wP')
        backing_game.set_tile_positions()
        s.add(wM.tile)
        s.bring_to_front(wB.tile)
        s.play(FadeOut(wB.tile))
        s.play(Rotate(wM.svg_bug, PI, about_point=wM.svg_t.get_center()))

        backing_game.move('bG2', '-bG1')
        backing_game.set_tile_positions()
        bG = backing_game.bugs['bG2']
        bG.tile.rotate(-PI/3)
        s.remove(bG.tile)
        s.play(Rotate(bM.svg_bug, -2*PI/3, about_point=bM.svg_t.get_center()))
        s.play(AnimationGroup(FadeIn(bG.svg_bug), FadeOut(bM.svg_bug)))
        bG.svg_t.rotate(-PI/3)
        s.add(bG.svg_t)
        s.remove(bM.tile)
        s.remove(bM.svg_t)
        s.remove(bM.svg_bug)
        s.play(AnimationGroup(Succession(ScaleInPlace(bG.tile, 5/4, run_time=0.5),ScaleInPlace(bG.tile, 4/5, run_time=0.5)),backing_game.move('bG2','bA1-', curve_dir=0.0001)))
        backing_game.move('bM', 'bA1-')
        backing_game.set_tile_positions()
        s.add(bM.tile)
        s.bring_to_front(bG.tile)
        s.play(FadeOut(bG.tile))
        s.play(Rotate(bM.svg_bug, 2*PI/3, about_point=bM.svg_t.get_center()))

        wB.svg_bug.rotate(PI, about_point=wB.svg_t.get_center())
        s.play(AnimationGroup(FadeIn(wB.svg_bug), FadeOut(wM.svg_bug)))
        s.remove(wM.svg_t)
        s.play(backing_game.move('wB2', '-wA1'))
        backing_game.move('wM','-wA1')
        backing_game.set_tile_positions()
        s.add(wM.tile)
        s.bring_to_front(wB.tile)
        s.play(FadeOut(wB.tile))

        s.play(Wait(4))


class piece_rules_5(Scene):
    def construct(self):
        piece_rules_5.play_scene(self)
    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 46.m4a")
        pieces, text, backing_game = piece_rules.get_pieces(s)
        s.add(*pieces, *backing_game.get_live_tiles(), *text[0:6])
        s.play(AddTextLetterByLetter(text[6]))
        s.wait(1)
        moves = [
            ['wL bL', 'wL bG1', 'wL -bG1'],
            ['wL bG1', 'wL bQ', 'wL bM-'],
            ['wL bM', 'wL bA1', 'wL \\bA1'],
            ['wL bB1', 'wL bG1', 'wL -wG1']
        ]

        for move in moves:
            s.play(Wait(1.5))
            for submove in move:
                s.play(backing_game.move(*submove.split(' ')))
        s.play(Wait(1.5))

class piece_rules_6(Scene):
    def construct(self):
        piece_rules_6.play_scene(self)
    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 51.m4a")
        pieces, text, backing_game = piece_rules.get_pieces(s)
        s.add(*pieces, *backing_game.get_live_tiles(), *text[0:7])
        s.play(Wait(1))
        s.play(AddTextLetterByLetter(text[7][:5]))
        s.play(Wait(1))
        moves = ['wP \\wS1', 'bP bS1\\', 'wP -wS1', 'bP bS1-']
        for m in range(len(moves)):
            s.play(backing_game.move(*moves[m].split(' '),curve_dir=1 if m < 2 else -1))
        s.play(AddTextLetterByLetter(text[7][5:]))
        wP = backing_game.bugs['wP'].tile
        bP = backing_game.bugs['bP'].tile
        s.play(Wait(1))
        s.play(backing_game.move('wS1', 'wP'), Rotate(wP, TAU,axis=UP))
        s.play(Wait(1))
        s.play(backing_game.move('wS1', 'wP/'), Rotate(wP,TAU, axis=rotate_vector(UP, PI/3)))
        s.play(Wait(2))
        ant_sequence_b = ['-bB1', '-bG1', '-wL', '-wQ', '-wM', '-wP', '-wS1']
        for i in ant_sequence_b:
            s.play(backing_game.move('bA1', i, run_time=0.24))
        bA = backing_game.bugs['bA1'].tile
        for _ in range(3):
            bA.z_index = 1
            wP.z_index=0
            s.play(Wait(0.5))
            s.play(AnimationGroup(backing_game.move('bA1','wP'), Rotate(wP,TAU,rotate_vector(UP, -PI/3)),run_time=0.3))
            bA.z_index = 1
            wP.z_index=0
            s.play(AnimationGroup(backing_game.move('bA1','-wP'), Rotate(wP,TAU,UP),run_time=0.3))
            s.play(Wait(0.5))
            s.play(backing_game.move('bA1', '\\wP', curve_dir=1), run_time=0.4)
        bA.z_index=0
        s.play(Wait(0.5))
        top_x = VGroup(Line(UP,DOWN, stroke_width=20),Line(LEFT,RIGHT, stroke_width=20)).rotate(PI/4).move_to((bA.get_center() + wP.get_center())/2).set_stroke_color(RED)
        top_x.z_index=1
        s.play(FadeIn(top_x))
        s.play(Wait(3))
        s.play(FadeOut(top_x))
        ant_sequence_w = ['wB1-', 'wG1-', 'bL-', 'bQ-', 'bM-', 'bP-']        
        for i in ant_sequence_w:
            s.play(backing_game.move('wA1', i, curve_dir=1, run_time=0.24), run_time=0.24)
        wA = backing_game.bugs['wA1'].tile
        wA.z_index = 1
        s.play(Wait(0.5))
        x_small = VGroup(Line(UP,DOWN, stroke_width=12), Line(LEFT,RIGHT, stroke_width=12)).scale(0.6).rotate(PI/4).move_to(wA.get_center()+RIGHT) .set_stroke_color(RED)
        s.play(backing_game.move('wA1', 'bP'), Rotate(bP, TAU, axis=UP), FadeIn(x_small, shift=LEFT))
        s.play(backing_game.move('wA1', 'bP-'), Rotate(bP, -TAU, axis=UP))
        s.play(Wait(0.5))
        s.play(backing_game.move('bB1', 'bG1'), FadeOut(x_small))
        s.play(backing_game.move('wB1', 'wG1'))
        check = Tex("\checkmark").set_color(GREEN).shift(LEFT).move_to(x_small.get_center())
        s.play(backing_game.move('wA1', 'bP'), Rotate(bP, TAU, axis=UP), FadeIn(check, shift=LEFT))
        s.play(Wait(0.5))
        s.play(backing_game.move('wA1', '\\bP'), Rotate(bP, TAU, axis=rotate_vector(UP, -PI/3)))
        s.play(FadeOut(check))
        x_small.move_to(backing_game.get_location('\\wA1'))
        check.move_to(x_small)
        s.play(FadeIn(x_small, shift=RIGHT), backing_game.move('wA1', '-bQ', curve_dir=1))
        s.play(FadeOut(x_small),backing_game.move('wA1', '-bM', curve_dir=-1))
        s.play(backing_game.move('wB1', 'bL'))
        s.play(backing_game.move('bB1', 'wB1'))
        s.play(FadeIn(check, shift=RIGHT),backing_game.move('wA1','-bQ', curve_dir=1))
        s.play(Wait(1.75))
        s.play(*[FadeOut(x) for x in [check] + [x.tile for x in backing_game.get_live_bugs()]])

class beetle_gate(Scene):
    def construct(self):
        beetle_gate.play_scene(self)
    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 53.m4a")
        pieces, text, backing_game = piece_rules.get_pieces(s)
        s.remove(*backing_game.all_tiles)
        s.add(*pieces,*text)
        s.play(Wait(1.5))
        s.play(LaggedStart(*[MoveAlongPath(i, CubicBezier(i.get_center(), i.get_center()+RIGHT, i.get_center() + RIGHT, i.get_center())) for i in text]), 
               LaggedStart(*[Succession(ScaleInPlace(i, 6/5, run_time=0.5), ScaleInPlace(i, 5/6, run_time=0.5)) for i in pieces]))
        g = game(s, center=RIGHT*2)
        g.move('bQ', "")
        g.make_moves(['wQ -bQ', 'bA1 bQ\\', 'wA1 bQ/', 'bB1 wA1-', 'wB1 bA1-', 'wB2 bQ-'])
        g.set_tile_positions()
        s.play(FadeIn(VGroup(g.get_live_tiles())))
        s.play(g.move('wB1', 'bA1'))
        s.play(g.move('bB1', 'wA1'))
        
        t1 = Tex('Google').move_to(3*UP + 1.5*RIGHT)
        t2 = Tex('En Passant').next_to(t1).shift(UP*0.07)
        line = Line(t2.get_center() + LEFT *1.3, t2.get_center() + RIGHT * 1.3)
        
        s.play(FadeIn(VGroup(t1, t2), Write(line)))
        s.play(Write(line))
        s.play(FadeOut(line), Transform(t2, Tex('Beetle Gate').next_to(t1).shift(UP*0.07)))
        s.play(FadeOut(VGroup(t1, t2, *g.get_live_tiles(), *pieces, *text )))

class show_classic_set(Scene):
    def construct(self):
        show_classic_set.play_scene(self)
    def get_classic_game(s, analysis_file=None, from_side = False, center = ORIGIN):
        if analysis_file :
            with open(analysis_file, 'r') as file:
                data = json.load(file)
            g = game(s, analysis_json=data, center=center)
        else:
            g = game(s, center=center)
        g.black_bugs = [i for i in g.black_bugs if i.name.split(' ')[1] not in ['Pillbug', 'Ladybug', 'Mosquito']]
        g.white_bugs = [i for i in g.white_bugs if i.name.split(' ')[1] not in ['Pillbug', 'Ladybug', 'Mosquito']]
        if from_side:

            for i in range(11):
                g.black_bugs[i].tile.move_to((1 if i >= 5 else 0) * RIGHT+ (i if i < 5 else i - 5.5)* UP + 2*DOWN + 5.2*RIGHT)
                g.white_bugs[i].tile.move_to((1 if i >= 5 else 0) * LEFT+ (i if i < 5 else i - 5.5)* UP + 2*DOWN + 5.2 * LEFT)
            return g
        x = -5
        for i in g.black_bugs:
            i.tile.move_to(x*RIGHT+UP)
            x+=1
            
        x = -5
        for i in g.white_bugs:
            i.tile.move_to(x*RIGHT+DOWN)
            x+=1
        return g
    
    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 54.m4a")
        backing_game = show_classic_set.get_classic_game(s)
        s.wait(1)
        s.play(LaggedStart(*[FadeIn(i.tile, shift=UP) for i in backing_game.black_bugs ], lag_ratio = 0.1), LaggedStart(*[FadeIn(i.tile, shift=DOWN) for i in backing_game.white_bugs], lag_ratio = 0.1))
        s.wait(3.5)
        s.play(*[backing_game.bugs[i].tile.animate.shift(DOWN) for i in ['wA1', 'wA2', 'wA3']], *[backing_game.bugs[i].tile.animate.shift(UP) for i in ['bA1', 'bA2', 'bA3']])
        s.play(*[backing_game.bugs[i].tile.animate.shift(DOWN) for i in ['wG1', 'wG2', 'wG3']], *[backing_game.bugs[i].tile.animate.shift(UP) for i in ['bG1', 'bG2', 'bG3']])
        s.play(*[backing_game.bugs[i].tile.animate.shift(DOWN) for i in ['wB1', 'wB2']], *[backing_game.bugs[i].tile.animate.shift(UP) for i in ['bB1', 'bB2']])
        s.play(*[backing_game.bugs[i].tile.animate.shift(DOWN) for i in ['wS1', 'wS2']], *[backing_game.bugs[i].tile.animate.shift(UP) for i in ['bS1', 'bS2']])
        
        # s.play([ScaleInPlace(backing_game.bugs[i].tile, 1.1) for i in ['wG1', 'wG2', 'wG3', 'bG1', 'bG2', 'bG3']])
        # s.play([ScaleInPlace(backing_game.bugs[i].tile, 1.1) for i in ['wB1', 'wB2', 'bB1', 'bB2']])
        # s.play([ScaleInPlace(backing_game.bugs[i].tile, 1.1) for i in ['wS1', 'wS2', 'bS1', 'bS2']])
        # s.play([ScaleInPlace(i.tile, 1/1.1) for i in backing_game.black_bugs + backing_game.white_bugs])
        for i in range(11):
            backing_game.black_bugs[i].tile.generate_target().move_to((1 if i >= 5 else 0) * RIGHT+ (i if i < 5 else i - 5.5)* UP + 2*DOWN + 5.2*RIGHT)
            backing_game.white_bugs[i].tile.generate_target().move_to((1 if i >= 5 else 0) * LEFT+ (i if i < 5 else i - 5.5)* UP + 2*DOWN + 5.2 * LEFT)
        s.play(*[MoveAlongPath(i.tile, Line(i.tile.get_center(), i.tile.target.get_center())) for i in backing_game.black_bugs + backing_game.white_bugs])
        for i in range(3):
            backing_game.bugs[['wP','wL','wM'][i]].tile.move_to(4*LEFT + i*UP + DOWN)
            backing_game.bugs[['bP','bL','bM'][i]].tile.move_to(4*RIGHT + i*UP + DOWN)
        s.play(LaggedStart(*[FadeIn(backing_game.bugs[i].tile, shift=DOWN) for i in ['wP','wL','wM','bP','bL','bM']]))
        s.wait(3)
        s.play(LaggedStart(*[FadeOut(backing_game.bugs[i].tile, shift=DOWN) for i in ['wP','wL','wM','bP','bL','bM']]))
        s.wait(3.5)


class beginner_game(Scene):
    def construct(self):
        beginner_game.play_scene(self)
    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 55.m4a")
        s.add_sound(".\\media\\narration\\New Recording 56.m4a", time_offset=16)
        analysis_file = ".\\media\\analysis_files\\analysis_17-Jun-2025_19_50_13.json"
        backing_game = show_classic_set.get_classic_game(s, analysis_file, True)
        classic_pieces = [i for i in backing_game.bugs.values() if i.name.split(' ' )[1] not in ['Pillbug', 'Ladybug', 'Mosquito']]
        s.add(*[i.tile for i in classic_pieces])
        #pieces = VGroup([i.tile for i in classic_pieces])
        for i in classic_pieces:
            i.tile.save_state()
        #pieces.save_state()
        s.play(Wait(1))
        for i in range(23):
            s.play(backing_game.next_move(), run_time=0.4)
            s.wait(0.5)
        s.play(Wait(3))
        for i in range(11):
            backing_game.black_bugs[i].tile.generate_target().move_to((1 if i >= 5 else 0) * RIGHT+ (i if i < 5 else i - 5.5)* UP + 2*DOWN + 5.2*RIGHT)
            backing_game.white_bugs[i].tile.generate_target().move_to((1 if i >= 5 else 0) * LEFT+ (i if i < 5 else i - 5.5)* UP + 2*DOWN + 5.2 * LEFT)
        s.play([MoveToTarget(i.tile) for i in backing_game.black_bugs + backing_game.white_bugs])
        s.wait(1.5)

class basic_tactics(Scene):
    def get_text():
        return [Tex("Pin").set_y(3), Tex("Gate").set_y(2)]
    def construct(self):
        basic_tactics.play_scene(self)
    def play_scene(s):
        backing_game = show_classic_set.get_classic_game(s,  from_side=True)
        classic_pieces = [i for i in backing_game.bugs.values() if i.name.split(' ' )[1] not in ['Pillbug', 'Ladybug', 'Mosquito']]
        s.add(*[i.tile for i in classic_pieces])
        s.add_sound(".\\media\\narration\\New Recording 57.m4a")
        tactics = ['True Pin', 'False Pin', 'Bidirectional Pin', 'Pin Replacement', 'Double Beetle Attack', 'Recover', 'Trigger Fill','Direct Drop', 'Pocket','Beetle Factory', 'Cavern','Ring', 'Concentric Ring','C Opening', 'Z Opening','Buffer Opening', 'Anti-Spawn', 'Ant Farm','Instant Double Ant', 'Spider re-index','Ambiguous Spider', 'Mosquito Shutdown','Proximity Pillbug Attack','Choking the Queen']
        j = len(tactics)/2
        t=[]
        for i in range(len(tactics)):
            t.append(Tex(tactics[i]).set(height=0.2).move_to(i//j*RIGHT*3 + i%j*DOWN*0.5 + LEFT*1.5 + UP*j/4))
        s.play(LaggedStart(*[FadeIn(x) for x in t]))
        s.wait(2)
        dw = Tex("Don't worry, you don't need to know all these!").shift(DOWN * 3.2)
        s.play(FadeIn(dw, shift=UP))
        s.wait(3)
        s.play(FadeOut(VGroup(*t,dw)))
        text=basic_tactics.get_text()
        s.play(FadeIn(text[0]))
        s.play(FadeIn(text[1]))
        s.wait(1)

class pin(Scene):
    def construct(self):
        pin.play_scene(self)
    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 58.m4a")
        backing_game = show_classic_set.get_classic_game(s,  from_side=True)
        classic_pieces = [i for i in backing_game.bugs.values() if i.name.split(' ' )[1] not in ['Pillbug', 'Ladybug', 'Mosquito']]
        text = basic_tactics.get_text()
        s.add(*[i.tile for i in classic_pieces], *text)
        pointer = Triangle(color=WHITE, fill_opacity=1).rotate(-PI/2).scale(0.1).next_to(text[0],LEFT)
        s.play(FadeIn(pointer, shift=UP), text[1].animate.set_opacity(0.3))
        moves = ['wG1', 'bG1 wG1-', 'wQ /wG1', 'bQ bG1/','wA1 wQ\\', 'bA1 bG1\\']
        s.wait(3)
        s.play(backing_game.make_moves(moves))
        s.wait(1)
        s.play(backing_game.move('wA1', '/bA1'))
        s.wait(1)
        s.play(backing_game.bugs['bA1'].tile.animate.shift(RIGHT/2),LaggedStart( Wiggle(backing_game.bugs['wA1'].tile), Wiggle(VGroup([backing_game.bugs[i].tile for i in ['bQ','bG1','wQ','wG1']])), lag_ratio = 0.4))
        s.play(backing_game.bugs['bA1'].tile.animate.shift(LEFT/2))
        small_x=VGroup(Line(LEFT+UP,RIGHT+DOWN, color=RED),Line(LEFT+DOWN, RIGHT+UP, color=RED)).move_to(backing_game.bugs['bA1'].tile.get_center()).scale(0.5)
        s.play(Write(small_x))        
        s.wait(1)
        #s.play(*[MoveAlongPath(spot[0], Line(spot[0].get_center(), spot[1])) for spot in spots], FadeOut(small_x))
        s.play(FadeOut(small_x))


class gate(Scene):
    def construct(self):
        gate.play_scene(self)
    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 59.m4a")
        backing_game = show_classic_set.get_classic_game(s,  from_side=True)
        classic_pieces = [i for i in backing_game.bugs.values() if i.name.split(' ' )[1] not in ['Pillbug', 'Ladybug', 'Mosquito']]
        text = basic_tactics.get_text()
        text[1].set_opacity(0.3)
        pointer = Triangle(color=WHITE, fill_opacity=1).rotate(-PI/2).scale(0.1).next_to(text[0],LEFT)
        moves = ['wG1', 'bG1 wG1-', 'wQ /wG1', 'bQ bG1/','wA1 wQ\\', 'bA1 bG1\\', 'wA1 /bA1']
        backing_game.make_moves(moves)
        backing_game.set_tile_positions()
        s.add(*[i.tile for i in classic_pieces], *text, pointer)
        line = Line(backing_game.bugs['wQ'].tile.get_center(), backing_game.bugs['wA1'].tile.get_center()).scale(0.33)
        s.play(text[0].animate.set_opacity(0.3),text[1].animate.set_opacity(1), pointer.animate.next_to(text[1], LEFT))
        s.wait(3)
        s.play(Wiggle(backing_game.bugs['wA1'].tile))
        s.play(Write(line))
        s.wait(2)
        hex = backing_game.hex_at_position('wQ-')
        s.play(GrowFromCenter(hex))
        s.wait(2)
        s.play(LaggedStart(FadeOut(text[0]),FadeOut(text[1]), FadeOut(pointer), FadeOut(hex),FadeOut(line)))

class defense_game(Scene):
    def construct(self):
        defense_game.play_scene(self)
    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 60.m4a")
        s.add_sound(".\\media\\narration\\New Recording 63.m4a", time_offset=11)
        analysis_file = ".\\media\\analysis_files\\analysis_17-Jun-2025_20_14_11.json"
        backing_game = show_classic_set.get_classic_game(s, analysis_file, True)
        classic_pieces = [i for i in backing_game.bugs.values() if i.name.split(' ' )[1] not in ['Pillbug', 'Ladybug', 'Mosquito']]        
        spots = []
        for i in classic_pieces:
           spots.append([i.tile, i.tile.get_center()])
        moves = ['wG1', 'bG1 wG1-', 'wQ /wG1', 'bQ bG1/','wA1 wQ\\', 'bA1 bG1\\', 'wA1 /bA1']
        backing_game.make_moves(moves)
        backing_game.set_tile_positions()
        s.add(*[i.tile for i in classic_pieces])
        s.play(*[MoveAlongPath(spot[0], Line(spot[0].get_center(), spot[1])) for spot in spots])
        backing_game.center= UP+LEFT/2
        pass_turns = [34,36,38,40,42,44,46]
        pass_text = Text('White passes').move_to(3*LEFT + DOWN)
        s.wait(3)
        p =0.5
        a= 0.3
        for i in range(48):
            if i in pass_turns:
                backing_game.next_move()
                s.remove(backing_game.bugs['wM'].tile)
                s.wait(p)
                s.play(FadeIn(pass_text),run_time=a)
                continue
            elif i-1 in pass_turns:
                s.play(FadeOut(pass_text), run_time=p)
            else:
                s.wait(p)
            s.play(backing_game.next_move(), run_time=a)
        s.wait(2)
        s.play(ShrinkToCenter(VGroup([i.tile for i in backing_game.white_bugs + backing_game.black_bugs])))

class real_goal(Scene):
    def construct(self):
        real_goal.play_scene(self)
    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 64.m4a")
        goal_text=Text('Goal of hive:').shift(UP*2+4*LEFT)
        surround_text=Text('Surround the enemy queen').next_to(goal_text)
        goal_text.shift(UP*0.08)
        s.play(AddTextLetterByLetter(goal_text))
        s.wait(1)
        s.play(AddTextLetterByLetter(surround_text))
        strikethrough = Line(goal_text.get_center()+ goal_text.width/2*LEFT,goal_text.get_center()+ goal_text.width/2*RIGHT, stroke_width=12)
        s.play(Write(strikethrough))
        s.wait(1)
        s.play(Transform(goal_text, Text('How you win:').next_to(surround_text, LEFT)), FadeOut(strikethrough))
        s.wait(1.5)
        goal_text_2 = Text("Goal").shift(DOWN/2)
        efficiency = Text("Efficiency").shift(2*DOWN, 3*LEFT)
        control = Text("Control").shift(2*DOWN, 3*RIGHT)
        lines = (Line(DOWN, LEFT*3+1.5*DOWN),Line(DOWN, RIGHT*3+1.5*DOWN))
        s.play(FadeIn(goal_text_2))
        s.play(Write(lines[0]),FadeIn(efficiency))
        s.play(Write(lines[1]),FadeIn(control))
        s.wait()
        s.play(Wiggle(control, rotation_angle=0))
        s.wait(2)
        s.play(Wiggle(efficiency, rotation_angle=0))
        s.play(LaggedStart(FadeOut(goal_text, surround_text), VGroup(goal_text_2, efficiency, control, *lines).animate.shift(UP*4), lag_ratio=0.15))
        
class team(Scene):
    def construct(self):
        team.play_scene(self)
    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 65.m4a")
        goal_text = Text("Goal").shift(DOWN/2).shift(UP*4)
        efficiency = Text("Efficiency").shift(2*UP, 3*LEFT)
        control = Text("Control").shift(2*UP, 3*RIGHT)
        lines = (Line(UP*3, LEFT*3+2.5*UP),Line(UP*3, RIGHT*3+2.5*UP))
        s.add(goal_text, efficiency, control, *lines)
        s.wait(6)
        bg1=game(s, center=3*LEFT,tile_size=0.5)
        bg1.make_moves(['bQ','bA1 /bQ','bG1 -bA1','bB1 \\bG1','bS1 bB1/','bL bS1-',
                    'wQ bQ-','wA1 bA1\\','wG1 /bG1', 'wB1 -bB1', 'wS1 \\bS1','wL bL/'])
        bg1.set_tile_positions()
        s.remove(*bg1.get_live_tiles())
        s.play(FadeIn(VGroup(bg1.get_live_tiles())))
        bg2 = game(s, tile_size=0.75)
        bg2.make_moves(['wM', 'wP wM-', 'wB1 wM/', 'wL \\wM', 'wA1 -wM'])
        bg2.set_tile_positions()
        s.remove(*bg2.get_live_tiles())
        s.play(LaggedStart(FadeIn(VGroup([bg2.bugs[i].tile for i in ['wP', 'wB1', 'wL', 'wA1']])), FadeIn(bg2.bugs['wM'].tile), lag_ratio=0.6))
        bg3 = game(s, tile_size=0.75, center = 3*RIGHT, right_basis=rotate_vector(RIGHT, -PI/6), up_basis = rotate_vector(RIGHT, PI/6))
        bg3.make_moves(['bQ', 'bP \\bQ','wB1 bP','wS1 -bP', 'wA1 bQ\\', 'wG1 /wA1', 'wG2 wA1-'])
        bg3.set_tile_positions()
        for i in bg3.get_live_tiles():
            i.rotate(-PI/6)
        s.remove(*bg3.get_live_tiles())
        bg3.bugs['wB1'].tile.z_index = 1
        s.play(LaggedStart(FadeIn(VGroup([bg3.bugs[i].tile for i in ['wA1', 'bQ', 'bP']])), FadeIn(VGroup([bg3.bugs[i].tile for i in ['wS1', 'wG1', 'wG2', 'wB1']])), lag_ratio = 0.6))
        s.wait(2.5)
        s.play(Wiggle(efficiency, rotation_angle=0))
        s.wait(2.5)
        s.play(Wiggle(control, rotation_angle=0))
        left_questions = ['Should I try to free my ant?','Is now a good time to spawn the hopper?','Do my beetles need the support of my mosquito?']
        right_questions = ['Should I stop their beetle from climbing?', 'Which pin spot would cut off more spawn points?', 'Can complicating the situation make finding a good move harder?']
        s.play(LaggedStart(*[FadeIn(Tex(left_questions[i]).set(height=0.2).move_to(i*DOWN/2 + DOWN*2 + 3*LEFT)) for i in range(len(left_questions))], lag_ratio=0.4))
        s.play(LaggedStart(*[FadeIn(Tex(right_questions[i]).set(height=0.2).move_to(i*DOWN/2 + DOWN*2 + 3*RIGHT)) for i in range(len(right_questions))], lag_ratio=0.4))
        s.wait(5)
        s.play(LaggedStart([ShrinkToCenter(i) for i in s.mobjects]))
        
class thats_hive(Scene):
    def construct(self):
        thats_hive.play_scene(self)
    def play_scene(s):
        s.add_sound(".\\media\\narration\\New Recording 66.m4a")
        s.wait(2.2)
        analysis_file='./media/analysis_files/analysis_24-Jun-2025_00_14_21.json'
        with open(analysis_file, 'r') as file:
            data = json.load(file)
        bg= game(s, right_basis=DOWN, up_basis=rotate_vector(DOWN, PI/3), analysis_json=data)
        counter = -4
        for i in bg.black_bugs:
            i.tile.move_to(UP*6 + counter*RIGHT)
        counter = -4
        for i in bg.white_bugs:
            i.tile.move_to(DOWN*6 + counter*RIGHT)
        topline= ['bQ', 'wA1', 'wS1', 'wB1', 'wG1', 'wM', 'wL']
        bottomline= ['wQ', 'bA1', 'bS1', 'bB1', 'bG1', 'bM', 'bL']
        for i in topline:
            bg.bugs[i].tile.rotate(-2*PI/3)
        for i in bottomline:
            bg.bugs[i].tile.rotate(PI/3)
        s.play(LaggedStart(LaggedStart(*[MoveAlongPath(bg.bugs[topline[i]].tile, Line(UP*1.5 + LEFT * 12, UP*1.5+RIGHT*2).add_line_to(UP*1.5+RIGHT*3 if i==0 else UP*1.5+RIGHT*3 + rotate_vector(LEFT, PI/3 * (i-1)))) for i in range(7)], lag_ratio=0.42),
               LaggedStart(*[MoveAlongPath(bg.bugs[bottomline[i]].tile, Line(DOWN*1.5 + RIGHT * 12, DOWN*1.5+LEFT*2).add_line_to(DOWN*1.5+LEFT*3 if i==0 else DOWN*1.5+LEFT*3 + rotate_vector(RIGHT, PI/3 * (i-1)))) for i in range(7)], lag_ratio=0.25), lag_ratio=0.15),
               )
        s.play(LaggedStart(*[Rotate(bg.bugs[i].tile, -2*PI/3, run_time=0.3) for i in bottomline+topline]))
        whiteline = [bg.bugs[i].tile for i in topline[1:4]+topline[4:]]
        blackline = [bg.bugs[i].tile for i in bottomline[1:4]+bottomline[4:]]
        wq=bg.bugs['wQ'].tile
        bq=bg.bugs['bQ'].tile
        s.wait(0.5)
        s.play(Transform(wq, wq.copy().rotate(PI/6).move_to(wq.get_center() + RIGHT * 3 + DOWN)),Transform(bq, bq.copy().rotate(PI/6).move_to(bq.get_center() + LEFT * 3 + UP)), run_time=0.66)
        s.play(*[Transform(blackline[i], blackline[i].copy().move_to(UP/2+ RIGHT*i*1.25 - 2.5*1.25*RIGHT).rotate(7*PI/6)) for i in range(6)],
            *[Transform(whiteline[i], whiteline[i].copy().move_to(DOWN/2+ LEFT*i*1.25 - 2.5*1.25*LEFT).rotate(7*PI/6)) for i in range(6)])

        def flip_func(i):
            def func(mob, dt):
                mob.shift(UP*dt * 0.9 * sin(s.time*(1+ 1/(i+1)+(i+3)%6) + i))
            return func 
        for i in range(6):
            whiteline[i].add_updater(flip_func(i))
            blackline[5-i].add_updater(flip_func(i))
        s.wait(5)
        for i in whiteline+blackline:
            i.clear_updaters()
        inventory = ['wA3', 'wS2', 'bG2', 'bG3','bS2']
        spots = [6*RIGHT+UP/2, 6*RIGHT-UP/2, 6*LEFT+UP, 6*LEFT, 6*LEFT-UP]
        for i in bg.bugs.keys():
            if i in topline or i in bottomline:
                continue
            bg.bugs[i].tile.rotate(-PI/6)
        for i in range(5):
            bg.bugs[inventory[i]].tile.generate_target().move_to(spots[i])
            
        s.play(bg.next_n_moves(50), *[MoveToTarget(bg.bugs[i].tile) for i in inventory])
        
class skill_ceiling(Scene):        
    def construct(self):
        skill_ceiling.play_scene(self)
    def play_scene(s):
        # s.add_sound(".\\media\\narration\\New Recording 67.m4a")
        analysis_file='./media/analysis_files/analysis_24-Jun-2025_00_14_21.json'
        with open(analysis_file, 'r') as file:
            data = json.load(file)
        bg= game(s, right_basis=DOWN, up_basis=rotate_vector(DOWN, PI/3), analysis_json=data)
        inventory = ['wA3', 'wS2', 'bG2', 'bG3','bS2']
        spots = [6*RIGHT+UP/2, 6*RIGHT-UP/2, 6*LEFT+UP, 6*LEFT, 6*LEFT-UP]
        for i in range(50):
            bg.next_move()
        for i in bg.all_tiles:
            i.rotate(-PI/6)
        for i in range(5):
            bg.bugs[inventory[i]].tile.move_to(spots[i])
        for i in bg.get_live_bugs():
            i.tile.move_to(i.tile.target.get_center())
        for i in  ['bQ', 'bA1', 'bS1', 'bB1', 'bG1', 'bM', 'bL'] :
            bg.bugs[i].tile.rotate(PI)
        s.add(*bg.all_tiles)
        s.wait(1)