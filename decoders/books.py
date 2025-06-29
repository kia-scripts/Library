def decode_book(doc) -> dict:
    return {
        "id": doc.id,
        'label': doc.label,
        'author': doc.author,
        'year' : doc.year,
        'ibsn' : doc.ibsn,
        'value' : doc.value
    }

def decode_books(docs) -> list:
    return [decode_book(doc) for doc in docs]
