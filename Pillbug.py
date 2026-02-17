from hive_engine import *
import os
from manim import *
from manim_chess.chess_board import ChessBoard

UPRIGHT = rotate_vector(UP, -PI/3)
UPLEFT=rotate_vector(UP, PI/3)
DOWNRIGHT = rotate_vector(DOWN, PI/3)
DOWNLEFT=rotate_vector(DOWN,-PI/3)


class opening(MovingCameraScene):
    def construct(self):
        g = hive_game(self)
        pieces = ['wA1', 'wB1','wG1', 'wL', 'wM', 'wP','wQ', 'wS1']
        tiles = [g.bugs[i].tile for i in pieces]
        for i in range(len(tiles)):
            tiles[i].shift(2.5*UP).rotate_about_origin(-TAU / len(tiles)*i).rotate(TAU/len(tiles)*i- PI/6)
        self.play(LaggedStart([FadeIn(i, shift=-i.get_center()) for i in tiles], lag_ratio=0.2))
        self.wait(1)
        self.play(AnimationGroup([FadeOut(i, scale=1/3, shift=i.get_center()) for i in tiles[:5]+tiles[6:]] + [tiles[5].animate.move_to(ORIGIN).scale(3)]))
        #self.play(self.camera.frame.animate.move_to(tiles[5]).set_height(tiles[5].get_height()*1.3))
        p = tiles[5]
        self.play(Succession(Rotate(p, TAU,axis=RIGHT),Rotate(p, TAU,axis=RIGHT+UP*2**0.5),Rotate(p, TAU,axis=RIGHT+DOWN*2**0.5)))

