def normalize_order_number(value: str) -> str:
    """
    Приводит номер заказа к каноническому виду:
    оставляет только цифры, убирает ведущие нули.
    '034567', ' 34567 ', '№34567' -> '34567'
    """
    digits = ''.join(ch for ch in str(value) if ch.isdigit())
    return digits.lstrip('0') or '0'