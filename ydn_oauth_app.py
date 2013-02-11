#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import required modules
import os, sys, pickle

# update sys path to include bundled modules with priority
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

import oauthlib.oauth

import yahoo.oauth, yahoo.yql, yahoo.application

class YdnOauthApp(object):

	def __init__(self, ck, cks, app, cb, tk):
		self.ck = ck
		self.cks = cks
		self.app = app
		self.cb = cb
		self.tk = tk
		# make public request for data oauth requests for profiles
		self._oauthapp = yahoo.application.OAuthApplication(self.ck, self.cks, self.app, self.cb)

	def is_token(self):
		"""
		Token Check & Get Authorization URL
		True,""		:Exists Token
		False,url 	:Not Exists Token,Authorization URL
		"""
		_access_token = self._load()

  		if _access_token:
    			self._access_token = _access_token
    			self._oauthapp.token = _access_token
    			return True,""
  		else:
    			self.request_token = self._oauthapp.get_request_token(self.cb)
    			auth_url = '\nAuthorization URL:\n%s' % self._oauthapp.get_authorization_url(self.request_token)
    			return False, auth_url

    	def get_token(self,verifier):
		"""
		Get Access Token(input:verifier)
		"""
    		self._access_token = self._oauthapp.get_access_token(self.request_token, verifier.strip())
    		self._oauthapp.token = self._access_token
    		self._dump(self._access_token)

	def _dump(self,value):
		"""
		pickle dump
		"""
		pkl_file=open(self.tk, 'wb')
		try:
	    		pickle.dump(value, pkl_file)
	    	finally:
	    		pkl_file.close()

	def _load(self):
		"""
		pickle load
		"""
		pkl_file = None
		value = None
  		try:
    			pkl_file=open(self.tk, 'rb')
    			value=pickle.load(pkl_file)
  		except:
    			value=None
    		finally:
    			if pkl_file != None:
	    			pkl_file.close()
	    	return value


    	def _get_access_token(self):
    		return self._access_token

    	def _get_oauthapp(self):
    		return self._oauthapp

    	access_token =property(_get_access_token)
    	oauthapp =property(_get_oauthapp)

if __name__ == '__main__':
	import pprint
	from ydn_conf import CONSUMER_KEY,CONSUMER_SECRET,CALLBACK_URL,APPLICATION_ID,TOKEN_STORAGE
	ydn = YdnOauthApp(CONSUMER_KEY,CONSUMER_SECRET,APPLICATION_ID,CALLBACK_URL,TOKEN_STORAGE)
	hoge,url = ydn.is_token()
	print hoge
	print url
	if hoge == False:
		verifier = raw_input('Please authorize the url params "verifier" value:')
		ydn.get_token(verifier)
	print '\nkey: %s' % str(ydn.access_token.key)
	print 'secret: %s' % str(ydn.access_token.secret)
	print 'yahoo guid: %s' % str(ydn.access_token.yahoo_guid)
	pprint.PrettyPrinter(indent=2).pprint(ydn.oauthapp.getProfile())