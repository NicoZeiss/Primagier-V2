
 # Init DB with some categories
categories = {
	'alimentation': ['fruits & légumes', 'ingrédients', 'actions'], 
	'vêtements': ['accessoires', 'hauts', 'bas', 'chaussures'],
	'animaux': ['dinosaures', 'savane', 'domestiques', 'pays froids', 'marins', 'montagne', 'ferme', 'petites bêtes', 'forêt', 'actions'],
	'parties du corps': ['visage', 'corps'],
	'forêt': ['animaux', 'arbres', 'trésors de la nature'],
	'albums': ['ansel & gretel'],
	'fêtes': ['halloween', 'pâques', 'noël', 'carnaval & chandeleur', 'anniversaires', 'galette'],
	'saisons': ['été', 'automne','hiver', 'printemps'],
	'maison': ['chambre', 'cuisine', 'sanitaires', 'salon'],
	'école': ['lieux', 'matériel', 'jeux'],
	'transports': ['aérien', 'terrestre', 'maritime', 'infrastructures', 'actions'],
	'ferme': ['animaux', 'outils', 'lieux', 'équipements', 'actions'],
	'jardin': ['actions', 'outils', 'plantes', 'équipements'],
	'formes & couleurs': ['formes', 'couleurs'],
	'salle de jeux': ['matériel', 'actions']}

items = {
	'dinosaures': [
		{'name': 'vélociraptor', 'pict': 'https://vignette.wikia.nocookie.net/jurassicpark/images/7/73/Blue_Fallen_Kingdom.png/revision/latest?cb=20181014190546&path-prefix=fr'},
		{'name': 'tyrannosaure', 'pict': 'https://i.pinimg.com/originals/23/11/00/2311006e167119b2c139cf56796f16de.jpg'},
		{'name': 'diplodocus', 'pict': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Diplodocus_carnegii.jpg/1200px-Diplodocus_carnegii.jpg'},
		{'name': 'tricératops', 'pict': 'https://crowscastle.com/133-large_default/collecta-dinosaur-30-triceratops.jpg'},
		{'name': 'ptérodactile', 'pict': 'https://static.pratique.fr/images/unsized/pt/pteranodon.jpg'},
	],
	'savane': [
		{'name': 'lion', 'pict': 'https://img.lemde.fr/2015/12/15/0/0/3120/2127/688/0/60/0/8e8b20c_944931e5ec7c4a1dbaf6eef09caebcad-e2d79a2dab8a4fbb9d94b0bf38645b45-0.jpg'},
		{'name': 'tigre', 'pict': 'https://cdn.futura-sciences.com/buildsv6/images/largeoriginal/8/e/3/8e39442adf_50036032_panthera-tigris-tigris.jpg'},
		{'name': 'zèbre', 'pict': 'https://www.zoom-nature.fr/wp-content/uploads/2018/02/zebre-gp.jpg'},
		{'name': 'girafe', 'pict': 'https://cdn-media.rtl.fr/cache/QCQWfrvkHwkQdURm6hw8Yw/880v587-0/online/image/2018/0410/7792965662_une-girafe-illustration.jpg'},
		{'name': 'éléphant', 'pict': 'https://s.yimg.com/ny/api/res/1.2/Rhka7DXgiSGm.76OAoe85g--~A/YXBwaWQ9aGlnaGxhbmRlcjtzbT0xO3c9Njk5O2g9Mzkz/https://media.zenfs.com/fr/franceinfo_865/24ab2afe1ee7c9c8ccd1fa3bfc166f97'},
	],
	'marins': [
		{'name': 'dauphin', 'pict': 'https://www.animaw.com/wp-content/uploads/2017/08/deux-grands-dauphins-810x442.jpg'},
		{'name': 'requin', 'pict': 'https://static.lpnt.fr/images/2019/04/19/18492445lpw-18493261-article-jpg_6148647_660x281.jpg'},
		{'name': 'baleine', 'pict': 'https://images.ladepeche.fr/api/v1/images/view/5c2e902f8fe56f62f029399b/large/image.jpg'},
		{'name': 'raie manta', 'pict': 'https://img-4.linternaute.com/3iDIbLAFc9Q4WFnFDa4KJRZTflw=/620x/smart/2c6caeeae7b2460c92a62993ee1a7273/ccmcms-linternaute/10775921.jpg'},
		{'name': 'hippocampe', 'pict': 'https://aquariumdevannes.fr/wp-content/uploads/2015/11/Hippocampe-chevelu-hippocampus-guttulatus-24.jpg'},
	],
}