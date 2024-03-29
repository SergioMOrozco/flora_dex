from pyinaturalist import *
import pprint
import os
import glob
import requests
import pandas as pd
import time
import uuid
from distributed import Client, LocalCluster,as_completed

inps = [
"Acantholimon aff. venustum",
"Acantholimon hohenackeri",
"Acantholimon sp.",
"Acanthus spinosus",
"Achillea filipendulina 'Parker’s Variety'",
"Achillea 'Hoffnung' Great Expectations",
"Achillea 'Lachsschonheit' Salmon Beauty",
"Achillea millefolium",
"Achillea millefolium 'Apfelblute' Appleblossom",
"Achillea millefolium 'Rosea'",
"Achillea millefolium 'Royal Tapestry'",
"Achillea millefolium 'Summer Wine'",
"Achillea millefolium 'Walther Funcke'",
"Achillea 'Moonshine'",
"Acineta superba",
"Aconitum 'Bressingham Spire'",
"Aconitum × cammarum 'Eleanor'",
"Aconitum lycoctonum ssp. neapolitanum",
"Aconitum volubile",
"Actaea matsumurae 'White Pearl'",
"Actaea racemosa",
"Actaea simplex 'Black Negligee' (Atropurpurea Group)",
"Aechmea chantinii 'Vista'",
"Aechmea miniata var. discolor",
"Aechmea × 'Royal Wine'",
"Aesculus parviflora",
"Agapanthus 'Blue Yonder'",
"Agapanthus inapertus ssp. pendulus 'Graskop'",
"Agapanthus 'Tom Thumb'",
"Agastache aurantiaca 'P012S' CORONADO®",
"Agastache barberi",
"Agastache Blue Traditional Hyssop",
"Agastache cana 'Purple Pygmy'",
"Agastache cana 'Sinning' SONORAN SUNSET®",
"Agastache Red 'Pstessene' CORONADO®",
"Agastache rugosa",
"Agastache rupestris",
"Agastache sp.",
"Agastache 'Tangerine Dreams'",
"Agastache ×",
"Agave havardiana",
"Agave parryi",
"Agave parryi ssp. neomexicana",
"Agave parryi ssp. parryi",
"Alcea rosea",
"Alcea rosea 'Peaches ’n’ Dreams'",
"Alcea rugosa",
"Alchemilla alpina",
"Alchemilla xanthochlora",
"Allium caeruleum",
"Allium carinatum ssp. pulchellum f. album",
"Allium cernuum",
"Allium cyaneum",
"Allium flavum",
"Allium galanthum",
"Allium humile",
"Allium ramosum",
"Allium senescens",
"Allium senescens ssp. glaucum",
"Allium sp.",
"Allium sphaerocephalum",
"Allium stellatum",
"Aloe aristata",
"Althaea officinalis",
"Alyssum caespitosum",
"Alyssum markgrafii",
"Ambrosia psilostachya",
"Amorpha canescens",
"Amorpha fruticosa",
"Anagallis monelli",
"Anagallis monelli ssp. monelli",
"Anaphalis margaritacea",
"Anaphalis margaritacea var. yedoensis",
"Anchusa capensis",
"Andropogon gerardii",
"Andropogon hallii",
"Androsace hedreantha",
"Androsace lanuginosa",
"Anemone canadensis",
"Anemone sylvestris",
"Anemonopsis macrophylla",
"Angelica acutiloba",
"Angelica brevicaulis",
"Angelica sp.",
"Angraecum distichum",
"Anguloa cliftonii 'Larry Johnston'",
"Anguloa dubia",
"Anguloa virginalis",
"Anthemis marschalliana",
"Anthericum ramosum",
"Anthurium 'Cotton Candy'",
"Aquilegia chaplinei",
"Aquilegia chrysantha",
"Aquilegia chrysantha DENVER GOLD®",
"Aquilegia elegantula",
"Aquilegia formosa",
"Aquilegia glandulosa",
"Aquilegia 'Swan Violet &amp; White' REMEMBRANCE®",
"Aralia racemosa",
"Arctotis arctotoides",
"Argemone pleiacantha",
"Argemone polyanthemos",
"Arisaema candidissimum",
"Arisaema tashiroi",
"Arisaema ternatipartitum",
"Aristida purpurea",
"Armeria curvifolia",
"Artemisia frigida",
"Artemisia ludoviciana",
"Artemisia nova",
"Artemisia versicolor 'Sea Foam'",
"Arum nigrum",
"Asclepias incarnata",
"Asclepias pumila",
"Asclepias speciosa",
"Asclepias speciosa 'Davis'",
"Asclepias tuberosa",
"Aster asteroides",
"Astilbe grandis",
"Asyneuma canescens",
"Athamanta turbith ssp. haynaldii",
"Atraphaxis sp.",
"Atriplex hortensis var. rubra",
"Ballota acetabulosa",
"Begonia 'Pink Spot Lucerne'",
"Begonia 'Pollux'",
"Begonia × semperflorens-cultorum 'Whopper Red With Bronze Leaf'",
"Berkheya cirsiifolia",
"Berkheya purpurea",
"Berlandiera lyrata",
"Betonica officinalis",
"Betula litwinowii",
"Blepharoneuron tricholepis",
"Bolax gummifera",
"Borago officinalis",
"Bougainvillea glabra",
"Bouteloua curtipendula",
"Bouteloua curtipendula 'Butte'",
"Bouteloua curtipendula 'Trailway'",
"Bouteloua gracilis 'Blonde Ambition'",
"Bouteloua gracilis 'Lovington'",
"Brassavola acaulis",
"Brassavola cucullata",
"Brassia signata",
"Brassia verrucosa",
"Brunnera macrophylla 'Jack Frost'",
"Buchloe dactyloides 'Sharp’s Improved'",
"Buddleja alternifolia 'Argentea'",
"Buddleja davidii 'Adokeep' Adonis Blue",
"Buddleja davidii 'Peakeep' Peacock",
"Buddleja davidii 'Pink Delight'",
"Buddleja davidii 'Pyrkeep' Purple Emperor™",
"Buddleja davidii 'Royal Red'",
"Buddleja lindleyana",
"Bukiniczia cabulica",
"Bulbine 'Athena Compact Yellow'",
"Bulbine capitata",
"Bulbine frutescens",
"Bulbine frutescens TINY TANGERINE™",
"Bulbine narcissifolia",
"Bulbophyllum carunculatum",
"Bulbophyllum echinolabium",
"Bulbophyllum gracilipes",
"Bulbophyllum longissimum",
"Bulbophyllum makoyanum",
"Bulbophyllum medusae 'Onca'",
"Bulbophyllum saurocephalum 'Hihimanu'",
"Calamagrostis × acutiflora 'Eldorado'",
"Calamagrostis × acutiflora 'Karl Foerster'",
"Calamintha grandiflora",
"Calamintha nepeta ssp. glandulosa 'White Cloud'",
"Calamovilfa longifolia",
"Calathea loeseneri",
"Calceolaria arachnoidea",
"Callirhoe involucrata",
"Calycanthus 'Aphrodite'",
"Calylophus serrulatus 'Prairie Lode'",
"Campanula alliariifolia",
"Campanula armena",
"Campanula cochleariifolia 'Alba'",
"Campanula hercegovina 'Nana'",
"Campanula incurva",
"Campanula patula ssp. abietina",
"Campanula 'Pink Octopus'",
"Campanula pyramidalis",
"Campanula rotundifolia",
"Campanula rumeliana",
"Campanula thyrsoides",
"Campanula trachelium",
"Campanula troegerae",
"Campanula waldsteiniana",
"Campanula zangezura",
"Campsis radicans",
"Campsis radicans 'Flava'",
"Canna 'Erebus'",
"Capsicum annuum 'Black Pearl'",
"Carex appalachica",
"Carex grayi",
"Carex muskingumensis",
"Carex pensylvanica",
"Carex sp.",
"Caryota mitis",
"Castilleja integra",
"Catalpa × erubescens",
"Catalpa × erubescens 'Purpurea'",
"Catasetum expansum",
"Cattleya amethystoglossa",
"Cattleya harrisoniana",
"Celosia argentea var. cristata 'Arrabona Red'",
"Centaurea macrocephala",
"Centaurea simplicicaulis",
"Centaurea sp.",
"Cephalanthus occidentalis",
"Cerinthe major",
"Chamaebatiaria millefolium",
"Chamaecrista fasciculata",
"Chasmanthium latifolium",
"Chilopsis Denver Botanic Garnets",
"Chilopsis linearis",
"Chrysanthemum 'Betty Lou'",
"Chrysanthemum 'Fireworks'",
"Chrysanthemum 'Maroon Pride'",
"Cischweinfia dasyandra",
"Clematis 'Alba Luxurians'",
"Clematis fruticosa 'Mongolian Gold'",
"Clematis hexapetala",
"Clematis hirsutissima var. scottii",
"Clematis integrifolia 'PSHarlan' MONGOLIAN BELLS®",
"Clematis 'Madame Baron Veillard'",
"Clematis paniculata",
"Clematis vitalba",
"Cleome serrulata",
"Cleome 'Sparkler Blush'",
"Clinopodium japonicum",
"Clivia miniata",
"Coelogyne pandurata",
"Coelogyne swaniana",
"Coelogyne usitana",
"Colutea arborescens",
"Combretum indicum",
"Commelina erecta",
"Consolida ajacis",
"Coreopsis 'Full Moon' Big Bang™",
"Coreopsis lanceolata",
"Coreopsis rosea 'American Dream'",
"Coreopsis tinctoria",
"Coreopsis verticillata 'Moonbeam'",
"Cornus sericea 'Baileyi'",
"Cortaderia selloana 'Patagonia'",
"Cosmos sulphureus 'Cosmic Orange'",
"Costus osae",
"Cota tinctoria",
"Cota triumfettii ssp. triumfettii",
"Cotinus coggygria",
"Cotinus 'Grace'",
"Cotula hispida",
"Cotyledon orbiculata",
"Crassula sarcocaulis ssp. rupicola",
"Crinum bulbispermum",
"Crocosmia 'Lucifer'",
"Curcuma longa",
"Curcuma zedoaria",
"Cyclamen purpurascens",
"Cylindropuntia imbricata",
"Cylindropuntia whipplei",
"Cymbidium Jill 'Katalnica'",
"Dahlia coccinea 'Lemon Blush'",
"Dalea candida",
"Dalea purpurea",
"Dalea purpurea 'Stephanie'",
"Daphne × burkwoodii 'Carol Mackie'",
"Dasiphora fruticosa",
"Dasiphora fruticosa 'McKay’s White'",
"Datura wrightii",
"Deinanthe bifida",
"Delosperma 'Alan’s Apricot'",
"Delosperma carterae 'Carlile Pink'",
"Delosperma cooperi",
"Delosperma davyi",
"Delosperma dyeri 'Psdold' RED MOUNTAIN™",
"Delosperma Fire Wonder 'Wowday2' Wheels Of Wonder®",
"Delosperma Flame 'PWWG02S' RED MOUNTAIN®",
"Delosperma floribundum STARBURST®",
"Delosperma Golden Wonder 'WOWD20111' Wheels Of Wonder®",
"Delosperma 'John Proffitt' TABLE MOUNTAIN®",
"Delosperma 'Kelaidis' MESA VERDE®",
"Delosperma Orange 'PJS02S' GRANITA®",
"Delosperma 'P001S' FIRE SPINNER®",
"Delosperma 'Psfave' Lavender Ice",
"Delosperma Raspberry 'PJS01S' GRANITA®",
"Delosperma Red Wonder Wheels Of Wonder",
"Delosperma sp.",
"Delosperma White Wonder 'WOWDW7' Wheels Of Wonder®",
"Delphinium semibarbatum",
"Dendrobium Gatton Sunray",
"Dendrobium Jaq-Hawaii",
"Dendrobium lawesii 'Purple'",
"Dendrobium nakaharae",
"Dendrobium oligophyllum",
"Dendrobium thyrsiflorum",
"Desmanthus illinoensis",
"Dianthus barbatus 'Bouquet Purple'",
"Dianthus chinensis",
"Dianthus erinaceus var. alpinus",
"Dianthus knappii",
"Dianthus 'Nyewoods Cream'",
"Dianthus petraeus ssp. noeanus",
"Dianthus FIRST LOVE®",
"Dianthus sp.",
"Dianthus superbus",
"Diascia integerrima",
"Diascia integerrima 'P009S' CORAL CANYON®",
"Dichelostemma congestum",
"Digitalis grandiflora",
"Digitalis mariana",
"Digitalis mariana ssp. heywoodii",
"Digitalis obscura SUNSET®",
"Digitalis purpurea 'Candy Mountain'",
"Digitalis stewartii",
"Digitalis thapsi SPANISH PEAKS®",
"Dracocephalum nutans",
"Dracocephalum renati",
"Dracula Swamp Fox",
"Dracula vampira",
"Drimiopsis kirkii",
"Dryadella simula",
"Dyckia leptostachya",
"Ecballium elaterium",
"Echinacea angustifolia",
"Echinacea 'Art’s Pride' Orange Meadowbrite™",
"Echinacea 'Cheyenne Spirit'",
"Echinacea 'Evan Saul' Sundown Big Sky Series™",
"Echinacea 'Mama Mia'",
"Echinacea 'Matthew Saul' Harvest Moon Big Sky Series™",
"Echinacea pallida",
"Echinacea paradoxa",
"Echinacea purpurea",
"Echinacea purpurea 'Alba'",
"Echinacea purpurea 'Doppelganger' Doubledecker",
"Echinacea purpurea 'Merlot'",
"Echinacea purpurea Prairie Splendor™",
"Echinacea purpurea 'White' PowWow™",
"Echinacea 'Quills ’N Thrills'",
"Echinacea 'Secret Lust'",
"Echinacea 'Sunrise' Big Sky Series™",
"Echinacea 'Tangerine Dream'",
"Echinacea tennesseensis",
"Echinops bannaticus 'Blue Glow'",
"Echinops bannaticus 'Taplow Blue'",
"Echinops ritro 'Veitch’s Blue'",
"Echinops sphaerocephalus",
"Echinops tjanschanicus",
"Echium russicum compact form",
"Elymus canadensis",
"Elymus smithii",
"Encyclia adenocaula",
"Encyclia alata × mooreana",
"Encyclia cyanocolumna",
"Encyclia maculosa",
"Encyclia polybulbon",
"Encyclia unaensis",
"Engelmannia peristenia",
"Epidendrum cinnabarinum",
"Epidendrum cristatum",
"Epidendrum longirepens",
"Epidendrum marmoratum",
"Epidendrum melistagum",
"Epidendrum peperomia",
"Epidendrum secundum",
"Epilobium angustifolium",
"Epilobium canum ssp. garrettii",
"Epilobium canum ssp. garrettii 'PWWG01S' ORANGE CARPET®",
"Epilobium canum ssp. latifolium",
"Epilobium fleischeri",
"Eria hyacinthoides",
"Ericameria laricifolia",
"Ericameria nauseosa baby blue form ssp. nauseosa",
"Ericameria nauseosa ssp. nauseosa var. nauseosa",
"Erigeron divergens",
"Erigeron karvinskianus",
"Erigeron speciosus",
"Erigeron ursinus",
"Eriogonum allenii 'Little Rascal'",
"Eriogonum arcuatum",
"Eriogonum effusum",
"Eriogonum jamesii",
"Eriogonum pharnaceoides",
"Eriogonum racemosum",
"Eriogonum sphaerocephalum var. sphaerocephalum",
"Eriogonum tenellum",
"Eriogonum umbellatum",
"Eriogonum umbellatum var. aureum 'Psdowns' KANNAH CREEK®",
"Eriogonum umbellatum var. majus",
"Erodium absinthoides",
"Erodium chrysanthum",
"Erodium 'Katherine Joy'",
"Erodium manescavii",
"Erodium rupestre",
"Eryngium giganteum",
"Eryngium planum 'Blaukappe'",
"Eryngium spinalba",
"Eryngium × zabelii 'Big Blue'",
"Eschscholzia californica",
"Eschscholzia californica 'Milky White'",
"Escobaria sneedii ssp. koenigii",
"Eucomis autumnalis",
"Euphorbia corollata",
"Euphorbia donii",
"Euphorbia marginata",
"Exochorda × macrantha 'The Bride'",
"Fallugia paradoxa",
"Festuca glauca Festina™",
"Filipendula rubra 'Venusta'",
"Foeniculum vulgare 'Purpureum'",
"Fuchsia magellanica 'Riccartonii'",
"Gaillardia aristata",
"Gaillardia aristata 'Amber Wheels'",
"Gaillardia aristata 'Arizona Sun'",
"Gaillardia pinnatifida",
"Gaura neomexicana ssp. coloradensis",
"Gazania krebsiana TANAGER®",
"Gazania linearis 'P004S' COLORADO GOLD®",
"Genista tinctoria",
"Genista tinctoria 'Royal Gold'",
"Gentiana asclepiadea",
"Gentiana clausa",
"Gentiana cruciata",
"Gentiana gelida",
"Geranium dalmaticum",
"Geranium 'Gerwat' Rozanne®",
"Geranium × johnsonii 'Johnson’s Blue'",
"Geranium magniflorum 'P013S' LA VETA LACE®",
"Geranium sessiliflorum",
"Gilia capitata",
"Gladiolus 'Atomic'",
"Gladiolus 'Las Vegas'",
"Gladiolus 'Mirella'",
"Gladiolus murielae",
"Gladiolus 'Nathalie'",
"Gladiolus 'Robinetta'",
"Glandularia bipinnatifida",
"Glandularia bipinnatifida VALLEY LAVENDER®",
"Glottiphyllum longum",
"Gomphostigma virgatum",
"Gomphrena globosa 'Audray Pink'",
"Gongora sp.",
"Goniolimon incanum 'Sea Spray'",
"Goniolimon tataricum",
"Grammatophyllum speciosum",
"Guzmania lingulata var. splendens 'Variegata'",
"Guzmania pennellii",
"Guzmania remyi",
"Guzmania sanguinea",
"Gypsophila sp.",
"Haplopappus glutinosus",
"Hedeoma todsenii",
"Hedychium forrestii",
"Hedychium 'Pink V'",
"Helenium autumnale 'Helena Gold'",
"Helenium autumnale 'Rotgold' Red And Gold",
"Helenium 'Helbro' Mardi Gras",
"Helianthemum 'Wisley Pink'",
"Helianthus annuus",
"Helianthus annuus 'Soraya'",
"Helianthus annuus 'Suntastic Yellow With Black Center'",
"Helianthus annuus 'Suntastic Yellow With Clear Center'",
"Helianthus maximiliani",
"Helianthus × multiflorus 'Loddon Gold'",
"Helichrysum trilineatum",
"Helictotrichon sempervirens",
"Heliomeris multiflora",
"Hemerocallis 'Afternoon Tea Time'",
"Hemerocallis 'All Fired Up'",
"Hemerocallis 'Always Afternoon'",
"Hemerocallis 'Amber Palace'",
"Hemerocallis 'Apple Tart'",
"Hemerocallis 'Arctic Snow'",
"Hemerocallis 'Atlas'",
"Hemerocallis 'Autumn Minaret'",
"Hemerocallis 'Aztec Furnace'",
"Hemerocallis 'Barbara Mitchell'",
"Hemerocallis 'Bertie Ferris'",
"Hemerocallis 'Best Of Friends'",
"Hemerocallis 'Betty Woods'",
"Hemerocallis 'Bijou'",
"Hemerocallis 'Bold Streaker'",
"Hemerocallis 'Borgia'",
"Hemerocallis 'Brocaded Gown'",
"Hemerocallis 'Buddha'",
"Hemerocallis 'Canyon Lullaby'",
"Hemerocallis 'Carrots Forever'",
"Hemerocallis 'Challenger'",
"Hemerocallis 'Charles Johnston'",
"Hemerocallis 'Chicago Knobby'",
"Hemerocallis 'Chicago Picotee Promise'",
"Hemerocallis 'Chicago Ruby'",
"Hemerocallis 'Chipper Cherry'",
"Hemerocallis 'Chorus Line'",
"Hemerocallis 'Coral Gem'",
"Hemerocallis 'Cricket'",
"Hemerocallis 'Curls'",
"Hemerocallis 'Custard Candy'",
"Hemerocallis 'Daring Deception'",
"Hemerocallis 'Designer Jeans'",
"Hemerocallis 'Divertissment'",
"Hemerocallis 'Dominic'",
"Hemerocallis 'Double Bourbon'",
"Hemerocallis 'Dragon Lore'",
"Hemerocallis 'Dragons Eye'",
"Hemerocallis 'Ed Murray'",
"Hemerocallis 'Eleonore'",
"Hemerocallis 'Elizabeth Salter'",
"Hemerocallis esculenta",
"Hemerocallis 'Fairy Tale Pink'",
"Hemerocallis 'Flame Fagot'",
"Hemerocallis fulva 'Kwanzo Variegata'",
"Hemerocallis 'Golden Chimes'",
"Hemerocallis 'Golden Scarab'",
"Hemerocallis 'Green Tarantula'",
"Hemerocallis 'Green Valley'",
"Hemerocallis 'Guardian Angel'",
"Hemerocallis 'Hesperus'",
"Hemerocallis 'Hold That Tiger'",
"Hemerocallis 'Hortensia'",
"Hemerocallis 'Hot Glow'",
"Hemerocallis 'Houdini'",
"Hemerocallis 'Ida’s Magic'",
"Hemerocallis 'Imperial Guard'",
"Hemerocallis 'Inez Ways'",
"Hemerocallis 'James Marsh'",
"Hemerocallis 'Janice Brown'",
"Hemerocallis 'Jet Signal'",
"Hemerocallis 'Kindly Light'",
"Hemerocallis 'Lady Fingers'",
"Hemerocallis lilioasphodelus",
"Hemerocallis 'Linda'",
"Hemerocallis 'Little Cream Puff'",
"Hemerocallis 'Little Grapette'",
"Hemerocallis 'Little Greenie'",
"Hemerocallis 'Little Orange Giant'",
"Hemerocallis 'Little Wart'",
"Hemerocallis 'Little Zinger'",
"Hemerocallis 'Long Stocking'",
"Hemerocallis 'Look Ahead'",
"Hemerocallis 'Made In Dixie'",
"Hemerocallis 'Make Believe Magic'",
"Hemerocallis 'Mary Todd'",
"Hemerocallis 'Melonade'",
"Hemerocallis 'Mikado'",
"Hemerocallis 'Milk Chocolate'",
"Hemerocallis 'Misha'",
"Hemerocallis 'Monument Magic'",
"Hemerocallis 'Moonlit Masquerade'",
"Hemerocallis 'Mrs. W. H. Wyman'",
"Hemerocallis multiflora",
"Hemerocallis 'Nanuq'",
"Hemerocallis 'New Tangerine Twist'",
"Hemerocallis 'Nightsong'",
"Hemerocallis 'Olive Bailey Langdon'",
"Hemerocallis 'Ophir'",
"Hemerocallis 'Paper Butterfly'",
"Hemerocallis 'Paradise Princess'",
"Hemerocallis 'Persian Market'",
"Hemerocallis 'Petite Ballet'",
"Hemerocallis 'Pink Mystique'",
"Hemerocallis 'Rajah'",
"Hemerocallis 'Real Purple Star'",
"Hemerocallis 'Red Mittens'",
"Hemerocallis 'Red Ribbons'",
"Hemerocallis 'Rocky Ford'",
"Hemerocallis 'Rose Emily'",
"Hemerocallis 'Ruby Spider'",
"Hemerocallis 'Ruffled Apricot'",
"Hemerocallis 'Ruffled Parchment'",
"Hemerocallis 'Ruffled Pinafore'",
"Hemerocallis 'September Gold'",
"Hemerocallis 'Siloam Double Classic'",
"Hemerocallis 'Snow Ballerina'",
"Hemerocallis 'Snow Orchid'",
"Hemerocallis 'Sound and Fury'",
"Hemerocallis 'Statuesque'",
"Hemerocallis 'Strawberry Candy'",
"Hemerocallis 'Summer Wind'",
"Hemerocallis 'Sunshine Express'",
"Hemerocallis 'Suzie Wong'",
"Hemerocallis 'Techny Spider'",
"Hemerocallis thunbergii",
"Hemerocallis 'Treasure Gold'",
"Hemerocallis 'Violet Hour'",
"Hemerocallis 'Wayne Johnson'",
"Hemerocallis 'Winning Ticket'",
"Hemerocallis 'Yellow Bouquet'",
"Hemerocallis 'Yellow Wax'",
"Hesperaloe parviflora",
"Hesperaloe parviflora 'Perpa' BRAKELIGHTS®",
"Hesperaloe parviflora yellow",
"Hesperaloe 'Perfu' Pink Parade®",
"Hesperostipa comata",
"Heterotheca jonesii",
"Heterotheca villosa × jonesii 'Goldhill'",
"Heterotheca villosa var. villosa",
"Heuchera cylindrica",
"Heuchera 'Frosted Violet'",
"Heuchera pulchella",
"Heuchera sanguinea 'Snow Angel'",
"Hibiscus moscheutos 'Splash Pinot Noir'",
"Hibiscus sabdariffa",
"Hibiscus sp.",
"Hieracium tomentosum ssp. tomentosum",
"Hillia triflora",
"Hirpicium armerioides",
"Holodiscus dumosus",
"Homalopetalum kienastii",
"Hosta 'Blue Angel'",
"Hosta clausa",
"Hosta 'Earth Angel'",
"Hosta 'Fortunei Albopicta'",
"Hosta lancifolia 'Numor'",
"Houttuynia cordata 'Flore-Pleno'",
"Hoya sp.",
"Huernia oculata",
"Hydrangea arborescens 'Annabelle'",
"Hydrangea macrophylla 'Fanfare' Next Generation Wedding Ring",
"Hydrangea paniculata 'Wim’s Red ' Fire And Ice",
"Hydrangea quercifolia 'Brido' Snowflake",
"Hydriastele pinangoides",
"Hypericum 'Cfflpc-1' Blue Velvet™",
"Hypericum elongatum",
"Hypericum frondosum 'Sunburst'",
"Hyssopus seravschanicus",
"Hyssopus sp.",
"Impatiens balfourii",
"Impatiens mackeyana ssp. claeri",
"Impatiens pallida",
"Incarvillea olgae",
"Inula ensifolia 'Compacta'",
"Inula helenium",
"Inula magnifica",
"Inula royleana",
"Ipomoea leptophylla",
"Ipomoea purpurea",
"Ipomopsis aggregata",
"Ipomopsis rubra",
"Iris 'Champagne Elegance'",
"Iris domestica",
"Iris ×",
"Juniperus scopulorum 'Woodward'",
"Justicia brasiliana",
"Justicia carnea var. purpurea",
"Kaempferia gilbertii",
"Kingidium decumbens",
"Knautia macedonica",
"Kniphofia 'Alcazar'",
"Kniphofia 'Bees’ Sunset'",
"Kniphofia 'Border Ballet'",
"Kniphofia caulescens",
"Kniphofia 'Coral'",
"Kniphofia fluviatilis",
"Kniphofia hirsuta 'Fire Dance'",
"Kniphofia linearifolia",
"Kniphofia 'Lord Roberts'",
"Kniphofia 'Pineapple Popsicle'",
"Kniphofia × praecox",
"Kniphofia 'Stark’s Early Hybrid'",
"Kniphofia triangularis",
"Kniphofia 'Wayside Flame'",
"Koelreuteria paniculata",
"Lablab purpureus ssp. purpureus 'Ruby Moon'",
"Laelia anceps",
"Lathyrus latifolius",
"Lavandula angustifolia",
"Lavandula angustifolia 'Munstead'",
"Lavandula angustifolia 'Wee One'",
"Lavandula × intermedia 'Grosso'",
"Lavandula sp.",
"Lavatera thuringiaca",
"Leontopodium nivale ssp. alpinum",
"Leptosiphon nuttallii ssp. nuttallii",
"Leucanthemum × superbum 'Alaska'",
"Leucanthemum × superbum 'Becky'",
"Leucanthemum × superbum 'Crazy Daisy'",
"Leucanthemum × superbum 'Leuzoo1' Freak!®",
"Leucanthemum × superbum 'Snowcap'",
"Leucanthemum × superbum 'Switzerland'",
"Levisticum officinale",
"Lewisia cotyledon (Sunset Group)",
"Liatris spicata",
"Liatris spicata 'Kobold'",
"Ligularia 'Little Rocket'",
"Ligularia przewalskii",
"Ligustrum vulgare 'Aureum'",
"Lilium (African Queen Group)",
"Lilium 'American Bandstand'",
"Lilium 'American Dream'",
"Lilium 'American Heritage'",
"Lilium 'American Sensation'",
"Lilium 'American Spirit'",
"Lilium 'American Way'",
"Lilium 'Black Beauty'",
"Lilium 'Blackout'",
"Lilium 'Bonbini'",
"Lilium 'Bright Diamond'",
"Lilium 'Brushstroke'",
"Lilium concolor",
"Lilium 'Connecticut King'",
"Lilium davidii",
"Lilium 'Forever Susan'",
"Lilium formosanum",
"Lilium 'Gironde'",
"Lilium henryi",
"Lilium 'High Tea'",
"Lilium 'Lady Alice'",
"Lilium lancifolium",
"Lilium lancifolium 'Flore Pleno'",
"Lilium 'Landini'",
"Lilium 'Miss Feya'",
"Lilium 'Mona Lisa'",
"Lilium 'Montezuma'",
"Lilium 'Orania'",
"Lilium pardalinum",
"Lilium philadelphicum",
"Lilium 'Pizzazz'",
"Lilium regale",
"Lilium 'Reinesse'",
"Lilium 'Richmond'",
"Lilium 'Scheherazade'",
"Lilium 'Silk Road'",
"Lilium sp.",
"Lilium 'Starburst Sensation'",
"Lilium 'Sun Ray'",
"Lilium 'Tango Strawberry And Cream'",
"Lilium Tiger Babies Group",
"Lilium 'Tiny Ghost'",
"Lilium 'Tiny Icon'",
"Lilium 'Tiny Orange Sensation'",
"Lilium 'Touching'",
"Lilium 'Yelloween'",
"Limonium binervosum",
"Limonium gmelinii",
"Limonium minutum",
"Limonium platyphyllum",
"Linum capitatum",
"Linum lewisii",
"Linum ×",
"Liriope spicata",
"Lobelia cardinalis",
"Lonicera × heckrottii 'Goldflame'",
"Lonicera reticulata 'P015S' KINTZLEY",
"Lupinus argenteus",
"Lycaste Balliae",
"Lycaste Peter Sander",
"Lycaste schilleriana",
"Lycaste tricolor",
"Lysimachia ciliata 'Rubra'",
"Lysimachia clethroides",
"Lysimachia nummularia 'Aurea'",
"Lysimachia punctata 'Alexander'",
"Malva moschata f. alba",
"Masdevallia amabilis",
"Masdevallia Angel Frost 'Ord Court'",
"Masdevallia Aquarius",
"Masdevallia Aquarius 'Laramie'",
"Masdevallia Bella Donna",
"Masdevallia Cassiope",
"Masdevallia Cheryl Shohan",
"Masdevallia coccinea",
"Masdevallia Heathii",
"Masdevallia Redwing 'Dark Wonder'",
"Masdevallia Sunset Jaguar 'Regal Cat'",
"Masdevallia Ted Khoe 'Gina'",
"Matthiola montana",
"Maxillaria longipetala",
"Maxillaria uncata",
"Medinilla magnifica",
"Meiracyllium trinasutum",
"Melampodium leucanthum",
"Melica ciliata",
"Melissa officinalis",
"Mentha longifolia",
"Mentha suaveolens 'Variegata'",
"Mentzelia decapetala",
"Mentzelia nuda",
"Michauxia campanuloides",
"Micromeria dalmatica",
"Miltonia Petunia 'Red Admiral'",
"Miltonia spectabilis var. semi-alba",
"Mimulus cardinalis",
"Mirabilis multiflora",
"Monarda 'Bergamo'",
"Monarda bradburiana 'Prairie Gypsy'",
"Monarda citriodora",
"Monarda didyma",
"Monarda didyma 'Croftway Pink'",
"Monarda didyma Lilac 'Balbalmac' BALMY™",
"Monarda fistulosa",
"Monarda fistulosa var. menthifolia",
"Monarda 'Marshall’s Delight'",
"Monarda sp.",
"Monardella macrantha 'Marian Sampson'",
"Montiopsis umbellata",
"Morina longifolia",
"Musa itinerans var. guangdongensis",
"Myrmecophila tibicinis",
"Nageliella purpurea",
"Nelumbo nucifera 'Huan Qing' Celebration",
"Nelumbo nucifera 'Mrs. Perry D. Slocum'",
"Nelumbo 'Rosy Clouds'",
"Neoregelia ampullacea var. rubra",
"Neoregelia ampullacea 'Variegata'",
"Neoregelia 'Cheers'",
"Neoregelia concentrica 'Pewter'",
"Neoregelia kerryi red form",
"Neoregelia marmorata",
"Nepeta 'Psfike' LITTLE TRUDY®",
"Nicotiana 'Perfume Deep Purple'",
"Nidularium innocentii 'Nana'",
"Nierembergia Dark Blue 'KLENC07344' Lara™",
"Nierembergia hippomanica var. coerulea 'White Robe'",
"Nierembergia 'USNRB1201' Augusta Blue Skies®",
"Nigella damascena",
"Nolina microcarpa",
"Nuphar japonica",
"Nymphaea 'Clyde Ikins'",
"Nymphaea 'Denver’s Delight'",
"Nymphaea 'Detective Erika'",
"Nymphaea 'James Brydon'",
"Nymphaea 'Manee Red'",
"Nymphaea 'Mangkala Ubol'",
"Nymphaea 'Peach Glow'",
"Nymphaea 'Pink Grapefruit'",
"Nymphaea 'Tan-khwan'",
"Nymphaea 'Tuonta'",
"Nymphoides geminata",
"Oenothera canescens",
"Oenothera cespitosa",
"Oenothera elata ssp. hookeri",
"Oenothera hartwegii ssp. fendleri",
"Oenothera howardii",
"Oenothera macrocarpa",
"Oenothera macrocarpa ssp. incana",
"Oenothera macrocarpa ssp. incana SILVER BLADE®",
"Oncidium hyphaematicum",
"Ononis repens",
"Ophiopogon planiscapus 'Nigrescens'",
"Opuntia engelmannii",
"Opuntia macrocentra var. minor",
"Opuntia phaeacantha",
"Origanum laevigatum 'Herrenhausen'",
"Origanum laevigatum 'Hopleys'",
"Origanum libanoticum",
"Origanum rotundifolium",
"Origanum scabrum",
"Origanum vulgare",
"Origanum vulgare 'Woods Compact'",
"Ornithogalum candicans",
"Ornithogalum viridiflorum",
"Orostachys spinosa",
"Osteospermum 'Avalanche'",
"Osteospermum 'P005S' PURPLE MOUNTAIN®",
"Osteospermum 'P006S' LAVENDER MIST®",
"Oxytropis lambertii",
"Panicum virgatum",
"Panicum virgatum 'Shenandoah'",
"Papaver paeoniflorum 'Black'",
"Papaver rupifragum 'Double Tangerine Gem'",
"Papaver triniifolium",
"Paphinia Majestic",
"Paphiopedilum Hsinying Alien",
"Paphiopedilum victoria-regina",
"Parthenium integrifolium",
"Pelargonium endlicherianum",
"Pelargonium endlicherianum 'Sunscapes Select'",
"Pelargonium quercetorum",
"Pennisetum glaucum 'Jade Princess'",
"Penstemon aff. osterhoutii",
"Penstemon ambiguus",
"Penstemon barbatus",
"Penstemon barbatus 'Coral Baby'",
"Penstemon cardinalis",
"Penstemon cinicola",
"Penstemon cobaea",
"Penstemon degeneri",
"Penstemon fruticosus var. serratus",
"Penstemon leonensis",
"Penstemon linarioides ssp. coloradoensis 'P014S' SILVERTON®",
"Penstemon × mexicali",
"Penstemon × mexicali 'Carolyn’s Hope'",
"Penstemon × mexicali 'P007S' PIKES PEAK PURPLE®",
"Penstemon × mexicali 'P008S' RED ROCKS®",
"Penstemon × mexicali 'Psmyers' SHADOW MOUNTAIN®",
"Penstemon × mexicali 'PWIN02S' WINDWALKER®",
"Penstemon neomexicanus",
"Penstemon pinifolius",
"Penstemon pinifolius 'Mersea Yellow'",
"Penstemon pseudospectabilis",
"Penstemon richardsonii",
"Penstemon richardsonii var. dentatus",
"Penstemon rostriflorus",
"Penstemon rubicundus",
"Penstemon strictus",
"Penstemon wilcoxii",
"Peperomia fraseri",
"Persicaria amplexicaulis 'Atrosanguinea'",
"Persicaria amplexicaulis 'Firetail'",
"Petrophytum cinerascens",
"Petunia patagonica",
"Phacelia campanularia",
"Phalaenopsis chibae",
"Phalaenopsis venosa",
"Phemeranthus calycinus",
"Philadelphus lewisii 'PWY01S' CHEYENNE®",
"Phlomis grandiflora",
"Phlox carolina 'Miss Lingard'",
"Phlox longifolia ssp. brevifolia",
"Phlox paniculata 'Delilah'",
"Phlox paniculata 'Ditomfav' Candy Store Cotton Candy™",
"Phlox paniculata 'Franz Schubert'",
"Phlox paniculata 'Laura'",
"Phragmipedium Eric Young",
"Phragmipedium Inca Embers",
"Phragmipedium ×",
"Phygelius capensis",
"Phygelius × rectus",
"Phygelius × rectus 'Pink Elf'",
"Phyla cuneifolia",
"Physostegia virginiana 'Miss Manners'",
"Physostegia virginiana 'Vivid'",
"Phytolacca americana",
"Picea pungens 'Hoopsii'",
"Picradeniopsis oppositifolia",
"Pinellia pedatisecta",
"Pinellia tripartita",
"Pinus aristata",
"Plantago argentea",
"Plantago subulata",
"Platycodon grandiflorus",
"Platystele consobrina 'Gail'",
"Plectranthus argentatus",
"Pleurothallis bivalvis",
"Pleurothallis herpestes",
"Pleurothallis minutalis",
"Pleurothallis niveoglobula",
"Pleurothallis schiedei",
"Polanisia dodecandra",
"Polemonium reptans 'Touch Of Class'",
"Potentilla hippiana",
"Potentilla nepalensis 'Shogran'",
"Potentilla sp.",
"Potentilla thurberi 'Monarch’s Velvet'",
"Primula beesiana",
"Primula rusbyi",
"Promenaea stapelioides",
"Prosthechea livida",
"Prosthechea mariae 'Denver Botanic Gardens'",
"Prosthechea vitellina",
"Prunella grandiflora",
"Pseuderanthemum reticulatum 'Eldorado'",
"Pterocephalus depressus",
"Pterocephalus perennis",
"Purshia mexicana",
"Putoria calabrica",
"Pycnanthemum tenuifolium",
"Quesnelia marmorata 'Tim Plowman'",
"Ratibida columnifera",
"Ratibida columnifera f. pulcherrima",
"Ratibida columnifera 'Yellow'",
"Ratibida pinnata",
"Ratibida tagetes",
"Restrepia antennifera",
"Rhodanthemum atlanticum",
"Rhodophiala splendens",
"Robinia neomexicana",
"Rosa 'AUSbite' Spirit of Freedom",
"Rosa 'Ausbonny' Wildeve",
"Rosa 'Ausjake' Miss Alice",
"Rosa 'Ausjo' Jude the Obscure",
"Rosa 'Auslow' Yellow Button",
"Rosa 'Ausmove' Tess of the d",
"Rosa 'Ausreef' Sharifa Asma",
"Rosa 'Ausrelate' Lichfield Angel",
"Rosa 'AUSrimini' Strawberry Hill",
"Rosa 'Auswalker' The Pilgrim",
"Rosa 'AUSwinter' Crown Princess Margareta",
"Rosa 'Ballerina'",
"Rosa 'Fantin-Latour'",
"Rosa 'HARpageant' Easy Does It™",
"Rosa 'Harwelcome' Livin",
"Rosa 'JACthain' Tuscan Sun",
"Rosa 'Jasru' RUBY VOODOO",
"Rosa 'KORsixkono' Kolorscape Kardinal™",
"Rosa 'KORtemma' Red Ribbons®",
"Rosa 'Meiviolin' Eden Rose",
"Rosa 'Morten' Linda Campbell™",
"Rosa 'Pike’s Peak'",
"Rosa 'Poulans' Martha's Vineyard™",
"Rosa 'POUlgret ' Hampton™",
"Rosa 'Poulharm' Manhattan™",
"Rosa 'Radtko' Double Knock Out®",
"Rosa Velvet Abundance",
"Rosa 'Sprolem' Eyeconic Lemonade",
"Rosa 'WEKbijou' Koko Loko",
"Rosa 'Wekebtidere' Twilight Zone",
"Rosa 'WEKplapic' BETTY BOOP™",
"Rubus odoratus",
"Rudbeckia 'Denver Daisy'",
"Rudbeckia fulgida var. speciosa",
"Rudbeckia hirta",
"Rudbeckia hirta 'Indian Summer'",
"Rudbeckia laciniata",
"Rudbeckia laciniata 'Golden Glow'",
"Rudbeckia montana",
"Rudbeckia triloba 'Prairie Glow'",
"Ruellia humilis",
"Salvia argentea",
"Salvia Azure 'Mes Azur' Mesa™",
"Salvia cyanescens",
"Salvia daghestanica PLATINUM®",
"Salvia darcyi",
"Salvia darcyi × microphylla 'PWIN03S'",
"Salvia darcyi 'Pscarl' VERMILION BLUFFS®",
"Salvia dorrii",
"Salvia engelmannii",
"Salvia forskaehlei",
"Salvia greggii",
"Salvia greggii 'Furman’s Red'",
"Salvia greggii 'Red Letter'",
"Salvia greggii 'Teresa'",
"Salvia greggii 'Wild Thing'",
"Salvia jurisicii",
"Salvia lemmonii Desert Rose 'PWIN04S' WINDWALKER®",
"Salvia moorcroftiana × indica",
"Salvia nemorosa 'Caradonna'",
"Salvia nemorosa 'Ostfriesland' East Friesland",
"Salvia nemorosa 'Pusztaflamme' Plumosa",
"Salvia officinalis × fruticosa",
"Salvia officinalis 'Icterina'",
"Salvia officinalis (Purpurascens Group)",
"Salvia pachyphylla",
"Salvia penstemonoides",
"Salvia pisidica",
"Salvia reptans",
"Salvia sp.",
"Salvia 'Ultra Violet'",
"Salvia verticillata 'Purple Rain'",
"Salvia yangii",
"Santolina chamaecyparissus",
"Santolina rosmarinifolia",
"Satureja montana",
"Satureja montana ssp. illyrica",
"Satureja spinosa",
"Saururus cernuus",
"Saussurea japonica",
"Scabiosa 'Butterfly Blue'",
"Scabiosa caucasica 'Fama'",
"Scabiosa caucasica House's hybrids",
"Scabiosa columbaria 'Blue Note'",
"Scabiosa graminifolia var. compacta",
"Scabiosa 'Mariposa Violet'",
"Scabiosa ochroleuca",
"Scaphosepalum ovulare",
"Schizachyrium scoparium 'Standing Ovation'",
"Scrophularia macrantha",
"Scutellaria baicalensis",
"Scutellaria orientalis ssp. pinnatifida",
"Scutellaria resinosa",
"Scutellaria resinosa 'Smoky Hills'",
"Scutellaria salviifolia",
"Scutellaria scordiifolia",
"Scutellaria scordiifolia 'Pat Hayward' SKY",
"Scutellaria suffrutescens",
"Sedum acre",
"Sedum album",
"Sedum album 'Atropurpureum'",
"Sedum 'Autumn Fire'",
"Sedum rupestre 'Angelina'",
"Sedum sediforme Turquoise Tails (don't include on signs) '",
"Sedum sp.",
"Sedum spurium",
"Sedum spurium 'Coccineum'",
"Sedum takesimense",
"Senecio sp.",
"Senna marilandica",
"Seseli gummiferum",
"Sesleria autumnalis",
"Sesleria heufleriana",
"Sideritis syriaca",
"Silene armeria",
"Silene caryophylloides ssp. echinus",
"Silene chalcedonica",
"Silene coronaria",
"Silene flos-cuculi 'Petite Jenny'",
"Silene regia",
"Silene saxifraga",
"Silene schafta",
"Silphium laciniatum",
"Silphium terebinthinaceum",
"Sium sisarum",
"Sobralia decora",
"Sobralia macrantha",
"Solanum elaeagnifolium",
"Solanum melongena 'Fairy Tale'",
"Solidago gigantea",
"Solidago 'Goldkind' Golden Baby",
"Solidago rigida",
"Solidago sp.",
"Sorbaria sorbifolia",
"Spartina pectinata",
"Spathicarpa sagittifolia",
"Specklinia grobyi",
"Sphaeralcea ambigua Papago Pink™",
"Sphaeralcea coccinea",
"Sphaeralcea incana",
"Sphaeralcea parvifolia",
"Spiraea japonica 'Goldflame'",
"Sporobolus airoides",
"Sporobolus heterolepis",
"Sporobolus wrightii",
"Stachys byzantina",
"Stachys byzantina 'Big Ears' Countess Helen von Stein",
"Stachys coccinea",
"Stachys monieri 'Hummelo'",
"Stanhopea embreei",
"Stanhopea jenischiana",
"Stanhopea martiana",
"Stanhopea oculata",
"Stanhopea saccata 'Hoosier'",
"Stelis purpurascens",
"Stipa capillata",
"Stipa ichu",
"Stokesia laevis 'Honeysong Purple'",
"Streptocarpus saxorum",
"Styphnolobium japonicum 'Regent'",
"Symphyotrichum laeve var. laeve",
"Symphyotrichum novae-angliae 'Hella Lacy'",
"Symphyotrichum novi-belgii 'Melody'",
"Symphytum × uplandicum",
"Tagetes patula Bolero BONANZA™",
"Tanacetum armenum",
"Tanacetum corymbosum",
"Tanacetum densum ssp. amani",
"Telekia speciosa",
"Tetraneuris scaposa var. scaposa",
"Teucrium chamaedrys",
"Teucrium chamaedrys 'Gold Tip'",
"Teucrium hircanicum",
"Thelesperma filifolium",
"Thymus × citriodorus",
"Thymus comosus",
"Thymus serpyllum 'Pink Chintz'",
"Thymus vulgaris",
"Tibouchina naudiniana",
"Tillandsia capitata 'Marron'",
"Tillandsia 'Creation'",
"Tillandsia leiboldiana",
"Tillandsia lindenii var. caeca",
"Tradescantia × andersonianna 'Sweet Kate'",
"Tradescantia 'Innocence' (Andersoniana Group)",
"Trichoglottis brachiata",
"Trichosalpinx chamaelepanthes",
"Tricyrtis latifolia",
"Verbascum atroviolaceum",
"Verbascum bombyciferum",
"Verbascum bombyciferum 'Polarsommer' Arctic Summer",
"Verbascum chaixii",
"Verbascum chaixii 'Album'",
"Verbascum olympicum",
"Verbena 'Balendurp' Enduro Purple",
"Verbena × hybrida 'Peaches And Cream'",
"Verbena 'Imagination'",
"Verbena stricta",
"Verbesina encelioides",
"Veronica allionii",
"Veronica alpina 'Alba'",
"Veronica longifolia",
"Veronica longifolia 'Blauriesin' Foerster's Blue",
"Veronica 'P018S' SNOWMASS®",
"Veronica spicata",
"Veronicastrum virginicum",
"Veronicastrum virginicum 'Alboroseum'",
"Veronicastrum virginicum f. roseum",
"Viburnum plicatum f. tomentosum 'Summer Snowflake'",
"Viola cornuta 'Alba Minor'",
"Viola corsica",
"Vitex agnus-castus 'Little Madame'",
"Vitex agnus-castus 'Montrose Purple'",
"Vitex agnus-castus Petty Blue Daytona Heat™",
"Vriesea bleheri",
"Vriesea × 'Marcella'",
"Vriesea saundersii",
"Wahlenbergia undulata",
"Westringia fruticosa",
"x Angulocaste Flemenco",
"x Ascocenda Fat Tuesday",
"x Brassolaeliocattleya Penny's Spot 'Hawaiian Dream'",
"x Chitalpa tashkentensis 'Pink Dawn'",
"x Colmanara Wildcat 'Gold Country'",
"x Laeliocattleya Christmas Bouquet",
"x Laeliocattleya Mini Purple 'Blue Hawaii'",
"x Laeliocattleya Twilight Song",
"x Laeliocattleya ×",
"x Lowara Trinket",
"x Miltassia Royal Robe 'Jerry’s Pick'",
"x Quesmea 'Quista'",
"x Rhyncholaeliocattleya Hawaiian Satisfaction",
"x Sophrocattleya June Bug 'Mendenhall'",
"x Sophrolaeliocattleya Fuchsia Fire",
"x Sophrolaeliocattleya Mini Beau",
"x Vaughnara ×",
"Xanthisma coloradoense",
"Yucca 'Color Guard'",
"Yucca elata",
"Yucca glauca",
"Yucca rostrata",
"Yucca rupicola",
"Yucca thompsoniana",
"Zingiber spectabile",
"Zinnia elegans 'Zowie! Yellow Flame'",
"Zinnia grandiflora",
"Zinnia grandiflora 'Gold on Blue'",
"Ziziphus jujuba"
]

