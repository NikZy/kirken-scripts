# -*- coding: cp1252 -*-
from PIL import Image, ImageDraw, ImageFont
import CSVscraper

# VARIABLER
FILEOUT = "juli.jpg"
FILE = "data/data-juli.csv"
MONTH = "JULI"
MONTH2 = ".07.2015"
STDTID = "11:00"
COLOR = (51,204,51) # dark green
# X and Y cordinates for text
X = 300
Y = 390

#gudstjenester = [{'tekst': 'Gudstjeneste Tom Olaf Josephsen/Jan Rosenvinge ', 'tid1': '11:00', 'dato': '05.07.2015', 'tittel': 'Gudstjeneste i Teie kirke', 'tid2': '12:00'},{'tekst': '?? Konsert ', 'tid1': '11:00', 'dato': '07.07.2015', 'tittel': 'Gudstjeneste i Teie kirke', 'tid2': '12:00'},{'tekst': '19.30:  Aftensang (Ferge kl.19.05) Maia Koren/Wenche Henriksen ', 'tid1': '19:30', 'dato': '09.07.2015', 'tittel': 'Gudstjeneste i Teie kirke', 'tid2': '20:30'}]

# get an image
base = Image.open('MAL.jpg').convert('RGBA')

# make a blank image for the text, initialized to transparent text color
txt = Image.new('RGBA', base.size, (0,0,0,0))


# if main
if __name__ == "__main__":
    #get data
    gudstjenester = CSVscraper.parseCsv(FILE, MONTH2, STDTID)

    # checks lenght of g
    for g in gudstjenester:
        print g
        if "Teie" in g["tittel"]:
            if len(g["tekst"]) < 65:
                X = 400
            elif len(g["tekst"]) < 70:
                X = 300
            elif len(g["tekst"]) < 80:
                X = 70
                break
        
    # get a font
    fnt1 = ImageFont.truetype('Lato-reg.ttf', 60)
    fnt2 = ImageFont.truetype('Lato-reg.ttf', 40)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # HEADER
    d.text((X,Y-90), "GUDSTJENESTER I " + MONTH, COLOR, font=fnt1)

    # for hver gudstjeneste som er i Teie
    space = 0
    for g in gudstjenester:
        if "Teie" in g["tittel"]:
            #print g["tekst"]
            # Søndag + dato
            d.text((X,Y+space), "Søndag " + g["dato"][0:2], COLOR, font=fnt2)
            # tid + tekst
            if g["tid1"] != '11:00':
                g["tid1"] = ""
            d.text((X+200,Y+space), g["tid1"] +" "+ g["tekst"], (0, 0, 0), font=fnt2)
            space += 150


    out = Image.alpha_composite(base, txt)
    
    # save
    out.save(FILEOUT, "JPEG")
