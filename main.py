from manim import *
from hive import bug, game, assetPathOfficial
from Dice import create_dice
import json

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
    def play_scene(s):
        analysis_file='./media/analysis_files/analysis_08-Jun-2025_22_55_03.json'
        with open(analysis_file, 'r') as file:
            data = json.load(file)
        backing_game=game(s,analysis_json=data)
        backing_game.next_n_moves(8)
        backing_game.set_tile_positions()
        s.add(*backing_game.get_live_tiles())
        s.play(Wait(1))
        for i in ('wL\\','/bA1','bA1\\'):
            s.play(backing_game.move('wS1', i, curve_dir=-1), run_time=0.4)
        s.play(MoveAlongPath(backing_game.bugs['bS1'].tile, backing_game.get_multi_path('\\bQ','\\bL','wA1/','\\wA1', curve_dir=-1),rate_func=linear, run_time=1.2))



