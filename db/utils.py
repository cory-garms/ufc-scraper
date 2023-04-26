from schema import tables

db_file = 'fight.sqlite'

def add_quotes(string):
    return ''.join(['"', string, '"'])

def format_by_type(table, string, key):
    key_type = tables[table][key]['type']
    if not string: 
        return 'NULL'

    match key_type:
        case 'TEXT':
            return add_quotes(string)
        case 'INTEGER':
            if is_number(string):
                return string
            else:
                return 'NULL'
        case 'REAL':
            if is_number(string):
                return string
            else:
                return 'NULL'
        case other:
            return string

def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
