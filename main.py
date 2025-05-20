from get_from_jira import GetParsedIssues
from saveFile import SaveAsCsv,GetUniqueFilepath
from OpenAI_GEN import GeneratePatchNotes
import argparse


#API VALIDATION
from requests.auth import HTTPBasicAuth
import credentials as c
from openai import OpenAI
import json
import requests
import base64

def parse_arguments(): 
    parser = argparse.ArgumentParser(description='Use the JIRA and OpenAI api to generate patch notes and or just get a list of all of them')
    parser.add_argument('--csv','-c', default='', type=str,  help='exports a csv of given name')
    parser.add_argument('--openai','--md','-o', default='', type=str,  help='use openAI to automatically generate markdown file of notes ')
    parser.add_argument('--apiTest','--test','--testApi','-t', action='store_true', help='test the api credentials for both jira and openai without generating anything')


    return parser

def CheckCredentials(jira,openAI):
    jiraCred = jira
    openCred = openAI

    if jira:
        auth_str = f"{c.JIRA_EMAIL}:{c.JIRA_API_TOKEN}".encode("ascii")
        auth_b64 = base64.b64encode(auth_str).decode("ascii")
        payload = {}
        HEADERS = {
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"https://{c.JIRA_DOMAIN}/rest/api/3/", headers=HEADERS, data=json.dumps(payload))
        if(response.status_code in (200,201,202)):
            print("JIRA credentials validated successfully!")
        else:
            print(f"{response.status_code}: Invalid JIRA credentials!")
            jiraCred = False

    if openAI:
        HEADERS = {
            "Authorization": f'Bearer {c.OPENAI_API_KEY}',
            "Content-Type": "application/json"
        }
        response = requests.get("https://api.openai.com/v1/models",headers=HEADERS,)
        if(response.status_code in (200,201,202)): 
            print("OpenAI credentials validated successfully!")
        else:
            print(f"{response.status_code}: Invalid OpenAI credentials!")
            openCred = False
    
    return (jira == jiraCred and openAI == openCred)








if (__name__=="__main__"):
    parser =parse_arguments()
    args = parser.parse_args()
    makeCsv = args.csv
    makeMd = args.openai
    test = args.apiTest

    if not makeMd and not makeCsv and not test:
        print(makeCsv)
        print("Please see instructions, specify either csv or openai")
        parser.print_help()
        exit()

    if test: APIsuccess = CheckCredentials(True,True)
    else: APIsuccess = CheckCredentials(makeCsv or makeMd,makeMd)

    if not APIsuccess: exit()
    if test: exit() #

    issues = GetParsedIssues()
    if makeMd: 
        patch_notes = GeneratePatchNotes(issues)

            
    if makeCsv:
        SaveAsCsv(issues,'Outputs',makeCsv)


    


