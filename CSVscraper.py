# -*- coding: iso-8859-1 -*-
import csv, sys, getopt

# VARIABLER
MONTH = ".08.2015"
STDTID = "11:00"
FILE = "data/data-august.csv"
def show_usage():
    print "\nusage: CSV.scraper.py -m <month.year> -f <file> "
    print "example: arg.py -m 08.2015 -f data.csv"
    sys.exit()

def check_usage(argv):
    if len(argv) < 1:
                show_usage()

    try:
            opts, args = getopt.getopt(argv, "hm:f:", ["month=", "file="])
    except getopt.GetoptError:
            show_usage()

    for opt, arg in opts:
            if opt == "-h":
                    show_usage()
            elif opt in ("-m", "--month"):
                arg2 = arg.split(".") # check that arg is xx.xxxx
                if arg2[0].isdigit() and arg2[1].isdigit() and len(arg2[0]) == 2 and len(arg2[1]) == 4:
                        global MONTH
                        MONTH = "." + arg
                else:
                        show_usage()
            elif opt in ("-f", "--file"):
                global FILE
                FILE = arg
    return True

def parseCsv(FILE, MONTH, STDTID):
    # Leser inn dataen i rows
    # Liste over dictionaries med gudstjenester.
    # Hvert element har i.text og i.dato
    gudstjenester = []
    error = []
    rows = []
    count = 0
    # Åpne fil og leser rows
    with open (FILE, 'rb') as csvfile:
        reader = csv.reader(csvfile, quotechar='|')
        for row in reader:

            count = count +1
            # DETTE HAR BLITT LØST PÅ EN BEDRE MÅTE, SÅ linje 63
            # sletter del 1 av "PREKENTEKST" som gjør listen for lang
            #if len(row) > 14:
             #   del row[2]

            # if csv table error
            if len(row) < 7:
                error.append(row)
                print "ERROR ROW DELETED_________" + str(count)
                print" ______"
                #del row[:]

            # Fjerner komma i prekentekst som "fucker opp" listen
            if len(row) > 14: #and "." in row[2]:
                # legger sammen eks: "Luk.12" + 41-48
                row[2] = row[2] + row[3]
                # sletter "41-48" fordi den er i row[2]
                del row[3]

            rows.append(row)

    # Går igjennom listen å sjekker etter error
    for r in rows:
        if len(r[1]) > 2 and r[1] != 'DATO ':

                    r[1] = r[1][:2]
                    if r[1].isdigit() != True:
                        r[1] = '""'


    for i, val in enumerate(rows):

        # Fikser lese error. Hvis noe info mangler
        if len(rows[i]) > 6:

            if rows[i][1] != '""' and rows[i][1] != 'DATO ': #Hvis det er en dato

                # fikser lese error. Tar bort prekentekst hvis neste linj eikke er dato.
                #Nøtterøy
                getData(i, 3, rows, gudstjenester)
                   

                #Teie
                getData(i, 4, rows, gudstjenester)
                #Torød
                getData(i, 5, rows, gudstjenester)

                # Veierland
                getData(i, 6, rows, gudstjenester)
    #print error
    return gudstjenester

