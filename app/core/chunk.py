#from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

import sys
print(sys.executable)


def split_text(text: str) -> list[str]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=250,
        chunk_overlap=50,
        length_function=len,
    )

    chunks = splitter.split_text(text)

    return chunks