import re


def extract_page_title(doc: str) -> str:
    title_matches = re.findall(r"^# (.+)$", doc, re.MULTILINE)

    if title_matches is None or len(title_matches) != 1:
        raise ValueError("page must have one h1 title", doc)

    return title_matches[0]
