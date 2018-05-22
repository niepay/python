import re
import io
import os

copyVector            = False    #for copying vector modules
vector_module         = ""
content_string        = ""
content_newSIM        = ""
header                = ""
keyword_MODULE_start  =  "MODULE["
keyword_DOLLAR        = {}      #dictionary for dollar sign + value
dollar                = ""      #temp variable to store dollarname
dollarValue           = 0       #temp value to store dollar value

#write sim-file into string:
with open('C:/Users/nip/Documents/hannes/x.sim', 'rt') as input_simFile:
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
        keyword_DOLLAR[line.split(" ")[0]] = line.split(" ")[1]

# go through simfile with every $variable:

    #go through string line by line and extract vector modules:
for line in content_simFile.split("\n"):

    #if line.startswith(keyword_MODULE_start + nameOfDollar + "]"):
    #    copyVector = True

        #vector_module += line

    if line.startswith("MODULE["):
        copyVector = True
        for nameOfDollar,valOfDollar in keyword_DOLLAR.items():
            if nameOfDollar in line:
                dollar = nameOfDollar
                dollarValue = valOfDollar
            print("inif")
        #if not content_string in content_newSIM:
        content_newSIM += "\n" + content_string
        content_string =''

    if not copyVector:
        content_string += line + "\n"

    if "PIPELINED" in line or\
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
        line.startswith("END"):
            copyVector = False
            i = 0
            vector_module = "".join([s for s in vector_module.splitlines(True) if s.strip("\r\n")])
            vector_list = vector_module.split("\n")
            vector_module =""

            while i < int(dollarValue):
                if i == 0:
                    if "//" in vector_list[0] and "MODULE" in vector_list[0] :
                        vector_list[0] = vector_list[0].replace("//", "IF UID " + str(i) + " //")
                        #print(vector_list)
                    elif "//" not in vector_list[0] and "MODULE" in vector_list[0]:
                        vector_list[0] = vector_list[0] + "\tIF UID " + str(i)
                        #print(vector_list)

                    vector_module += "\n" + "\n".join(vector_list)

                if i != 0:
                    vector_list[0] = vector_list[0].replace(str(i-1), str(i))
                    vector_module += "\n" + "\n".join(vector_list) + "\n"
                i += 1
            print(vector_module)
            #if not vector_module in content_newSIM:
            content_newSIM += "\n" + vector_module
            #else:
            vector_module = ''

    if copyVector:
        vector_module += line + "\n"

#FORMAT OUTPUT STRING
#replace $variables with dedicated value and remove [$...] from module:
for nameOfDollar,valOfDollar in keyword_DOLLAR.items():
    for line in content_newSIM.split("\n"):
        content_newSIM = content_newSIM.replace("["+nameOfDollar+"]","")
        content_newSIM = content_newSIM.replace(nameOfDollar,valOfDollar)

#remove unneccessary parts and format string:
index = content_newSIM.find("MODULE")
new = content_newSIM[index:]
content_newSIM = header + "\n" + new
content_newSIM = "".join([s for s in content_newSIM.splitlines(True) if s.strip("\r\n")])
content_newSIM = content_newSIM + "END"
#write to file
with open('C:/Users/nip/Documents/hannes/x_.sim', 'r+') as output_simFile:
    output_simFile.truncate()
    output_simFile.write(content_newSIM)
