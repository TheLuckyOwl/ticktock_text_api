# this is to detect the name entity of a sentence, the return value [['New York'],[Pittsburgh]]
import nltk
#import fileinput
import json
import urllib
def find_NE(t,name_entity): # only return the first NE found, will ignore the rest
    try:
        t.label()
    except AttributeError:
        print t
        #return None
    else:
        # now we know that t.node is defined
        if t.label() == 'NE':
            print 'this is the NE'
            print [item[0] for item in t]
            name_entity.append( [item[0] for item in t])
        else:
            for child in t:
                find_NE(child,name_entity)
    return name_entity
def name_entity_detection(user_input):
        sent_postag = nltk.pos_tag(nltk.word_tokenize(user_input))
        sent_tree = nltk.ne_chunk(sent_postag,binary=True)
        print sent_tree
        ne = find_NE(sent_tree,[])
        return ne

def NE_disp(name_entity_list):
    api_key = 'AIzaSyA_MGutOdKJTwhq0iVn7TBPfOYJbrDcfG8'
    response_disp_list =[]
    for item in name_entity_list:
	#query = 'Football'
	query = item
        print query
	service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
	params = {
    	'query': query,
    	'limit': 10,
    	'indent': True,
    	'key': api_key,
	}
	url = service_url + '?' + urllib.urlencode(params)
	response = json.loads(urllib.urlopen(url).read())
	print response
	disp = response['itemListElement'][0]['result']['description']
        response_disp_list.append(disp)
        print response['itemListElement'][0]['result']['detailedDescription']['articleBody']
    return response_disp_list
#
def name_entity_generation(response_disp_list):
    # we only talk about the first entity, /we can try random as well
    select_item = response_disp_list[0]
    output = 'Are you talking about '+select_item
    return output

