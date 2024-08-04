from typing import Any


@classmethod
def check_all_empty(cls, data: Any) -> Any:
    """
    모든 필드가 비어있는 경우 체크
    """
    count = 0
    for attr_name, attr_value in enumerate(data):
        if attr_value is not None:
            count += 1

    if count == 0:
        raise ValueError("적어도 하나의 필드에는 값을 입력해야 합니다.")

    return data
