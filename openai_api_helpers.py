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
            "content": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n    <link rel=\"stylesheet\" href=\"https://assets.ea.asu.edu/ulc/css/stylesheet.css\">\n    <title>[Course Code] | [Title of the Video]</title>\n</head>\n<body>\n<main>\n<header>\n    <h1>[Course Code] | [Title of the Video]</h1>\n</header>\n<div>\n    <h2>[Speaker Name]</h2>\n    <p>[Transcript text paragraph 1]</p>\n    <h3>[Subheading if applicable]</h3>\n    <p>[Transcript text paragraph 2]</p>\n    <!-- Additional paragraphs follow the same pattern -->\n</div>\n</main>\n<footer>\n    <hr>\n    <img src=\"https://assets.ea.asu.edu/ulc/images/asu_header%20logo%20small%20200%20px.png\" alt=\"ASU Web Logo\">\n    <br>\n    <p>This page was created by <a href=\"https://ea.asu.edu/\">ASU Universal Learner Courses.</a></p>\n</footer>\n</body>\n</html>\n"
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
                "content": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n    <link rel=\"stylesheet\" type=\"text/css\" href=\"https://assets.ea.asu.edu/ulc/css/stylesheet.css\">\n    <title>Module - 4 - Tableau - Make your first Chart.mp4</title>\n</head>\n<body>\n<main>\n    <header><h1>Module - 4 - Tableau - Make your first Chart.mp4</h1></header>\n    <div><p>Hello learners, welcome to CIS 310. Let's start creating our first visualization. But before we do that, let's start to learn a little bit about what the visualization screen looks like. We're going to start with a simple example. I know in the last video series, we saw a little bit of what everything Tableau can connect to. But for this example, we're just going to use Microsoft Excel and download the stationary dataset that has been provided.</p><p></p><p>And this is the screen that we see for data manipulation. But this is mainly just for making sure that the data we have is in the correct format. So let's say for example, here we have date in string format, but we want it to be in date format. So I'm just going to change this to date. I'm just going to check everything else looks good. Our units are in number format, which is great.</p><p></p><p>Now let's go, like here, there's options shown here. Go to worksheet. I'm just going to click on worksheet right here. And let's focus on some of the areas that a worksheet has. One of the biggest screen that you will see over here is blank sheet, which is called a canvas. And all of these small bars, which is pages, filters, and this marks, they're called cards.</p><p></p><p>And on this sidebar, what you will notice is that Tableau has done a fantastic job of segmenting our columns into something called dimensions and measures. Now, what are dimensions and what is a measure? Think of this, and they're color-coded. There's blue for dimensions and green for measures. But think of them as anything blue is your text, your string, your date values. Anything green is your numerical values. They, you can do your aggregation, your sum, your averages on the green values. And you can get your blue values, which is your dimensions, into the rows and columns to get the depth or the details in your data.</p><p></p><p>So apart, just me going, showing this and talking to you about it might not help. So let me show what this actually works. And Tableau is very intuitive. The way the whole thing works is by dragging and dropping. And they're called pills. You can see these items are called pills because of the way they have this shape around it. But you can just drag them.</p><p></p><p>So let's say I want to create a very simple visualization to start with. What I'm going to do is I'm going to drag region, put it into columns. Now I have three columns, which has every region possible. Now I'm going to, but this does not make sense because it does not have any values in it, right? I'm going to take the total sales that happened in these region and drag it right over here. There, there we go. And you see that it has already populated the sheets over here.</p><p></p><p>Now, this is not a chart, right? This is not, this is not, this is just a data value. And I can get this from Excel as well. How can I make it different? I'm just going to drag this and put it right over here. There you go. This is not very intuitive either. So I'm just going to swap it by using this swap. This is where things get a little bit interesting, right? Like we now start getting these visualizations that we need and we can expand them. So I'm going to take this order date, take it to columns. I have expanded on what central east and west region can do based in all the years.</p><p></p><p>So I can definitely see that the central has been from 2021, 2022 and their sales increased. But on the case of east, their sales start to decrease. These very simple inferences that you can start gaining from this exploration is what you want to start doing in this module.</p><p></p><p>For this assessment in this module, we are going to go over all these different, simple different methods of chart making that can happen. And let me, let's just remove all this and start from scratch, which is what I want to show. One of the most important feature over here is called show me. And the way the show me works is that you can select any two dimension and a measure and it'll automatically recommend you what is a good chart for it. So let's, I'm going to select order date and total. We're here to show. And it automatically tells me that the line chart for me is the best chart. I'm just going to put it right over here. Here, there you go.</p><p></p><p>And we already know that overall for the stationary sales from 2021 to 2022, it was increased, but from 2022 to 2023, it decreased. And I can expand this a little bit more by using what is the marks card. The marks card is a little bit different from filters and pages. Filters is a simple card. Over here, as it shows, like if I want to filter this out by a certain region, I can just go put the region, select central, press okay. All the values now just show me central region values.</p></div>\n</main>\n<footer>\n    <hr>\n    <img src=\"https://assets.ea.asu.edu/ulc/images/asu_header%20logo%20small%20200%20px.png\" alt=\"ASU logo\">\n    <br>\n    <p>This page was created by Universal Learner Courses. Visit <a href=\"https://ea.asu.edu/\">ASU Universal Learner courses</a> to learn more.</p>\n</footer>\n</body>\n</html>"
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"
    