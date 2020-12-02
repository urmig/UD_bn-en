#!/usr/bin/env python
# -*- coding=utf-8 -*-

# This program Bengali-English tweets and provides for Language, POS, Dependency tags for the normalised text in accordance with the Universal Dependencies. The program is based on Hindi-English Tweet Crawler by I.A.Bhat.
# python crawl_tweets.py --t DATA/<dev/test/train>_twids.txt  --a DATA/<dev/test/train>_annot.json --o <dev/test/train>_output.conllu
# LTRC, IIIT-Hyderabad

from __future__ import (division, unicode_literals)
import os
import re
import sys
import string
import argparse
import tweepy
import json
import io
import pickle
__version__ = '2.0'

# Enter your twitter application's access token  details


CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
twitter = tweepy.API(auth)


file_path = os.path.dirname(os.path.abspath(__file__))

def tokenize(text):
    cnotanum = re.compile(',([^0-9])')
    text = cnotanum.sub(r' , \1', text)
    return text.split()

def get_tweets(tweet_ids):
    tweets = {}
    for i in range(0, len(tweet_ids), 100):
      for twid in [tweet_ids[i:i+100]]:
           tw = [t.split('-')[0] for t in twid]
           n_tweets = twitter.statuses_lookup(tw)
           for t in n_tweets:
              if t:
                tweets[t.id_str] = ' '.join(t.text.split())
    return tweets


if __name__ == '__main__':
    description = 'Download, tokenize and get annotations for Bengali-English tweets'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-t', '--twid-file', metavar='', dest='twidfile', type=str, help='Tweet Ids input file')
    parser.add_argument('-a', '--annot-file', metavar='', dest='annotfile', type=str, help='Annotation file in JSON format')
    parser.add_argument('-o', '--output', metavar='', dest='outfile', type=str, help='Output file')

    args = parser.parse_args()

    #initialise output file
    op = io.open(args.outfile, mode='w', encoding='utf-8')

    #loading annotations in JSON format
    with io.open(args.annotfile, encoding='utf-8') as fp:
        annot_map = json.load(fp)

    #crawl tweets
    with io.open(args.twidfile) as fp:
        tweet_ids = fp.read().split('\n')

    tweets = get_tweets(tweet_ids)

    #Loading required edits
    edits = {}
    with io.open('%s/DATA/EDITS' %file_path, encoding='utf-8') as fp:
        for line in fp:
            line = line.strip().split('\t')
            tid, eds = line[0], line[1:]
            edits.setdefault(tid, [])
            for edit in eds:
                edits[tid].append(edit.split('|'))

    for tid in tweet_ids:
        annot = annot_map[tid]
        lno = int(annot_map[tid]['lno'])
        err_flag = False

        tok=tid.split('-')
        if tok[0] not in tweets:
        	if not annot['deleted']:
        	    err_flag = True
        	    sys.stderr.write('Tweet deleted recently :: t_id %s :: Please report' %tok[0])
        else:
            if tok[0] in edits:
                for edit in edits[ tok[0]]:
                	tweets[ tok[0]] = tweets[ tok[0]].replace(edit[0], edit[1])
            tweet = tokenize(tweets[ tok[0]])

            #Splitting Sentences within a tweet
            size=len(tweet)
            idx_list = [idx + 1 for idx, val in enumerate(tweet) if (re.match('[.!?]', val)!=None)]
            if(idx_list):
            	tweet_x = [tweet[i: j] for i, j in zip([0] + idx_list, idx_list +  ([size] if idx_list[-1] != size else []))]
            else:
            	tweet_x=[tweet]

            tweet = tweet_x[lno-1]

            org_tweet = annot['tweet']
            for i,wd in enumerate(org_tweet):
                    new_wd = tweet[i]
                    if new_wd[0] == wd[0]:
                        org_tweet[i] = new_wd
                    else:
                        sys.stderr.write('Annotation mismatch :: t_id %s :: Please report\n' %tok[0])
                        err_flag = True
            annot['tweet'] = org_tweet

        if err_flag:
            break

        pad = ['_']*len(annot['ids'])
        norm = [n if n!='_' else r for n,r in zip(annot['norm'], annot['tweet'])]
        dep_tweet = zip(annot['ids'], annot['tweet'], norm, annot['pos'], annot['cpos'],
                        annot['chunk'], annot['parent'], annot['drel'], annot['lid'], pad)
        dep_tweet = '\n'.join(['\t'.join(x) for x in dep_tweet])
        op.write('%s\n\n' % dep_tweet)

    #close files
    op.close()