def get_pyinaturalist_image_urls():
    image_ids = []
    labels = []

    for inp in inps:

        # get observations for pyinaturalist api
        observations = get_observations(
            taxon_name=inp,
            photos=True,
            identifications="most agree",
            page=1,
            per_page=200,
        )

        print(inp + ": ", len(observations["results"]))

        ## dont do too many requests at a time
        time.sleep(1.0)

        line_count = 0
        for obs in observations["results"]:

            if(len(observations["results"]) < 50):
                print(inp + " has too few images. skipping...")
                break

            ## get image_id of observation
            image_id = obs["photos"][0]["url"]
            image_id = image_id.replace("square", "original")

            print(image_id)

            image_ids.append(image_id)
            labels.append(inp)

        # write image
        d = {'image-id' : image_ids, 'label' : labels}
        df = pd.DataFrame(data=d)
        df.to_csv("inaturalist_csv/image_ids.csv",index=False)





def save_images(chunk):
    image_paths = []
    image_ids = [image_id for image_id in chunk['image-id']]
    labels = [label for label in chunk['label']]

    for i in range(len(image_ids)):
        flower_directory = f"raw_data/{labels[i]}/"

        # create flower directory if it does not exist
        if not os.path.exists(flower_directory):
            os.makedirs(flower_directory)
        
        # TODO: account for .jpg .jpeg .png
        if '.jpg' in image_ids[i]:
            suffix = 'jpg'
        elif '.png' in image_ids[i]:
            suffix = 'png'
        elif 'jpeg' in image_ids[i]:
            suffix = 'jpeg'

        file_name = f"{flower_directory}{uuid.uuid4()}.{suffix}"

        image_url = image_ids[i].split('?',1)[0]

        print("Writing {0} to file_name {1}".format(image_url, file_name))

        nb_tries = 10
        while True:
            nb_tries -= 1
            try:
                ## write image url to file
                f = open(file_name, "wb")
                f.write(requests.get(image_url).content)
                f.close()

                image_paths.append(file_name)

                break
            except:
                if nb_tries == 0:
                    print("ERROR")
                    exit(-1)
                else:
                    # dont get yelled at by internet
                    print("got yelled at")
                    time.sleep(1)
    
    return image_paths, labels

def download_and_save_image_ids():
    futures = []
    for chunk in pd.read_csv("inaturalist_csv/image_ids.csv", chunksize= 500):
        future= client.submit(save_images, chunk, key=str(uuid.uuid4()))
        futures.append(future)

    completed = as_completed(futures)

    image_paths =[]
    labels = []
    for i in completed:
        p,l = i.result()

        image_paths += p
        labels += l

    d = {'image-path' : image_paths, 'label' : labels}
    df = pd.DataFrame(data=d)
    df.to_csv("raw_data/image_paths.csv",index=False)

if __name__ == "__main__":
    cluster = LocalCluster()
    client = Client(cluster)
    
    print("Retreiving Image Ids")
    time.sleep(1.0)
    get_pyinaturalist_image_urls()

    print("Downloading Image Ids")
    time.sleep(1.0)
    download_and_save_image_ids()
