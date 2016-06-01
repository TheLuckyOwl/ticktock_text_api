from depth_rater_features import get_convolist, create_learnable
from numpy import corrcoef


feature_list, label_list = create_learnable(get_convolist())

category_list = ['response len', 'switch count', 'continue count', 'end count']

keywords = ['sense', 'something', 'when', 'where', 'why']
category_list = category_list + map(lambda x : '\'' + x + '\'' + " count", keywords)
category_list += map(lambda x : 'magic index ' + str(x), [0, 5, 26, 46, 63, 73, 75, 77, 94])
category_list += map(lambda x : 'similarity ' + str(x) + ' turns', [1, 2, 3, 4, 5])
# add the variance. find the smallest cosin similarity score, test if it is before utterance 6,utterance 10.
for x in range(0, len(category_list)):
    spec = map(lambda y : y[x], feature_list)
    score = corrcoef(spec, label_list)
    print category_list[x] + ': '+ str(score)
maxie = 0
high_list = []
for x in range(len(category_list), len(feature_list[0])):
    spec = map(lambda y : y[x], feature_list)
    score = corrcoef(spec, label_list)[0][1]
    if abs(score) > abs(maxie):
        maxie = score
    if abs(score) > 0.2:
        high_list.append(x - len(category_list))
    print score
print "maximum: " + str(maxie)
print high_list


# extract all the Nouns. try to use wikipedia.https://pypi.python.org/pypi/wikipedia/
# model.similarity('None', themes)
#https://code.google.com/archive/p/word2vec/
