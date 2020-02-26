from prettytable import PrettyTable
from datetime import datetime,date
import pickle
import re

x= PrettyTable()
y= PrettyTable()
lines=[]
outputlines=[]
with open('Family-2-21-Feb-2020-525.ged') as line:
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
#Splitting all the individual records 
for i in validlinesstring.split("INDI"):
    validpeople.append(i)
#Getting  all the family records 
families=validpeople[-1].split("0|FAM")[1:]
validpeople[-1]=validpeople[-1].split("0|FAM")[0]
#Getting and fetching all the details in Individuals Table
x.field_names = ["ID", "Name", "Gender", "Birthday","Alive","Age","Death","Child","Spouse"]
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

#Getting and Fetching all the details in Families Table
y.field_names = ["ID", "Married", "Divorced", 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children']
person1 = ['N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A']

for i in range(0, len(families)):
    member = families[i].split("\n") 
    c = set()
    person1 = ['N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A'] 
    for j in range(0,len(member)): 
        mb = member[j].split('|')
        if '' == mb[0]: #Getting all the ids 
            last = mb[-1].replace('@','') 
            person1[0] = last
        elif 'HUSB' in mb: #Getting all the Huband IDS and their respected name
            last = mb[-1].replace('@','')
            person1[3] = last
            for row in x:
                row.border = False
                row.header = False
                if (row.get_string(fields=["ID"]).strip()) == last:
                    person1[4]=(row.get_string(fields=["Name"]).strip())
        elif 'WIFE' in mb: #Getting all the Huband IDS and their respected name
            last = mb[-1].replace('@','')
            person1[5] = last
            for row in x:
                row.border = False
                row.header = False
                if (row.get_string(fields=["ID"]).strip()) == last:
                    person1[6]=(row.get_string(fields=["Name"]).strip())
        elif 'CHIL' in mb: #Getting all the Children IDS and storing it in variable of type set
            last = mb[-1].replace('@','')
            c.add(last)
            person1[7] = c
        elif 'DIV' in mb: #Getting information about divorce details
            person1[2] = member[j+1].split('|')[-1]
        elif 'MARR' in mb: #Getting information about Marriage details
            person1[1] = member[j+1].split('|')[-1]
    y.add_row(person1)

print ("Individuals")
print (x)
print ("Families")
print (y)

#___________________________________________________________________________________________________________

def StoryIDUS23():
    names=[]
    dob=[]
    id=[]

    for row in x:
        row.border = False
        row.header = False
        names.append(row.get_string(fields=["Name"]).strip().replace('/',''))
        dob.append(datetime.strptime((row.get_string(fields=["Birthday"]).strip()), '%d %b %Y'))
        id.append(row.get_string(fields=["ID"]).strip().replace('/',''))
    warning=0
    error=0
    for i in range(0,len(names)):
        for j in range(i+1, len(names)):
            if(names[i]==names[j]):
                if(dob[i]==dob[j]):
                    return (f"Error : Might be the same {id[i]}:{names[i]} and {id[j]}:{names[j]}")
                    error=error+1

                else:
                    return (f"Warning : Might be the same {id[i]}:{names[i]} and {id[j]}:{names[j]} ")
                    warning=warning+1

    if warning==0 and error==0:
        return ("No errors found")




def StoryIDUS25():
    family={}
    for row in y:
        row.border = False
        row.header = False
        fam=[]
        fam.append(row.get_string(fields=["Husband Name"]).strip().replace('/','').split(" ")[0])
        fam.append(row.get_string(fields=["Wife Name"]).strip().replace('/','').split(" ")[0])
        id=(row.get_string(fields=["ID"]).strip().replace('/',''))
        fam.append(row.get_string(fields=["Children"]).strip().replace('/',''))
        family[id]=fam

    for i in family:
        childern= family[i][-1]
        patterns= r'\w+'
        if childern != 'N/A':
            match= re.findall(patterns, childern)
            child=[]
            if (match[0]!='NA'):
                for j in range(0,len(match)):
                    for row in x:
                        row.border = False
                        row.header = False
                        if (row.get_string(fields=["ID"]).strip()) == match[j]:
                            child.append(row.get_string(fields=["Name"]).strip().replace('/','').split(" ")[0])
                        
            family[i].pop()
            family[i]=family[i]+child
    error=0
    for i in family:
        uniquefamily=list(set(family[i]))
        if(len(family[i])!=len(uniquefamily)):
            error=1
            return(f"Error: family Id {i} has duplicate names")
    if(error==0):
        return ("No error detected.")


#___________________________________________________________________________________________________




#_________tushr's storis_________________________________________________________________________________________________________________

def StoryIDUS01():
    dates=[]
    errors=[]
    for row in x:
        row.border = False
        row.header = False
        dates.append(datetime.strptime((row.get_string(fields=["Birthday"]).strip()), '%d %b %Y'))
        if((row.get_string(fields=["Death"]).strip()=='N/A')==False):
            dates.append(datetime.strptime((row.get_string(fields=["Death"]).strip()), '%d %b %Y'))
    for row in y:
        row.border = False
        row.header = False
        dates.append(datetime.strptime((row.get_string(fields=["Married"]).strip()), '%d %b %Y'))
        if((row.get_string(fields=["Divorced"]).strip()=='N/A')==False):
            dates.append(datetime.strptime((row.get_string(fields=["Divorced"]).strip()), '%d %b %Y'))

     
    for i in dates:
        if(datetime.date(i) > date.today()):
            errors.append(i)

    
    return errors

StoryIDUS01()

def StoryIDUS02():
    errors=[]
    for row in y:
        row.border = False
        row.header = False
        married=(datetime.strptime((row.get_string(fields=["Married"]).strip()), '%d %b %Y'))
        Husband = (row.get_string(fields=["Husband ID"]).strip())
        Wife = (row.get_string(fields=["Wife ID"]).strip())
        for row1 in x:
            row1.border = False
            row1.header = False
            if row1.get_string(fields=["ID"]).strip() == Husband:
                husbanddate=(datetime.strptime((row1.get_string(fields=["Birthday"]).strip()), '%d %b %Y'))
                if(husbanddate>married):
                    errors.append(Husband)
            if row1.get_string(fields=["ID"]).strip() == Wife:
                wifebdate=(datetime.strptime((row1.get_string(fields=["Birthday"]).strip()), '%d %b %Y'))
                if(wifebdate>married):
                    errors.append(Wife)

    
#_______________________________________________________________________________________________________________________________________

def StoryIDUS30():
    livingMarried = PrettyTable()
    livingMarried.field_names = ['Husband ID', 'Husband Name', 'Wife ID', 'Wife Name']
    for row in y:
        marriedPeople = []
        row.border = False
        row.header = False
        if (row.get_string(fields=["Married"]).strip()) != 'N/A' and (row.get_string(fields=["Divorced"]).strip()) == 'N/A':
            Hid = (row.get_string(fields=["Husband ID"]).strip())
            Wid = (row.get_string(fields=["Wife ID"]).strip())
            flag=0
            for row1 in x:
                row1.border = False
                row1.header = False
                if (row1.get_string(fields=["Alive"]).strip()) == 'False':
                    if (row1.get_string(fields=["ID"]).strip()) == Hid or (row1.get_string(fields=["ID"]).strip()) == Wid:
                        flag=1
            if flag == 0:
                marriedPeople.append((row.get_string(fields=["Husband ID"]).strip()))
                marriedPeople.append((row.get_string(fields=["Husband Name"]).strip()))
                marriedPeople.append((row.get_string(fields=["Wife ID"]).strip()))
                marriedPeople.append((row.get_string(fields=["Wife Name"]).strip()))
                livingMarried.add_row(marriedPeople)

    #print ('List of Living Married is -->')
    #print (livingMarried)
    return (livingMarried)





def StoryIDUS31():
    livingSingle = PrettyTable()
    livingSingle.field_names = ['ID','Name']
    
    for row in x:
        row.border = False
        row.header = False
        havingNoValentine = []
        if (row.get_string(fields=["Spouse"]).strip()) == 'N/A':
            havingNoValentine.append(row.get_string(fields=["ID"]).strip())
            havingNoValentine.append(row.get_string(fields=["Name"]).strip())
            livingSingle.add_row(havingNoValentine)
    
    #print ('List of Living Single is -->')
    #print (livingSingle)
    return livingSingle
    


#_____________Prateek's code__________________________________________________________________________________________________________