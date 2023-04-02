import random



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


def random_phone():
    numbers = '0123456789'
    digits = random_string(9, 12, numbers)
    result = digits
    return result