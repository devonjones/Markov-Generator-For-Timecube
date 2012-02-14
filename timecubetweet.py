#!/usr/bin/env python
import tweepy
import yaml
import os
import sys
import datetime
import random
from optparse import OptionParser

def twitter_connect(config):
	auth = twitter_auth(config)
	return tweepy.API(auth)

def twitter_auth(config):
	auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
	auth.set_access_token(config['access_token'], config['access_token_secret'])
	return auth

def get_config():
	if os.path.exists('moartimecube.yaml'):
		return yaml.load(file('moartimecube.yaml', 'r'))['moartimecube']
	elif os.path.exists(os.path.expanduser('~/.moartimecube')):
		return yaml.load(file(os.path.expanduser('~/.moartimecube'), 'r'))['moartimecube']
	elif os.path.exists('/etc/moartimecube.yaml'):
		return yaml.load(file('/etc/moartimecube.yaml', 'r'))['moartimecube']
	else:
		raise Exception('No config file')

def post_tweet(config, doc):
	api = twitter_connect(config)
	api.update_status(doc)

def tweet(config):
	doc = "".join(sys.stdin.readlines())
	if len(doc) > 140:
		return
	elif len(doc) <= 130:
		random.seed(datetime.datetime.now())
		val = random.random()
		if val < 0.02:
			doc = "@TimeCube " + doc
		elif val > 0.98:
			doc = doc + " @TimeCube"
	print doc.strip()
	post_tweet(config, doc.strip())

def option_parser():
	parser = OptionParser(usage="Posts generated tweets to Moar Time Cube twitter account.")
	return parser

def main():
	parser = option_parser()
	config = get_config()
	tweet(config)

if __name__ == "__main__":
	main()
