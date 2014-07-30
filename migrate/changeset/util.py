"""
Safe quoting method
"""


def safe_quote(obj):
    # this is the SQLA 0.9 approach
    if hasattr(obj, 'name') and hasattr(obj.name, 'quote'):
        return obj.name.quote
    else:
        return obj.quote