## Henter dataen til gudstjenesten
def getData (kolonne, rad, rows, gudstjenester):
    # For å få riktig tittel
    if rad == 3:
        kirke = "Nøtterøy kirke"
    elif rad == 4:
        kirke = "Teie kirke"
    elif rad == 5:
        kirke = "Torød kirke"
    elif rad == 6:
        kirke = "Veierland kirke"

    # fikser lese error. Tar bort prekentekst hvis neste linj eikke er dato.
    if rows[kolonne][rad] != '""':
        text = rows[kolonne][rad].rstrip('""')

        # Sjekker om g.tekst strekker seg over flere rader
        # Hvis den gjør, så legg til denne teksten også
        n = 1
        while rows[kolonne+n][1] == '""':
            if rows[kolonne+n][rad] != '""':
                text = text + rows[kolonne+n][rad]
            n = n + 1
        # Bytter ut forkortelser med fulle navn
        text = initialerParse(text)
        # Legger til tittel
        tittel = "Gudstjeneste i " + kirke
        
        ## TODO! Fjerne alt med TID og putte det inn i tidspunktParse
         # Sjekker om det er oppgitt tidspunkt
        tid = tidspunktParse (rows[kolonne][rad])
        tid1 = ""
        tid2 = ""
        
        # det var ikke noe tid der
        if tid == False:
            tid1 = STDTID
            
            tid2 = int(tid1[:2])
            tid2 = tid2 + 1
            tid2 = str(tid2) + tid1[2:]
            
        # det var ikke noe slutt tid der
        elif len(tid) < 2:
            tid1 = tid[0]
            # Slutttiden er tid1 + en time
            tid2 = int(tid1[:2])
            tid2 = tid2 + 1
            tid2 = str(tid2) + tid1[2:]
            
        # der var slutt tid der
        elif len(tid) == 2:
            tid1 = tid[0]
            tid2 = tid[1]
        
        N = {"dato": rows[kolonne][1] + MONTH, "tekst": text, "tittel": tittel, "tid1": tid1, "tid2":tid2}
        gudstjenester.append(N)
    
def initialerParse (tekst):
    n = 0
    # Bytter ut forkortelser med fulle navn
    initialer = {"TOJ":"Tom Olaf Josephsen",
                 "IB": "Inger Bækken",
                 "MK": "Maia Koren",
                 "KOS": "Karl Olav Skilbreid",
                 "DAG": "Dag Litleskare",
                 "Margaretha": "Margaretha Almenningen",
                 "ASTRID": "Astrid Hansen",
                 "GUDRUN": "Gudrun Axelsen",
                 "Ingunn": "Ingunn Aas Andreassen",
                 "Kristin": "Kristin Vold Nese",
                 "Jan": "Jan Rosenvinge",
                 "Wenche": "Wenche Henriksen",
                 "Ellen": "Ellen Haga",
                 "Sonja": "Sonja Thorsnes",
                 "Kristine": "Kristine Amundsen"
                 }
    for i, value in dict.items(initialer):
        if i in tekst and i != "Kristin" and 1 != "Kristine":
            # TODO: 
            # t = "sindre fredrik"
            #t[:t.index("fredrik")] + " Ole " + t[t.index("fredrik"):] 
            #'sindre  Ole fredrik'
            if tekst[tekst.index(i) - 1] != "/":
                tekst = tekst[:tekst.index(i)] + "\nMedvirkende: " + tekst[tekst.index(i):]
            #tekst.index(value)
            tekst = tekst.replace(i, value)
            
        #Passer på at den ikke bytter ut Kristine med Kristin 
        elif i == "Kristin" and "Kristine" not in tekst:
            tekst = tekst.replace(i, value)
        elif i == "Kristine":
            tekst = tekst.replace(i, value)

    return tekst
    
def tidspunktParse (tekst):
    # Sjekker om hendelsen har et annet tidspunkt en standard
    retur = []
    #hvis tekst starter med tidspunkt
    #eksempel: 12. blablabla
    if tekst[:2].isdigit():
        tid = tekst[:2]
        
        #Hvis tekst har spesifik tid
        #Eksempel: 12:30 blabla bla
        if tekst[3:5].isdigit() and tekst[2] != '-':
            tid = tid + ':' + tekst[3:5]
            
        #hvis tekst ikke er spesifikk, legg til :00
        elif tekst[2] != '-':
            tid = tid[:2] + ":00"
        retur.append(tid)
        
        # eksempel 12-14
        if tekst[2] == '-':
            retur[0] = retur[0] + ":00"
            tids = tekst[3:5] + ":00"
            retur.append(tids)
            
        return retur
    return False


if __name__ == "__main__":

    check_usage(sys.argv[1:])
    gudstjenester = parseCsv(FILE, MONTH, STDTID)
    for g in gudstjenester:
        print "\n-------------\n"
        print g["tittel"]
        print g["dato"]
        print g["tid1"]
        print g["tekst"]
        print "\n-------------\n"
