# -*- coding: utf8 -*-
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

    def list_my_current_issues(self):
        query = 'project=%s and assignee=%s and resolution=unresolved' % (
                                                   self.project, self.username)
        my_issues = self.jira.search_issues(query)

        for issue in my_issues:
            print '%s\t%s' % (issue.key, issue.fields.summary)

