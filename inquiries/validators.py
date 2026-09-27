from .exceptions import CardValidationError

def validate_card_number(raw):
    card = raw.replace(" ", "").replace("-", "")
    if not card:
        raise CardValidationError("card is empty")

    if not card.isdigit():
        raise CardValidationError("card must contain only digits")

    if len(card) != 16:
        raise CardValidationError("card must be 16 digits")

    total = 0
    for i, ch in enumerate(card):
        digit = int(ch)
        if i % 2 == 0:
            digit = digit * 2
            if digit > 9:
                digit = digit - 9
        total = total + digit

    if total % 10 != 0:
        raise CardValidationError("card failed checksum")

    return card