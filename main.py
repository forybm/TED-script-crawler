import re
import sys

import requests
from bs4 import BeautifulSoup
from fpdf import FPDF


def _save_as_txt(file_name, paragraphs):
    with open(f"{file_name}.txt", "w") as f:
        for paragraph in paragraphs:
            cues = paragraph["cues"]
            for cue in cues:
                text = cue["text"].replace("\n", "") + "\n"
                f.writelines(text)

            f.writelines("\n")


def _save_as_pdf(file_name, paragraphs):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("NanumSquareR", "", "NanumSquareR.ttf", uni=True)  # 한글 작성이 가능한 폰트 추가
    pdf.set_font("NanumSquareR", size=12)

    for paragraph in paragraphs:
        cues = paragraph["cues"]
        for cue in cues:
            text = cue["text"].replace("\n", " ")
            pdf.cell(200, 10, txt=text.encode("utf-8").decode(), ln=1)

        pdf.cell(200, 10, txt="\n", ln=1)

    pdf.output(f"{file_name}.pdf")
    pdf.close()


def main(link):
    talks = link.split("/")[-1]

    rsp = requests.get(link)
    soup = BeautifulSoup(rsp.text, "html.parser")

    _meta = soup.find("meta", attrs={"name": "twitter:app:url:ipad"})
    _content = _meta.attrs["content"]
    script_id = re.search(r"\d+", _content).group()

    languages = ("en", "ko")
    script = "https://www.ted.com/talks/{id}/transcript.json?language={language}"

    for language in languages:
        file_name = f"{talks}_{language}"
        _link = script.format(id=script_id, language=language)
        response = requests.get(_link)
        result = response.json()
        paragraphs = result["paragraphs"]

        _save_as_pdf(file_name, paragraphs)        


if __name__ == "__main__":
    link = sys.argv[1]
    main(link)
