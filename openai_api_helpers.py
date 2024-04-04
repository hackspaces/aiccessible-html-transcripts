from openai import OpenAI
import streamlit as st

open_ai_key = st.secrets["openai_key"]


client = OpenAI(api_key=open_ai_key)

def call_to_whisper(audiofile):
    try: 
        print("Calling Whisper API")
        audiofile = open(audiofile, "rb")
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file = audiofile
        )
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"
    
def call_to_gpt4(prompt, raw_transcription):
    try:
        print("Calling GPT-4 for Cleanup")
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system","content":prompt},
                {"role": "user","content": raw_transcription}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"
    
def call_to_gpt4_cleaner(raw_transcription):
    try:
        prompt_cleaner = "\"You are the AI text-editor\"\nTASK:\nYour task is to reformat the transcript into a more readable format by breaking it into paragraphs to improve readability.\n\nINSTRUCTIONS:\n1. You are provided with a raw transcript from a course video.\n2. Ensure all original content remains intact, and do not add any headers or titles. The aim is to enhance the flow and readability while maintaining the integrity of the original content.\n3. Reformat the transcript to make it more reader-friendly without altering the content or adding titles.\n\nDO:\n1. Follow the instructions\n\nHere is the raw transcript:"
        print("Calling GPT-4 for Cleanup")
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system","content":prompt_cleaner},
                {"role": "user","content": raw_transcription}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"
    
def call_to_gpt4_as_htmlcreator(raw_transcription):
    try:
        print("Calling GPT-4 for Cleanup")
        response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
            "role": "system",
            "content": "Generate a structured HTML document based on the provided template. The HTML should be fully compliant with WCAG 2.1 AA accessibility guidelines, incorporating the provided raw transcript text into the structure without adding or removing any comments or tags from the original template.\n\nReplace \"ABC 100\" in the <title> and <h1> tags with the course code and the title of the transcript file. \nInsert the name of the speaker in the <h2> tag.\nBreak up the raw transcript text into paragraphs, enclosing each paragraph with <p> tags. Insert these paragraphs in the designated section within the <div> tags."
            },
            {
            "role": "assistant",
            "content": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n    <link rel=\"stylesheet\" href=\"https://assets.ea.asu.edu/ulc/css/stylesheet.css\">\n    <title>[Course Code] | [Title of the Video]</title>\n</head>\n<body>\n<main>\n<header>\n    <h1>[Course Code] | [Title of the Video]</h1>\n</header>\n<div>\n    <h2>[Speaker Name]</h2>\n    <p>[Transcript text paragraph 1]</p>\n  <p>[Transcript text paragraph 2]</p>\n    <!-- Additional paragraphs follow the same pattern -->\n</div>\n</main>\n<footer>\n    <hr>\n    <img src=\"https://assets.ea.asu.edu/ulc/images/asu_header%20logo%20small%20200%20px.png\" alt=\"ASU Web Logo\">\n    <br>\n    <p>This page was created by <a href=\"https://ea.asu.edu/\">ASU Universal Learner Courses.</a></p>\n</footer>\n</body>\n</html>\n"
            },
            {
            "role": "user",
            "content": raw_transcription
            }
        ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"
    
def call_to_gpt4_as_accessibiltychecker(html):
    try:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {
                "role": "system",
                "content": "Role: WCAG Compliance Checker\n\nTask:\n\nAnalyze the provided HTML content to evaluate its compliance with the latest Web Content Accessibility Guidelines (WCAG). Your analysis should focus on key accessibility features, including but not limited to semantic HTML structure, alt attributes for images, color contrast, font sizes, ease of navigation, ARIA roles, and keyboard accessibility. WCAG 2.1 consists of 78 success criteria, which are pass-or-fail statements that address accessibility barriers.\n\nOutput:\n\nProduce two outputs based on your analysis:\n\nAccessibility Score: Provide a score from 0 to 100, where 100 indicates full compliance with the latest WCAG guidelines.\n\nFeedback: Offer one sentence of feedback highlighting either a significant area for improvement or an exemplary aspect of the HTML's accessibility. Ensure this feedback is actionable and contains fewer than 50 words."
                },
                {
                "role": "user",
                "content": html
                }
            ],
            temperature=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"
    