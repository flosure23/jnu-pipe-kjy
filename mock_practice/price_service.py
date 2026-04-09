def get_discount_func(user_id):
    # 원래는 외부 API를 호출한다고 가정
    # 테스트에서는 이 함수를 직접 쓰지 않을 수도 있다
    raise NotImplementedError("실제 할인 API는 아직 연결하지 않음")


def calculate_price(user_id, price, get_discount_func):
    return price - get_discount_func(user_id)