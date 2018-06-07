def money_as_string(amount):
    return '%s.%s$' % (str(int(amount / 100)), str(amount % 100).ljust(2, '0'))

def money_as_int(amount):
    dollars = int(amount.split(".")[0])
    cents = int(amount.split(".")[1][:-1])
    return dollars * 100 + cents

def is_integer(string):
    try:
        int(string)
        return True
    except:
        return False