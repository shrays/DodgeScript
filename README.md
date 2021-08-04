# DodgeScript

_A realtime, Hypixel Bedwars stats-grabber_

## Description
DodgeScript is a Python project meant for grabbing Hypixel Bedwars stats from members of a lobby by simply screenshotting the player list. This means users can quickly determine whether the lobby is filled with sweaty players and promptly evacuate before the round starts. The script works in a matter of seconds and uses Mojang and Hypixel's API to get the information.
## Installation
Installing DodgeScript is as simple as the following:
```sh
git clone https://github.com/shrays/DodgeScript DodgeScript
cd ./DodgeScript
pip install -r requirements.txt
```
To run the program:
```sh
python dodger.py
```
## Caveats
There may be some slight modifications you will need to make for your computer for this program to run. Notably, this includes the screenshots directory. As it stands, it currently references the creator's directory.
- MacOS: Replace the username 'shrayswarup' with your own.
- Linux: Use ~/.minecraft/screenshots
- Windows: Idk something something appdata.

Furthermore, this script is not perfect. As it stands, there is usually only a ~50% success rate in grabbing all the names from a lobby. This is because of imperfections in pytesseract, the image-to-text library used. This is a point that may be addressed with future updates.
## Contributions
Feel free to fork this project for your own use. If you do, or if you find any issues, please use our [issues page](https://github.com/shrays/DodgeScript/issues) for reporting bugs or making suggestions. You can also submit pull requests at our [pull requests page](https://github.com/shrays/DodgeScript/pulls).