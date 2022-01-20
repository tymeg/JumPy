title = "Pawel Jumper"  # will probably change xD
background_color = 'black'  # might change for some image
player_and_text_color = 'red'  # might change for some image
missile_color = 'orange'

font_name = 'verdana'
big_font_size = 48
small_font_size = 20

fps = 60

map_width = 10
map_heigth = 15
tile_size = 54

screen_width = map_width * tile_size
screen_height = 800

start_pos = (map_width / 2, map_heigth - 1)
player_dimensions = (30, 60)

start_world_descend_speed = 1
horizontal_speed = 9
start_scroll_speed = 10
start_scroll_border = 2*screen_height/5
gravity = 0.8
jump_speed = -22

# platform types with different chance of being generated
platform_types = ['normal', 'normal', 'normal', 'normal', 'bounce', 'collapse']
normal_platform_color = "white"
bounce_platform_color = "green"
collapse_platform_color = "grey40"
bounce_speed = -30
platform_thickness = 10

# missiles - dimensions, speed, start spawn frequencies in miliseconds
missile_dimensions = (20, 40)
missile_speed = 4
start_missile_spawn_frequency_down = 5000
start_missile_spawn_frequency_up = 10000

# 0
# 1
# 2 XXX
# 3
# 4
# 5        XXX
# 6
# 7
# 8     XXX
# 9
# 10
# 11  XXX
# 12
# 13
# 14 XXXXXXXXXX
#    0123456789
