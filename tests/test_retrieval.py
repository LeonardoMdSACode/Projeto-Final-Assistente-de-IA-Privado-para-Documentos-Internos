# test_retrieval.py

from app.services.retrieval_service import search


results = search(
    "Quantos dias de férias existem?"
)

for result in results:

    print("=" * 50)

    print(result["document"])
    print(result["score"])

    print(result["text"])
