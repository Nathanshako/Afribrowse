import json
import re
from collections import Counter

class AfribrowseEngine:
    def __init__(self, data_path="data/sample_data.json"):
        self.data_path = data_path
        self.documents = []
        self.load_data()

    def load_data(self):
        """Loads the offline JSON database."""
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                self.documents = json.load(f)
        except FileNotFoundError:
            self.documents = []
            print(f"Warning: {self.data_path} not found. Start with an empty dataset.")

    def clean_text(self, text):
        """Converts text to lowercase and removes punctuation for fair matching."""
        return re.findall(r'\w+', text.lower())

    def search(self, query):
        """
        Searches the offline documents and scores them based on keyword frequency.
        Returns a sorted list of documents based on relevance.
        """
        query_words = self.clean_text(query)
        if not query_words:
            return []

        results = []

        for doc in self.documents:
            score = 0
            # Clean the title and content to search through them
            title_words = self.clean_text(doc.get("title", ""))
            content_words = self.clean_text(doc.get("content", ""))

            # Count word occurrences
            title_counts = Counter(title_words)
            content_counts = Counter(content_words)

            for word in query_words:
                # Keywords found in the TITLE are worth more weight (e.g., 5 points)
                if word in title_counts:
                    score += title_counts[word] * 5
                # Keywords found in the CONTENT are worth standard weight (1 point)
                if word in content_counts:
                    score += content_counts[word]

            # If the document matched any query words, keep it
            if score > 0:
                results.append({
                    "id": doc["id"],
                    "title": doc["title"],
                    "url": doc["url"],
                    "snippet": doc["content"][:160] + "...",  # Create a search snippet
                    "score": score
                })

        # Sort results so the highest scoring document appears first
        return sorted(results, key=lambda x: x["score"], reverse=True)