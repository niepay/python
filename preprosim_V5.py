#Created on:    20/02/2018
#Author:        Patrick Niederhold
#Simfile Vector Module Converter:
#The following Code converts a simfile with vector modules and global variables
#into a new simfile.
import argparse



#Header:
print(" __ _              ___ _ _          ___                          _            ")
print("/ _(_)_ __ ___    / __(_) | ___    / __\___  _ ____   _____ _ __| |_ ___ _ __ ")
print("\ \| | '_ ` _ \  / _\ | | |/ _ \  / /  / _ \| '_ \ \ / / _ \ '__| __/ _ \ '__|")
print("_\ \ | | | | | |/ /   | | |  __/ / /__| (_) | | | \ V /  __/ |  | ||  __/ |   ")
print("\__/_|_| |_| |_|\/    |_|_|\___| \____/\___/|_| |_|\_/ \___|_|   \__\___|_|   ")

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
#enter path of simefile for conversion:
#pathOfSimfile           = "C:/Users/nip/Documents/hannes/x.sim"
#pathOfSimfile           = "C:/Users/nip/Documents/hannes/precod01_FullSet.sim"
#variable declaration:
copyVector            = False    #for copying vector modules
vector_module         = ""
vector_loop_parameter_module   = ""
content_string        = ""
content_newSIM        = ""
header                = ""
match                 = ""
keyword_MODULE_start  =  "MODULE["
keyword_DOLLAR        = {}      #dictionary for dollar sign + value
keyword_DOLLARDOLLAR  = {}      #dictionary for loop variables
dollarValue = 0

print("\n\nInput Simfile path:\n" + pathOfSimfile + "\n\n")

#write sim-file into string:
with open(pathOfSimfile, 'rt') as input_simFile:
    content_simFile = input_simFile.read()
    #print(content_simFile)


#find number of $ vaiables and their names
#make a variable for it and get its value
#extract header:
for line in content_simFile.split("\n"):
    if line.startswith("//"):
        header += "\n" + line
    if line.startswith("MODULE"):
        break
    if line.startswith("$"):
        if not line.startswith("$$"):
            keyword_DOLLAR[line.split(" ")[0]] = line.split(" ")[1]
            #print("line$:" + line)
        #else:
        #    keyword_DOLLARDOLLAR[line.split(" ")[0]] = line.split(" ")[1]
            #print("line$$:" + line)

#replace $variables with dedicated value and remove [$...] from module:
for nameOfDollar,valOfDollar in keyword_DOLLAR.items():
    content_simFile = content_simFile.replace(nameOfDollar,valOfDollar)
for line in content_newSIM.split("\n"):
    if line.startswith("//"):
            header += "\n" + line

