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
    "files": "<Scrap Mechanic Data folder>",
    "language": "<Your language ('English' recommended)>"
}
```

## Executing SMIconExtractor
Run `python extract.py` with the needed arguments

The value of `-n` (name) or `-u` (UUID) needs to be set to the name/UUID of the icon

The map can be specified with `-m`, maps available: data, customization, tool, survival

If you are extracting from customizations you need to specify a gender with `-g` (male or female, the most things only work with male)
