import logging
import re
from nltk.corpus import stopwords
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#from gensim import corpora,models, similarities
def oov_out(user_input, dictionary_value):
	print user_input
	#documents=[]
	#with open('documents.txt') as f:
	#	for line in f:
	#		documents.append(line)
	stoplist = stopwords.words('english')
	#texts =[[word for word in document.lower().split() if word not in stoplist] for document in documents]
	#dictionary = corpora.Dictionary.load('/tmp/deerwester.dic')
	#dictionary_value = dictionary.values()
	#dictionary.save('ticktock_v2.dict')
	#print type(dictionary)
	#print dictionary
	#new_vec = dictionary.doc2bow(user_input.lower().split())
	#print "we are pring the new vec"
	#print(new_vec)
	user_input = re.sub('[?.,()!:]','', user_input)
	user_input = [ word for word in user_input.lower().split() if word not in stoplist]
	for word in user_input:
		if word not in dictionary_value:
			is_triggered =1
			output = 'what is '+word +'?'
			return is_triggered, output
		
	return 0, None

