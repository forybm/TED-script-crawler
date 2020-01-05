import re

import requests
from bs4 import BeautifulSoup


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
        with open(f"{talks}_{language}.txt", "w") as f:
            _link = script.format(id=script_id, language=language)
            response = requests.get(_link)
            result = response.json()
            paragraphs = result["paragraphs"]
            for paragraph in paragraphs:
                cues = paragraph["cues"]
                for cue in cues:
                    text = cue["text"].replace("\n", "") + "\n"
                    f.writelines(text)

                f.writelines("\n")


if __name__ == "__main__":
    link = ""  # Enter the TED talks link
    main(link)
