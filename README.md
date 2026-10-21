# ThittamTrack

> Making Tamil Nadu budget information easier to find and understand in Tamil and English.

## Problem

Journalists often spend a lot of time searching through government budget PDFs to find one figure or confirm a claim. The information may be spread across several documents, and some are available in Tamil while others are available only in English. ThittamTrack is designed to make this research easier. Users can ask a question in either language, and the system uses RAG to find relevant passages from official budget documents and generate an answer with citations.

## Who it is for

- Journalists reporting on Tamil Nadu government spending and public schemes.
- Researchers and citizens who want to understand or verify information in the Tamil Nadu budget.

## Signature feature

Ask a question in Tamil or English and get an answer based on official budget documents, with source details and matching Tamil-English passages shown when available.

## Hardest problem (my interview story)

One of the biggest challenges is helping the system find the right information even when the question and the document use different languages. For example, someone might ask a question in Tamil while the relevant budget detail appears in an English PDF. The system also needs to keep track of the correct year, budget version, and page number so that answers can be checked. I plan to test retrieval with 60 questions—30 in Tamil and 30 in English—and aim for at least 85% Recall@5. I will also test whether the answers and citations are actually correct.

## Dataset

| Source | Link | Documents | Pages | Licence / terms |
|---|---|---:|---:|---|
| Tamil Nadu Finance Department — budget publications | https://financedept.tn.gov.in/en/budget-speech | To be counted | Target: 2,500+ pages | Official government publications. Check the website's terms and copyright notices before redistributing documents or extracted content. |

**Planned coverage:** At least five budget years, including Tamil and English budget speeches where available, Budget Highlights, the Citizen's Guide to Budget, Interim and Revised Budget 2026–27 documents, and the Economic Survey of Tamil Nadu. I will confirm which documents and language versions are available before adding them.

## 10 real questions

See [docs/QUESTIONS.md](docs/QUESTIONS.md).

The questions will cover Tamil questions answered using English sources, English questions answered using Tamil sources, and questions where the source and question are in the same language. I will check each question against the official documents before using it for evaluation.

## Run it

These are the planned commands for a Python FastAPI version of the project. They will work once the application files and dependencies are in place.

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements-dev.txt

# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env

uvicorn app.main:app --reload
curl http://localhost:8000/health
```

Create `.env` from `.env.example` and add any required credentials locally. Keep API keys and passwords out of GitHub. If I choose Django or a different backend, I will update these commands to match the actual project.

## How it works

1. **Collect the documents:** Download budget PDFs from official sources.
2. **Extract the text:** Read the PDF text and use OCR for scanned pages when needed.
3. **Prepare the passages:** Split the text into smaller sections and keep details such as language, year, document name, and page number.
4. **Find relevant information:** Use multilingual embeddings to search for passages by meaning, including across Tamil and English.
5. **Write an answer:** Give the retrieved passages to the language model so it can answer using the available evidence.
6. **Show the sources:** Include the document and page details so users can check the answer themselves. If the evidence is not clear, the system should say so instead of guessing.

## Future updates

These are features I would like to add as the project develops:

- **Hybrid search:** Combine meaning-based search with keyword search to improve results for exact figures and department names.
- **Stronger testing:** Check Tamil-to-English, English-to-Tamil, and same-language retrieval separately.
- **Citation checks:** Test whether answers are supported by the cited passages and whether the page numbers are correct.
- **Budget comparisons:** Make it easier to compare Interim and Revised Budget figures without mixing up years or categories.
- **Side-by-side translations:** Show the matching Tamil and English passages together when both versions exist.
- **Fact-checking:** Let users enter a claim and receive a provisional True, False, or Misleading assessment based on official evidence. A journalist should review the evidence before publishing.
- **Background processing:** Process large collections of PDFs without making users wait on one long request.
- **User accounts:** Allow journalists to sign in and save useful questions and answers.
- **Deployment and performance testing:** Publish the application, check how quickly it responds, and estimate running costs.

These are future plans, not features that are already finished. I will update this section as each feature is built and tested.

## Evaluation goals

- Prepare 60 questions: 30 in Tamil and 30 in English.
- Measure Recall@5 for Tamil-to-English, English-to-Tamil, and same-language retrieval.
- Aim for at least 85% Recall@5 and report the separate results too.
- Check answer accuracy, citation accuracy, and how the system handles questions it cannot answer from the documents.

## Live link

Not available yet — planned for Week 2.

## Project status

The project is in the planning and setup stage. Document processing, multilingual RAG search, answers with citations, evaluation, and deployment still need to be built and tested.
