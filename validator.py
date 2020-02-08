from prettytable import PrettyTable
from datetime import datetime,date
import pickle

x= PrettyTable()
y= PrettyTable()
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

x.field_names = ["ID", "Name", "Gender", "Birthday","Alive","Age","Death","Child","Spouse"]
a = set()
b = set()
person=['N/A','N/A','N/A','N/A',True,'N/A','N/A','N/A','N/A']

for i in range(1, len(validpeople)):
    individual=validpeople[i].split("\n")
    a = set()
    b = set()
    person=['N/A','N/A','N/A','N/A',True,'N/A','N/A','N/A','N/A']
    for j in range(0,len(individual)):
        
        if individual[j].split("|")[0]=='':
            person[0]=((individual[j].split("|")[-1]).replace('@',''))
        elif len(individual[j].split("|")) >1 and individual[j].split("|")[1]=='NAME':
            person[1]=(individual[j].split("|")[-1])
        elif len(individual[j].split("|")) >1 and individual[j].split("|")[1]=='SEX':
            person[2]=(individual[j].split("|")[-1])
        elif len(individual[j].split("|")) >1 and individual[j].split("|")[1]=='BIRT':
            person[3]=(individual[j+1].split("|")[-1])
            born = datetime.strptime((individual[j+1].split("|")[-1]), '%d %b %Y')
            today=date.today()
            person[5]=(today.year - born.year - ((today.month, today.day) < (born.month, born.day)))
        elif len(individual[j].split("|")) >1 and individual[j].split("|")[1]=='DEAT':
            person[4]=False
            person[6]=(individual[j+1].split("|")[-1])
            death=datetime.strptime((individual[j+1].split("|")[-1]), '%d %b %Y')
            person[5]=(death.year - born.year - ((death.month, death.day) < (born.month, born.day)))
        elif len(individual[j].split("|")) >1 and individual[j].split("|")[1]=='FAMS':
            b.add((individual[j].split("|")[-1]).replace('@',''))
            person[8]=b
        elif len(individual[j].split("|")) >1 and individual[j].split("|")[1]=='FAMC':
            a.add((individual[j].split("|")[-1]).replace('@',''))
            person[7]=a
        
    x.add_row(person)

y.field_names = ["ID", "Married", "Divorced", 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children']
c = set()
person1 = ['N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A']

for i in range(0, len(families)):
    member = families[i].split("\n")
    c = set()
    person1 = ['N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A']
    for j in member: 
        mb = j.split('|')
        if '' == mb[0]:
            last = mb[-1].replace('@','')
            person1[0] = last
        elif 'HUSB' in mb:
            last = mb[-1].replace('@','')
            person1[3] = last
            for row in x:
                row.border = False
                row.header = False
                if (row.get_string(fields=["ID"]).strip()) == last:
                    person1[4]=(row.get_string(fields=["Name"]).strip())
        elif 'WIFE' in mb:
            last = mb[-1].replace('@','')
            person1[5] = last
            for row in x:
                row.border = False
                row.header = False
                if (row.get_string(fields=["ID"]).strip()) == last:
                    person1[6]=(row.get_string(fields=["Name"]).strip())
        elif 'CHIL' in mb:
            last = mb[-1].replace('@','')
            c.add(last)
            person1[7] = c
        elif 'DIV' in mb:
            person1[2] = 'Y'
        elif 'MARR' in mb:
            person1[1] = 'Y'
    y.add_row(person1)

print ("Individuals")
print (x)
print ("Families")
print (y)


    
