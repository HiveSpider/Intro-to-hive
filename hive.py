from manim import *
import json

assetPathOfficial = ".\\media\\assets\\tiles\\official\\"


class bug():
    def __init__(self, svg_filename, color, height=1, scale=2.0/3, off_x=-0.02, off_y=0, dot_id = 0):
        self.color = color
        self.name = color + " " + svg_filename
        self.svg_t = SVGMobject(assetPathOfficial+color+".svg", height= height)
        self.svg_bug = SVGMobject(assetPathOfficial + svg_filename + ".svg", height = height * scale).rotate(-PI/6).set_x(off_x * height).set_y(off_y*height).rotate(PI/6)
        self.tile = VGroup(self.svg_t, self.svg_bug)
        self.z_index = 0
        self.game_coordinate = None
        self.dot_id = dot_id
    def draw(self, animation = DrawBorderThenFill, run_time = None):
        return AnimationGroup(animation(self.svg_t), animation(self.svg_bug), run_time = run_time)
      

class game():
    def __init__(self,scene, analysis_json=json.loads('{"tree":{"nodes":[]}}'), game_type = "MLP", center=ORIGIN, tile_size=1.0, up_basis = UP*0.866+RIGHT/2, right_basis = RIGHT, vertical_ratio = 0.1, rotate_by_dot = True):
        self.scene = scene
        self.center = center
        self.tile_size = tile_size
        self.up_basis = up_basis * tile_size
        self.right_basis = right_basis * tile_size
        self.tree = analysis_json['tree']['nodes']
        #self.game_type=self.analysis.game_type
        self.node = None
        self.climb_basis = (self.up_basis - self.right_basis) * vertical_ratio
        self.bugs = {
                "wA3": bug("Ant","white",height=tile_size, dot_id=3),
                "bA3": bug("Ant","black",height=tile_size, dot_id=3),
                "wA2": bug("Ant","white",height=tile_size, dot_id=2),
                "bA2": bug("Ant","black",height=tile_size, dot_id=2),
                "wA1": bug("Ant","white",height=tile_size, dot_id=1),
                "bA1": bug("Ant","black",height=tile_size, dot_id=1),
                "wB1": bug("Beetle","white",height=tile_size, dot_id=1),
                "bB1": bug("Beetle","black",height=tile_size, dot_id=1),
                "wB2": bug("Beetle","white",height=tile_size, dot_id=2),
                "bB2": bug("Beetle","black",height=tile_size, dot_id=2),
                "wG1": bug("Grasshopper","white",height=tile_size, dot_id=1),
                "bG1": bug("Grasshopper","black",height=tile_size, dot_id=1),
                "wG2": bug("Grasshopper","white",height=tile_size, dot_id=2),
                "bG2": bug("Grasshopper","black",height=tile_size, dot_id=2),
                "wG3": bug("Grasshopper","white",height=tile_size, dot_id=3),
                "bG3": bug("Grasshopper","black",height=tile_size, dot_id=3),            
                "wL": bug("Ladybug","white",height=tile_size),
                "bL": bug("Ladybug","black",height=tile_size),                
                "wM": bug("Mosquito","white",height=tile_size),
                "bM": bug("Mosquito","black",height=tile_size),
                "wP": bug("Pillbug","white",height=tile_size),
                "bP": bug("Pillbug","black",height=tile_size),
                "wQ": bug("Queen","white",height=tile_size, off_y=-0.08*tile_size, off_x=0.04*tile_size),
                "bQ": bug("Queen","black",height=tile_size, off_y=-0.08*tile_size, off_x=0.04*tile_size),
                "wS1": bug("Spider","white",height=tile_size, dot_id=1),
                "bS1": bug("Spider","black",height=tile_size, dot_id=1),
                "wS2": bug("Spider","white",height=tile_size, dot_id=2),
                "bS2": bug("Spider","black",height=tile_size, dot_id=2)
                         }
        self.white_bugs = list(dict(filter(lambda x: x[0][0]=="w", self.bugs.items())).values())
        self.black_bugs = list(dict(filter(lambda x: x[0][0]=="b", self.bugs.items())).values())
        self.all_tiles = [x.tile for x in self.bugs.values()]
        if rotate_by_dot:
            for i in self.bugs.values():
                if i.dot_id > 1:
                    i.tile.rotate(-PI/3 * (i.dot_id - 1))
    def set_stacks(self, ratio, run_time = 1):
        live_bugs = []
        for cur_bug in self.bugs.values():
            if cur_bug.z_index > 0:
                new_coords = self.center + self.right_basis * cur_bug.game_coordinate[0] +  self.up_basis * cur_bug.game_coordinate[1] + cur_bug.z_index * self.climb_basis * ratio
                cur_bug.tile.generate_target().set_x(new_coords[0]).set_y(new_coords[1]).set_z(cur_bug.z_index)
                live_bugs.append(cur_bug)
        live_bugs = sorted(live_bugs, key= lambda x:  x.z_index)
        animations = [MoveToTarget(x.tile) for x in live_bugs]
        return AnimationGroup(*animations, run_time=run_time)
    def reveal_stacks(self, run_time = 1):
        #print ('jth3')
        return self.set_stacks(4, run_time)
    def collapse_stacks(self, run_time = 1):
        return self.set_stacks(1, run_time)
    def set_tile_positions(self):
        for cur_bug in self.bugs.values():
            if cur_bug.game_coordinate is not None:
                new_coords = self.center + self.right_basis * cur_bug.game_coordinate[0] +  self.up_basis * cur_bug.game_coordinate[1] + cur_bug.z_index * self.climb_basis
                cur_bug.tile.set_x(new_coords[0]).set_y(new_coords[1])
    def move_to_current_position(self, run_time = 1):
        for cur_bug in self.bugs.values():
            if cur_bug.game_coordinate != None:
                new_coords = self.center + self.right_basis * cur_bug.game_coordinate[0] +  self.up_basis * cur_bug.game_coordinate[1] + cur_bug.z_index * self.climb_basis
                cur_bug.tile.generate_target().set_x(new_coords[0]).set_y(new_coords[1]).set_z(cur_bug.z_index).set_z_index(cur_bug.z_index).set_z_index_by_z_Point3D()

        live_bugs = sorted(self.get_live_bugs(), key = lambda x: x.z_index)
        animations = [MoveToTarget(x.tile) for x in live_bugs]
        self.scene.bring_to_front(*[i.tile for i in live_bugs[::-1]])
        return AnimationGroup(*animations, run_time=run_time)
    def display(self, animation = GrowFromCenter, run_time = None):
        for i in range(len(self.white_bugs)):
            list(self.white_bugs)[i].tile.set_x(self.center[0] - 7 * self.tile_size + i * self.tile_size).set_y(self.center[1] - 3.5)
            
        for i in range(len(self.black_bugs)):
            list(self.black_bugs)[i].tile.set_x(self.center[0] - 7 * self.tile_size + i * self.tile_size).set_y(self.center[1] + 3.5)
        return LaggedStart(*[(x.draw(animation, run_time = run_time)) for x in self.bugs.values()])
    def hex_at_position(self, position, rotate_off=0):
        coords= self.get_coords_from_position(position)
        return RegularPolygon().move_to(self.center + self.right_basis*coords[0] + self.up_basis*coords[1]).scale(0.5*self.tile_size).rotate(PI/6 + rotate_off).scale(1.15)
    def get_coords_from_position(self,position):
        rel_bug = self.bugs["".join(x for x in position if x.isalnum())]
        rel_coor = rel_bug.game_coordinate
        if rel_coor == None:
            return rel_bug.tile.get_center()
        coords=[0, 0]
        if position[0]=="\\":
            coords = (rel_coor[0]-1,rel_coor[1] +1)
        elif position[0] =="-":
            coords = (rel_coor[0]-1,rel_coor[1])
        elif position[0] == "/":
            coords = (rel_coor[0],rel_coor[1] -1)
        elif position[-1] == "\\":
            coords = (rel_coor[0]+1,rel_coor[1] -1)
        elif position[-1] == "-":
            coords = (rel_coor[0]+1,rel_coor[1])
        elif position[-1] == "/":
            coords = (rel_coor[0], rel_coor[1]+1)
        else:
            coords = (rel_coor[0], rel_coor[1])
        return coords
    def get_location_from_coords(self, right, up):
        return self.center + self.up_basis * up + self.right_basis * right
    def get_curve(self, position_start, position_end, curve_dir=0):
        start = self.get_location_from_coords(*self.get_coords_from_position(position_start))
        end =  self.get_location_from_coords(*self.get_coords_from_position(position_end))
        if not curve_dir:
            return Line(start, end)
        dir = curve_dir * rotate_vector( (end - start), PI/2) * 0.24
        return CubicBezier(start, start + dir, end + dir, end)

        pass
    def play_curve(self,piece, position_start, position_end, curve_dir=0, **kwargs):
        self.scene.play(MoveAlongPath(self.bugs[piece].tile,self.get_curve(position_start, position_end, curve_dir),**kwargs))
        self.move(piece, position_end, no_animate=True)
    def move(self, piece, position, run_time=1.0, curve_dir=0, no_animate=False):
        coords = None
        z_index = 0
        if position == "":
            coords = [0,0]
        else:            
            rel_bug = self.bugs["".join(x for x in position if x.isalnum())]
            rel_coor = rel_bug.game_coordinate
            coords=self.get_coords_from_position(position)
            if position == "".join(x for x in position if x.isalnum()):
                z_index = rel_bug.z_index + 1
        cur_bug = self.bugs[piece]
        cur_bug.game_coordinate = coords
        cur_bug.z_index = z_index
        cur_bug.tile.z_index = z_index
        new_coord = self.center + self.right_basis * cur_bug.game_coordinate[0] +  self.up_basis * cur_bug.game_coordinate[1] + z_index * self.climb_basis
        #print(self.center, self.right_basis, self.up_basis, cur_bug.game_coordinate, new_coord)
        cur_bug.tile.generate_target().set_x(new_coord[0]).set_y(new_coord[1]).set_z(z_index).set_z_index(z_index)
        # cur_bug.tile.target.set_z_index(z_index)
        # cur_bug.tile.target.set_z(z_index)
        # cur_bug.tile.z_index = z_index
        # cur_bug.svg_bug.set_z_index(z_index)
        # cur_bug.svg_t.set_z_index(z_index)
        self.scene.bring_to_front(cur_bug.tile)
        if curve_dir:
            start = cur_bug.tile.get_center()
            end = cur_bug.tile.target.get_center()
            dir = rotate_vector(end - start, curve_dir*PI/2) * 0.2
            curve = CubicBezier(start, start +dir, end + dir, end)
            return MoveAlongPath(cur_bug.tile, curve)
        if no_animate:
            return
        return AnimationGroup(MoveToTarget(cur_bug.tile, run_time=run_time), run_time=run_time )
    def get_location(self,position):
        rel_bug = self.bugs["".join(x for x in position if x.isalnum())]
        rel_coor = rel_bug.game_coordinate
        if rel_coor == None:
            return rel_bug.tile.get_center()
        coords = self.get_coords_from_position(position)
        return coords[0]*self.right_basis + coords[1]*self.up_basis + self.center
    def arrow(self, fro, to):
        return Arrow(start=self.get_location(fro), end=(self.get_location(to)))
    def get_path_from(self, source, to, curve_dir=0, curve_to_append=None):
        a = self.get_location(source)
        b = self.get_location(to)
        if curve_dir==0:
            return Line(a, b)
        dir = rotate_vector(b - a, curve_dir*PI/2) * 0.2
        if curve_to_append != None:
            curve_to_append.add_cubic_bezier_curve(a, a+ dir, b+dir, b)
        return CubicBezier(a, a+ dir, b+dir, b)
    def get_multi_path(self, *stops, curve_dir=0):
        toRet = self.get_path_from(stops[0],stops[1],curve_dir)
        for i in range(2, len(stops)):
            self.get_path_from(stops[i-1],stops[i], curve_dir=curve_dir, curve_to_append=toRet)
        return toRet
    def next_n_moves(self, n, run_time = 1):
        all_moves = []
        for i in range(n):
            a = self.next_move(run_time=run_time)
            if a == None:
                return all_moves
            all_moves.append(self.move_to_current_position(run_time = run_time))
        return all_moves
    #Example usage: game.make_moves(["wA1 -bQ","bP /bG2"])
    def make_moves(self, moves, run_time = 1, no_animate=False):
        ret = []
        for move in moves:
            s = move.split(' ')
            piece = s[0]
            position = s[1] if len(s) > 1 else ""
            self.move(piece, position, run_time,no_animate=no_animate)
            if not no_animate:
                ret.append(self.move_to_current_position(run_time=run_time))
        return ret

    def next_move(self, branch = 0, run_time=1.0):
        if self.node == None:
            self.node = self.tree[0]
        else:
            old_node = self.node['node_id']
            i = old_node
            cur_branch = 0
            while cur_branch <= branch:
                i+=1
                if i >= len(self.tree): return None
                if (self.tree[i]['parent'] == old_node):
                    cur_branch += 1
            self.node = self.tree[i]
        node_value = self.node['value']
        return self.move(node_value['piece'], node_value['position'], run_time)
    def get_live_bugs(self):
        return [x for x in self.bugs.values() if x.game_coordinate != None]
    def get_live_tiles(self):
        return [x.tile for x in self.get_live_bugs()]
    def set_z_indices(self):
        for i in self.get_live_tiles(): self.scene.remove(i)
        sorted = self.get_live_tiles()
        sorted.sort(key=lambda tile: -tile.z_index)
        for i in sorted: self.scene.add(i)
    def set_tiles_to_target(self):
        b = sorted(list(self.bugs.values()), key=lambda x: x.z_index, reverse=False)
        for x in b:
            self.scene.remove(x.tile)
        for x in b:
            if (x.game_coordinate != None):
                t = x.tile
                t.set_x(t.target.get_x()).set_y(t.target.get_y())
                self.scene.add(t)
    def move_along_path(self,piece, spots, curve_dir=0):
        return self._move_along_path(piece, [[spot,curve_dir] for spot in spots])
    def _move_along_path(self,piece, spots_with_curve_dirs):
        spots_with_curve_dirs = [[piece,0]]+spots_with_curve_dirs
        return Succession([MoveAlongPath(self.bugs[piece].tile,self.get_curve(i[0][0],i[1][0], i[1][1])) for i in [spots_with_curve_dirs[j:j+2] for j in range(len(spots_with_curve_dirs)-1)]])





