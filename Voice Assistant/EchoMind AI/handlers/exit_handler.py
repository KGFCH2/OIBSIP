"""Exit handler"""
import re
from config.settings import EXIT_KEYWORDS

def handle_exit(command):
    """Handle exit/quit commands"""
    if re.search(r'\b(exit|quit|stop|bye|goodbye|terminate)\b', command, re.IGNORECASE):
        return True
    return False
