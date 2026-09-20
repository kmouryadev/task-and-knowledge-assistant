from app.rag.chunking import chunk_markdown


def test_chunk_markdown_splits_by_heading_and_size():
    text = (
        "# Title\n\n"
        "Intro paragraph.\n\n"
        "## Section A\n\n"
        + ("word " * 300)
        + "\n\n## Section B\n\nShort content."
    )

    chunks = chunk_markdown(text, source="notes/example.md", chunk_size=800, overlap=150)

    assert len(chunks) >= 2
    assert all(c.content.strip() for c in chunks)
    section_names = {c.section for c in chunks}
    assert "Section A" in section_names
    assert "Section B" in section_names


def test_chunk_markdown_overlap_shares_content():
    text = "## Section\n\n" + "".join(f"sentence number {i}. " for i in range(200))

    chunks = chunk_markdown(text, source="notes/example.md", chunk_size=500, overlap=100)

    assert len(chunks) >= 2
    tail = chunks[0].content[-50:]
    assert tail[:20] in chunks[1].content


def test_chunk_markdown_assigns_sequential_indices():
    text = "## Section\n\n" + ("word " * 400)

    chunks = chunk_markdown(text, source="notes/example.md", chunk_size=300, overlap=50)

    assert [c.chunk_index for c in chunks] == list(range(len(chunks)))


def test_chunk_markdown_empty_text_returns_no_chunks():
    assert chunk_markdown("", source="notes/empty.md") == []
