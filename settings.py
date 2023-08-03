WIDTH = 1280
HEIGHT = 720
FPS = 60

TILE_SIZE = 16

# Player Characteristics
PLAYER_SPEED = 5
PLAYER_SIZE = 16
PLAYER_HEALTH_POINTS = 50
PLAYER_ATTACK_POINTS = 10
PLAYER_ATTACK_COOLDOWN = 500
PLAYER_SWITCH_WEAPON_COOLDOWN = 1000

# Weapons
weapons_data = {
    'sword' : {'cooldown' : 100, 'damage' : 15, 'graphic' : ''},
    'axe' : {'cooldown' : 50, 'damage' : 7, 'graphic' : ''}}

monster_data = {
    'skull' : {'health' : 20, 'damage' : 15, 'exp' :100, 'attack_type' : 'slash', 'attack_sound' : None, 'speed' : 5, 'resistance' : 3, 'attack_radius': 80, 'notice_radius': 360},
    'cyclope' : {'health' : 100, 'damage' : 25, 'exp' :250, 'attack_type' : 'claw', 'attack_sound' : None, 'speed' : 3, 'resistance' : 10, 'attack_radius': 50, 'notice_radius': 360}}
# MAP

EMPTY_MAP = "map_empty_80_45"