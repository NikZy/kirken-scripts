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
import getopt
import os

# VARIABLER
MONTH = ".08.2015"
STDTID = "11:00"
FILE = ""#data/data-august.csv"
LOGIN= ""

#List of added events
name = []
date = []

# Load the page
br = mechanize.Browser()
site = br.open("http://www.kirken.notteroy.no/index.phtml?pid=2742")
br._factory.is_html = True # Må ha med dette

def show_usage():
        print "\nusage: arg.py -m <month.year> -f <datafile (csv file)> -l <'username & password'>"
        print "example: arg.py -m 08.2015 -f filename.csv -l 'user pw'"
        sys.exit()

def check_usage(argv):
        if len(argv) != 6:
                show_usage()

        try:
                opts, args = getopt.getopt(argv, "hm:l:f:", ["month=", "login=", "file"])
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
                elif opt in ("-f", "--datafile"):
                        global FILE
                        FILE = arg
                elif opt in ("-l", "--login"):
                        global LOGIN
                        LOGIN = arg.split(" ")
        return True

def main(argv):
        #get data from csv file.
        print "collects data from", FILE
        print "Month = ", MONTH

        hendelser = CSVscraper.parseCsv(FILE, MONTH, STDTID)

        #be bruker om å se etter errors
        for h in hendelser:
                for g in h:
                        print ""
                        print g["dato"]
                        print g["tittel"]
                        print g["tekst"]
                        print g["type"]
                        print g["tid1"]

        key = ""             
        while key != "y" and key != "n":
                key = raw_input ("CHECK FOR ERRORS \n want to make changes? (Y/N): ")
        
        if key == "y":
                f = open("temp.txt", "w")
                for e in hendelser:
                        for g in e:
                                f.write(g["tekst"]+"\n")
                f.close()
                key = raw_input("\nMAKE CHANGES IN 'tempt.txt' and press enter when complete")
                
                f = open("temp.txt", "r")

                for h in hendelser:
                        for g in h:
                                l = f.readline()
                                g["tekst"] = l.rstrip("\n")
                f.close()
                os.remove("temp.txt")
                #be bruker om å se etter errors
                for h in hendelser:
                        for g in h:
                                print ""
                                print g["dato"]
                                print g["tittel"]
                                print g["tekst"]
                                print g["type"]
                                print g["tid1"]
                        
                key = raw_input ("\nCHECK FOR ERRORS 1 LAST TIME. Press 'ENTER' when rdy ")



        logIn()
        
        enterLink()
        
        # Fill forms
        fillForm(br.form, hendelser)

        print "ALL ADDED EVENTS:"
        for i in range(len(name)):
                print name[i]
                print date[i]
                    
        return 0
def logIn ():
        print "Logging inn.. (if this fails you have wrong LOGIN details\n"
        # Print all forms on page
        #for form in br.forms():
        #        print form

        # Select "login" form
        username = br.form = list(br.forms())[0]
 
        br.form["username"] = LOGIN[0]
        br.form["password"] = LOGIN[1]

        try:
                br.submit()
                
        except IndexError:
                print "WRONG LOGIN"
                sys.quit()
def enterLink ():
        print  "Go to kalender"
        site = br.open("http://www.kirken.notteroy.no/index.phtml?pid=59")
        
        #site = br.response()
        br._factory.is_html = True # Må ha med dette

        #første formen på nettsiden
        form = br.form = list(br.forms())[1]
        #print br.form

def fillForm(form, hendelser):
        print "Filling out forms...\n"
        br._factory.is_html = True # Må ha med dette

        count = 0
        #log file
        log = open("log.txt", "w")
        log.write("Forms submitted:\n")
        # hendelser[["gudstjenester"], ["konsert"], ["annet"]
        for h in hendelser:
                for g in h:
                        # Det går bare ann å legge inn 10 samtidig
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
                        # sjekke hvilket "type" vi er på atm
                        if hendelser.index(h) == 0:
                                # Type event. 109 = gudstjeneste
                                form["kaltype"] = ["109"]
                        elif hendelser.index(h) == 1:
                                # 128 = konserter
                                form["kaltype"] = ["128"]
                        elif hendelser.index(h) == 2:
                                # 129 = annet
                                form["kaltype"] = ["129"]

                        # Lesertilgang 0 = alle
                        form["lesegruppe"] = ["0"]
                        # Redigeringstilgang 1 = admin
                        form["skrivegruppe"] = ["1"]

                        name.append(g["tittel"])
                        date.append(g["dato"])
                        
                        #write to log.txt
                        log.write("\n-------------\n")
                        log.write(g["tittel"])
                        log.write(g["dato"])
                        log.write(g["tid1"])
                        log.write(g["tekst"])
                        log.write("\n-------------\n")
                        count+= 1
                        
                # Submit når en "type" hendelse er ferdig
                print "ferdig med index: "+ str(hendelser.index(h))
                count = 0
                br.submit()
                enterLink()
                form = br.form = list(br.forms())[1]
        print "n submitted = ", count
        print "submited ALL + check log.txt"
        # close log file
        log.close()
        
if __name__ == "__main__":
        check_usage(sys.argv[1:])
        main(sys.argv[1:])
