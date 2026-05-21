class SimpleSpamModel:
    """Small local spam classifier used by the checked-in joblib artifact."""

    classes_ = ["ham", "spam"]

    def __init__(self):
        self.spam_keywords = [
            "free",
            "win",
            "winner",
            "prize",
            "click",
            "buy now",
            "urgent",
            "cash",
            "money",
            "offer",
            "deal",
            "reward",
            "verify",
            "payment",
            "claim",
        ]

    def predict(self, texts):
        return [self._predict_one(text) for text in texts]

    def predict_proba(self, texts):
        probabilities = []

        for text in texts:
            score = self._score(text)
            spam_probability = min(0.95, score / 3)
            probabilities.append([1 - spam_probability, spam_probability])

        return probabilities

    def _predict_one(self, text):
        return "spam" if self._score(text) >= 2 else "ham"

    def _score(self, text):
        normalized = text.lower().strip()
        return sum(keyword in normalized for keyword in self.spam_keywords)