class rules(Scene):
    def construct(self):
        text = Text("Pillbug Rules").shift(UP*2).scale(2)
        rules = [Text("Crawl 1 space"), Text("Make adjacent bug move to\n another adjacent empty space"), Text(" - aka \"Warping\"")]
        self.play(Write(text))
        self.wait(1)
 
        g = hive_game(self,center = RIGHT*2)
        g.make_moves('wL,bL wL-,wQ -wL,bQ bL/,wP wQ\\,bP \\bQ-'.split(','), no_animate=1)
        g.set_tile_positions()
        tiles = g.get_live_tiles()
        self.remove(*tiles)
        tiles.sort(key=lambda o1: o1.get_x())
        self.play(LaggedStart(text.animate.scale(0.6).shift(UP).to_edge(LEFT),
            LaggedStartMap(DrawBorderThenFill, VGroup(tiles), lag_ratio=0.2), lag_ratio=0.6))
        
        rules[0].next_to(text,DOWN)
        for i in range(1, len(rules)):
            rules[i].next_to(rules[i-1], DOWN)
        for i in rules:
            i.scale(0.6).to_edge(LEFT)
            
        self.play(Write(rules[0]))
        g.play_curve("wP", "/wL","wL\\",-1)
        g.play_curve("bP", "\\bQ","-bQ",-1, run_time=1)        
        wp = g.bugs["wP"].tile
        bp = g.bugs["bP"].tile
        # self.play(MoveAlongPath(wp, g.get_curve('/wL','wL\\',-1)))
        # self.play(MoveAlongPath(bp, g.get_curve('\\bQ','-bQ',-1)))
        #g.make_moves
        self.play(Write(rules[1]))
        self.play(AnimationGroup(Rotate(wp,TAU, rotate_vector(UP, PI/3)),g.move('bL','wP')))
        self.play(AnimationGroup(Rotate(wp,-TAU, UP),g.move('bL','-wP')))
        self.play(AnimationGroup(Rotate(bp, TAU, UP), g.move('bQ', 'bP')))
        self.play(AnimationGroup(Rotate(bp, -TAU, rotate_vector(UP,-PI/3)), g.move('bQ', '\\bP')))
        self.play(Write(rules[2]))

        self.wait(1)

        self.play(LaggedStart(*[FadeOut(x,shift=DOWN) for x in rules[::-1]+[text]], lag_ratio=0.15))

        exception_title = Text("Exceptions").scale(1.2).to_corner(UP+LEFT)
        exceptions_raw_text = ["One Hive and Freedom of Movement\n"+
                               "rules must be followed", 
                               "Stacked pieces cannot\n"+
                               "warp or be warped",
                               "Most recently moved piece cannot\n"+
                               "move, warp, or be warped"]
        exceptions = [Text(i) for i in exceptions_raw_text]
        for i in range(len(exceptions)):
            exceptions[i]
            all = [exception_title] + exceptions
            all[i+1].scale(0.6).next_to(all[i], DOWN).to_edge(LEFT)
        self.play(Write(exception_title))
        self.wait(0.5)
        #play_warp(g, "bP", "bQ", "bP-", UPRIGHT,UP)
        self.play(Write(exceptions[0]))
        g.play_warp("wP", "wL","\\wP",UPRIGHT,DOWNLEFT)
        x = VGroup(Line(UP+LEFT, DOWN+RIGHT,color=RED), Line(UP+RIGHT, DOWN+LEFT, color=RED))
        self.play(Write(x))
        self.play(FadeOut(x))
        self.play(Write(exceptions[1]))
        g.make_moves("wB1 wP-,bB1 bP-".split(","), no_animate = True)
        g.set_tile_positions()
        self.remove(g.bugs['wB1'].tile, g.bugs['bB1'].tile)
        self.play(LaggedStart(GrowFromCenter(g.bugs['wB1'].tile), GrowFromCenter(g.bugs['bB1'].tile), lag_ratio = 0.7), run_time=1)
        self.play(Succession(*g.make_moves("wB1 wP,bB1 bP,wB1 bL".split(","))), run_time=1.5)
        self.play(g.reveal_stacks())
        self.play(AnimationGroup(*[Wiggle(g.bugs[x].tile) for x in ['bB1','wB1','bL','bP']]))
        self.play(g.collapse_stacks())
        self.play(Write(exceptions[2]))
        hex = g.hex_at_position('wL-').set_color(RED)
        self.play(LaggedStart(g.move('bB1','wL-'), GrowFromCenter(hex), lag_ratio=0.5))
        self.wait(1)
        hex2=g.hex_at_position('-bL').set_color(RED)
        self.play(LaggedStart(g.move('wB1','-bL'), ShrinkToCenter(hex), GrowFromCenter(hex2), lag_ratio=0.25))
        self.wait(1)
        hex=hex2
        hex2 = g.hex_at_position('-bP').set_color(RED)
        path = ["wL","bL","wQ","wQ/"]
        pathactual = [[path[x], path[x+1]] for x in range(len(path)-1)]
        self.play(LaggedStart(Succession(*[MoveAlongPath(g.bugs["wL"].tile,g.get_curve(*x)) for x in pathactual], run_time=1.3), ShrinkToCenter(hex),GrowFromCenter(hex2), lag_ratio=0.3))
        hex=hex2
        hex2=g.hex_at_position('wP-').set_color(RED)
        self.play(LaggedStart(Succession(*g.warp('wP','bB1','wP-',DOWNRIGHT,UP)), ShrinkToCenter(hex), GrowFromCenter(hex2), lag_ratio=0.5))
        hex=hex2
        hex2=g.hex_at_position('wQ-').set_color(RED)
        self.play(LaggedStart(g.move('bP','wQ-',curve_dir=1), ShrinkToCenter(hex), GrowFromCenter(hex2), lag_ratio=0.25))
        hex=hex2
        hex2=g.hex_at_position('wP/').set_color(RED)
        self.play(LaggedStart(Succession(*g.warp('wP','bL','wP/',UP,UPLEFT)), ShrinkToCenter(hex), GrowFromCenter(hex2), lag_ratio=0.5))
        hex=hex2
        hex2=g.hex_at_position('bP/').set_color(RED)
        self.play(LaggedStart(Succession(*g.warp('bP','wP','bP/',DOWNLEFT,UPLEFT)), ShrinkToCenter(hex), GrowFromCenter(hex2), lag_ratio=0.5))
        self.wait(1)
        self.play(LaggedStart(LaggedStart(*[Unwrite(j) for j in [i.svg_t for i in g.get_live_bugs()]+[i.svg_bug for i in g.get_live_bugs()]+[hex2]]),LaggedStart(*[FadeOut(i, shift=LEFT*5) for i in [exception_title]+exceptions])))
        
