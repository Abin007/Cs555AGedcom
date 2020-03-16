from prettytable import PrettyTable
from datetime import datetime,date,timedelta
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
#User story 23 - No more than one individual with the same name and birth date should appear in a GEDCOM file
def StoryIDUS23():
    names=[]
    dob=[]
    id=[]

    for row in x:
        row.border = False
        row.header = False
        names.append(row.get_string(fields=["Name"]).strip().replace('/',''))
        if (row.get_string(fields=["Birthday"]).strip()) != 'N/A':
            dob.append(datetime.strptime((row.get_string(fields=["Birthday"]).strip()), '%d %b %Y'))
        else:
            dob.append('N/A')
        id.append(row.get_string(fields=["ID"]).strip().replace('/',''))
    error=[]
    for i in range(0,len(names)):
        for j in range(i+1, len(names)):
            if(names[i]==names[j]):
                if(dob[i]==dob[j]):
                    error.append(f"US23 - Error : Individual {id[i]} and {id[j]} Might be the same")
                else:
                    error.append(f"US23 - Error : Individual {id[i]} and {id[j]} Might be the same")
                    

            elif(names[i]!=names[j]):
                if(dob[i]==dob[j]):
                    error.append(f"US23 - Error : Individual {id[i]} and {id[j]} Might be the same")
                    

    if len(error)!=0:
        return (error)
    else:
        return ("US23 - No errors found")

print(StoryIDUS23())
    


#User story 25 - No more than one child with the same name and birth date should appear in a family

def StoryIDUS25():
    family={}
    errors=[]
    for row in y:
        row.border = False
        row.header = False
        fam=[]
        id=(row.get_string(fields=["ID"]).strip().replace('/',''))
        fam.append(row.get_string(fields=["Children"]).strip().replace('/',''))
        family[id]=fam

    for i in family:
        childern= family[i][0]
        patterns= r'\w+'
        if childern != 'N/A':
            match= re.findall(patterns, childern)
            child=[]
            dob=[]
            if (match[0]!='NA'):
                for j in range(0,len(match)):
                    for row in x:
                        row.border = False
                        row.header = False
                        if (row.get_string(fields=["ID"]).strip()) == match[j]:
                            child.append(row.get_string(fields=["Name"]).strip().replace('/','').split(" ")[0].lower())
                            dob.append(datetime.strptime((row.get_string(fields=["Birthday"]).strip()), '%d %b %Y'))
                        
            # family[i].pop()
            # family[i]=family[i]+child
            
            for k in range(0,len(child)):
                for j in range(k+1, len(child)):
                    if(child[k]==child[j]):
                        if(dob[k]==dob[j]):
                            # errors.append(match[k])
                            # errors.append(match[j])
                            indi=[]
                            indi.append(match[k])
                            indi.append(match[j])
                            indi.sort()
                            strindi=" ".join(indi)

                            errors.append(f"US25 - Error : Individual {strindi} might be the same  in Family {i}")
                            
                    #     else:
                    #         errors.append(f"US Story US25 - Warning : Might be the same {match[k]} and {match[j]} in Family {i}")

                    

                    # elif(child[k]!=child[j]):
                    #     if(dob[k]==dob[j]):
                    #         errors.append(f"US Story US25 - Warning : Might be the same {match[k]} and {match[j]} in Family {i}")
            

    # error=0
    # print(family)
    # for i in family:
    #     uniquefamily=list(set(family[i]))
    #     if(len(family[i])!=len(uniquefamily)):
    #         error=1
    #         return(f"Error: family Id {i} has duplicate names")
    if(len(errors)==0):
        return ("US25 - No error detected.")
    else:
        return (sorted(errors))

print(StoryIDUS25())

#US-16 - Male last names

