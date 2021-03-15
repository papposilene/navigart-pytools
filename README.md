# Scraper for Navigart

[Videomuseum](https://www.videomuseum.fr/) est un réseau de musées et d’organismes gérant des collections d’art moderne et contemporain (musées nationaux, régionaux, départementaux ou municipaux, Cnap (collection du Fnac), Frac, fondations) qui se sont regroupés pour développer, en commun, des méthodes et des outils utilisant les nouvelles technologies de traitement de l’information afin de mieux recenser et diffuser la connaissance de leur patrimoine muséographique.

Les méthodes et outils utilisés dans ce réseau permettent : l’informatisation de la documentation et de la gestion des collections par le logiciel Gcoll et la diffusion de la connaissance de ces mêmes collections par Internet avec le logiciel Navigart.

Ce projet, d'initiative publique, ne permet pas (encore ?) la mise en place d'une API publique offrant à chacun, alors que les collections nationales françaises sont publiques, d'explorer à sa guise le patrimoine de la Nation. Dans le cadre d'un projet personnel, il m'a fallu récupérer quelques données du Centre Pompidou, d'où l'existence de ce petit script en python.

## Installation
```
pip install argparse json re requests time
```

## Usage
To scrape Navigart, run:
```
python3 navigart-scraper.py --museum cnam --start 0 --limit 1000
```

## Supported french museum databases
The `--museum` parameter actually supports the databases of those french museum:
- `cnam`: [Centre national d'art moderne (Centre Georges Pompidou)](https://collection.centrepompidou.fr/).
- `mnpp`: [Musée national Pablo Picasso](https://www.museepicassoparis.fr/fr/collection-en-ligne).

## JSON Merger
By default, this script produces a JSON file by the given limit parameter. It helps to not having a too big final file but some smaller files. A JSON merger script is provided.
```
python3 json-merger.py --folder data
```
