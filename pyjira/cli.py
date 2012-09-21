# -*- coding: utf8 -*-
import argparse
import getpass
import sys
import os
from ConfigParser import RawConfigParser

from pyjira.core import JiraClient

def get_config():
    conf_dir = os.path.dirname(__file__)
    conf_path = os.path.join(conf_dir, 'pyjira.conf')
    config_parser = RawConfigParser()
    config_parser.read([conf_path])

    return config_parser

def create_argparse():
    parser = argparse.ArgumentParser(description='CLI for common JIRA tasks')
    subparsers = parser.add_subparsers(title='valid actions', dest="action")

    list_my_issues_parser = subparsers.add_parser('my',
                                             help='List issues assigned to me')
    list_my_issues_parser.add_argument('-p', '--project', 
                                     help='Only issues from specified project')
    list_my_issues_parser.add_argument('-u', '--unresolved', 
                                     action='store_true',
                                     help='Issues that have unresolved status')

    issue_details_parser = subparsers.add_parser('issue',
                                                 help='Displays issue details')
    issue_details_parser.add_argument('issue_id', help='Issue key')

    log_work_parser = subparsers.add_parser('log', help='Log your work')
    log_work_parser.add_argument('issue_id', help='Issue key')
    log_work_parser.add_argument('-m', '--message', required=True, 
                                              help='Message; work description')
    log_work_parser.add_argument('-t', '--time', help='Time spent', 
                                                                 required=True)

    resolve_parser = subparsers.add_parser('resolve', help='Resolve issue')
    resolve_parser.add_argument('issue_id', help='Issue key')
    
    return parser

def main():
    config = get_config()
    server = config.get('jira settings', 'host')
    username = config.get('jira settings', 'username')
    password = config.get('jira settings', 'password')
    project = config.get('jira settings', 'default_project')

    if not server:
        sys.exit('Please specify valid server address in pyjira.conf')
    if not username:
        username = raw_input('Username: ') 
    if not password: 
        password = getpass.getpass()
    if project.strip() == '':
        project = None
   
    parser = create_argparse()
    args = parser.parse_args()
    args = vars(args)
    jira_client = JiraClient(server, username, password, project)
    method_to_call = getattr(jira_client, args['action'])
    method_to_call(**args)

