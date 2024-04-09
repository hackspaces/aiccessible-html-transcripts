from openai_api_helpers import call_to_gpt4_cleaner, call_to_gpt4_as_htmlcreator
from jinja2 import Environment, FileSystemLoader


def create_html_transcript_direclty_gpt4(transcript_text, gpt4_switch, speaker_name_text=None):
    """
    Creates an HTML transcript from the given transcript text.

    :param transcript_text: The transcript text to be converted to HTML.
    :return: The HTML transcript
    """
    transcript_text = transcript_text
    speaker_name_text = speaker_name_text
    full_html = ""
    if gpt4_switch is True:
        print("Calling GPT-4 for HTML creation")
        # Call the GPT-4 API to reformat the transcript
        clean_up_transcript =  call_to_gpt4_cleaner(transcript_text)
        full_html = call_to_gpt4_as_htmlcreator(clean_up_transcript)
        print("GPT-4 HTML creation complete")
        
    return full_html

def create_html_transcript(title, transcript_text, gpt4_switch, speaker_name=None):
    """
    Creates an HTML transcript from the given transcript text.

    :param transcript_text: The transcript text to be converted to HTML.
    :return: The HTML transcript
    """
    transcript_text = transcript_text
    #Split the transcript into paragraphs
    paragraphs = transcript_text.split("\n")
    
    if gpt4_switch is True:
        # Call the GPT-4 API to reformat the transcript
        formatted_transcript = call_to_gpt4_cleaner(transcript_text)
        paragraphs = formatted_transcript.split("\n")
        
    # Setup Jinja2 environment and load the template
    env = Environment(loader=FileSystemLoader(searchpath='./templates'))
    template = env.get_template('template.html')

    #Render the HTML content with dynamic data
    html_content = template.render(speaker_name=speaker_name, title=title, paragraphs=paragraphs, css_file_path= "https://assets.ea.asu.edu/ulc/css/stylesheet.css")

    return html_content
