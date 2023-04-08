import random
# import phonenumbers


def random_string(min_len, max_len, charset):
    length = random.randint(min_len, max_len+1)
    result = ''.join(random.choices(charset, k=length))
    return result


def random_email():
    validchars = 'abcdefghijklmnopqrstuvwxyz1234567890'
    validoms = 'abcdefghijklmnopqrstuvwxyz'
    login = random_string(4, 15, validchars)
    domain = random_string(3, 9, validoms)
    last_piece = random.choice(['ru', 'com', 'org'])
    result = f'{login}@{domain}.{last_piece}'
    return result


# def random_phone():
#     country_code = random.choice(list(phonenumbers.supported_calling_codes()))
#     region_code = random.choice(phonenumbers.COUNTRY_CODE_TO_REGION_CODE[country_code])
#     number_obj = phonenumbers.example_number(region_code)
#     result = f'+{number_obj.country_code}{number_obj.national_number}'
#     return result