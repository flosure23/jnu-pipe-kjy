from app.spam import check_spam


def test_check_spam_empty():
    label, score = check_spam("")
    assert label == "ham"
    assert score == 0


def test_check_spam_ham():
    label, score = check_spam("hello nice to meet you")
    assert label == "ham"
    assert score == 0


def test_check_spam_spam():
    label, score = check_spam("free prize click now")
    assert label == "spam"
    assert score >= 2


def test_check_spam_case_insensitive():
    label, score = check_spam("FREE Prize")
    assert label == "spam"
    assert score == 2


def test_check_spam_strip_whitespace():
    label, score = check_spam("   free prize   ")
    assert label == "spam"
    assert score == 2