# -*- coding: cp1252 -*-
# Oppdaterer www.kirken.notteroy.no sin kalender
# Tar input fra en csv fil med dette oppsette:
'''UKE ,DATO ,KIRKEÅRSDAG / ,NØTTERØY ,TEIE ,TORØD ,VEIERLAND ,ANDAKTER ,DÅPS- ,STABS- ,KOR / ,TROS- ,DIAKONI ,DIVERSE 
"","",PREKENTEKST ,"","","","",INSTITUSJON ,SAMTALER ,MØTER ,KONSERTER ,OPPLÆRING ,"",""
"",01 ,"","","","","","","","","","","",""
"",02 ,"","","","","","","","","","","",""
"",03 ,"","","","","","","","","","","",""
"",04 ,"","","","","","","","","","","",""
"",05 ,Aposteldagen ,"",Gudstjeneste ,"","","","","","","","",""
"","","Matt.16,13-20 ","",TOJ/Jan ,"","","","","","","","",""
'''
import CSVscraper
import mechanize
import sys

# VARIABLER
MONTH = ".08.2015"
STDTID = "11:00"
FILE = "data/data-august.csv"

#get data from csv file.
gudstjenester = CSVscraper.parseCsv(FILE, MONTH, STDTID)

#List of added events
name = []
date = []

# Load the page
br = mechanize.Browser()
site = br.open("http://www.kirken.notteroy.no/index.phtml?pid=2742")
br._factory.is_html = True # Må ha med dette

def main(argv):
        logIn()
        
        enterLink()
        
        # Fill forms
        fillForm(br.form, gudstjenester)

        print "ALL ADDED EVENTS:"
        for i in range(len(name)):
                print name[i]
                print date[i]
                    
        return 0
def logIn ():
        print "Logging inn..\n"
        # Print all forms on page
        #for form in br.forms():
        #        print form

        # Select "login" form
        username = br.form = list(br.forms())[0]
 
        br.form["username"] = "pybot"
        br.form["password"] = "kalender"

        br.submit()
        
def enterLink ():
        # Go to "kalender"
        site = br.open("http://www.kirken.notteroy.no/index.phtml?pid=59")
        
        #site = br.response()
        br._factory.is_html = True # Må ha med dette

        #første formen på nettsiden
        form = br.form = list(br.forms())[1]
        #print br.form

def fillForm(form, gudstjenester):
        print "Filling out forms...\n"
        br._factory.is_html = True # Må ha med dette

        count = 0
        
        for g in gudstjenester:
                if count == 9:
                        
                        br.submit()
                        print "submiting first 10..."
                        enterLink()
                        form = br.form = list(br.forms())[1]
                        count = 0
                        
                count = count % 10
                
                form["sdato_" + str(count)] = g["dato"]
                form["start_" + str(count)] = g["tid1"]
                form["slutt_" + str(count)] = g["tid2"]
                form["emne_" + str(count)] = g["tittel"]
                form["tekst_" + str(count)] = g["tekst"]
                # Type event. 109 = gudstjeneste
                form["kaltype"] = ["109"]
                # Lesertilgang 0 = alle
                form["lesegruppe"] = ["0"]
                # Redigeringstilgang 1 = admin
                form["skrivegruppe"] = ["1"]

                name.append(g["tittel"])
                date.append(g["dato"])
                
                count+= 1
        
        br.submit()
        print "submited ALL"
        
        
        
        
if __name__ == "__main__":
        main(sys.argv)