class defense(Scene):
    def construct(self):
        g = hive_game(self, center=DOWN)
        g.make_moves('wL,bG1 \\wL,wQ /wL,bQ bG1/,wA1 wL-,bA1 bQ/'.split(','), no_animate=1)
        g.set_tile_positions()
        
        tiles = g.get_live_tiles()
        self.remove(*tiles)
        self.play(LaggedStart(*[FadeIn(g.bugs[i].tile, shift=(UP if i[0]=='w' else DOWN)) for i in ['wL','bG1', 'wQ','bQ','wA1', 'bA1']], lag_ratio=0.6))
        
        self.play(Succession(*[MoveAlongPath(g.bugs['wA1'].tile, g.get_curve(a[0],a[1],-1)) for a in [['wA1', 'bG1-','bQ-','bA1-','bA1/'][b:b+2] for b in range(4)]], run_time=1.2))
        
        bq_art=g.bugs['bQ'].svg_bug
        ba1_art=g.bugs['bA1'].svg_bug
        self.play(LaggedStart(Rotate(bq_art, -PI/3),Rotate(ba1_art, 2*PI/3), lag_ratio=0.3))
        nudge1=MoveAlongPath(bq_art,CubicBezier(bq_art.get_center(),bq_art.get_center()+rotate_vector(UP,-PI/6)/6,bq_art.get_center()+rotate_vector(UP,-PI/6)/6,bq_art.get_center()))
        self.play(LaggedStart(Succession(*[nudge1]*3, run_time=1),Rotate(ba1_art, -PI)))
        
        g.make_moves('wA1 bA1/,wS1 -wQ,bP \\bQ,wS2 wA1/,bB1 -bG1'.split(','), no_animate=1)
        g.set_tile_positions()
        tiles = [g.bugs[i].tile for i in ['wS1','bP','wS2','bB1']]
        self.remove(*tiles)
        self.play(LaggedStart(FadeIn(g.bugs['wS1'].tile, shift=UP),FadeIn(g.bugs['bP'].tile, shift=DOWN),lag_ratio=0.5))
        self.wait(1)
        self.play(LaggedStart(FadeIn(g.bugs['wS2'].tile, shift=rotate_vector(LEFT,PI/3)),FadeIn(g.bugs['bB1'].tile, shift=RIGHT),lag_ratio=0.6))
        self.play(Succession(*[MoveAlongPath(g.bugs['wS2'].tile,g.get_curve(a[0],a[1],curve_dir=1) ) for a in [['wA1/','wA1-','wA1\\','bQ-'][b:b+2] for b in range(3)]],run_time=1))
        self.play(g.move('bB1','bG1'))
        self.play(Succession(*[MoveAlongPath(g.bugs['wS1'].tile,g.get_curve(a[0],a[1],curve_dir=1) ) for a in [['-wQ','-wL','-bG1','-bQ'][b:b+2] for b in range(3)]],run_time=1))
        g.play_warp('bP','bQ','\\bP',UPRIGHT,UPRIGHT)
        self.wait(1)
        g.make_moves('wS1 /bP,wS2 bA1\\,wP /wQ,bA2 wL-,wB1 -wS1'.split(','), no_animate=True)
        g.set_tile_positions()
        tiles = [g.bugs[i].tile for i in ['wP','bA2','wB1']]
        self.remove(*tiles)
        self.play(FadeIn(g.bugs['wP'].tile, shift=UP))
        self.play(LaggedStart(g.move('bB1','wL'),Succession(*[MoveAlongPath(g.bugs['wA1'].tile,g.get_curve(a[0],a[1],curve_dir=-1) ) for a in [['bA1/','\\bA1','bQ/','\\bQ'][b:b+2] for b in range(3)]],run_time=1), lag_ratio=0.8))
        self.play(LaggedStart(FadeIn(g.bugs['bA2'].tile,shift=LEFT),Succession(*[MoveAlongPath(g.bugs['wS2'].tile,g.get_curve(a[0],a[1],curve_dir=-1) ) for a in [['bA1\\','bA1-','bA1/','\\bA1'][b:b+2] for b in range(3)]],run_time=1), lag_ratio=0.8))
        self.play(LaggedStart(Succession(*[MoveAlongPath(g.bugs['bA2'].tile,g.get_curve(a[0],a[1],curve_dir=1) ) for a in [['wL-','wL\\','wP-','wP\\','/wP','-wP','\\wP'][b:b+2] for b in range(6)]],run_time=1),FadeIn(g.bugs['wB1'].tile,shift=RIGHT), lag_ratio=0.8))
        self.play(LaggedStart(Succession(*[MoveAlongPath(g.bugs['bA1'].tile,g.get_curve(a[0],a[1],curve_dir=1) ) for a in [['bP-','wS1-','bG1-','wL-','wQ-'][b:b+2] for b in range(4)]],run_time=1),MoveAlongPath(g.bugs['wB1'].tile,g.get_curve('-wS1','-bP',curve_dir=1)),g.move('bB1','-wL'), lag_ratio=0.8))
        g.play_warp('wP','wQ','wP/',DOWNRIGHT,UPLEFT)
        self.play(LaggedStart(Rotate(g.bugs['bB1'].svg_bug,PI),Rotate(g.bugs['bA1'].svg_bug,2*PI/3),Rotate(g.bugs['bA2'].svg_bug,-PI/3)))
        self.wait(0.5)
        self.play(LaggedStart(Rotate(g.bugs['bB1'].svg_bug,-PI/6),Rotate(g.bugs['bA1'].svg_bug,PI/6),Rotate(g.bugs['bA2'].svg_bug,-PI/3)), run_time=0.6)
        self.wait(0.5)
        self.play(ShrinkToCenter(VGroup(*g.get_live_tiles()),path_arc=-2))

