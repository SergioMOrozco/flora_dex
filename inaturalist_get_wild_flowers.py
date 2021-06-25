from pyinaturalist import *
import pprint
import os
import glob
import requests

inps = [
    "Abronia elliptica",
    "Abronia fragrans",
    "Abronia nana",
    "Achillea millefolium",
    "Acmispon wrightii",
    "Aconitum columbianum",
    "Actaea rubra",
    "Agastache pallidiflora",
    "Agastache urticifolia",
    "Agoseris aurantiaca",
    "Agoseris glauca",
    "Aliciella haydenii",
    "Aliciella pinnatifida",
    "Aliciella subnuda",
    "Alisma triviale",
    "Allionia incarnata",
    "Allium acuminatum",
    "Allium cernuum",
    "Allium geyeri",
    "Allium macropetalum",
    "Allium nevadense",
    "Allium schoenoprasum",
    "Almutaster pauciflorus",
    "Alyssum simplex",
    "Amauriopsis dissecta",
    "Amelanchier utahensis",
    "Anagallis arvensis",
    "Anaphalis margaritacea",
    "Androsace septentrionalis",
    "Androstephium breviflorum",
    "Anemone multifida",
    "Anemone narcissiflora",
    "Anemone patens",
    "Anemopsis californica",
    "Angelica grayi",
    "Angelica pinnata",
    "Antennaria anaphaloides",
    "Antennaria dimorpha",
    "Antennaria media",
    "Antennaria microphylla",
    "Antennaria parvifolia",
    "Antennaria rosea",
    "Antennaria umbrinella",
    "Anthemis cotula",
    "Anticlea elegans",
    "Anticlea vaginata",
    "Apocynum androsaemifolium",
    "Apocynum cannabinum",
    "Aquilegia caerulea",
    "Aquilegia caerulea",
    "Aquilegia chrysantha",
    "Aquilegia elegantula",
    "Arctium minus",
    "Arctostaphylos patula",
    "Arenaria lanuginosa",
    "Argemone polyanthemos",
    "Arnica chamissonis",
    "Arnica cordifolia",
    "Arnica latifolia",
    "Arnica longifolia",
    "Arnica mollis",
    "Arnica parryi",
    "Arnica rydbergii",
    "Artemisia cana",
    "Artemisia dracunculus",
    "Artemisia ludoviciana",
    "Artemisia michauxiana",
    "Artemisia norvegica",
    "Artemisia nova",
    "Artemisia scopulorum",
    "Artemisia tridentata",
    "Asclepias asperula",
    "Asclepias involucrata",
    "Asclepias speciosa",
    "Asclepias subverticillata",
    "Astragalus allochrous",
    "Astragalus alpinus",
    "Astragalus amphioxys",
    "Astragalus calycosus",
    "Astragalus ceramicus",
    "Astragalus cicer",
    "Astragalus desperatus",
    "Astragalus flavus",
    "Astragalus hallii",
    "Astragalus kentrophyta",
    "Astragalus lentiginosus",
    "Astragalus miser",
    "Astragalus missouriensis",
    "Astragalus mollissimus",
    "Astragalus musiniensis",
    "Astragalus newberryi",
    "Astragalus nuttallianus",
    "Astragalus praelongus",
    "Astragalus tephrodes",
    "Atriplex canescens",
    "Atriplex confertifolia",
    "Berlandiera lyrata",
    "Berteroa incana",
    "Bistorta bistortoides",
    "Bistorta vivipara",
    "Boechera lemmonii",
    "Boechera pendulocarpa",
    "Boechera perennans",
]


for inp in inps:

    data_directory = "/home/sorozco0612/dev/flora_dex/raw_data/"

    flower_directory = data_directory + inp + "/"

    ## make flower directory if it doesnt exist
    if not os.path.exists(flower_directory):
        os.makedirs(flower_directory)

    ## delete all files in flower directory before adding
    files = glob.glob(flower_directory + "*")
    for f in files:
        os.remove(f)

    observations = get_observations(
        taxon_name=inp,
        photos=True,
        identifications="most agree",
        page=1,
        per_page=100,
    )

    print(inp + ": ", len(observations["results"]))

    line_count = 0
    for obs in observations["results"]:

        ## get image_id of observation
        image_id = obs["photos"][0]["url"]
        image_id = image_id.replace("square", "original")

        file_name = flower_directory + "{0}.jpg".format(line_count)

        print("Writing {0} to file_name {1}".format(image_id, file_name))

        ## write image url to file
        f = open(file_name, "wb")
        f.write(requests.get(image_id).content)
        f.close()

        line_count += 1
        # print(row[0])
        # print(image_id)
