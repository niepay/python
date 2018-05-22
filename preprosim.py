import re
import codecs
import string

#declaration of variables:
lines = []
l = 0
COUNT_MODULE = 0
copyline = False
keyword_MODULE_start =  ("MODULE[$n]")
#keyword_MODULE_end =    ("PIPELINED")
string_find = ("$")

#opnes sim-file and looks for multivector content:
with open('C:/Users/nip/Documents/hannes/x.sim', 'rt')  as input_simFile:
    for line in input_simFile:
        #extract the vectormodule number:


        if any(s in line for s in string_find):
            str(line)
            for t in line.split():
                try:
                    l = int(t)
                except ValueError:
                    pass


        if all(s in line for s in keyword_MODULE_start):
            copyline = True
            COUNT_MODULE += 1


        if line == "END" or         \
           line.find("PIPELINED")  or   \
           line == "MODULE" or      \
           line == "TESTPOINT" or   \
           line == "LABEL" or       \
           line == "BRANCH" or      \
           line == "STATIC_PIPE" or \
           line == "NEWSIMU" or     \
           line == "PAR_START" or   \
           line == "PAR_END" or     \
           line == "REMOTE_START" or\
           line == "REMOTE_END":
            copyline = False

            #format string:
            string_lines= ''.join(lines)
            codecs.decode(string_lines, 'unicode_escape')
            #save string to new file with chosen number of modules:
            with open('C:/Users/nip/Documents/hannes/x_.sim', 'r+') as output_simFile:
                output_simFile.truncate()

                # replace $n with correct number:
                for i in range(1,l+1):
                    if i == 1:
                        string_lines = string_lines.replace("$n",str(i))
                    if i != 1:
                        string_lines = string_lines.replace(str(i-1) ,str(i),1)
                    output_simFile.write(string_lines)
                    output_simFile.write('\n')

        if copyline:
            lines.append(line)
"""
#format string:
string_lines= ''.join(lines)
codecs.decode(string_lines, 'unicode_escape')
#save string to new file with chosen number of modules:
with open('C:/Users/nip/Documents/hannes/x_.sim', 'r+') as output_simFile:
    output_simFile.truncate()
    for i in range(1,l+1):
        if i == 1:
            string_lines = string_lines.replace("$n",str(i))
        if i != 1:
            string_lines = string_lines.replace(str(i-1) ,str(i),1)
        output_simFile.write(string_lines)
        output_simFile.write('\n')
"""
