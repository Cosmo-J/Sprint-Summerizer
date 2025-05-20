import os
import openai
from get_from_jira import GetParsedIssues
import credentials as c

openai.api_key = c.OPENAI_API_KEY


def GeneratePatchNotes(issues):


    issue_summaries = []
    for idx, issue in enumerate(issues, start=1):
        title = issue.get("title", "No title")
        desc = issue.get("description", "No description")
        solver = issue.get("solver", "No solver")
        reporter = issue.get("reporter", "No reporter")
        issue_type = issue.get("type", "Unknown type")
        link = issue.get("link", "No link")

        summary = (
            f"Issue #{idx}:\n"
            f"  - Title: {title}\n"
            f"  - Type: {issue_type}\n"
            f"  - Description: {desc}\n"
            f"  - Reporter: {reporter}\n"
            f"  - Solver: {solver}\n"
            f"  - Link: {link}\n"
        )
        issue_summaries.append(summary)

    combined_issues_text = "\n".join(issue_summaries)
    #TODO: read from prompt.tx
    prompt = (
        "You are an assistant that generates concise, developer-friendly patch notes. "
        "Using the following list of issues, please create clear, short patch notes: \n\n"
        f"{combined_issues_text}\n\n"
        "Output patch notes in bullet points. "
        "Each bullet should summarize the fix/change, referencing relevant items. "
        "Use developer-friendly language."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You produce patch notes for software updates."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=500
    )

    # Extract the assistant's output
    patch_notes = response["choices"][0]["message"]["content"].strip()
    return patch_notes