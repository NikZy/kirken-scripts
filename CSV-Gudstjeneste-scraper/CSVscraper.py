# -*- coding: iso-8859-1 -*-
import csv



def parseCsv(FILE, MONTH, STDTID):

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
            # sletter del 1 av "PREKENTEKST" som gjør listen for lang
            if len(row) > 14:
                del row[2]

            # if csv table error
            if len(row) < 7:
                error.append(row)
                print "ERROR ROW DELETED_________" + str(count)
                print" ______"
                #del row[:]


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
                #s = 1

                #if rows.index(rows[i+s]) < len(rows) -1:
                #    while rows[i+s][1] != rows[i+s][1].strip().isdigit():
                    #    print rows[i+s][1]
                 #       rows[i+s][1] = '""'
                 #       s = s + 1

                #Nøtterøy
                if rows[i][3] != '""':

                    text = rows[i][3].rstrip('""') # colonnen og raden der teksten er

                    # legger til flere radene hvis teksten strekker seg over flere
                    n = 1
                    while rows[i+n][1] == '""':
                        if rows[i+n][3] != '""':   
                            text = text + rows[i+n][3]
                        n = n + 1
                    # Bytter ut forkortelser med fulle navn
                    text = initialerParse(text)
                    
                    # TODO: LEGGE TIL TITTEL!
                    tittel = "Gudstjeneste i Nøtterøy kirke"

                    # Sjekker om det er oppgitt tidspunkt
                    tid = tidspunktParse (rows[i][3])
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
                    
                    N = {"dato": rows[i][1] + MONTH, "tekst": text, "tittel": tittel, "tid1": tid1, "tid2":tid2}
                    gudstjenester.append(N)
                   

                #Teie
                if rows[i][4] != '""':
                    text = rows[i][4].rstrip('""')

                    n = 1
                    while rows[i+n][1] == '""':
                        if rows[i+n][4] != '""':
                            text = text + rows[i+n][4]
                        n = n + 1

                    text = initialerParse(text)
                    tittel = "Gudstjeneste i Teie kirke"

                      # Sjekker om det er oppgitt tidspunkt
                    tid = tidspunktParse (rows[i][4])
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
                    
                    N = {"dato": rows[i][1] + MONTH, "tekst": text, "tittel": tittel, "tid1": tid1, "tid2":tid2}
                    gudstjenester.append(N)
                #Torød
                if rows[i][5] != '""':
                    text = rows[i][5].rstrip('""')

                    n = 1
                    while rows[i+n][1] == '""':
                        if rows[i+n][5] != '""':
                            text = text + rows[i+n][5]
                        n = n + 1
                    text = initialerParse(text)
                    tittel = "Gudstjeneste i Torød kirke"
                    
                     # Sjekker om det er oppgitt tidspunkt
                    tid = tidspunktParse (rows[i][5])
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
                    
                    N = {"dato": rows[i][1] + MONTH, "tekst": text, "tittel": tittel, "tid1": tid1, "tid2":tid2}
                    gudstjenester.append(N)

                if rows[i][6] != '""':  #Veierland
                    text = rows[i][6].rstrip('""')

                    n = 1
                    while rows[i+n][1] == '""':
                        if rows[i+n][6] != '""':
                            text = text + rows[i+n][6]
                        n = n + 1
                    text = initialerParse(text)
                    tittel = "Gudstjeneste i Veierland kirke"

                     # Sjekker om det er oppgitt tidspunkt
                    tid = tidspunktParse (rows[i][6])
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
                    
                    N = {"dato": rows[i][1] + MONTH, "tekst": text, "tittel": tittel, "tid1": tid1, "tid2":tid2}
                    gudstjenester.append(N)
    #print error
    return gudstjenester

## BRUKES IKKE ENDA. SKAL TA OVER FOR NÅVÆRENDE,.#TODO: FULLFØRE DENNE
def getData (kolonne):
    # Henter dara fra gitt colonne
    # returnerer dictinary
    if kolonne != '""':
        text = rows[i][3].rstrip('""') # colonnen og raden der teksten er

         # legger til flere radene hvis teksten strekker seg over flere
        n = 1
        
        while rows[i+n][1] == '""':
            if rows[i+n][3] != '""':   
                text = text + rows[i+n][3] + "\n"
            n = n + 1
            
        # Bytter ut forkortelser med fulle navn
        text = initialerParse(text)
                    
        # TODO: LEGGE TIL TITTEL!
        tittel = "Gudstjeneste i Nøtterøy kirke"

        # Legger til tidspunk
        tid1 = tidspunktParse (rows[i][3])
        if tid1 == False:
            tid1 = STDTID

        # Slutttiden er tid1 + en time
        tid2 = int(tid1[:2])
        tid2 = tid2 + 1
        tid2 = str(tid2) + tid1[2:]
    
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
            tekst = tekst.replace(i, value)
            
        #Passer på at den ikke bytter ut Kristine med Kristin 
        elif i == "Kristin" and "Kristine" in tekst == False:
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
    
    # VARIABLER
    MONTH = ".08.2015"
    STDTID = "11:00"
    FILE = "data/data-august.csv"
    
    gudstjenester = parseCsv(FILE, MONTH, STDTID)
    for g in gudstjenester:
        print g
