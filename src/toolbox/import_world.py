import pytmx

def get_boundary(file_name):
    tmxdata = pytmx.TiledMap(file_name)
    return tmxdata.get_layer_by_name("collision").data


if __name__ == "__main__":
    FILE_DATA = "C:\\01-Projet\\01-Jeu\\proto\\proto\\_user\\tmx\\map_empty_32.tmx"
    mat_collsion = get_boundary(FILE_DATA)

    # print(mat_collsion)


