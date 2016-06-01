import pickle as pkl
def name(user_input):
    database = pkl.load(open('superhero_db_lower.pickle'))
    input_plain = user_input.lower().replace(" ","").replace('-','')
    for key in database.keys():
        if key in input_plain:
            eyecolor = database[key]['Eyes']
            output = 'I love ' + database[key]['Name'] +"'s "+ eyecolor.lower() +' eyes.'
            return output
    if 'batman' in input_plain:
        output = 'I love his black eyes.'
        return output
    if 'superman' in input_plain:
        output = 'I love his blue eyes.'
        return output

    return None
