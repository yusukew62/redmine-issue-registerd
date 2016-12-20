#!/usr/bin/env python
# -*- coding: utf8 -*-

import ConfigParser
import email
import datetime
import os

from email.parser import Parser
from redmine import Redmine
from redmine.exceptions import ResourceNotFoundError

"""
Register auto issue of Redmine by receiving e-mail
"""

class RedmineIssueRegisterd(object):
    def __init__(self):
        # Initialize variables
        self.url = ""
        self.username = ""
        self.password = ""
        self.key = ""
        self.redmine = None
        self.mail_list = list()
        self.issue_list = list()
        self.subject_head = dict()
        self.iid = None

    def setSubjectHead(self, subject_head):
        # Setting the subject head
        self.subject_head = subject_head

    def useBasicAuthentication(self, url, username, password):
        # Using Basic Authentication
        self.url = url
        self.username = username
        self.password = password
        return 1

    def useAPIKeyAuthentication(self, url, key):
        # Using REST API Key Authentication
        self.url = url
        self.key = key
        return 2

    def checkAuthentication(self, auth):
        # Checking Authentication
        if auth == 1:
            # case by using Basic Authentication
            self.redmine = Redmine(self.url, username=self.username, password=self.password)
            print 'auth: [SUCCESS] Basic Authentication
        elif auth == 2:
            # case by using REST API Key Authentication
            self.redmine = Redmine(self.url, key=self.key)
            print 'auth: [SUCCESS] REST API Key Authentication

    def getProjectInfo(self):
        project = self.redmine.project.get('test')
        print "#" * 20 + " Project Info " + "#" * 20
        print i[0], ", ", i[1]
        print "#" * 50

    def getAllProjectInfo(self):
        try:
            # response of all project
            projects = self.redmine.project.all()
            for project in projects:
                print 'Project:' + project.name
            for wiki_page in project.wiki_pages:
                wiki_page_details = self.redmine.wiki_page.get(wiki_page.title, project_id=project.id)
        excdpt:
            print 'not found'

    def getAPI(self):
        try:
            # response of all project
            projects = self.redmine.project.all()
            for project in projects:
                print 'Project: ' + project.name
            for wiki_page in project.wiki_pages:
                wiki_page_details = self.redmine.wiki_page.get(wiki_page.title, project_id=project.id)
        except:
            print 'not found'
          
    def getMail(self):
        pass

    def findMail(self, mail_path):
        for base_dir, dirs, files in os.walk(mail_path):
            if len(files) != 0:
                self.mail_list = [base_dir + "/" + f for f in files]

    def parseMail(self):
        for mail in self.mail_list:
            headers = Parser().parse(open(mail), 'r')

            # added the title heading to the subject
            for h in self.subject_head:
                if h in header['from']:
                    subject = str(self.subject_header[h]) + " " + str(header['subject'])
                    self.issue_list.append({
                        "mail_key": mail,
                        "from": headers['from'],
                        "to": headers['to'],
                        "subject": subject,
                    })

    def createIssue(self):
        for data in self.issue_list:
            try:
                issue = self.redmine.issue.new()
                issue.project_id = 'test'
                issue.subject = data['subject']
                issue.tracket_id = 1
                issue.description = 'test description
                issue.status_id = 1
                issue.priority_id = 1
                issue.assigned_to_id = 1
                issue.watcher_user_ids = [1]
                issue.parent_issue_id = 1
                issue.status_date = datetime.date(2016, 11, 1)
                issue.due_date = datetime.date(2016, 11, 7)
                issue.estimated_hours = 4
                issue.done_ration = 40
                issue.custom_fields = [{'id': 1, 'value': 'foo'}]
                issue.uploads = [{'path': '/share/test.txt'}]
                issue.save()
            except:
                print 'error'

    def confirmIssue(self):
        # get latest issue number
        issues = self.redmine.issue.all(sort='id:desc', limit=1)
        for latest_issue in issues:
            self.iid = latest_issue.id
        print "idd: " + str(self.iid)

 
def main():
    # Reading the configuration file of this script
    config = ConfigParser.SafeConfigParser()
    config.read('redmine_ird.conf')

    # Reading variables from configuration file
    container = config.get('global', 'target')
    url = config.get(container, 'url')
    username = config.get(container, 'username')
    password = config.get(container, 'password')
    key = config.get(container, 'key')
    mail_path = config.get('global', 'mail_path')
    subject_head = dict(config.items('subject'))

    # Debugging
    print "usr: " + str(url)
    print "username: " + str(username)
    print "password: " + str(password)
    print "key:" + str(key)
    print "mail_path: " + str(mail_path)
    print "subject_head: " + str(subject_head)

    # Create instance from RedmineIssueRegisterd class
    obj = RedmineIssueRegisterd()

    # set subject head
    obj.setSubjectHead(subject_head)

    # Select Basic Authentication or API Key Authentication
    auth = obj.useBasicAuthentication(url, username, password)
#   auth = obj.userAPIKeyAuthentication(url, key)

    # execute the checking authentication and create auth object of the redmine class
    obj.checkAuthentication(auth)

    # find mail
    obj.findMail(mail_path)
    obj.parseMail()
#   obj.createItem()
    obj.confirmIssue()

    # Operation
#   obj.getProjectInfo()
#   obj.getAllProjectInfo()
#   obj.getAPI()


if __name__ == "__main__":
    main()

