import re
from datetime import datetime

def is_valid_phone(phone: str) -> bool:
    # O'zbekiston telefon raqami formati: +998912223344
    pattern = r"^\+998\d{9}$"
    return re.match(pattern, phone) is not None

def is_valid_date(date: str) -> bool:
    # O'zbekiston sana formatlari: dd.mm.yyyy, dd/mm/yyyy, dd-mm-yyyy
    try:
        datetime.strptime(date, "%d.%m.%Y")
        return True
    except ValueError:
        return False
