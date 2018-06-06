#  Created on:    20/02/2018
#  Author:        Patrick Niederhold
#  Simfile Vector Module Converter:
#  The following Code converts a simfile with vector modules and global variables
#  into a new simfile.
import argparse
import re
from argparse import ArgumentParser

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

# Header:
print(
    '''
 __ _              ___ _ _          ___                          _
/ _(_)_ __ ___    / __(_) | ___    / __\___  _ ____   _____ _ __| |_ ___ _ __
\ \| | '_ ` _ \  / _\ | | |/ _ \  / /  / _ \| '_ \ \ / / _ \ '__| __/ _ \ '__|
_\ \ | | | | | |/ /   | | |  __/ / /__| (_) | | | \ V /  __/ |  | ||  __/ |
\__/_|_| |_| |_|\/    |_|_|\___| \____/\___/|_| |_|\_/ \___|_|   \__\___|_|
''')
# add possibility to give filepath in command window with -f/-file
parser: ArgumentParser = argparse.ArgumentParser(description="convert simFiles with vector modules and global variables")
parser.add_argument("-file", "-f", metavar='\b', help="indicate full file path")
# parser.add_argument("-hvector", "-hv", metavar='\b', help = "explains vector module syntax")
# parser.add_argument("-gvariable", "-gv", metavar='\b', help = "explains global varible syntax")

# read arguments from the command line
args = parser.parse_args()
for arg in vars(args):
    print(arg, getattr(args, arg))
#   check for -file or -f
if args.file:
    pathOfSimfile = args.file
    #  print("file was %s" % args.file)
else:
     # pathOfSimfile = "C:/Users/nip/Documents/projects/hannes/precod02_5beams.sim"  # pathOfSimfile           = "C:/Users/nip/Documents/hannes/hannes.sim"
     pathOfSimfile = "C:/Users/nip/Documents/projects/hannes/double_module.sim"
#  if args.hvector:
#      print("help for vector modules")
#  enter path of simefile for conversion:
#  pathOfSimfile           = "C:/Users/nip/Documents/hannes/x.sim"
#  pathOfSimfile           = "C:/Users/nip/Documents/hannes/precod01_FullSet.sim"
#  variable declaration:
copyVector = False  # for copying vector modules
vector_module = ""
content_string = ""
content_newSIM = ""
header = ""
keyword_MODULE_start = "MODULE["
keyword_DOLLAR = {}  # dictionary for dollar sign + value
keyword_DOLLARDOLLAR = {}  # dictionary for loop variables
dollarValue = 0
print("\n\nInput Simfile path:\n" + pathOfSimfile + "\n\n")

# write sim-file into string:
with open(pathOfSimfile, 'rt') as input_simFile:
    content_simFile = input_simFile.read()
    # print(content_simFile)


# find number of $ vaiables and their names
# make a variable for it and get its value
# extract header:
for line in content_simFile.split("\n"):
    if line.startswith("//"):
        header += "\n" + line
    if line.startswith("MODULE"):
        break
    if line.startswith("$"):
        if not line.startswith("$$"):
            keyword_DOLLAR[line.split(" ")[0]] = line.split(" ")[1]
            # print("line$:" + line)
        # else:
        #     keyword_DOLLARDOLLAR[line.split(" ")[0]] = line.split(" ")[1]
        # print("line$$:" + line)
print("Using following Global Variables:")
# replace $variables with dedicated value and remove [$...] from module:
for nameOfDollar, valOfDollar in keyword_DOLLAR.items():
    print(nameOfDollar,valOfDollar)
    content_simFile = content_simFile.replace(nameOfDollar, valOfDollar)
for line in content_newSIM.split("\n"):
    if line.startswith("//"):
        header += "\n" + line

