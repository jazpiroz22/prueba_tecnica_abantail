#from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

import sys
print(sys.executable)


def split_text(text: str) -> list[str]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
    )

    chunks = splitter.split_text(text)

    return chunks