"""Symbol conversion and text processing utilities"""
import re

def convert_spoken_symbols(text):
    """Convert spoken punctuation marks and symbols into their actual characters"""
    symbol_map = {
        r'\bquestion mark\b': '?',
        r'\bquestion\s+mark\b': '?',
        r'\bquestion\b$': '?',
        r'\bexclamation mark\b': '!',
        r'\bexclamation point\b': '!',
        r'\bexclamation\b$': '!',
        r'\bperiod\b': '.',
        r'\bfull stop\b': '.',
        r'\bdot\b': '.',
        r'\bcomma\b': ',',
        r'\bcolon\b': ':',
        r'\bsemicolon\b': ';',
        r'\bapostrophe\b': "'",
        r'\bquote\b': '"',
        r'\bdouble quote\b': '"',
        r'\bleft paren\b|\bopening paren\b|\bparens\b': '(',
        r'\bright paren\b|\bclosing paren\b': ')',
        r'\bsquare bracket\b|\bleft bracket\b|\bleft square bracket\b': '[',
        r'\bright bracket\b|\bclosing bracket\b|\bright square bracket\b': ']',
        r'\bat sign\b': '@',
        r'\bhash\b|\bhashtag\b|\bpound sign\b': '#',
        r'\bdollar sign\b': '$',
        r'\bpercent\b|\bpercent sign\b': '%',
        r'\bampersand\b|\band sign\b': '&',
        r'\basterisk\b|\bstar\b': '*',
    }
    
    result = text
    for spoken, symbol in symbol_map.items():
        result = re.sub(spoken, symbol, result, flags=re.IGNORECASE)
    
    return result

def is_symbol_only(text):
    """Check if command contains only symbols"""
    return bool(re.match(r'^[?!.,;:\'"()\[\]@#$%&*\-/+=~`|\\<>]+$', text.strip()))

def clean_connector_words(text):
    """Remove connector words from the beginning of text"""
    from config.settings import CONNECTOR_WORDS
    
    for connector in CONNECTOR_WORDS:
        if text.lower().startswith(connector):
            return text[len(connector):].strip()
    return text
