def check_spam(text: str) -> tuple[str, int]:
    # 소문자 변환 및 양끝 공백 제거
    text = text.lower().strip()
    
    if text == "":
        return "ham", 0
        
    spam_keywords = [
        "free", "win", "winner", "prize", "click",
        "buy now", "urgent", "cash", "money", "offer", "deal"
    ]
    
    hit = 0
    for kw in spam_keywords:
        # 디버깅을 위한 출력 (실제 서비스 시에는 주석 처리 권장)
        # print(kw, text) 
        if kw in text:
            hit += 1
            
    # 키워드가 2개 이상 검출되면 spam, 아니면 ham 반환
    label = "spam" if hit >= 2 else "ham"
    
    return label, hit