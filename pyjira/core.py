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

    def issue(self, **kwargs):
        issue_id = kwargs['issue_id']
        issue = self.jira.issue(issue_id)

        print 'ID: %s' % issue.key
        print 'URL: %s/browse/%s' % (self.server, issue.key)
        print 'Assignee: %s' % issue.fields.assignee.name
        print 'Status: %s' % issue.fields.status.name
        print ''
        print 'Summary: %s' % issue.fields.summary
        print ''
        print 'Details: %s' % issue.fields.description

    def log(self, **kwargs):
        issue_id = kwargs['issue_id']
        issue = self.jira.issue(issue_id)

        time_spent = kwargs['time']
        msg = kwargs['message']

        #FIXME: add comment as a part of worklog (investigate API)
        self.jira.add_comment(issue, msg)
        self.jira.add_worklog(issue, time_spent)
        print 'Your worklog was saved'

    def resolve(self, **kwargs):
        issue_id = kwargs['issue_id']
        issue = self.jira.issue(issue_id)

        self.jira.transition_issue(issue, '5', resolution={'name': 'Implemented'})
        print 'Issue %s was resolved as implemented' % issue_id

    def assign(self, **kwargs):
        issue_id = kwargs['issue_id']
        issue = self.jira.issue(issue_id)

        self.jira.assign_issue(issue, self.username)
        print 'Issue %s was assigned to %s' % (issue_id, self.username)
        if kwargs['start']:
            self.jira.transition_issue(issue, '4')
            print 'Issue %s was started' % issue_id

    def todo(self, **kwargs):
        query_parts = ['status = Open', 'type != Story', 'created >= "-14d"']

        if kwargs['project'] is not None: 
            query_parts.append('project=%s' % kwargs['project'])
        elif self.default_project is not None:
            query_parts.append('project=%s' % self.default_project)

        query = ' and '.join(query_parts)      
        self._perform_and_print_query(query)

    def _list_my_issues(self, **kwargs):
        query_parts = ['assignee=%s' % (self.username)]

        if kwargs['project'] is not None: 
            query_parts.append('project=%s' % kwargs['project'])
        elif self.default_project is not None:
            query_parts.append('project=%s' % self.default_project)

        if kwargs['unresolved']:
            query_parts.append('resolution=unresolved')
        
        query = ' and '.join(query_parts)      
        self._perform_and_print_query(query)

    def _perform_and_print_query(self, query):
        my_issues = self.jira.search_issues(query)

        for issue in my_issues:
            print '%s\t%s' % (issue.key, issue.fields.summary)