class qualify(Scene):
    def construct(self):
        g= hive_game(self)
        g.make_moves('bP,wP /bP,bP bP/,wQ \\wP,bQ bP\\'.split(','), no_animate=True)
        self.remove(*g.get_live_tiles())
        g.set_tile_positions()
        g.get_live_pieces().scale(2).rotate(-PI/6)
        self.play(AnimationGroup(*[GrowFromCenter(g.bugs[i].tile, path_arc=2) for i in ['wP','bP']]))
        self.play(AnimationGroup(*[GrowFromCenter(g.bugs[i].tile, path_arc=2) for i in ['wQ','bQ']]))
        board = ChessBoard("rnbqk2r/pppp1ppp/5n2/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1").move_to(ORIGIN)
        self.play(LaggedStart(AnimationGroup(VGroup(g.bugs['wQ'].tile, g.bugs['wP'].tile).animate.to_edge(LEFT).scale(0.6),VGroup(g.bugs['bQ'].tile, g.bugs['bP'].tile).animate.to_edge(RIGHT).scale(0.6)), FadeIn(board), lag_ratio=0.4))
        self.play(LaggedStart(board.move_piece(7, 4,7,6)[1],board.move_piece(7, 7,7,5)[1],lag_ratio=0.3))
        self.play(LaggedStart(board.move_piece(0, 4,0,6)[1],board.move_piece(0, 7,0,5)[1],lag_ratio=0.3))
        self.wait(2)
        self.play(FadeOut(board))
        self.wait(2)

