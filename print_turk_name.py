#!/usr/bin/etc python

import sys
import socket
import time
import sqlite3
import os
import readall
global_key = ['TurkID','UserID','Gender','Age','HaveSeen','GoTogether']
rating_logs = readall.readall("/home/ubuntu/zhou/Backend/rating_log")

for f,r in rating_logs.iteritems():
    #print r
    print r['TurkID']