def StoryIDUS16():
    family={}
    errors=[]
    for row in y:
        row.border = False
        row.header = False
        fam=[]
        id=(row.get_string(fields=["ID"]).strip().replace('/',''))
        fam.append(row.get_string(fields=["Husband Name"]).strip().replace('/','').split(" ")[-1].lower())
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
                        if ((row.get_string(fields=["ID"]).strip()) == match[j]) and (row.get_string(fields=["Gender"]).strip()) == 'M' :
                            child.append(row.get_string(fields=["Name"]).strip().replace('/','').split(" ")[-1].lower())

                        
            family[i].pop()
            family[i]=family[i]+child
    for i in family:
        if(len(family[i])>1):
            if(len(list(set(family[i])))==len(family[i])):
                errors.append(f"US16 - Error : Family {i} has male members with different last names")
    
    if(len(errors)>0):
        return sorted(errors)
    else:
        return "US16 - No Family has male members with different last names"



print(StoryIDUS16())
#US-17 - Parents married to their children
def StoryIDUS17():
    family={}
    errors=[]
    for row in y:
        row.border = False
        row.header = False
        fam=[]
        id=(row.get_string(fields=["ID"]).strip().replace('/',''))
        fam.append(row.get_string(fields=["Husband ID"]).strip().replace('/','').split(" ")[0])
        fam.append(row.get_string(fields=["Wife ID"]).strip().replace('/','').split(" ")[0])
        fam.append(row.get_string(fields=["Children"]).strip().replace('/',''))
        family[id]=fam
    
    for i in family:
        childern= family[i][-1]
        patterns= r'\w+'
        if childern != 'N/A':
            match= re.findall(patterns, childern)
            family[i].pop()
            family[i].append(match)
        if (family[i][0] in family[i][-1]) or (family[i][1] in family[i][-1]):
            errors.append(f"US17 - Error : In Family {i} has parents who are married to their children ")
    if errors:
        return errors
    else:
        return "US17 - No Parents are married to their children"
            
    
print(StoryIDUS17())

def StoryIDUS15():
    family={}
    errors=[]
    for row in y:
        row.border = False
        row.header = False
        fam=[]
        id=(row.get_string(fields=["ID"]).strip().replace('/',''))
        fam.append(row.get_string(fields=["Children"]).strip().replace('/',''))
        family[id]=fam
    for i in family:
        childern= family[i][-1]
        patterns= r'\w+'
        if childern != 'N/A':
            match= re.findall(patterns, childern)
          #  child=[]
            if (match[0]!='NA'):
                if(len(match)>15):
                    errors.append(f"US15 - Family {i} has more than 15 siblings")
    return errors

def StoryIDUS21():
    family={}
    errors=[]
    for row in y:
        row.border = False
        row.header = False
        fam=[]
        id=(row.get_string(fields=["ID"]).strip().replace('/',''))
        fam.append(row.get_string(fields=["Husband ID"]).strip().replace('/','').split(" ")[0])
        fam.append(row.get_string(fields=["Wife ID"]).strip().replace('/','').split(" ")[0])
        family[id]=fam
    for i in family:
        for row in x:
            row.border = False
            row.header = False
            
            if ((row.get_string(fields=["ID"]).strip()) == family[i][0]) and (row.get_string(fields=["Gender"]).strip()) != 'M' :
                errors.append(f"US21 - Error : In Family {i} have parents of wrong gender")
            elif ((row.get_string(fields=["ID"]).strip()) == family[i][1]) and (row.get_string(fields=["Gender"]).strip()) != 'F':
                errors.append(f"US21 - Error : In Family {i} have parents of wrong gender")
    return list(set(errors))

def StoryIDUS22():
    familyid=[]
    indiid=[]
    errors=[]
    for row in y:
        row.border = False
        row.header = False
        familyid.append(row.get_string(fields=["ID"]).strip().replace('/',''))
    for row in x:
        row.border = False
        row.header = False
        indiid.append(row.get_string(fields=["ID"]).strip().replace('/',''))
    if(len(list(set(familyid)))!=len(familyid)):
        errors.append("US22 - Error : Family IDs is not Unique") 
    if(len(list(set(indiid)))!=len(indiid)):
        errors.append("US22 - Error : Individual IDs is not Unique")
    if errors:
        return errors
    else:
        return "US22 - No errors found"
