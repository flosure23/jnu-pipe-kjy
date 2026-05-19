from app.config import MODEL_MODE
from app.model_loader import load_model


def check_spam_rules(text: str) -> tuple[str, int]:
    text = text.lower().strip()

    if text == "":
        return "ham", 0

    spam_keywords = [
        "free", "win", "winner", "prize", "click",
        "buy now", "urgent", "cash", "money", "offer", "deal"
    ]

    hit = 0

    for kw in spam_keywords:
        if kw in text:
            hit += 1

    label = "spam" if hit >= 2 else "ham"

    return label, hit


def check_spam_ml(text: str) -> tuple[str, float]:
    text = text.strip()

    if text == "":
        return "ham", 0.0

    model = load_model()

    pred = model.predict([text])[0]

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba([text])[0]
        classes = list(model.classes_)
        pred_index = classes.index(pred)
        score = float(proba[pred_index])
    else:
        score = 1.0

    return pred, score


def check_spam(text: str) -> tuple[str, float]:
    if MODEL_MODE in ["ml", "mlflow"]:
        return check_spam_ml(text)

    return check_spam_rules(text)