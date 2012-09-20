# -*- coding: utf8 -*-
import getpass
from ConfigParser import RawConfigParser

from jira.client import JIRA

class JiraClient(object):
    
    def __init__(self, server, username, password, project=None):
        self.username = username
        self.password = password 
        self.project = project 
        self.server = server

        self.jira = JIRA(options={'server': self.server},
                         basic_auth=(self.username, self.password))

    def list_my_issues(self):
        query = 'project=%s and assignee=%s' % (self.project, self.username)
        my_issues = self.jira.search_issues(query)

        for issue in my_issues:
            print '%s\t%s' % (issue.key, issue.fields.summary)


if __name__ == '__main__':
    config_parser = RawConfigParser()
    config_parser.read(['pyjira.conf'])

    server = config_parser.get('jira settings', 'host')
    username = config_parser.get('jira settings', 'username')
    password = config_parser.get('jira settings', 'password')
    project = config_parser.get('jira settings', 'default_project')

    if not username:
        username = getpass.getuser()
    if not password: 
        password = getpass.getpass()
    
    jira_client = JiraClient(server, username, password, project)
    jira_client.list_my_issues()



