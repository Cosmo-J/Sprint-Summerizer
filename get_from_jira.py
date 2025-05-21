import requests
import base64
from NLP import compress_summary,text_length

import Settings as s
import credentials as c

JIRA_API_TOKEN = c.JIRA_API_TOKEN
JIRA_EMAIL = c.JIRA_EMAIL
JIRA_DOMAIN = c.JIRA_DOMAIN

auth_str = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}".encode("ascii")
auth_b64 = base64.b64encode(auth_str).decode("ascii")

HEADERS = {
    "Authorization": f"Basic {auth_b64}",
    "Content-Type": "application/json"
}

def GetActiveSprint():
    #board default is one because that is the product board
    url = f"https://{JIRA_DOMAIN}/rest/agile/1.0/board/{s.BOARD}/sprint?state=active"
    payload = {}
    response = requests.get(url, headers=HEADERS)# , data=json.dumps(payload))
    data = response.json()
    if (response.status_code == 200):
        values = data.get("values")[0]
        return values.get("id")
    else:
        print(f"Response:{response.status_code}")
        return None
    


def GetParsedIssues():
    sprintId = GetActiveSprint()
    issues = GetAllIssues(sprintId)
    parsedIssues = IssueIter(issues)
    print(f"Total issues retrieved: {len(parsedIssues)}")
    return parsedIssues

    

def GetAllIssues(sprintId):
    url = f"https://{JIRA_DOMAIN}/rest/agile/1.0/sprint/{sprintId}/issue"

    all_issues = []
    start_at = 0
    max_results = 50  # or set to something larger, up to Jira’s maximum limit

    while True:
        # Provide JQL, startAt, and maxResults as query params
        params = {
            "jql": f'status = {s.JIRACOLUMN}',
            "startAt": start_at,
            "maxResults": max_results
        }

        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"Error - response status code: {response.status_code}")
            print(f"Response body: {response.text}")
            break

        data = response.json()
        issues = data.get("issues", [])

        if not issues:
            break  # No more issues to fetch

        all_issues.extend(issues)
        
        # If we got fewer than max_results, we're done
        if len(issues) < max_results:
            break

        # Otherwise, increment startAt and fetch the next page
        start_at += max_results

    return all_issues

def IssueIter(issue_data):
    issues = []
    for issue in issue_data:
        issues.append(parse_issue_info(issue))
    return issues

def parse_issue_info(issue_data):
    fields = issue_data.get("fields", {})

    title = fields.get("summary", "No summary")
    numeric_id = issue_data.get("id", "N/A")
    issue_key = issue_data.get("key", "N/A")

    reporter = fields.get("reporter", {}).get("displayName", "No reporter")

    assignee_info = fields.get("assignee") or {}
    solver = assignee_info.get("displayName", "No assignee")

    issue_type = fields.get("issuetype", {}).get("name")
    description = fields.get("description", {})
    issue_url = f"https://{JIRA_DOMAIN}/browse/{issue_key}"

    return {
        "title": title,
        "description": description,
        "type": issue_type,
        "reporter": reporter,
        "solver": solver,
        "link": issue_url
    }

def compress_summary(parsed_data):
    for issue in parsed_data:
        if(issue["type"]=="Bug"):
            newSum=compress_summary(issue["summary"])
        if(text_length(issue["summary"])):
            #shorten the text somehow (maybe using openai)
            print("Text is too long")

