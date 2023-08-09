WIDTH = 1280
HEIGHT = 720
FPS = 60

TILE_SIZE = 16
TILE_SIZE_BUILDINGS = 64
GAME_UPSCALE = 4

#UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ITEM_BOX_SIZE = 80
UI_FONT = 'assets/font/joystix.ttf'
UI_FONT_SIZE = 18

#icon
HEART_ICON = 'assets/ui/heart.png'
COIN_ICON = 'assets/ui/coin.png'

#general colors
UI_BG_COLOR = '#4C4F4F'
UI_BORDER_COLOR = '#222222'
UI_TEXT_COLOR = '#FFFCF2'

#UI colors
HEALTH_COLOR = 'red'
UI_BORDER_COLOR_ACTIVE = 'gold'

# Player
player_data = {'health': 100, 'damage' : 5, 'speed': 1.5}
PLAYER_SIZE = 16
PLAYER_HEALTH_POINTS = 50
PLAYER_ATTACK_POINTS = 10
PLAYER_ATTACK_COOLDOWN = 300
PLAYER_SWITCH_WEAPON_COOLDOWN = 500
BUILD_COOLDOWN = 1000

# Weapons
weapons_data = {
    'sword' : {'cooldown' : 100, 'damage' : 10, 'graphic' : 'assets/weapon/sword/full.png'},
    'axe' : {'cooldown' : 200, 'damage' : 5, 'graphic' : 'assets/weapon/axe/full.png'}}

# Enemys
monster_data = {
    'skull' : {'health' : 20,    'damage' : 5, 'gold_amount': 1, 'attack_type' : 'slash', 'attack_sound' : None, 'speed' : 5, 'resistance' : 3, 'attack_radius': 20, 'notice_radius': 360},
    'cyclope' : {'health' : 100, 'damage' : 15, 'gold_amount': 5, 'attack_type' : 'claw',  'attack_sound' : None, 'speed' : 3, 'resistance' : 10, 'attack_radius': 50, 'notice_radius': 360}}

# House
house_data = {
    'health': 1000,
    'graphic' : { 'asset' : 'assets\entity\maison.png', 'width' : 80, 'height' : 80}
}


# MAP
EMPTY_MAP = "map_empty_80_45"