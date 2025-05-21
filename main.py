from get_from_jira import GetParsedIssues
from saveFile import SaveAsCsv,SaveAsMd
from OpenAI_GEN import GeneratePatchNotes
import argparse
import Settings as s
import credentials as c

def parse_arguments(): 
    parser = argparse.ArgumentParser(description='Use the JIRA and OpenAI api to generate patch notes and or just get a list of all of them')
    parser.add_argument('--csv','-c', default='', type=str,  help='exports a csv of given name')
    parser.add_argument('--openai','--md','-o','-m', default='', type=str,  help='use openAI to automatically generate markdown file of notes ')
    parser.add_argument('--apiTest','--test','--testApi','-t', action='store_true', help='test the api credentials for both jira and openai without generating anything')
    return parser



if (__name__=="__main__"):
    print("\n")
    parser =parse_arguments()
    args = parser.parse_args()
    makeCsv = args.csv
    makeMd = args.openai
    test = args.apiTest

    if test: print("Testing API credentials:")
    if makeCsv: print(f"Creating CSV from all the tickets in jira board {s.BOARD}, column '{s.JIRACOLUMN}':")
    if makeMd: print(f"Creating a markdown file using openAI from all the tickets in jira board {s.BOARD}, column '{s.JIRACOLUMN}':")

    if not makeMd and not makeCsv and not test:
        print(makeCsv)
        print("Please see instructions, specify either csv or openai")
        parser.print_help()
        exit()

    if test: APIsuccess = c.CheckCredentials(True,True)
    else: APIsuccess = c.CheckCredentials(makeCsv or makeMd,makeMd)

    if not APIsuccess: exit()
    if test: exit() #

    issues = GetParsedIssues()
    if makeMd: 
        patch_notes = GeneratePatchNotes(issues)
        SaveAsMd(s.OUTPUTFOLDERmd)

            
    if makeCsv:
        SaveAsCsv(s.OUTPUTFOLDERcsv,makeCsv,issues)


    


