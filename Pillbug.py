from hive_engine import *
from manim import *

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
        pass






