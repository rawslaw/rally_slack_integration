# coding=utf8
"""
rally.py - Willie Rally module
Copyright 2016, Allen Rawls

http://willie.dftba.net

This module will find Rally work items in messages and
provide a link to the artifact on Rally site.
"""
from __future__ import unicode_literals

import re
import requests
import json
from willie.tools import Identifier, WillieMemory
from willie.module import rule, priority
from willie.formatting import bold


@rule("(.*?)(US|F|DE|TA|us|f|de|ta)[0-9]+(.*?)")
@priority('high')
def lookuprally(bot, trigger):
		
	reg = re.compile('(US|F|DE|TA)[0-9]+');
	workitem = reg.search(trigger.upper()).group(0);

	phrase = workitem_parse(workitem)

	bot.say(phrase)


def workitem_parse(workitem):
    ws_url = 'https://rally1.rallydev.com/slm/webservice/v2.0/'
    web_url = 'https://rally1.rallydev.com/#/detail/'

    if workitem.startswith('US'):
        ws_type = 'HierarchicalRequirement'
        web_type = 'userstory/'
    elif workitem.startswith('DE'):
        ws_type = 'defect'
        web_type = 'defect/'
    elif workitem.startswith('F'):
        ws_type = 'portfolioitem/feature'
        web_type = 'portfolioitem/feature/'
    elif workitem.startswith('TA'):
        ws_type = 'task'
        web_type = 'task/'

    req = ws_url + ws_type + '?query=(FormattedID%20%3D%20' + workitem + ')&fetch=_refObjectName,ObjectID'
    resp = requests.get(req, headers={"zsessionid":"_nQLJ3PAXSX6UZ3z6yxz5YPmXlvg0HJtAfOWSwQNnI"})

    if (resp.status_code != 200):
        return 'RallyLookup: Non-200 returned'
    
    parsed_json = resp.json()

    if len(parsed_json['QueryResult']['Results']) == 0:
        return 'RallyLookup: no results'


    d = parsed_json['QueryResult']['Results'][0]

    url = web_url + web_type + str(d['ObjectID'])

    return workitem + ': ' + d['_refObjectName'] + ' ' + url


