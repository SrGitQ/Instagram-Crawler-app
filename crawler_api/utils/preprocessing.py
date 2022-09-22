import json
#cast json to dic 
def dictonary(file):
    doc = open(file)
    data = json.load(doc)
    
    return data

#Change the data type 
def changeDataType(data):

    Noposts = data['NoPosts']
    Noposts = Noposts.split(' ')
    data['No Posts'] = int(Noposts[0])

    followers = data['Followers']
    followers = followers.split(' ')
    if data['Followers'].find(','):
        followers = followers[0].split(',')
        data['Followers'] = int(''.join(map(str,followers)))
    else: 
        data['Followers'] = int(followers[0])

    Following = data['Following']
    Following = Following.split(' ')
    if data['Following'].find(','):
        Following = Following[0].split(',')
        data['Following'] = int(''.join(map(str,Following)))
    else: 
        data['Following'] = int(Following[0])
    
    return data

def preprocess(data):
    data["NoPosts"] = normalizeGreatCant(data["NoPosts"].replace(" posts", ""))
    data["Followers"] = normalizeGreatCant(data["Followers"].replace(" followers", ""))
    data["Following"] = normalizeGreatCant(data["Following"].replace(" following", ""))
    return data
  
def normalizeGreatCant(str_nm):
  if 'K' in str_nm or 'K' in str_nm:
    base = 1000
  elif 'M' in str_nm or 'M' in str_nm:
    base = 1000000
  else:
    base = 1
  return int(float(str_nm.replace(',','').replace('K', '').replace('M', '')) * base)