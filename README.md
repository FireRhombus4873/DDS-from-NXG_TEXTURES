# DDS from NXG_TEXTURES
A simple python script that will convert the Traveller's Tales games NXG_TEXTURES into the embedded DDS image files.

## Usage
Use [QuickBMS](https://github.com/LittleBigBug/QuickBMS) alongside the [TTGames.bms](https://aluigi.altervista.org/quickbms.htm#:~:text=Traveller%27s%20Tales%20games%20DAT%20files%20extractor%20(*.dat/hdr)%20(ttgames.bms)) to extract the games files into a folder "Extracted".

Then use this script to find the .DDS images files inside the .NXG_TEXTURES files.

```
usage: extractDDS.py [-h] [-s] [-S] [directory]

Extracts .DDS files from .NXG_TEXTURES files.

positional arguments:
  directory      Directory to extract from (relative to Extracted).

options:
  -h, --help     show this help message and exit
  -s, --silent   Run the script in silent mode.
  -S, --subdirs  Extract from all subdirectories.
```
