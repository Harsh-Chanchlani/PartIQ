import fitz
from pathlib import Path


def extract_pdf(pdf_path: str):

    document = fitz.open(pdf_path)

    extracted_pages = []

    for page_number, page in enumerate(
        document, start=1
    ):

        text = page.get_text(
            "text",
            sort=True
        ).strip()

        if not text:
            print(
                f"Warning: No text on page {page_number}"
            )
            continue

        extracted_pages.append({
            "page": page_number,
            "text": text
        })

    document.close()

    return extracted_pages


if __name__ == "__main__":

    pages = extract_pdf(
        "data/uploads/ESP32_Datasheet.pdf"
    )

    for page in pages:
        print(
            f"\nPAGE {page['page']}\n"
        )
        print(page["text"][:500])