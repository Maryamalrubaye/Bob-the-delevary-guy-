import sys

from os import path

from map import Map
from a_star_algorithm import *
from settings import *
from buildings import *
from player import Player
from camera import Camera
from obstacle import Obstacle
vec = pg.math.Vector2

HOUSE_TARGETS = [(87, 127), (215, 124), (383, 125), (793, 125), (918, 122), (1067, 122), (1062, 284), (1066, 461), (1064, 654), (647, 670), (502, 670), (361, 666), (214, 668), (118, 668), (85, 286), (216, 282), (387, 446), (584, 286), (770, 286), (889, 290), (768, 461), (874, 463)]
RESTURANT_TARGETS = [(99, 452), (623, 125), (897, 653)]
# RESTURANT_TARGETS = [(96, 435), (622, 116),(896, 645)]
OBSTACLES = []

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.selected_building_type = ''
        self.destination_position = vec()
        self.current_position = vec()
        self.path ={}

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')
        self.map = Map(path.join(map_folder, 'map1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        # load arrow sprites
        icon_dir = path.join(path.dirname(__file__))
        self.arrows = {}
        arrow_img = pg.image.load(path.join(icon_dir, './img/arrowRight.png')).convert_alpha()
        arrow_img = pg.transform.scale(arrow_img, (50, 50))
        for dir in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            self.arrows[dir] = pg.transform.rotate(arrow_img, vec(dir).angle_to(vec(1, 0)))
     

    def new(self):
       
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.houses = pg.sprite.Group()
        self.restaurants = pg.sprite.Group()
        self.obs = []
        for tile_object in self.map.tmxdata.objects:

            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'restricted':
                self.obs += [(int(tile_object.x), int(tile_object.y), int(tile_object.width), int(tile_object.height))]
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.type == str('house'):
                House(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height,tile_object.name)
                #print(tile_object.name)

            if tile_object.type == str('restaurant'):
                Restaurant(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height,tile_object.name)

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
    def get_obstacles_cordinates(self) -> list:
        """Write out all the obstacle cordinates to the obsticle_cordinates.txt file"""
        def unback_obstacle(tuple_) -> list:
            x_cordinates = [*tuple_[0]]
            y_cordinates = [*tuple_[1]]
            obstacles = [(x, y) for x in x_cordinates for y in y_cordinates]
            return obstacles
        obstacle = [*self.obs]
        obstacles_cordinates = [(range(obs[0], obs[0] + obs[2]),
                                 range(obs[1], obs[1] + obs[3]))
                                for obs in obstacle]
        all_obstacles_cordinates = [unback_obstacle(obs) for obs in obstacles_cordinates]
        all_obstacles_cordinates_flatten = [obs_tuple for obs_list in all_obstacles_cordinates
                                            for obs_tuple in obs_list]
        return all_obstacles_cordinates_flatten
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))

        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
        #CODE FOR DRAWING AROUND HOUSES
            for house in self.houses:
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(house.rect), 1)
        #CODE FOR DRAWING AROUND RESTAURANTS
            for restaurant in self.restaurants:
                pg.draw.rect(self.screen, YELLOW, self.camera.apply_rect(restaurant.rect), 1)
     
        
            
       
        self.draw_path(self.current_position ,self.destination_position ,self.path)

        pg.display.flip()
    
    def draw_path(self, start: pg.math.Vector2, goal: pg.math.Vector2, path: {(int, int): pg.math.Vector2}):
        current = start
        path_len = 0

        try:
            while current != goal:
                v = path[(current.x, current.y)]

                if v.length_squared() == 1:

                    path_len += 10
                else:
                    path_len += 14


                img = self.arrows[vec2int(v)]
                x = current.x * TILESIZE + TILESIZE / 2
                y = current.y * TILESIZE + TILESIZE / 2
                rect = img.get_rect(center=(x, y))
                self.screen.blit(img, rect)
                # find next in path
                current = current + path[vec2int(current)]
        except: pass

        self.path_len = path_len

    def get_object_target(self, object_type: str, position_x: int, position_y: int) -> tuple:
        """Get the target cordinations of the given object type (resturant, house)
        """
        object_classes = {'house': {'object': self.houses, 'target': HOUSE_TARGETS},
                          'restaurant': {'object': self.restaurants, 'target': RESTURANT_TARGETS}}
        object_class = object_classes[object_type]

        for building_type in object_class['object']:
            end_x = building_type.rect.x + building_type.rect.width
            end_y = building_type.rect.y + building_type.rect.height
            if position_x in range(building_type.rect.x, end_x):
                if position_y in range(building_type.rect.y, end_y):
                    #print(f"building no: {building_type.name}, target: {building_type}")
                    return object_class['target'][int(building_type.name) - 1]
        return ()

    def get_target(self, position_x: int, position_y: int) -> tuple:
        """Get the type of the building along with the cordinates of the building target"""
        building_objects = {'restaurant': (), 'house': ()}

        for building_object in building_objects.keys():
            building_objects[building_object] = self.get_object_target(building_object, position_x, position_y)
            if building_objects[building_object] != ():
                return building_object, building_objects[building_object]
        return '', ()


    def get_tile(self) -> tuple:
        """ Returns the tile on which the sprite is located. """
        return vec(self.player.pos.x // TILESIZE, self.player.pos.y // TILESIZE)

    def find_destination_path(self):
        #print("goal before entry",self.destination_position )
        #print("get tile says",self.get_tile())
        self.current_position = self.get_tile()
        #print("start at find destination path in  main line 205",self.current_position )
        grid = WeightedGrid(GRIDWIDTH, GRIDHEIGHT)

        for wall in WALLS:
            grid.walls.append(vec(wall))

        self.path, c = a_star_search(grid, self.destination_position, self.current_position)

    
         
    def events(self):
        # catch all events here
        self.get_obstacles_cordinates()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                
                self.current_position = self.get_tile()
                print("self.current_position ", self.current_position)
                print(f"self.current_position={self.current_position}, self.destination_position={self.destination_position}")
                if (self.current_position[0] != self.destination_position[0]) or (self.current_position[1] != self.destination_position[1]):
                    self.find_destination_path()
                else:
                    self.destination_position = vec()

                # call the A* algorithm to update the path to the given destiation
                print("key pressed")
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug

            if event.type == pg.MOUSEBUTTONDOWN:
                 self.returnGoal()

    def returnGoal(self):
        position_x, position_y = pg.mouse.get_pos()
        #print(self.get_target(position_x, position_y))
        building_type, target_cordinates = self.get_target(position_x, position_y)

        if building_type != '':
            print(f"self.selected_building_type= {self.selected_building_type}, building_type= {building_type}")
            print(f"self.destination_position = {self.destination_position}, condition: {self.destination_position == '' and building_type != self.selected_building_type}")
            if self.selected_building_type == '' and building_type == 'restaurant':
                self.selected_building_type = building_type
                dest_x, dest_y = target_cordinates
                
                self.destination_position = vec(dest_x // TILESIZE, dest_y // TILESIZE)
                # implement the A* algorithm to reach the destination
                self.find_destination_path()

            elif self.destination_position == '' and building_type != self.selected_building_type:
                    print("----------------------")
                    self.selected_building_type = building_type
                    dest_x, dest_y = target_cordinates

                    self.destination_position = vec(dest_x // TILESIZE, dest_y // TILESIZE)
                    # implement the A* algorithm to reach the destination
                    self.find_destination_path()
            elif self.destination_position == [0, 0] and building_type != self.selected_building_type and self.selected_building_type != '':
                    self.selected_building_type = building_type
                    dest_x, dest_y = target_cordinates

                    self.destination_position = vec(dest_x // TILESIZE, dest_y // TILESIZE)
                    # implement the A* algorithm to reach the destination
                    self.find_destination_path()
                    pass

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    # create the game object
    g = Game()
    g.show_start_screen()
    # OBSTACLES = g.get_obstacle_cordinates()
    while True:
        g.new()
        g.run()
        g.show_go_screen()
