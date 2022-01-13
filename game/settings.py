title = "Pawel Jumper" # will probably change xD
background_color = 'black' # might change for some image
player_color = 'Red' # might change for some image

fps = 60

map_width = 10
map_heigth = 15
tile_size = 54

screen_width = map_width * tile_size
screen_height = 800

start_pos = (map_width/2, map_heigth-1)

start_world_descend_speed = 2
horizontal_speed = 9
scroll_speed = 12
gravity = 0.8
jump_speed = -21

# platform types with different chance of being generated
platform_types = ['normal', 'normal', 'normal', 'normal', 'bounce', 'collapse']
bounce_speed = -30
platform_thickness = 10

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