print(StoryIDUS22())
#___________________________________________________________________________________________________
# print(StoryIDUS22())

def StoryIDUS27():
    error=[]
    for row in x:
        row.border = False
        row.header = False
        id=(row.get_string(fields=["ID"]).strip().replace('/',''))
        if(row.get_string(fields=["Age"]).strip()=='N/A'):
            error.append(id)
    error=sorted(error)
    if error:
        return f"US27 - Error : Individual {error} has no ages displayed"
    else:
        return "US27 - No errors found"

print(StoryIDUS27())

# print(StoryIDUS27())

#_________Tushar's storis_________________________________________________________________________________________________________________

def StoryIDUS01():
    dates=[]
    errors=[]
    for row in x:
        row.border = False
        row.header = False
        if((row.get_string(fields=["Birthday"]).strip()=='N/A')==False):
            birthstr=row.get_string(fields=["Birthday"]).strip()
            birth=(datetime.strptime((row.get_string(fields=["Birthday"]).strip()), '%d %b %Y'))
            if(datetime.date(birth) > date.today()):
                id=(row.get_string(fields=["ID"]).strip().replace('/',''))
                errors.append(f"US01 - Error : Individual - {id} Birthday {birthstr} occurs in the future")

        if((row.get_string(fields=["Death"]).strip()=='N/A')==False):
            birthstr=row.get_string(fields=["Death"]).strip()
            birth=(datetime.strptime((row.get_string(fields=["Death"]).strip()), '%d %b %Y'))
            if(datetime.date(birth) > date.today()):
                id=(row.get_string(fields=["ID"]).strip().replace('/',''))
                errors.append(f"US01 - Error : Individual - {id} Death {birthstr} occurs in the future")
    for row in y:
        row.border = False
        row.header = False
        if((row.get_string(fields=["Married"]).strip()=='N/A')==False):
            marriedstr=row.get_string(fields=["Married"]).strip()
            married=(datetime.strptime((row.get_string(fields=["Married"]).strip()), '%d %b %Y'))
            if(datetime.date(married) > date.today()):
                id=(row.get_string(fields=["ID"]).strip().replace('/',''))
                errors.append(f"US01 - Error : Family ID - {id} Married {marriedstr} occurs in the future")
        if((row.get_string(fields=["Divorced"]).strip()=='N/A')==False):
            deathstr=row.get_string(fields=["Divorced"]).strip()
            death=(datetime.strptime((row.get_string(fields=["Divorced"]).strip()), '%d %b %Y'))
            if(datetime.date(death) > date.today()):
                id=(row.get_string(fields=["ID"]).strip().replace('/',''))
                errors.append(f"US01 - Error : Family ID - {id} Divorced {deathstr} occurs in the future")

     
    for i in dates:
        if(datetime.date(i) > date.today()):
            errors.append(i)

    
    return errors


print(StoryIDUS01())

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
                if (row1.get_string(fields=["Birthday"]).strip())!='N/A':
                    husbanddate=(datetime.strptime((row1.get_string(fields=["Birthday"]).strip()), '%d %b %Y'))
                if(husbanddate>married):
                    errors.append(f"US02 - Error : individual {Husband} birthdate {husbanddate} occurs after marriage {married}")
            if row1.get_string(fields=["ID"]).strip() == Wife:
                if (row1.get_string(fields=["Birthday"]).strip())!='N/A':
                    wifebdate=(datetime.strptime((row1.get_string(fields=["Birthday"]).strip()), '%d %b %Y'))
                if(wifebdate>married):
                    errors.append(f"US02 - Error : individual {Wife} birthdate-{wifebdate} occurs after marriage {married}")
    return errors


