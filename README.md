# SMIconExtractor
## Extracts icons from Scrap Mechanic
![GitHub](https://img.shields.io/github/license/EV3R4/SMIconExtractor)
![GitHub repo size](https://img.shields.io/github/repo-size/EV3R4/SMIconExtractor)

## Installation
* Install [Python](https://www.python.org/)
* Clone the repository with `git clone https://github.com/EV3R4/SMIconExtractor.git` or download the [zip](https://github.com/EV3R4/SMIconExtractor/archive/master.zip)
* Install the requirements with `pip install -r requirements.txt`

## Setup
### Config
```json
{
    "iconmappng": "<insert Scrap Mechanic Data/Survival folder here>/Gui/IconMap<Survival>.png",
    "iconmapxml": "<insert Scrap Mechanic Data/Survival folder here>/Gui/IconMap<Survival>.xml",
    "descriptions": "<insert Scrap Mechanic Data/Survival folder here>/Gui/Language/<insert 'English' or your language here>/inventoryDescriptions.json"
}
```

## Executing SMIconExtractor
Run `python extract.py` with the needed arguments

The value of `-n` (name) or `-u` (uuid) needs to be set to the name/uuid of the icon
