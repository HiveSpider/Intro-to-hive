from manim import *
from hive_engine import hive_game

class demo(Scene):
    def construct(self):
        game = hive_game(self)
        game.make_moves("wM,bM wM-,wQ /wM,bQ bM/,wL -wM,bL bM-,wA1 \\wM,bA1 bM\\".split(','))
        game.set_tile_positions()
        self.add(game.get_live_pieces())
        self.make_moves("")