#print(content_simFile)
#go through string line by line and extract vector modules:
for line in content_simFile.split("\n"):
    #starting condition for vector module:
    if line.startswith(keyword_MODULE_start):
        copyVector = True
        #extract number of vector modules:
        dollarValue=int(line[line.find("[")+1:line.find("]")])
        vector_module = line.replace("[" + str(dollarValue) + "]","")
        #print(vector_module)

        content_newSIM += "\n" + content_string
        content_string =''
    #if copyvector flag is false copy original simfile text 1:1 to new file.
    if not copyVector or line.startswith("//"):# or line.startswith("END"):
        content_string += line + "\n"
        #print(line)
    #end condition for vector module:
    if ("PIPELINED" in line or\
        "TESTPOINT" in line or\
        "LABEL" in line or\
        "BRANCH" in line or\
        "STATIC_PIPE" in line or\
        "NEWSIMU" in line or\
        "PAR_START" in line or\
        "PAR_END" in line or\
        "REMOTE_START" in line or\
        "REMOTE_END" in line or\
        line == "" or\
        line == "\t" or\
        line.startswith("MODULE ") or\
        #line.startswith("MODULE[") or\
        line.startswith("END")) and\
        copyVector == True:
            #if not"PIPELINED" in line:
            #    line = line.replace("[","")
            #    line = line.replace("]","")
            copyVector = False
            i = 0       # iteration variable for while loop
            #print("line:",line)
            #vector_module += "\n" + line
            vector_module = "".join([s for s in vector_module.splitlines(True) if s.strip("\r\n")])
            #print(vector_module)
            vector_list = vector_module.split("\n")
            vector_module = ""

            while i < int(dollarValue):
                #print("dollarValue",dollarValue)
                if i == 0:
                    if "//" in vector_list[0] and "MODULE" in vector_list[0] :
                        vector_list[0] = vector_list[0].replace("//", "IF UID " + str(i) + " //")
                    elif "//" not in vector_list[0] and "MODULE" in vector_list[0]:
                        vector_list[0] = vector_list[0] + "\tIF UID " + str(i)

                if i != 0:
                    vector_list[0] = vector_list[0].replace(str(i-1), str(i))
                #print(line)
                #if "[" not in vector_list[-1] or line.startswith("END"):
                #    vector_list[-1] = ""
                #elif i == (int(dollarValue) - 1) and :
                #    vector_list[-1] = ""


                #search and replace $$ values in module:
                #for nameOfDollar,valOfDollar in keyword_DOLLARDOLLAR.items():
                #    vector_module = vector_module.replace(nameOfDollar,str(i))
                vector_module += "\n" + '\n'.join(map(str,vector_list))
                if "PIPELINED" and "[" in line:
                    #end of vector module is inserted everytime:
                    buffer = line.replace("[","\t")
                    buffer2 = buffer.replace("]","")
                    vector_module += "\n" + buffer2

                i += 1
            #if "[" in line:
                #end of vector module is only inserted once:
            #    vector_module += "\n" + line

            #print(vector_module)
            #replace loop paramter in vetor module according to is UID:
            for idx, vector_Line in enumerate(vector_module.split("\n")):
                vector_Line_Output = ""
                if "UID" in vector_Line:
                    #print(vector_Line)
                    if not "//" in vector_Line:
                        UID = vector_Line[vector_Line.find("UID")+4:len(vector_Line)]
                    #else:
                    #    UID = vector_Line[vector_Line.find("UID")+4:vector_Line.find("//")]
                    #    print("slse")
                    #print("UID:",UID)
                #print(vector_Line)
                if "[" in vector_Line and vector_Line[vector_Line.find("[")+1:vector_Line.find("]")] == UID:
                    #print("match")
                    vector_Line_Output = vector_Line.replace(vector_Line[vector_Line.find("["):vector_Line.find("]")+1],"\t")
                    #print(vector_Line_Output)
                elif "[" in vector_Line and vector_Line[vector_Line.find("[")+1:vector_Line.find("]")] != UID:
                    print(vector_Line_Output)
                else:
                    vector_Line_Output = vector_Line
                vector_loop_parameter_module += vector_Line_Output + "\n"

            if "[" in vector_module:
                #if there are loop variables in vector module insert vector_loop_parameter_module
                content_newSIM += "\n" + vector_loop_parameter_module + "\n" + line + "\n"
            else:
                #if there are NO loop variables insert vector_module
                content_newSIM += "\n" + vector_module + "\n"

            vector_module = ''
            vector_loop_parameter_module = ''


    #make sure that 2 or more vector modules are not put together:
    if copyVector and not line.startswith(keyword_MODULE_start):
        vector_module += "\n" + line
    #only f if the last pasrt of simFile is not a vecotr module:
    if line.startswith("END"):
        content_newSIM += "\n" + content_string
        #print(content_newSIM)



#FORMAT OUTPUT STRING:
#remove unneccessary parts and format string:
index = content_newSIM.find("MODULE")
new = content_newSIM[index:]
content_newSIM = header + "\n" + new
content_newSIM = "".join([s for s in content_newSIM.splitlines(True) if s.strip("\r\n")])
#write to file:
#generate output name by adding an "_" at the end of the filename:
nameofOutputSim = pathOfSimfile[:pathOfSimfile.find(".")] + "_" + pathOfSimfile[pathOfSimfile.find("."):]
nameofOutputSim = nameofOutputSim.replace("\\\\", "/")
print("Output Simfile path:\n" + nameofOutputSim)

with open(nameofOutputSim, 'w+') as output_simFile:
    output_simFile.truncate()
    output_simFile.write(content_newSIM)

print("\n\nSimfile conversion finished!")
