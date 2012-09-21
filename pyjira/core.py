# -*- coding: utf8 -*-
from jira.client import JIRA

class JiraClient(object):
    
    def __init__(self, server, username, password, default_project=None):
        self.username = username
        self.password = password 
        self.default_project = default_project 
        self.server = server

        self.jira = JIRA(options={'server': self.server},
                         basic_auth=(self.username, self.password))

    def my(self, **kwargs):
        self._list_my_issues(**kwargs)

    def _list_my_issues(self, **kwargs):
        query_parts = ['assignee=%s' % (self.username)]

        if kwargs['project'] is not None: 
            query_parts.append('project=%s' % kwargs['project'])
        elif self.default_project is not None:
            query_parts.append('project=%s' % self.default_project)

        if kwargs['unresolved']:
            query_parts.append('resolution=unresolved')
        
        query = ' and '.join(query_parts)      
        my_issues = self.jira.search_issues(query)

        for issue in my_issues:
            print '%s\t%s' % (issue.key, issue.fields.summary)


