import re


def clean_text(text):
    """
    Clean and normalize extracted resume text.
    """

    # Convert text to lowercase
    text = text.lower()

    # Keep important technical symbols such as c++, c#, and .net
    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)

    # Replace multiple spaces/newlines with a single space
    text = re.sub(r"\s+", " ", text)

    # Remove unnecessary spaces around the text
    text = text.strip()

    return text