import pickle as pkl
data = pkl.load(open('superhero_db.pickle'))
data_2 ={}
for key in data.keys():
    key_2 = key.lower().replace(" ",'').replace('-', '')
    if key =='Thing':
        continue
    data_2[key_2] = data[key]
    data_2[key_2]['Name'] = key
print data_2
pkl.dump(data_2,open('superhero_db_lower.pickle','w'))
