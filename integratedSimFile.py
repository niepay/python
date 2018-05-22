#Created on:    20/02/2018
#Author:        Patrick Niederhold
#Simfile Vector Module Converter:
#The following Code converts a simfile with vector modules and global variables
#into a new simfile.


import argparse



#Header:
print(" _____      _                       _         _____ _          ______ _ _       ")
print("|_   _|    | |                     | |       /  ___(_)         |  ___(_) |      ")
print("  | | _ __ | |_ ___  __ _ _ __ __ _| |_ ___  \ `--. _ _ __ ___ | |_   _| | ___  ")
print("  | || '_ \| __/ _ \/ _` | '__/ _` | __/ _ \  `--. \ | '_ ` _ \|  _| | | |/ _ \\")
print(" _| || | | | ||  __/ (_| | | | (_| | ||  __/ /\__/ / | | | | | | |   | | |  __/ ")
print(" \___/_| |_|\__\___|\__, |_|  \__,_|\__\___| \____/|_|_| |_| |_\_|   |_|_|\___| ")
print("                     __/ |")
print("                    |___/ ")


print("Starting Integration:")

#add possibility to give filepath in command window with -f/-file
parser = argparse.ArgumentParser()
parser.add_argument("-file", "-f", help="indicate full file path")
# read arguments from the command line
args = parser.parse_args()
# check for -file or -f
if args.file:
    pathOfSimfile = args.file
    #print("file was %s" % args.file)
else:
    pathOfSimfile = "noFileAvailable" #pathOfSimfile           = "C:/Users/nip/Documents/hannes/hannes.sim"

print("Input Simfile path:\n" + pathOfSimfile)
content_header =""
content_headerComment = ""
with open(pathOfSimfile, 'rt') as input_simFile:
    content_simFile = input_simFile.read()

for line in content_simFile.split("\n"):
    if not line =="":
        line = line.replace('"','""')
        content_header += (line + "\\" + "\n")
        #content_headerComment += (line + "\\\n")

prefix = '#include <string>\n\n\nnamespace integratedSimfile{\n\n\textern std::string simfileContent ="'
suffix = "\n};\n\n"

content_header = prefix + "\\\n" + content_header + '";'+ suffix# + content_headerComment

nameofOutputSim = "C:\modemsim\simulator\src\integratedSimfile.h"
print(content_header)
print("Output Simfile path:\n" + nameofOutputSim)

with open(nameofOutputSim, 'w+') as output_simFile:
    output_simFile.truncate()
    output_simFile.write(content_header)
print("\n\nSimfile integration finished!")
