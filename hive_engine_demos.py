from hive_engine import *
from manim import *
import json

class move_game_like_vgroup(Scene):
    def construct(self):
        analysis_file='./media/analysis_files/analysis_24-Jun-2025_00_14_21.json'
        with open(analysis_file, 'r') as file:
            data = json.load(file)
        #print(data)
        game = hive_game(self, data)
        inventory = ['wA3', 'wS2', 'bG2', 'bG3','bS2']
        spots = [6*RIGHT+UP/2, 6*RIGHT-UP/2, 6*LEFT+UP, 6*LEFT, 6*LEFT-UP]
        for i in range(50):
            game.next_move()
        # for i in game.game.all_tiles:
        #     i.rotate(-PI/6)
        for i in range(5):
            game.bugs[inventory[i]].tile.move_to(spots[i])
        for i in game.get_live_bugs():
            i.tile.move_to(i.tile.target.get_center())
        p = game.get_live_pieces()
        #self.play(Rotate(game.get_live_pieces()))
        #self.play(ScaleInPlace(game.get_live_pieces(), 0.3))
        #self.play(game.get_live_pieces().animate.shift_animate(LEFT))
        #self.play(game.get_live_pieces().animate.rotate_animate(PI/2))
        self.play(MoveAlongPath(p,Line(p.get_center()-DOWN, p.get_center()+ RIGHT + 2*UP)))
        #game.get_live_pieces().shift(RIGHT*2)
        self.play(game.move("bA3", "-bM"))

        