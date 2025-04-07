from pydantic import BaseModel
import json
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from .data import api_ProjectGutenberg
from .model import api_LLM

parameters = {
    "allEnglish" : {"mode":"export","output_dir":"allEnglish","tagged":False,"lemma":False,"persName":True,"placeName":True,"not_display_tags":[],"output_format":"TEI","randomize_order":True,"lexical_tags":[],"subcorpus1_restrictions":{"Genre":["fiction","nonfiction","play","poetry","periodical"],"Language":"English","wanted_tags":["front","docTitle","div:preface","contents","div:introduction","body","head","back","afterword","note","said","div:prologue","div:epilogue|play","div:epilogue|prose","lg|poetry","lg|play","castList","speaker","set","stage","p|play","p|poetry","p|prose"],"not_wanted_tags":[],"lexical_restrictions":[]},"num_subcorpora":1,"save_filename":"allEnglish","id":"412460"}
}
# print(json.dumps(parameters, indent=4))



app = FastAPI()
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)


# Dummy route to check the API status
@app.get("/")
def read_root():
    return {"message": "Welcome to the Poetry API"}

# # Dummy route to get metadata
@app.get("/metadata")
def get_metadata():
    metadata = api_ProjectGutenberg.getMetaData()
    return {"metadata_count": len(metadata)}

# # Dummy route to get poems by author
@app.get("/books/")
async def getBooksByAuthor(author: str = Query(None)):
    response = api_ProjectGutenberg.getBooksByAuthor(author)
    return response

@app.get("/book/")
async def getBookByID(bookID: int = Query(None)):
    response = api_ProjectGutenberg.getBookByID(bookID)
    if type(response) == api_ProjectGutenberg.ErrorResponse:
        raise HTTPException(status_code=404, detail=response.message)
    
    print(response.metadata)
    return Response(content=response.text_content, media_type="text/plain")


# final_text = text[2655:5500]
# print(final_text)
@app.get("/model/")
async def promptModel(text: str = Query(...)):
    poem_response = api_LLM.extractPoemTitles(text)
    poem_response_json = json.dumps(poem_response, indent=4)
    return Response(content=poem_response_json, media_type="json")

# Run the FastAPI application
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)