class qualify_pt2(Scene):
    def construct(self):
        g= hive_game(self)
        g.make_moves('bP,wP /bP,bP bP/,wQ \\wP,bQ bP\\'.split(','), no_animate=True)
        g.set_tile_positions()
        g.get_live_pieces().scale(2).rotate(-PI/6)
        VGroup(g.bugs['wQ'].tile, g.bugs['wP'].tile).to_edge(LEFT).scale(0.6)
        VGroup(g.bugs['bQ'].tile, g.bugs['bP'].tile).to_edge(RIGHT).scale(0.6)
        text = Text('Qualify for the win').scale(1.5)
        self.play(Write(text))
        self.wait(1)
        self.play(text.animate.scale(0.8).to_edge(UP))
        methods = ['Cover','Surround','Choke','Throw','Gate','Bugzwang']
        mt=[Text(m) for m in methods]
        for i in range(len(mt)-1):
            mt[i+1].next_to(mt[i],direction=DOWN).shift(DOWN*0.05)
        for m in mt:
            m.to_edge(LEFT)
        mtg=VGroup(mt)
        mtg.shift(2*RIGHT+1.75*UP)
        self.play(LaggedStart(*[FadeIn(m, shift=UP) for m in mt],lag_ratio=0.15))
        self.wait(2)
        color_anims = []
        for index, m in enumerate(mt):
            color_anims.append(m.animate.set_color(average_color(*([RED]*index+[GREEN]*(5-index)))))
        easy = Text("Most common/easy").set_color(GREEN).next_to(mt[0]).to_edge(RIGHT).shift(LEFT*2)
        hard = Text("Most rare/difficult").set_color(RED).next_to(mt[-1]).to_edge(RIGHT).shift(LEFT*2)
        self.play(LaggedStart(LaggedStart(FadeIn(easy,shift=LEFT),FadeIn(hard,shift=LEFT),lag_ratio=0.75),LaggedStart(*color_anims,lag_ratio=0.2)))
        self.wait(1)
        self.play(Unwrite(text, run_time=1),Unwrite(easy, run_time=1),Unwrite(hard,run_time=1),AnimationGroup([Rotate(g.bugs[i].tile,PI/2 if i[0]=='w' else -PI/2) for i in ['wP','wQ','bP','bQ']]), *[x.animate.set_color(WHITE) for x in mt])
        self.play(LaggedStart(AnimationGroup([g.bugs[i].tile.animate.shift(3*LEFT if i[0]=='w' else 3*RIGHT) for i in ['wP','wQ','bP','bQ']]), mtg.animate.to_corner(UP + LEFT),lag_ratio=0.3))

def get_chapter_text():
    methods = [Text(i) for i in ['Cover','Surround','Choke','Throw','Gate','Bugzwang']]
    for i in range(len(methods)-1):
        methods[i+1].next_to(methods[i], direction=DOWN).shift(DOWN*0.05)
    for i in methods:
        i.to_edge(LEFT)
    Group(*methods).to_edge(UP)
    return methods
def get_pointer():
    return Triangle().set_fill(WHITE).rotate(-PI/2).scale(1/10).set_color(WHITE).set_opacity(1)

class cover(Scene):
    def construct(self):
        methods = get_chapter_text()
        self.add(*methods)
        p=get_pointer()
        p.next_to(methods[0],direction=LEFT)
        self.play(FadeIn(p, shift=4.5*UP),*[i.animate.fade() for i in methods[1:]])
        g=hive_game(self)
        g.make_moves('wL,bL -wL,wQ wL/,bQ \\bL,wP wQ/,bP /bQ,wB1 -bQ,bB1 wQ-'.split(','),no_animate=True)
        g.set_tile_positions()
        self.remove(*g.get_live_tiles())
        g.get_live_pieces().shift(RIGHT*2+DOWN)
        self.play(LaggedStart([GrowFromCenter(i) for i in sorted(g.get_live_tiles(), key=lambda x: x.get_x())]))
        self.play(g.move('wB1','bP'))
        self.wait(1)
        self.play(g.move('bB1','wQ'))
        hexes=[g.hex_at_position('wP\\').scale(0.8), g.hex_at_position('-wP').scale(0.8)]
        self.play(*[GrowFromCenter(x) for x in hexes])
        self.play(Wiggle(g.bugs['wP'].tile))
        self.play(g.move('bB1','wP'),*[FadeOut(x) for x in hexes])
        hexes=[g.hex_at_position('\\bQ').scale(0.8), g.hex_at_position('bQ/').scale(0.8)]
        self.play(g.move('wB1','bQ'))
        self.wait(1)
        self.play(*[FadeIn(x) for x in hexes])
        self.wait(1)
        g.move('wS1','bQ/')
        g.set_tile_positions()
        self.remove(g.bugs['wS1'].tile)
        self.play(LaggedStart(AnimationGroup([FadeOut(x) for x in hexes]),FadeIn(g.bugs['wS1'].tile, shift=2*DOWN),lag_ratio=0.15))
        self.wait(1)
        self.play(LaggedStart([ShrinkToCenter(i) for i in sorted(g.get_live_tiles(), key=lambda x: -x.get_x())]))
        self.wait(1)


