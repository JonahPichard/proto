import pytmx

def get_info_map(map_name):
    tmxdata = pytmx.TiledMap("assets\\map\\tmx\\"+map_name+".tmx")
    layout = {
            "boundary" : tmxdata.get_layer_by_name("collision").data,
            "entity" : tmxdata.get_layer_by_name("entity").data
            }
    return layout

def distance(point1, point2):
    return ((point1[0]-point2[0])**2+(point1[1]-point2[1]**2)**.5)


if __name__ == "__main__":
    FILE_DATA = "C:\\01-Projet\\01-Jeu\\proto\\proto\\_user\\tmx\\map_empty_32.tmx"
    mat_collsion = get_info_map(FILE_DATA)
    
    # print(mat_collsion)


