import nanoid

def get_nanoid():

    return nanoid.generate( alphabet = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ', size = 16 )
