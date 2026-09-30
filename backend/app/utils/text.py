import html
import re


def sanitize_text(text: str) -> str:
    """
    Clean AI-generated text.
    """

    if not text:
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u00a0": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = "".join(
        char
        for char in text
        if char in ("\n", "\t") or ord(char) >= 32
    )

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def format_html_preview(text: str) -> str:
    """
    Convert document text into safe HTML preview.
    """

    clean_text = sanitize_text(text)

    escaped = html.escape(clean_text)

    lines = escaped.split("\n")

    output = []

    for line in lines:

        stripped = line.strip()

        if not stripped:
            output.append(
                "<div class='blank-line'></div>"
            )
            continue

        if stripped.startswith("### "):

            heading = stripped[4:]

            output.append(
                f"<h3>{heading}</h3>"
            )

        elif stripped.startswith("## "):

            heading = stripped[3:]

            output.append(
                f"<h2>{heading}</h2>"
            )

        elif stripped.startswith("# "):

            heading = stripped[2:]

            output.append(
                f"<h1>{heading}</h1>"
            )

        elif re.match(r"^\d+\.\s+", stripped):

            output.append(
                f"<p class='numbered'>{stripped}</p>"
            )

        elif stripped.startswith("- "):

            output.append(
                f"<p class='bullet'>&bull; {stripped[2:]}</p>"
            )

        elif stripped.startswith("* "):

            output.append(
                f"<p class='bullet'>&bull; {stripped[2:]}</p>"
            )

        else:

            output.append(
                f"<p>{stripped}</p>"
            )

    return "\n".join(output)