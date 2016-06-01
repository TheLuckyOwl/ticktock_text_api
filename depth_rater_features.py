#!/usr/bin/env python

from os import listdir, walk
from os.path import isfile, join
import re
import pickle
import pprint
import csv
import gensim
import numpy
import nltk
from itertools import izip_longest
import string
import pprint
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cosine
def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)

def tt_switch_length(convo):
    tot_dist = 0
    tot_switch = 0
    swi_idx = -1

    for x in range(0, len(convo)):
        if len(convo[x]['Strategy']) == 1 and convo[x]['Strategy'][0] == 'switch':
            if swi_idx != -1:
                tot_dist += x - swi_idx
                tot_switch += 1
            swi_idx = x

    return float(tot_dist) / (tot_switch + 1)


def word2vec_similarity(convo, model):

    def word2vec_responses(response):
        cur_vec_1 = []
        cur_vec_2 = []
        tmp1 = nltk.word_tokenize(response['You'])
        tmp2 = nltk.word_tokenize(response['TickTock'])

        for word in tmp1:
            try:
                cur_vec_1 += [model[word]]
            except:
                pass
        if len(cur_vec_1) == 0:
            cur_vec_1 = numpy.array([0.0 for x in range(0, 100)])
        else:
            cur_vec_1 = sum(cur_vec_1)

        cur_vec_2 = []
        for word in tmp2:
            try:
                cur_vec_2 += [model[word]]
            except:
                pass
        if len(cur_vec_2) == 0:
            cur_vec_2 = numpy.array([0.0 for x in range(0, 100)])
        else:
            cur_vec_2 = sum(cur_vec_2)
        return (cur_vec_1, cur_vec_2)

    word2vec_list = map(word2vec_responses, convo)
    similarity_sums = [0.0, 0.0, 0.0, 0.0, 0.0]
    similarity_count = [0 for x in similarity_sums]
    for idx in range(0, len(word2vec_list)):
        for x in range(0, len(similarity_sums)):
            if x + idx + 1 < len(word2vec_list):
                tmp = cosine(word2vec_list[idx][0], word2vec_list[x + idx + 1][0])
                if numpy.isnan(tmp):
                    tmp = numpy.float64(1.0)
                print type(tmp)
                similarity_sums[x] += tmp
                similarity_count[x] += 1

    for x in range(0, len(similarity_sums)):
        similarity_sums[x] /= float(similarity_count[x])

    convo_vec = sum([x[0] for x in word2vec_list] + [x[1] for x in word2vec_list])

    indices = [0, 5, 26, 46, 63, 73, 75, 77, 94]
    return [convo_vec[x] for x in indices] + similarity_sums[2:]
    #return vec_list


def strat_count(convo):
    #strat_list = ['init', 'switch', 'continue', 'end']
    strat_list = ['switch', 'continue', 'end']
    count_list = [0 for x in strat_list]
    for resp in convo:
        #print 'resp'
        #print resp
        for idx in range(0, len(strat_list)):
            if strat_list[idx] in resp['Strategy']:
                count_list[idx] += 1
    return map(lambda x : float(x) / (len(convo) + 1), count_list)


def keyword_count(convo):
    #keywords = ['sense', 'something', 'else', 'how', 'what', 'who', 'when', 'where', 'why']
    keywords = ['sense', 'something', 'when', 'where', 'why']
    count_list = [0 for x in keywords]
    exclude = set(string.punctuation)
    for response in convo:
        bare = (''.join(ch for ch in ((response['TickTock'] + ' ' + response['You'])) if ch not in exclude)).lower().split()
        for word in bare:
            for idx in range(0, len(keywords)):
                if keywords[idx] == word:
                    count_list[idx] += 1
    return count_list

def extract_features(convo):
    #word2vec disbaled since not all words are in the model.
    word2vec_model = gensim.models.Word2Vec.load('/tmp/word2vec_100_break')
    word2vec_scores = word2vec_similarity(convo, word2vec_model)
    strat_scores = strat_count(convo)
    response_num = len(convo)
    swi_len = tt_switch_length(convo)
    keyword_scores = keyword_count(convo)
    #res = [response_num, swi_len] + strat_scores + keyword_scores +  word2vec_scores
    res = [response_num] + strat_scores + keyword_scores +  word2vec_scores
    #print res
    return res


def get_convolist():
    data_file = open('depth_data.csv')
    data_csv = csv.reader(data_file, delimiter=',')
    file_list = [{'name' : row[0].strip(), 'label' : int(row[1])} for row in data_csv]
    pickle.dump(file_list, open('file_list.pkl','w'))#print file_list
    log_root = '/home/ubuntu/zhou/Backend/rating_log/'
    count = 0
    #print len(file_list)
    for root, subdirs, files in walk(log_root):
        for f in files:
            for item in file_list:
                if f == item['name']:
                    if 'path' not in item.keys():
                        item['path'] = join(root, f)
                        count += 1
    for item in file_list:
        if 'path' not in item.keys():
            print item['name']
    print count
    for item in file_list:
        item['convo'] = extract_convo(item['path'])
    return file_list

def extract_convo(path):
    themeList = ['music', 'movies', 'board games', 'sports', 'politcs']
    responseList = []
    with open(path, 'r') as log:
        lines = log.readlines()
        lines = [x.rstrip('\n') for x in lines]
        print lines
        turkID = lines[0].replace('TurkID: ', '')
        userID = lines[1].replace('UserID: ', '')
        theme = [lines[4].split(' ')[-1]]
        approNum = 0
        inapproNum = 0
        for response in grouper(lines[2:], 6):
            print response
            resDict = {}
            resDict['TurkID'] = turkID
            resDict['UserID'] = userID
            resDict['Turn'] = int(response[0].replace('Turn: ', ''))
            resDict['You'] = response[1].replace('You: ', '')
            resDict['TickTock'] = response[2].replace('TickTock: ', '')

            resDict['Appropriateness'] = int(response[3].replace('Appropriateness: ', ''))
            if resDict['Appropriateness'] < 3:
                inapproNum = inapproNum + 1
            else:
                approNum = approNum + 1
            resDict['PrevInappro'] = inapproNum
            resDict['PrevAppro'] = approNum

            resDict['Strategy'] = [x.strip() for x in response[4].replace('[', '').replace(']', '').replace('\'', '').replace('Strategy: ', '').split(',')]
            stratNum = len(resDict['Strategy'])
            if 'new' in resDict['Strategy'] or 'switch' in resDict['Strategy'] and (stratNum == 1 or ('anaphora' in resDict['Strategy'] and stratNum == 1)):
                theme = resDict['TickTock'].split(' ')[-1]
                if theme == 'games':
                    theme = 'board games'
            resDict['Theme'] = theme
            responseList += [resDict]
            print resDict
        for x in range(0, len(responseList)):
            if x == 0:
                responseList[x]['PrevResp'] = []
            else:
                responseList[x]['PrevResp'] = list(responseList[x - 1]['PrevResp']) + [responseList[x - 1]['You'], responseList[x - 1]['TickTock']]
    return responseList

def create_learnable(convolist):
    feature_list = []
    label_list = []
    for convo in convolist:
        feature_list.append(extract_features(convo['convo']))
        label_list.append(convo['label'])
    return feature_list, label_list



if __name__ == "__main__":
    f_list, l_list = create_learnable(get_convolist())
    pickle.dump(f_list, open('features.pkl', 'wb'))
    pickle.dump(l_list, open('labels.pkl', 'wb'))
