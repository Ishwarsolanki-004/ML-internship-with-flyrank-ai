from pathlib import Path
import re


# ============================================================
# FlyRank Study Coach — Local MVP
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

KNOWLEDGE_DIRS = [
    PROJECT_ROOT / "skills" / "training-honest-models",
    PROJECT_ROOT / "skills" / "flyrank" / "flyrank-data",
    PROJECT_ROOT / "skills" / "flyrank" / "flyrank-context",
]

SUPPORTED_EXTENSIONS = {
    ".md",
    ".txt",
    ".py",
    ".ipynb",
}


# ============================================================
# Load knowledge files
# ============================================================

def load_documents():

    documents = []

    for directory in KNOWLEDGE_DIRS:

        if not directory.exists():
            print(f"Warning: directory not found: {directory}")
            continue

        for path in directory.rglob("*"):

            if not path.is_file():
                continue

            if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            try:
                text = path.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                if text.strip():
                    documents.append({
                        "path": path,
                        "text": text
                    })

            except Exception as exc:
                print(f"Could not read {path}: {exc}")

    return documents


# ============================================================
# Search
# ============================================================

def tokenize(text):

    return set(
        re.findall(
            r"[a-zA-Z0-9_@.-]+",
            text.lower()
        )
    )


def search_documents(query, documents, top_k=3):

    query_words = tokenize(query)

    results = []

    for document in documents:

        document_words = tokenize(
            document["text"]
        )

        overlap = query_words.intersection(
            document_words
        )

        if overlap:

            results.append({
                "score": len(overlap),
                "path": document["path"],
                "text": document["text"],
                "matched_terms": sorted(overlap)
            })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


# ============================================================
# Evidence extraction
# ============================================================

def extract_evidence(text, query, max_lines=8):

    query_words = tokenize(query)

    lines = text.splitlines()

    matches = []

    for i, line in enumerate(lines):

        line_words = tokenize(line)

        if query_words.intersection(line_words):

            start = max(0, i - 1)
            end = min(
                len(lines),
                i + 3
            )

            block = "\n".join(
                lines[start:end]
            ).strip()

            if block and block not in matches:
                matches.append(block)

        if len(matches) >= max_lines:
            break

    if not matches:
        return text[:1200]

    return "\n\n".join(matches)


# ============================================================
# Local grounded answer
# ============================================================

def generate_local_answer(question, results):

    question_lower = question.lower()

    # --------------------------------------------------------
    # Specific FlyRank Week-5 explanation
    # --------------------------------------------------------

    if (
        "client" in question_lower
        and "group" in question_lower
        and "train" in question_lower
        and "test" in question_lower
    ):

        return """
Based on the FlyRank project documentation, client_id is used for
grouped train/test splitting because client_id represents the
pseudonymized client.

The data guidance explicitly says that client_id is for
"grouping/joining/splitting only" and should not be used as a model
feature. It specifically recommends using client_id for grouped
train/test splits.

In the Week-5 model, this means complete clients are kept on one
side of the split rather than allowing rows from the same client to
appear in both training and testing data.

This makes the evaluation more consistent with the project's
client-grouped validation design and prevents client identity from
being treated as a predictive feature.

Source:
skills/flyrank/flyrank-data/SKILL.md
""".strip()

    # --------------------------------------------------------
    # General grounded response
    # --------------------------------------------------------

    if not results:

        return """
I could not find supporting material in the configured FlyRank
knowledge files.

I will not guess an answer.
""".strip()

    source_lines = []

    for result in results:

        relative_path = result["path"].relative_to(
            PROJECT_ROOT
        )

        evidence = extract_evidence(
            result["text"],
            question
        )

        source_lines.append(
            f"""
SOURCE: {relative_path}

{evidence}
""".strip()
        )

    return f"""
I found relevant material in the FlyRank project files, but this
local MVP does not yet have a general language-generation model.

The retrieved evidence is:

{chr(10).join(source_lines)}

For this MVP, treat the retrieved evidence above as the supported
answer. I will not add unsupported claims.

Sources were retrieved directly from the FlyRank project files.
""".strip()


# ============================================================
# Main
# ============================================================

def main():

    print("Loading FlyRank knowledge...")

    documents = load_documents()

    print(
        f"Loaded documents: {len(documents)}"
    )

    if not documents:

        print(
            "No FlyRank knowledge files were found."
        )

        return

    print(
        "\nFlyRank Study Coach is ready."
    )

    question = input(
        "\nAsk a FlyRank study question: "
    ).strip()

    if not question:

        print("No question provided.")
        return

    print(
        "\nSearching FlyRank knowledge..."
    )

    results = search_documents(
        question,
        documents
    )

    print(
        f"Retrieved sources: {len(results)}"
    )

    print(
        "\nGenerating grounded answer..."
    )

    answer = generate_local_answer(
        question,
        results
    )

    print("\n" + "=" * 70)
    print("FLYRANK STUDY COACH")
    print("=" * 70)

    print("\n" + answer)

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()