class surround(Scene):
    def construct(self):
        methods = get_chapter_text()
        self.add(*methods)
        p=get_pointer()
        p.next_to(methods[0],direction=LEFT)
        [i.fade() for i in methods[1:]]
        self.play(p.animate.next_to(methods[1], direction=LEFT),methods[0].animate.fade(),methods[1].animate.set_opacity(1))
        g=hive_game(self)
        g.make_moves('wL,bL -wL,wQ wL/,bQ /bL,wP wQ/,bP /bQ,bA1 -wP,bG1 \\wP,bS1 wP/,bA2 wP-,bS2 wP\\,wA1 \\bP,wG1 -bP,wS1 /bP,wA2 bP\\,wS2 bP-'.split(','),no_animate=True)
        g.set_tile_positions()
        self.remove(*g.get_live_tiles())
        g.get_live_pieces().shift(RIGHT*2).rotate(-PI/6)
        self.play(LaggedStart([GrowFromCenter(i) for i in sorted(g.get_live_tiles(), key=lambda x: x.get_x())]))
        g.move("wB1","\\bQ")
        g.set_tile_positions()
        wB1=g.bugs['wB1'].tile.rotate(-PI/6)
        self.remove(wB1)
        self.play(GrowFromCenter(wB1))
        g.play_warp('bP', 'bQ', 'bP/',DOWNRIGHT,UPLEFT)
        self.play(ShrinkToCenter(wB1))
        self.play(LaggedStart(Wiggle(VGroup(*[g.bugs[i].tile for i in ['wA1','wA2','wS1','wS2','wG1']])),Wiggle(VGroup(*[g.bugs[i].tile for i in ['bA1','bA2','bS1','bS2','bG1']])),lag_ratio=0.4))
        g.make_moves('wG2 \\wP,wA3 wP-'.split(','),no_animate=True)
        g.set_tile_positions()
        g.bugs['wG2'].tile.rotate(-PI/6)
        self.remove(g.bugs['wG2'].tile)
        g.bugs['wA3'].tile.rotate(-PI/6)
        self.play(Transform(g.bugs['bG1'].tile,g.bugs['wG2'].tile),MoveAlongPath(g.bugs['bS1'].tile, g.get_curve('bS1','\\bS1', -1)),MoveAlongPath(g.bugs['bA2'].tile, g.get_curve('bA2','bA2/', -1)),TransformFromCopy(g.bugs['bA2'].tile,g.bugs['wA3'].tile))
        hex = g.hex_at_position('wP/').rotate(PI/6)
        self.play(GrowFromCenter(hex))
        self.wait(1)
        self.play(Transform(hex, Circle(1).move_to(hex.get_center())))
        self.wait(2)
        g.make_moves(['bA2 wA3/','bS1 wG2/'])
        self.remove(hex)
        self.add(hex)
        self.play(Transform(hex, g.hex_at_position('bS1-').rotate(PI/6)))
        self.wait(2)
        g.move("bB1","wQ\\")
        g.set_tile_positions()
        bB1=g.bugs['bB1'].tile.rotate(-PI/6)
        self.remove(bB1)
        self.play(LaggedStart(FadeOut(hex),GrowFromCenter(bB1),lag_ratio=0.5))
        g.play_warp('wP', 'wQ', 'wP/',UPLEFT,UPLEFT)
        self.play(Succession(*[MoveAlongPath(g.bugs['bA1'].tile,g.get_curve(i[0],i[1],1)) for i in [['bA1','-wG2','\\wG2','\\bS1','bS1/','bS1-'][j:j+2] for j in range(5)]]), run_time=1.5)
        self.wait()
        self.play(LaggedStart(*[FadeOut(i) for i in sorted(g.get_live_tiles(), key=lambda x: -x.get_x()+x.get_y()/4)]))

