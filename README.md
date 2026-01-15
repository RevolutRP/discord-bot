# Discord Bot

Ovo je jednostavan Discord bot deployan na Railwayu.  
- `bot.py` sadrži kod bota  
- `requirements.txt` sadrži zavisnosti (`discord.py`)  
- `Procfile` definiše kako se bot pokreće (`worker: python bot.py`)  

Token se povlači iz environment varijable `TOKEN` postavljene na Railwayu.
