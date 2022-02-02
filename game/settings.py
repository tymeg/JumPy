# title and colors
title = "Pawel Jumper"  # will probably change xD
background_color = 'black'  # might change for some image
player_and_text_color = 'red'  # might change for some image
missile_color = 'orange'

# fonts
font_name = 'verdana'
big_font_size = 48
small_font_size = 20

# fps
fps = 60

# map and screen dimensions
map_width = 10
map_heigth = 15
tile_size = 54

screen_width = map_width * tile_size
screen_height = 800

# player
start_pos = (map_width / 2, map_heigth - 1)
player_dimensions = (30, 60)

# speed settings
horizontal_speed = 9
scroll_speed = 10
scroll_border = 2*screen_height/5
gravity = 0.8
jump_speed = -22

# platform types with different chance of being generated
platform_types = ['normal', 'normal', 'normal', 'normal',
                  'bounce', 'horizontal', 'vertical', 'collapse']
platform_thickness = 10

normal_platform_color = "white"

bounce_platform_color = "green"
bounce_speed = -30

collapse_platform_color = "grey40"

horizontal_platform_color = "dodgerblue"
horizontal_platform_speed = 4

vertical_platform_color = "violet"
vertical_platform_speed = 2
vertical_platform_range = 27 * vertical_platform_speed

# missiles - dimensions, speed
missile_dimensions = (20, 40)
missile_speed = 4

# score thresholds and corresponding game difficulties
score_thresholds = [25, 50, 100, 150]
game_difficulty = [{'world_descend_speed': 1, 'missile_spawn_frequency_down': 5000, 'missile_spawn_frequency_up': 10000},
                   {'world_descend_speed': 2, 'missile_spawn_frequency_down': 4000,
                       'missile_spawn_frequency_up': 8000},
                   {'world_descend_speed': 3, 'missile_spawn_frequency_down': 6000,
                       'missile_spawn_frequency_up': 6000},
                   {'world_descend_speed': 3, 'missile_spawn_frequency_down': 2000,
                       'missile_spawn_frequency_up': 40000},
                   {'world_descend_speed': 4, 'missile_spawn_frequency_down': 1000, 'missile_spawn_frequency_up': 2000}]
