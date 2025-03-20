from gutenbergdammit.ziputils import retrieve_one, loadmetadata, searchandretrieve
# from GutenTag import GutenTag


def getMetaData(data_path: str):
    metadata = loadmetadata(data_path)
    return metadata
