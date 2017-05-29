def make_genres_big_and_lavin(piped_genres):
    gen_dict = {}
    with open("datadictionary.csv") as dd:
        for i in dd.readlines():
            gen_dict[i[1]] = i[2]
    gen_dict["chimyst"] = "crime"
    gen_dict["locghost"] = "gothic"
    gen_dict["lockandkey"] = "crime"
    gen_dict["lochorror"] = "gothic"
    gen_dict["chihorror"] = "gothic"
    genres_main = []
    genres_lavin = []
    for i in piped_genres:
        gen = i.split(" | ")
        g = []
        lavin_gens = []

        for z in gen:
            if "lavin" in z:
                lavin_gens.append(z)

            if z != "teamred" and z!= "teamblack" and z!= "stew" and z != "juvenile" and z != "drop" and "random" not in z:
                #look up and append big genre
                try:
                    g.append(gen_dict[z])
                except:
                    pass
                    #g.append(z)
        if len(lavin_gens) == 0:
            genres_lavin.append("no_lavin_tag")
        if len(lavin_gens) == 1:
            genres_lavin.append(lavin_gens[0])
        if len(lavin_gens) > 1:
            genres_lavin.append("lavin_multi")
        #merge duplicates
        g = list(set(g))
        if len(g) > 1:
            final_genre = "multi"
        if len(g) == 0:
            final_genre = "non_genre"
        if len(g) == 1:
            final_genre = g[0]
        genres_main.append((g, final_genre))
    processed_genre = [i[0] for i in genres_main]
    final_genre = [i[1] for i in genres_main]
    return processed_genre, final_genre, genres_lavin
