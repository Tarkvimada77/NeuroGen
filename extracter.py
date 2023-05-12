from pdfminer.high_level import extract_text
from bs4 import BeautifulSoup
import os
import docx
import re

class Extracter:
    def __init__(self, file):
        self.file = file
        self.result = ""

    def extract(self):
        if self.file[-3:] == "txt":
            with open(self.file, "r", encoding="utf-8") as f:
                self.result = f.read()
            self.result.replace("\ufeff", "")
            self.result.replace(r"\n", " ")
            self.result = re.sub(r'[^А-я ]', '', self.result)
            self.result = " ".join(self.result.split())

            return self.result.lower()

        elif self.file[-3:] == "pdf":

            self.result = extract_text(self.file)
            self.result.replace("\ufeff", "")
            self.result.replace(r"\n", " ")
            self.result = re.sub(r'[^А-я ]', '', self.result)
            self.result = " ".join(self.result.split())

            return self.result.lower()

        elif self.file[-3:] == "fb2":
            spis_xml = []
            os.rename(self.file, "res.xml")

            with open("res.xml", "r", encoding="utf-8") as f:
                spis_xml = f.readlines()

            spis_xml = "".join(spis_xml)

            soup = BeautifulSoup(spis_xml, "lxml")
            content = soup.find_all('p')

            for i in content:
                self.result = self.result + " " + i.get_text(strip=True)

            self.result.replace("\ufeff", "")
            self.result = re.sub(r'[^А-я ]', '', self.result)

            return self.result

        elif self.file[-4:] == "docx":
            dc = docx.Document(self.file)

            for i in dc.paragraphs:
                self.result = self.result + "\n" + i.text

            self.result.replace("\ufeff", "")
            self.result.replace(r"\n", " ")
            self.result = re.sub(r'[^А-я ]', '', self.result)
            self.result = " ".join(self.result.split())

            return self.result.lower()
        else:
            return "Невозможно Преобразовать!"


a = Extracter("skot.txt")

with open("a.txt", "w", encoding="utf-8") as f:
    f.write(a.extract())

