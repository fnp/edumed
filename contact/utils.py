def csv_escape(string):
    return '"' + string.replace('\r\n', ' ').replace('\n', ' ').replace('"', '\"') + '"'

def csv_prepare(obj):
    to_escape = obj
    if not isinstance(obj, unicode):
        to_escape = str(to_escape)
    return csv_escape(to_escape)