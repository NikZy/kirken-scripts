import sys, getopt
#from pudb import set_trace; set_trace() #debugging
def show_usage():
	print "\nusage: arg.py -m <month int(1-12)> -f <datafile (csv file)> -l <'username & password'>"
	print "example: arg.py -m 2 -f filename.csv -l 'user pw'"
	sys.exit()

def main(argv):
	month = ""
	login = ""
	file = ""

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
			if arg.isdigit() and  int(arg) > 0 and int(arg) < 13:
				month = arg
			else:
				show_usage()
		elif opt in ("-f", "--datafile"):
			file = arg
		elif opt in ("-l", "--login"):
			login = arg.split(" ")
			

	print "month" + month
	print "Login" + str(login)
	print "file"+ file

if __name__ == "__main__":
	main(sys.argv[1:])
	#print sys.argv