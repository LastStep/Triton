from typing import List
from gutenbergdammit.ziputils import retrieve_one, loadmetadata, searchandretrieve
# from GutenTag import GutenTag
import os
from pydantic import BaseModel
import json

DATA_ASSETS_FOLDER_NAME = "data-assets"

CORPUS_FILE_NAME = "gutenberg-dammit-files-v002.zip"
# CORPUS_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), DATA_ASSETS_FOLDER_NAME, CORPUS_FILE_NAME)
CORPUS_DATA_PATH = os.path.join(DATA_ASSETS_FOLDER_NAME, CORPUS_FILE_NAME)

METADATA_FILE_NAME = "gutenberg-metadata.json"
METADATA_FILE_PATH = os.path.join(DATA_ASSETS_FOLDER_NAME, METADATA_FILE_NAME)

# METADATA = loadmetadata(CORPUS_DATA_PATH)
with open(METADATA_FILE_PATH, 'r') as f:
    METADATA = json.load(f)

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

class ErrorResponse(BaseModel):
    message: str

class BookMetaData(BaseModel):
    id: int
    gd_id: str
    gd_path: str
    title: list
    subject: list
class AuthorMetaData(BaseModel):
    author: str
    author_birth: int
    author_death: int
    books: List[BookMetaData] = []

class BookResponse(BaseModel): # Structure for book detail response
    metadata: BookMetaData
    text_content: str

def getMetaData():
    return METADATA


def getBooksByAuthor(author: str) -> AuthorMetaData:
    author_books = [entry for entry in METADATA if author.lower() in " ".join(entry.get('Author', [])).lower()]
    if not author_books:
        return ErrorResponse(
            message = "No books found for this author"
        )
    
    books_metadata = []
    for author_book in author_books:
        book_metadata = BookMetaData(
            id = int(author_book['Num']),
            gd_id = author_book['gd-num-padded'], 
            gd_path = author_book['gd-path'], 
            title = author_book.get('Title', []),
            subject = author_book.get('Subject', [])
        )
        books_metadata.append(book_metadata)
    
    first_book = author_books[0]

    author_metadata = AuthorMetaData(
        author = first_book.get('Author', [None])[0],
        author_birth = first_book.get('Author Birth', [None])[0],
        author_death = first_book.get('Author Death', [None])[0],
        books = books_metadata
    )
    return author_metadata

def getBookByID(bookID: int) -> BookResponse:
    bookID = str(bookID)
    for entry in METADATA:
        if entry['Num'] == bookID:
            text = retrieve_one(CORPUS_DATA_PATH, entry['gd-path'])
            book_metadata = BookMetaData(
                id = int(entry['Num']),
                gd_id = entry['gd-num-padded'], 
                gd_path = entry['gd-path'], 
                title = entry.get('Title', []),
                subject = entry.get('Subject', [])
            )
            return BookResponse(metadata=book_metadata, text_content=text)
    return ErrorResponse(
        message = "Book not found"
    )