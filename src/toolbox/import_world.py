import pytmx

def get_info_map(map_name):
    tmxdata = pytmx.TiledMap("assets\\map\\tmx\\"+map_name+".tmx")
    layout = {
            "boundary" : tmxdata.get_layer_by_name("collision").data,
            "data" : tmxdata.get_layer_by_name("data").data
            }
    return layout


if __name__ == "__main__":
    FILE_DATA = "C:\\01-Projet\\01-Jeu\\proto\\proto\\_user\\tmx\\map_empty_32.tmx"
    mat_collsion = get_info_map(FILE_DATA)

    # print(mat_collsion)