print("\n\nDuplicating following Modules:")
# go through string line by line and extract vector modules:
for line in content_simFile.split("\n"):

    if copyVector:
        vector_module += "\n" + line
        # print(vector_module)

    if line.startswith(keyword_MODULE_start) and vector_module == "":
        copyVector = True
        # print vector module:
        print(line.replace(line[line.find("["):line.find("]")+1], ""))
        # extract number of vector modules:
        dollarValue = int(find_between(line, "[", "]"))
        vector_module = line.replace("[" + str(dollarValue) + "]", "")
        # print(vector_module)

    if ("PIPELINED" in line or
        "TESTPOINT" in line or
        "LABEL" in line or
        "BRANCH" in line or
        "STATIC_PIPE" in line or
        "NEWSIMU" in line or
        "PAR_START" in line or
        "PAR_END" in line or
        "REMOTE_START" in line or
        "REMOTE_END" in line or
        line.startswith("MODULE ") or
        line.startswith("END") or
        line.startswith("//") or
        line.isspace() or
        not line):

        copyVector = False



    if not copyVector:
        UID_module = ""
        UID_modules = ""
        # duplication of vector modules
        if vector_module:

            # first line is needed for IF UID insertion:
            first_vector_line = vector_module[:vector_module.find("\n")]
            # vector module doubling loop:
            for i in range(0, dollarValue):

                if "//" not in first_vector_line:
                    UID_module += "\n" + vector_module.replace(first_vector_line,
                                                                  first_vector_line + "\tIF UID " + str(i))
                elif "//" in first_vector_line:
                    firstVectorLine_comment = first_vector_line[:first_vector_line.find("//")+2]
                    UID_module += "\n" + vector_module.replace(firstVectorLine_comment[: -2:],
                                                                  firstVectorLine_comment[: -2:] + "\tIF UID " + str(i))
                    # check for pipelined[] or pipelined in vector module for duplication:
                if "PIPELINED" in UID_module:
                    vector_module_pipelined = UID_module[UID_module.find("PIPELINED"):]
                    print(vector_module_pipelined)
                    if "[" in vector_module_pipelined:
                        UID_module = UID_module.replace(find_between(vector_module_pipelined, "D", "]"), "")
                        UID_module = UID_module.replace("]", "")
                    elif not i == dollarValue - 1:
                        UID_module = UID_module.replace(vector_module_pipelined, "")

                loop_parameter = "$$"
                loop_parameter_value =""
                # replace loop parameter in the vector module according to its UID:
                # find loop parameter:
                if "[" in UID_module:

                    for loop_line in UID_module.split("\n"):
                        if "[" in loop_line:
                            loop_line = loop_line.replace("\t\t\t\t\t","]\t\t\t\t\t")
                            loop_parameter = loop_line[loop_line.find("\t") + 1:loop_line.find("[")]
                        if loop_parameter in loop_line:
                        # if loop_line[loop_parameter.__len__() + 1] == "\t":
                            loop_parameter_value = str(re.findall("\d+", loop_line))
                            loop_parameter_value = find_between(loop_parameter_value, "'", "'")
                    print("loop parameter:",loop_parameter)
                    print("loop parameter value:",loop_parameter_value)
                    # print(UID_module)
                    print("#################################################")

                UID_modules += UID_module
                UID_module = ""


            content_newSIM += "\n" + UID_modules
            vector_module = ""



        else:
            content_newSIM += "\n" + line
    if line.startswith("END"):
        break
# FORMAT OUTPUT STRING:
# remove unneccessary parts and format string:
index = content_newSIM.find("MODULE")
new = content_newSIM[index:]
content_newSIM = header + "\n" + new
content_newSIM = "".join([s for s in content_newSIM.splitlines(True) if s.strip("\r\n")])
#content_newSIM = content_newSIM.replace("\n", "")

# write to file:
# generate output name by adding an "_" at the end of the filename:
nameofOutputSim = pathOfSimfile[:pathOfSimfile.find(".")] + "_" + pathOfSimfile[pathOfSimfile.find("."):]
nameofOutputSim = nameofOutputSim.replace("\\\\", "/")
print("\nOutput Simfile path:\n" + nameofOutputSim)

with open(nameofOutputSim, 'w+') as output_simFile:
    output_simFile.truncate()
    output_simFile.write(content_newSIM)

print("\n\nSimfile conversion finished!")
