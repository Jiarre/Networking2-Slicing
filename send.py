import sys , getopt
import re
import os
import subprocess

def main(argv):
    list = {
        'h1' : "192.168.1.22",
        'h2' : "192.168.1.31",
        'h3' : "192.168.1.32",
        'h4' : "192.168.1.42",
        'h5' : "192.168.1.51",
        'h6' : "192.168.1.52",
        'a1' : "192.168.2.61",
        'a2' : "192.168.2.62",
        'a3' : "192.168.1.21",
        'a4' : "192.168.1.41",
        'it1' : "192.168.1.73",
        'it2' : "192.168.1.74",
        'ftp' : "192.168.1.75",
    }

    try:
      opts, args = getopt.getopt(argv,"hc:p:f:")
    except getopt.GetoptError:
      print('send.py -c destination \nsend.py -p destination \nsend.py -h \nsend.py -s destination')
      sys.exit(2)

    for opt, arg in opts:
        # argument check
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",arg) == None:
            if arg in list:
                arg = list[arg]
            else :
                print('name not found')
                sys.exit(-1)

        # help
        if opt == '-h' :
            print(' <Usages>\n send.py -c destination \n send.py -p destination \n send.py -h')
            sys.exit()

        # call voip
        elif opt == '-c':
            output = subprocess.run(['iperf', '-c',  arg, '-p',  '5060' , '-u' , '-t' , '2' ,'-i', '1'], stdout=subprocess.PIPE).stdout.decode('utf-8')
            if 'WARNING' in output:
                print("VOIP ERROR ")
            else:

                print("VoIP response from "+ args )
        elif opt == '-f':
            output = subprocess.run(['iperf', '-c',  arg, '-p',  '21' , '-t' , '2' ,'-i', '1'], stdout=subprocess.PIPE).stdout.decode('utf-8')
            if 'connected' in output:
                print("FTP response from "+arg)
            else:

                print("FTP ERROR")
        # ping
        elif opt == '-p':
            output = subprocess.run(['ping' , '-c', '3', arg], stdout=subprocess.PIPE).stdout.decode('utf-8')
            if "0 received" in output:
                print("PING ERROR "+arg)
            elif '3 received' in output :
                print("ping response from "+arg)
        

if __name__ == "__main__":
   main(sys.argv[1:])