import json
from manim import *
from hive import *
from collections.abc import Iterable


i = 0
def inc():
    global i
    i+=1
    return i -1

#This class should keep track of the analysis, branches, provide proper animations for moves
class hive_game(game):
    def get_crawl_paths(self,piece_from):
        start_coordinate = self.bugs[piece_from].game_coordinate
        spots = [start_coordinate]
        connections = {}
        while True:
            cur_spot = spots[0]
            connections[cur_spot] = []
            break
        pass
    def get_live_pieces(self):
        outer = self
        global i
        i = 0
        class piece_group(VGroup):
            # def __init__(self, *pieces: VMobject |Iterable[VMobject]):
            #     super().__init__(*pieces)
            def rotate_animate(self,
                angle: float,
                axis = OUT,
                about_point = None,
                **kwargs
            ):
                return self.rotate(angle, axis, about_point, scale=0.5, **kwargs)
            def rotate(
                self,
                angle: float,
                axis = OUT,
                about_point = None,
                scale = 1,
                **kwargs,
            ):
                # if about_point == None:
                #     about_point = self.game.center
                # self.game.up_basis.rotate(angle)
                outer.up_basis = rotate_vector(outer.up_basis,angle*scale)
                outer.right_basis = rotate_vector(outer.right_basis,angle*scale)
                outer.center = self.get_center() + rotate_vector(outer.center - self.get_center(), angle*scale)
                super().rotate(angle, axis, about_point, **kwargs)
                return self
            def shift_animate(self, *vectors):
                return self.shift(*vectors, scale=0.5)
            def shift(self,*vectors, scale = 1):
                for i in vectors:
                    outer.center = outer.center + i*scale
                super().shift(*vectors)
                return self
            def scale_animate(self, scale_factor:float, **kwargs):
                return self.scale(scale_factor, scale=0.5, **kwargs)
            def scale(self, scale_factor: float, scale=1, **kwargs):
                outer.tile_size = outer.tile_size * scale_factor**scale
                outer.up_basis = outer.up_basis * scale_factor**scale
                outer.right_basis = outer.right_basis * scale_factor**scale
                outer.center = self.get_center() + (outer.center - self.get_center()) * scale_factor
                super().scale(scale_factor)
                return self
        return piece_group(self.get_live_tiles())
    def play_warp(self, warper, warpee, spot, axis1, axis2, **kwargs):
        for i in self.warp(warper, warpee, spot, axis1, axis2):
            self.scene.play(i, **kwargs)

    def warp(self, warper, warpee, spot, axis1, axis2):
        return [AnimationGroup(Rotate(self.bugs[warper].tile, TAU, axis1), self.move(warpee, warper)),
                AnimationGroup(Rotate(self.bugs[warper].tile, TAU, axis2), self.move(warpee, spot))]
       
    # def get_all_pieces(self):
    #     return hive_piece_group(self.game, self.game.all_tiles)

# class hive_piece_group(VDict):
#     def __init__(self, bg: game, *pieces: VMobject|Iterable[VMobject]):
#         self.game = bg
#         self.pieces = pieces
#         super().__init__(*pieces)

class hive_piece_group_old(VGroup):
    def __init__(self, bg: game, *pieces: VMobject | Iterable[VMobject]):
        self.game = bg
        self.pieces = pieces
        super().__init__(*pieces)
    def rotate(
        self,
        angle: float,
        axis = OUT,
        about_point = None,
        **kwargs,
    ):
        # if about_point == None:
        #     about_point = self.game.center
        # self.game.up_basis.rotate(angle)
        super().rotate(angle, axis, about_point, **kwargs)
        return self
    def shift(self,*vectors):
        self.game.center.shift(*vectors)
        super().shift(*vectors)
    def get_center(self):
        return self.game.center
    def scale(self, scale_factor: float, **kwargs):
        self.game.tile_size = self.game.tile_size * scale_factor
        self.game.center = (self.game.center - self.get_center()) * scale_factor
        super().scale(scale_factor)