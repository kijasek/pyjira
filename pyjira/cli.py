# -*- coding: utf8 -*-
import getpass
import sys
import os
from ConfigParser import RawConfigParser

from pyjira.core import JiraClient

def main():
    conf_dir = os.path.dirname(__file__)
    conf_path = os.path.join(conf_dir, 'pyjira.conf')
    config_parser = RawConfigParser()
    config_parser.read([conf_path])

    server = config_parser.get('jira settings', 'host')
    username = config_parser.get('jira settings', 'username')
    password = config_parser.get('jira settings', 'password')
    project = config_parser.get('jira settings', 'default_project')

    if not server:
        sys.exit('Please specify valid server address in pyjira.conf')
    if not username:
        username = raw_input('Username: ') 
    if not password: 
        password = getpass.getpass()
    if project.strip() == '':
        project = None
    
    jira_client = JiraClient(server, username, password, project)
    jira_client.list_my_issues()

