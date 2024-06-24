""" We are checking to see which class can be used to parse the
contents of a file, using a for loop iterating over four choices.
"""

from abc import ABC, abstractmethod
from typing import List
from QuoteEngine import QuoteModel

import pandas, random, subprocess, os, docx

class IngestorException(Exception):
    "Raised when unable to ingest file"
    pass


class IngestorInterface(ABC):
    allowed_extensions = ['docx','pdf','txt','csv']

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        ext = path.split('.')[-1]
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel.QuoteModel]:
        pass


class DocxIngestor(IngestorInterface):
    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel.QuoteModel]:
        if not cls.can_ingest(path):
            raise IngestorException()

        quotes = []
        doc = docx.Document(path)

        for paragraph in doc.paragraphs:
            if paragraph.text != '':
                parse = paragraph.text.split('-')
                new_quote = QuoteModel.QuoteModel(parse[0], parse[1])
                quotes.append(new_quote)
        return quotes


class PDFIngestor(IngestorInterface):
    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel.QuoteModel]:
        if not cls.can_ingest(path):
            raise IngestorException()

        tmp_file_name = f'./tmp/{random.randint(0, 10000)}.txt'
        call = subprocess.call(['./pdftotext', path, tmp_file_name])

        quotes = []
        with open(tmp_file_name, "r", encoding='utf-8') as tmp_file:
            for idx, line in enumerate(tmp_file):
                parsed = line.strip().split('-')
                if parsed != ['']:
                    new_quote = QuoteModel.QuoteModel(parsed[0], parsed[1])
                    quotes.append(new_quote)
        return quotes


class TextIngestor(IngestorInterface):
    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel.QuoteModel]:
        if not cls.can_ingest(path):
            raise IngestorException()

        quotes = []

        with open(path, "r", encoding='utf-8') as file_contents:
            for idx, line in enumerate(file_contents):
                parsed = line.strip().split('-')
                new_quote = QuoteModel.QuoteModel(parsed[0], parsed[1])
                quotes.append(new_quote)
        return quotes


class CSVIngestor(IngestorInterface):
    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel.QuoteModel]:
        if not cls.can_ingest(path):
            raise IngestorException()

        quotes = []
        c = pandas.read_csv(path, header=0)

        for index, row in c.iterrows():
            new_quote = QuoteModel.QuoteModel(row['body'], row['author'])
            quotes.append(new_quote)
        return quotes


class Ingestor(IngestorInterface):
    importers = [DocxIngestor, TextIngestor,
                 CSVIngestor, PDFIngestor]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel.QuoteModel]:
        for importer in cls.importers:
            if importer.can_ingest(path):
                return importer.parse(path)