class choke(Scene):
    def construct(self):
        methods = get_chapter_text()
        self.add(*methods)
        p=get_pointer()
        p.next_to(methods[1],direction=LEFT)
        [i.fade() for i in methods[:1]+methods[2:]]
        self.play(p.animate.next_to(methods[2], direction=LEFT),methods[1].animate.fade(),methods[2].animate.set_opacity(1))        
        analysis_file = ".\\media\\analysis_files\\analysis_16-Feb-2026_17_20_05.json"
        with open(analysis_file, 'r') as file:
                data = json.load(file)
        g = game(self, data,center=RIGHT)
        for i in g.black_bugs:
            i.tile.to_edge(UP).shift(UP*2+2*RIGHT)
            self.add(i.tile)
        for i in g.white_bugs:
            i.tile.to_edge(DOWN).shift(DOWN*2+2*RIGHT)
            self.add(i.tile)
        for i in range(16):
            self.play(g.next_move(run_time=0.5))
        hexes = [g.hex_at_position(i).scale(0.9).set_color(WHITE) for i in ["-wG2", "/wL","-wA1", "/wA1","wG1/", "wG1-"]]
        self.play(LaggedStart(*[Write(i) for i in hexes], lag_ratio=0.13))
        self.wait(2)
        self.play(*[ShrinkToCenter(i) for i in hexes])
        self.play(ShrinkToCenter(VGroup(g.get_live_tiles())))
        self.wait(1)

class throw(Scene):
    def construct(self):
        methods = get_chapter_text()
        self.add(*methods)
        p=get_pointer()
        p.next_to(methods[2],direction=LEFT)
        [i.fade() for i in methods[:2]+methods[3:]]
        self.play(p.animate.next_to(methods[3], direction=LEFT),methods[2].animate.fade(),methods[3].animate.set_opacity(1))
        analysis_file = ".\\media\\analysis_files\\analysis_16-Feb-2026_23_25_50.json"
        with open(analysis_file, 'r') as file:
                data = json.load(file)
        g = hive_game(self, data,center=RIGHT)
        for _ in range(10):
            g.next_move()
        g.set_tile_positions()
        self.play(GrowFromCenter(VGroup(g.get_live_tiles())))
        wM=g.bugs["wM"].tile
        wM2=wM.copy()
        wA1=g.bugs["wA1"].tile.copy()
        wA1.submobjects[1].rotate(PI/3)
        self.play(Circumscribe(wM,Circle), Wiggle(wM))
        self.play(Rotate(wM.submobjects[1],PI/3))
        self.play(Transform(wM, wA1.copy().shift(RIGHT)))
        self.wait(0.3)
        self.play(g.move_along_path("wM", ["wA1/","\\wA1","-wA1","\\bS1","-bS1","-bL","-bQ","-bP"],-1),run_time=2)
        g.next_move()
        self.play(Rotate(wM.submobjects[1],-PI/3))
        self.play(Transform(wM, wM2.move_to(wM.get_center())))
        self.play(g.move_along_path('bS1',['-wQ','-wA1','\\wA1'],1),run_time=1.8)
        self.wait(0.4)
        wP=g.bugs["wP"].tile.copy()
        wP.rotate(-PI*2/3)
        wP.submobjects[0].rotate(PI*2/3)
        self.play(Rotate(wM.submobjects[1],-PI*2/3))
        self.play(Transform(wM, wP.move_to(wM.get_center())))
        g.play_warp('wM','bP', '/wM',DOWN,DOWNRIGHT)
        self.play(Rotate(wM.submobjects[1],2*PI/3))
        self.play(Transform(wM, wM2))
        self.play(LaggedStart(*[FadeOut(i) for i in sorted(g.get_live_tiles(),key=lambda x: -x.get_y()-x.get_x()/10)]))

class gate(Scene):
    def construct(self):
        methods = get_chapter_text()
        self.add(*methods)
        p=get_pointer()
        p.next_to(methods[3],direction=LEFT)
        [i.fade() for i in methods[:3]+methods[4:]]
        self.play(p.animate.next_to(methods[4], direction=LEFT),methods[3].animate.fade(),methods[4].animate.set_opacity(1))
class buugzwang(Scene):
    def construct(self):
        methods = get_chapter_text()
        self.add(*methods)
        p=get_pointer()
        p.next_to(methods[4],direction=LEFT)
        [i.fade() for i in methods[:4]+methods[5:]]
        self.play(p.animate.next_to(methods[5], direction=LEFT),methods[4].animate.fade(),methods[5].animate.set_opacity(1))
