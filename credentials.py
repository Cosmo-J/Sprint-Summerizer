JIRA_API_TOKEN= ""
JIRA_EMAIL= ""
JIRA_DOMAIN = ""
OPENAI_API_KEY = ""


import requests
import base64

def EmptyCred(jira,openAI):
    jiraPass = jira
    openPass = openAI
    if jira and (not JIRA_API_TOKEN or not JIRA_DOMAIN or not JIRA_EMAIL):
        print("Please add Jira credentials to 'credentials.py', see the following guide for how to find them:\nhttps://developer.atlassian.com/cloud/jira/software/basic-auth-for-rest-apis/\n")
        jiraPass = False
    if openAI and not OPENAI_API_KEY:
        print("Please add OpenAI credentials to 'credentials.py', see the following guide for how to find them:\nhttps://platform.openai.com/docs/api-reference/authentication/\n")
        openPass = False
    return (jira == jiraPass and openAI == openPass)
    

def CheckCredentials(jira,openAI):
    if not EmptyCred(jira,openAI):
        exit()

    jiraCred = jira
    openCred = openAI

    if jira:
        auth_str = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}".encode("ascii")
        auth_b64 = base64.b64encode(auth_str).decode("ascii")
        HEADERS = {
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"https://{JIRA_DOMAIN}/rest/api/3/dashboard", headers=HEADERS)

        if(response.status_code in (200,201,202)):
            print(f"{response.status_code}: JIRA credentials validated successfully!")
        else:
            print(f"{response.status_code}: Invalid JIRA credentials!")
            jiraCred = False



    if openAI:
        HEADERS = {
            "Authorization": f'Bearer {OPENAI_API_KEY}',
            "Content-Type": "application/json"
        }
        response = requests.get("https://api.openai.com/v1/models",headers=HEADERS)
        if(response.status_code in (200,201,202)): 
            print(f"{response.status_code}: OpenAI credentials validated successfully!")
        else:
            print(f"{response.status_code}: Invalid OpenAI credentials!")
            openCred = False
    
    return (jira == jiraCred and openAI == openCred)