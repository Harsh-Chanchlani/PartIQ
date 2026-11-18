def chunk_page(
    text,
    max_chars=2500,
    overlap_chars=400
):

    paragraphs = [
        p.strip()
        for p in text.split("\n")
        if p.strip()
    ]

    chunks = []
    current = ""

    for paragraph in paragraphs:

        candidate = (
            current + "\n" + paragraph
        ).strip()

        if len(candidate) > max_chars and current:
            chunks.append(current)

            # Preserve some previous context
            current = current[
                -overlap_chars:
            ] + "\n" + paragraph

        else:
            current = candidate

    if current.strip():
        chunks.append(current.strip())

    return chunks