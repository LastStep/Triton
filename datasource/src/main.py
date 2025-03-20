from pydantic import BaseModel
from pprint import pprint
import json
from fastapi import FastAPI, HTTPException, Query, Response
import uvicorn
import os
from . import api_ProjectGutenberg

parameters = {
    "allEnglish" : {"mode":"export","output_dir":"allEnglish","tagged":False,"lemma":False,"persName":True,"placeName":True,"not_display_tags":[],"output_format":"TEI","randomize_order":True,"lexical_tags":[],"subcorpus1_restrictions":{"Genre":["fiction","nonfiction","play","poetry","periodical"],"Language":"English","wanted_tags":["front","docTitle","div:preface","contents","div:introduction","body","head","back","afterword","note","said","div:prologue","div:epilogue|play","div:epilogue|prose","lg|poetry","lg|play","castList","speaker","set","stage","p|play","p|poetry","p|prose"],"not_wanted_tags":[],"lexical_restrictions":[]},"num_subcorpora":1,"save_filename":"allEnglish","id":"412460"}
}
# print(json.dumps(parameters, indent=4))

GutenbergMetadata = {
    "Author": [ "Robert Carlton Brown" ],
    "Author Birth": [ 1886 ],
    "Author Death": [ 1959 ],
    "Author Given": [ "Robert Carlton" ],
    "Author Surname": [ "Brown" ],
    "Copyright Status": [ "Not copyrighted in the United States." ],
    "Language": [ "English" ],
    "LoC Class": [ "SF: Agriculture: Animal culture" ],
    "Num": "14293",
    "Subject": [ "Cookery (Cheese)", "Cheese" ],
    "Title": [ "The Complete Book of Cheese" ],
    "charset": "iso-8859-1",
    "gd-num-padded": "14293",
    "gd-path": "142/14293.txt",
    "href": "/1/4/2/9/14293/14293_8.zip"
}
class BookMetadata(BaseModel): 
    gd_id: str
    gd_path: str 
    author: list = []
    title: list = []


class BookResponse(BaseModel): # Structure for book detail response
    metadata: BookMetadata
    text_content: str


data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "gutenberg-dammit-files-v002.zip")
print(data_path)
# Initialize FastAPI
app = FastAPI()



# Dummy route to check the API status
@app.get("/")
def read_root():
    return {"message": "Welcome to the Poetry API"}

# # Dummy route to get metadata
@app.get("/metadata")
def get_metadata():
    metadata = api_ProjectGutenberg.getMetaData(data_path)
    return {"metadata_count": len(metadata)}

# # Dummy route to get poems by author
# @app.get("/books/")
# async def get_poems_by_author(author: str = Query(None)):
#     author_books = [entry for entry in metadata if author.lower() in " ".join(entry.get('Author', [])).lower()]
#     if not author_books:
#         return {"message": "No books found for this author"}
#     # book_data = retrieve_one(data_path, author_books[0])
#     book_data = author_books[0]
#     result = BookMetadata(
#             gd_id=book_data['gd-num-padded'], 
#             gd_path=book_data['gd-path'], 
#             author=book_data.get('Author', []),
#             title=book_data['Title'],
#         )
#     # final_text = text[2655:5500]
#     return result

# @app.get("/books/poetry/id")
# def get_poetry_books():
#     poetryBookIDs = []
#     for entry in metadata:
#         if 'poetry' in " ".join(entry.get('Subject', [])).lower():
#             poetryBookIDs.append(entry['Num'])

#     return poetryBookIDs

# @app.get("/books/text/")
# async def getBookByID(bookID: int = Query(None)):
#     results = []
#     for info, text in searchandretrieve(data_path, {'Num': f'{bookID}'}):
#         results.append(text)

#     if not results:
#         raise HTTPException(status_code=404, detail=f"Book with ID '{bookID}' not found")

#     # Assuming searchandretrieve returns a list, and you want to return the first text found
#     text_content = results[0] if results else None

#     if text_content is None:
#         raise HTTPException(status_code=404, detail=f"Text content not available for book ID '{bookID}'")

#     return Response(content=text_content, media_type="text/plain")

# poetry_metadata = [entry for entry in metadata if 'American poetry' in entry.get('Subject', [])]
# print(len(poetry_metadata))
# pprint(poetry_metadata[10])
# author_books = [entry for entry in metadata if 'Robert Frost' in entry.get('Author', [])]
# pprint(author_books)
# text = retrieve_one(data_path, author_books[0]['gd-path'])

# final_text = text[2655:5500]
# print(final_text)

# Load a pre-trained model from Hugging Face

# messages = f"Extract the names of the poems from the following text: {final_text}"
# pipe = pipeline("summarization", model="facebook/bart-large-mnli")

# result = pipe(messages)

# print(result)

# Run the FastAPI application
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)


