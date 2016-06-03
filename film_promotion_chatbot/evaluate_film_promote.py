#!/usr/bin/etc python
import os
import readall
import numpy as np
def superhero(wlist):
    num_turns = len(wlist["Turns"])
    for i in range(2,num_turns+1):
      if 'type' in wlist['Turns'][i-1]['Strategy']:
        if 'disney' in wlist['Turns'][i]['You'].lower():
#            print 'disney:' +wlist['Turns'][i]['You']
            return 0
        elif 'hero' in wlist['Turns'][i]['You'].lower():
#            print 'superhero:' +wlist['Turns'][i]['You']
            return 1
        else:
#            print 'both'+wlist['Turns'][i]['You']
            return -1


global_key = ['TurkID','UserID','Gender','Age','HaveSeen','GoTogether']
rating_logs = readall.readall(os.getcwd())
#print rating_logs
writelist = readall.get_log(rating_logs)
turk_id_list =[]
have_seen_list =[]
go_together_list = []
conv_length_list = []
age_list=[]
gender_list=[]
superhero_list =[]
for f,wlist in rating_logs.iteritems():
    if wlist['TurkID'] not in turk_id_list:
        if 'HaveSeen' in wlist.keys():
            have_seen_list.append(wlist['HaveSeen'])
            go_together_list.append(wlist['GoTogether'])
            conv_length_list.append(len(wlist['Turns']))
            age_list.append(wlist['Age'])
            gender_list.append(wlist['Gender'])
            turk_id_list.append(wlist['TurkID'])
            superhero_list.append(superhero(wlist))
turk_number = len(turk_id_list)
print "Number of Turks: " + str(turk_number) +'\n'
print "There are in totall:" +str(len(have_seen_list)) +'\n'
print "Among them, the number of male:" +str(gender_list.count('male')) +'\n'
print "Among them, the number of female:" +str(gender_list.count('female')) +'\n'
print "The age distribution:\n"
print { x: age_list.count(x) for x in set(age_list) }
print "Number of people who prefer disney movies:" + str(superhero_list.count(0)) +'\n'
print "Number of people who prefer super hero movies:" + str(superhero_list.count(1)) +'\n'
print "Among them, have seen number:" +str(have_seen_list.count('1'))+ '\n'
index_seen=[pos for pos, char in enumerate(have_seen_list) if char == '1']
age_seen = [age_list[item] for item in index_seen]
gender_seen =[gender_list[item] for item in index_seen]
#print age_seen
#print gender_seen
age_below_30_seen = age_seen.count('below20')+age_seen.count('20-30')
print "The ones who have seen the movie, how many of them are below 30:" +str(age_below_30_seen)
index_seen_no=[pos for pos, char in enumerate(have_seen_list) if char == '-1']
print "age not seen\n"
age_seen_no = [age_list[item] for item in index_seen_no]
gender_seen_no =[gender_list[item] for item in index_seen_no]
#print age_seen_no
#print gender_seen_no
print "Among them, not have seen number:" +str(have_seen_list.count('-1'))+ '\n'
index_together=[pos for pos, char in enumerate(go_together_list) if char == '1']
age_together = [age_list[item] for item in index_together]
gender_together =[gender_list[item] for item in index_together]
print "Among them, want to go together:" +str(go_together_list.count('1')) +'\n'
#print age_together
#print gender_together
print "Among them, don't want to go together:" +str(go_together_list.count('-1')) +'\n'
index_together_no=[pos for pos, char in enumerate(go_together_list) if char == '-1']
age_together_no = [age_list[item] for item in index_together_no]
gender_together_no =[gender_list[item] for item in index_together_no]
#print age_together_no
#print gender_together_no
print "Total number of turns:" + str(sum(conv_length_list))
print "Conversation length:" +str(float(sum(conv_length_list))/len(conv_length_list))+'SD = '+ str(np.std(np.array(conv_length_list)))

