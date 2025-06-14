import random
import string

def generate_profile_id(role: str) -> str:
    prefix = {
        "university": "UNI",
        "student": "STU",
        "employer": "EMP"
    }.get(role, "GEN")

    id_length = {
        "university": 5,
        "student": 12,
        "employer": 6
    }.get(role, 8)

    random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=id_length))
    return random_id