print(StoryIDUS02())
  
def StoryIDUS03():
    errors=[]
    for row1 in x:
            row1.border = False
            row1.header = False
            id=(row1.get_string(fields = ["ID"]).strip().replace('/',''))
            if((row1.get_string(fields = ["Birthday"]).strip()) != 'N/A'):
                birthdays = (datetime.strptime((row1.get_string(fields = ["Birthday"]).strip()), '%d %b %Y'))
                if((row1.get_string(fields = ["Death"]).strip()) != 'N/A'):
                    death = (datetime.strptime((row1.get_string(fields = ["Death"]).strip()), '%d %b %Y'))
                    if(datetime.date(birthdays)>datetime.date(death) or datetime.date(birthdays) > date.today()):
                        errors.append(id)
    if(len(errors) != 0):
        # errors = sorted(errors)
        return errors
    else:
        return " US03 - No errors found "
print(StoryIDUS03())

def StoryIDUS04():
    errors=[]
    for row1 in y:
        row1.border = False
        row1.header = False
        id = (row1.get_string(fields = ["ID"]).strip().replace('/',''))
        if((row1.get_string(fields = ["Married"]).strip()) != 'N/A'):
            married = (datetime.strptime((row1.get_string(fields = ["Married"]).strip()), '%d %b %Y'))
            if((row1.get_string(fields = ["Divorced"]).strip()) != 'N/A'):
                divorce = (datetime.strptime((row1.get_string(fields = ["Divorced"]).strip()), '%d %b %Y'))
                if(datetime.date(married) > datetime.date(divorce)):
                        errors.append(f"US04 - Error : Family - {id} have been married after divorce")
    if(len(errors) != 0):
        errors = sorted(errors)

        return f" US04 - Error : Family - {errors} have been divorced before marriage "
    else:
        return " US04 - No errors found "
print(StoryIDUS04())
#___________________________________________________________________________________________________________________________________________


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

    return (livingMarried)

print ('US30 - List of Living Married is -->')
print(StoryIDUS30())

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
    
    return livingSingle

print ('US31 - List of Living Single is -->')
print(StoryIDUS31())

def StoryIDUS35():
    pastDate = (date.today()-timedelta(days=30)).isoformat()
    recentBirths=[]
    for row in x:
        row.border = False
        row.header = False
        if((row.get_string(fields=["Birthday"]).strip()=='N/A')==False):
            birthstr=row.get_string(fields=["Birthday"]).strip()
            birth=(datetime.strptime((row.get_string(fields=["Birthday"]).strip()), '%d %b %Y'))
            if(str(datetime.date(birth)) >= pastDate and datetime.date(birth) < date.today()):
                id=(row.get_string(fields=["ID"]).strip().replace('/',''))
                recentBirths.append(f"US35 - Error : Individual - {id} Birthday {birthstr} is born recently")
    
    if recentBirths:
        return(recentBirths)
    else:
        return('[ US35 - There are no recent births ]')

print(StoryIDUS35())

def StoryIDUS36():
    pastDate = (date.today()-timedelta(days=30)).isoformat()
    recentDeaths=[]
    for row in x:
        row.border = False
        row.header = False
        if((row.get_string(fields=["Death"]).strip()=='N/A')==False):
            deathstr=row.get_string(fields=["Death"]).strip()
            death=(datetime.strptime((row.get_string(fields=["Death"]).strip()), '%d %b %Y'))
            if(str(datetime.date(death)) >= pastDate and datetime.date(death) < date.today()):
                id=(row.get_string(fields=["ID"]).strip().replace('/',''))
                recentDeaths.append(f"US36 - Error : Individual - {id} Birthday {deathstr} died recently")
    
    if recentDeaths:
        return(recentDeaths)
    else:
        return('[ US36 - There are no recent deaths ]')

print(StoryIDUS36())


#_____________Prateek's code_______________________________________________________________________________________________________________________
