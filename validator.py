from prettytable import PrettyTable
from datetime import datetime,date
import pickle

x= PrettyTable()
lines=[]
outputlines=[]
with open('Family-2-7-Feb-2020-544.ged') as line:
    lines=line.read().splitlines()

tagdictionary={
    "INDI":"0",
    "NAME":"1",
    "SEX":"1",
    "BIRT":"1",
    "DEAT":"1",
    "FAMC":"1",
    "FAMS":"1",
    "FAM":"0",
    "MARR":"1",
    "HUSB":"1",
    "WIFE":"1",
    "CHIL":"1",
    "DIV":"1",
    "DATE":"2",
    "HEAD":"0",
    "TRLR":"0",
    "NOTE":"0"

}
for i in lines:
    outputlines.append("--> "+i)
    word=i.split(" ")

    if(word[1] in tagdictionary.keys()):
        if(int(word[0])==int(tagdictionary[word[1]]) and word[1] not in ["INDI","FAM"]):
            if(len(word)>2):
                outputlines.append("<-- "+word[0]+"|"+word[1]+"|"+"Y"+"|"+" ".join(word[2:]))
            else:
                outputlines.append("<-- "+word[0]+"|"+word[1]+"|"+"Y"+"|")
        else:
            if(len(word)>2):
                outputlines.append("<-- "+word[0]+"|"+word[1]+"|"+"N"+"|"+" ".join(word[2:]))
            else:
                outputlines.append("<-- "+word[0]+"|"+word[1]+"|"+"N"+"|")
    elif( len(word)>2 and (word[2] in tagdictionary.keys()) ):
        if(int(word[0])==int(tagdictionary[word[2]])):
            outputlines.append("<-- "+word[0]+"|"+word[2]+"|"+"Y"+"|"+word[1])
        else:
            outputlines.append("<-- "+word[0]+"|"+word[2]+"|"+"N"+"|"+word[1])
    else:
        if(len(word)>2):
            outputlines.append("<-- "+word[0]+"|"+word[1]+"|"+"N"+"|"+" ".join(word[2:]))
        else:
            outputlines.append("<-- "+word[0]+"|"+word[1]+"|"+"N"+"|")
validlines=[]
for i in outputlines:
    if ('Y' in i.split("|")):
        validlines.append(i)

validlinesstring="\n".join(validlines)
validpeople=[]

for i in validlinesstring.split("INDI"):
    validpeople.append(i)

families=validpeople[-1].split("0|FAM")[1:]
validpeople[-1]=validpeople[-1].split("0|FAM")[0]

x.field_names = ["ID", "Name", "Gender", "Birthday","Alive","Death","Child","Spouse"]
person=['N/A','N/A','N/A','N/A',False,'N/A',[],[]]


for i in range(1, len(validpeople)):
    individual=validpeople[i].split("\n")
    person=['N/A','N/A','N/A','N/A',False,'N/A',[],[]]
    for j in range(0,len(individual)):
        
        if individual[j].split("|")[0]=='':
            person[0]=((individual[j].split("|")[-1]).replace('@',''))
        elif len(individual[j].split("|")) >1 and individual[j].split("|")[1]=='NAME':
            person[1]=(individual[j].split("|")[-1])
        elif len(individual[j].split("|")) >1 and individual[j].split("|")[1]=='SEX':
            person[2]=(individual[j].split("|")[-1])
        elif len(individual[j].split("|")) >1 and individual[j].split("|")[1]=='BIRT':
            # person.append(today.year - born.year - ((today.month, today.day) < (born.month, born.day)))
            person[3]=(individual[j+1].split("|")[-1])
        elif len(individual[j].split("|")) >1 and individual[j].split("|")[1]=='DEAT':
            person[4]=True
            person[5]=(individual[j+1].split("|")[-1])
        elif len(individual[j].split("|")) >1 and individual[j].split("|")[1]=='FAMS':
            person[7].append((individual[j].split("|")[-1]).replace('@',''))
        elif len(individual[j].split("|")) >1 and individual[j].split("|")[1]=='FAMC':
            person[6].append((individual[j].split("|")[-1]).replace('@',''))
        
    x.add_row(person)

y=pickle.dump( x, open( "x.p", "wb" ) )

# for i in families:
#     print (i)   

# person=[]

# for i in range(len(validlines)):
#     if 'INDI' in validlines[i]:
#         person.append(validlines[i].split("|")[-1])
#         person.append(validlines[i+1].split("|")[-1])
#         person.append(validlines[i+2].split("|")[-1])
#         person.append(validlines[i+4].split("|")[-1])
#         print(person)
#         person=[]


    
