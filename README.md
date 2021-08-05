# DodgeScript

_A realtime, Hypixel Bedwars stats-grabber_

## Description
DodgeScript is a Python project meant for grabbing Hypixel Bedwars stats from members of a lobby by simply screenshotting the tab menu player list. This means users can better understand the skills of their opponents or quickly know when to dodge into a different lobby before the round starts. The script works in a matter of seconds and uses Pytesseract's image-to-text algorithm as well as Mojang and Hypixel's API to get player information.
## Installation
```sh
git clone https://github.com/shrays/DodgeScript DodgeScript
cd ./DodgeScript
pip install -r requirements.txt
brew install pytesseract
```
*note Homebrew is needed to brew install pytesseract

Then, go into `config.yml` and add your Hypixel API key, which can be obtained by running `/api` on the hypixel server.
```yml
hypixel_api_key: "12345678-9abc-def0-1234-56789abcdef0" # <---- REPLACE WITH YOUR API KEY
```
Still in `config.yml`, if you are using a the GUI scale `normal` you can leave this as is. If you are using large as your minecraft GUI scaling, change it to `large`. Note that other scalings such as small or 4x are not supported.
```yml
gui_scale: "large" # <--- REPLACE WITH YOUR MC GUI SCALE ('normal' or 'large')
```

To run the program:
```sh
python dodger.py
```
## Caveats
This script is not perfect. As it stands, there is usually only a ~50% success rate in correctly grabbing all the names from a lobby. This is because of imperfections in pytesseract, the image-to-text library used. This is a point that may be addressed with future updates. Furthermore, because different texturepacks can different fonts, different packs will yield different results. 

##Prefered Usage
Currently the script is intended for `Lunar Client` in that it has filters to remove the lunar logo from nametag readings although it can be used without lunar client by removing
```yml
if players[x].name.startswith('0'): # Lunar client symbol fix
```
from `dodger.py`

Furthermore, because different texturepacks can different fonts, different packs will yield different results. 

Pytesseract struggles with the default minecraft font so packs like aquari will help text recognition: https://www.mediafire.com/folder/bplato6za4yix/Aquari_Recolours

Sky brightness will also effect the accuracy of the image crop. The program is callibrated towards darker sky hues and was tested this the nightime setting of this pack: http://www.mediafire.com/file/a0ehaeewwcgzfpj/!++++%C3%82%C2%A7bClouds+&+Planets+Night+Overlay.zip/file
## Contributions
Feel free to fork this project for your own use. If you do, or if you find any issues, please use our [issues page](https://github.com/shrays/DodgeScript/issues) for reporting bugs or making suggestions. You can also submit pull requests at our [pull requests page](https://github.com/shrays/DodgeScript/pulls).
