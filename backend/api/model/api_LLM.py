import os, re
from typing import List, Optional, TypedDict
from google import genai
from google.genai import types
import pandas as pd

os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')


googleLLM = genai.Client()

promptExtractTitles = """
You are an expert literary analyst tasked with extracting structured information from poetry book texts.

First identify the content page or table of contents (hearby reffered as TOC_TEXT) in the book text, and then mark the rest of the book as the main text (hereby reffered as MAIN_TEXT).
This gives you a higher strucure of the book. Understand that some books may not have a content page, in which case you will only have the main text.

Your goal is to read the provided book text and identify:

1.  **Section Titles (if any):**  
    - These are larger headings that group multiple poems together. If a section title does not contain multiple poems, then you assume there is no section and keep it blank.
    - You will scan the Section Titles from the TOC_TEXT first, and then move onto the MAIN_TEXT.

2.  **Poem Titles:** 
    - These are the titles of individual poems.
    - You will extract the Poem Titles from the MAIN_TEXT.
    - You will prioritize the Poem Title as it appears at the beginning of the poem itself on the poem's page.
    - You will ignore the TOC_TEXT when extracting Poem Titles.
    
**Important: Output the extracted information in the following format for each poem entry. Use the following format EXACTLY:**

`SECTION_TITLE: <<Section Title or <NONE>>> === TITLE: <<Poem Title>>`

**Each poem entry should be separated by 6 hash charachters "######".**

**Important:** Make sure to wrap the text between "<< >>"

The provided book text is as follows:
"""

class PoemTitleResponse(TypedDict): 
    SectionTitle: Optional[str]
    PoemName: str

class BookResponse(TypedDict): 
    SectionTitle: Optional[str]
    PoemName: str
    PoemContent: str


def parseModelOutput(model_output: str) -> List[PoemTitleResponse]:
    poem_entries: List[PoemTitleResponse] = []
    entries = model_output.split("######") # Split into individual poem entries

    for entry in entries:
        if not entry.strip(): # If entry is empty, then skip the iteration
          continue

        parts = entry.split(" === ")
        pattern = r'<<(.*?)>>'
        section_title = re.findall(pattern, parts[0])[0]
        poem_title = re.findall(pattern, parts[1])[0]

        if section_title == "<NONE>":
            section_title = None

        poem_entries.append({
            "section_title": section_title,
            "poem_title": poem_title,
        })

    return poem_entries

def extractPoemTitles(book_text: str) -> List[PoemTitleResponse]:
    prompt = f"{promptExtractTitles} \n\n {book_text}"

    googleLLM_response = googleLLM.models.generate_content(
        model="gemini-1.5-pro", 
        contents=prompt,
    )

    extractedPoems = parseModelOutput(googleLLM_response.text)
    return extractedPoems