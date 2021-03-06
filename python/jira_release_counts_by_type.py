#!/usr/local/bin/python3

from jira import JIRA
from util import get_settings
from models.IssueType import IssueType
from models.TeamReport import TeamReport

import sys

settings = get_settings()
options = { 'server': settings["jira"]["server"] }
jira = JIRA(options, auth=(settings["jira"]["user"], settings["jira"]["password"]))

policyJQL = 'project = CLM AND fixVersion = [VER] AND statusCategory = Done AND type = Bug AND summary ~ "Nexus IQ:" AND Team = [TEAM]'
bugJQL = 'project = CLM AND fixVersion = [VER] AND statusCategory = Done AND type = Bug AND summary !~ "Nexus IQ:" AND Team = [TEAM]'
storyJQL = 'project = CLM AND fixVersion = [VER] AND statusCategory = Done AND type = Story AND Team = [TEAM]'
techDebtJQL = 'project = CLM AND fixVersion =[VER] AND statusCategory = Done AND type = "Technical Debt" AND Team = [TEAM]'

issueTypes = [IssueType(bugJQL, "Bugs"),
                IssueType(policyJQL, "Policy Violations"), 
                IssueType(storyJQL, "Story"), 
                IssueType(techDebtJQL, "Tech Debt")]

# set version
if len(sys.argv) > 1:
    version = sys.argv[1]
else:
    print("running with default version of Icarus")
    version = 'Icarus'
teamReports = [TeamReport(17), TeamReport(35), TeamReport(36), TeamReport(38)]
teams = [17,35,36,38]

# loop over each team
for team in teamReports:
    team.release = version
    ## collect data
    for issueType in issueTypes:
        issues = issueType.get_jira_issues(jira, version, team)
        team.issues.append(len(issues))

# print header
print(version, "Laurel", "Alpha", "Axon", "Atom","Total", sep=", ")

# log data
for index, iType in enumerate(issueTypes):
    tot = 0
    pstring = ""
    for j, team in enumerate(teamReports):
        if j == 0:
            pstring += iType.issueType + ", "
        tot += team.issues[index]
        pstring += str(team.issues[index]) + ", "
        
    print(pstring, tot, sep="")
