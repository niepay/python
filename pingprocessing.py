import argparse
from collections import Counter

content_newFile = ""
#add possibility to give filepath in command window with -f/-file
parser = argparse.ArgumentParser()
parser.add_argument("-file", "-f", help="indicate full file path")
# read arguments from the command line
args = parser.parse_args()
# check for -file or -f
if args.file:
    pathOfFile = args.file
    #print("file was %s" % args.file)
else:
    pathOfFile = "noFileAvailable" #pathOfFile           = "C:/Users/nip/Documents/hannes/hannes.sim"


print("\n\nInput Simfile path:\n" + pathOfFile + "\n\n")
list ={}
#write sim-file into string:
with open(pathOfFile, 'rt') as input_simFile:
    content_File = input_simFile.read()


list = content_File.split()
countList = Counter(list)

for ping,frequency in countList.items():
    content_newFile += str(ping) + "\t" + str(frequency) + "\n"

nameofOutputSim = pathOfFile[:pathOfFile.find(".")] + "_" + pathOfFile[pathOfFile.find("."):]
nameofOutputSim = nameofOutputSim.replace("\\\\", "/")
print("Output Simfile path:\n" + nameofOutputSim)

with open(nameofOutputSim, 'w+') as output_simFile:
    output_simFile.truncate()
    output_simFile.write(content_newFile)
