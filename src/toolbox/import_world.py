import pytmx

def get_collision(file_name):
    tmxdata = pytmx.TiledMap(FILE_DATA)
    return tmxdata.get_layer_by_name("collision").data

if __name__ == "__main__":
    FILE_DATA = "C:\\01-Projet\\01-Jeu\\proto\\proto\\_user\\tmx\\map_empty_32.tmx"
    mat_collsion = get_collision(FILE_DATA)

    print(mat_collsion)


