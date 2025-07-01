from fitparse import FitFile


def read_fit_file(file_path):
    """
    Liest ein FIT-File und gibt die Daten als Liste von Dictionaries zurück.
    """
    fitfile = FitFile(file_path)
    data = []

    for record in fitfile.get_messages('record'):
        record_data = {}
        for field in record:
            record_data[field.name] = field.value
        data.append(record_data)

    return data
