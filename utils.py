"""Reusable validation and input helper function"""


from datetime import datetime, date

VALID_PRIORITIES = ("low", "medium", "high")
VALID_STATUSES = ("todo", "in_progress", "done")
DATE_FORMAT = "%Y-%m-%d"


def print_header(title):
    """Print a formatted section heading."""
    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60)
    
    
def is_valid_date(text):
    """Checking whether text contains a valid YYYY-MM-DD date."""
    try:
        datetime.strptime(text, DATE_FORMAT)
        return True
    except (ValueError, TypeError):
        return False
    
    
def days_until(date_text):
    """Returrn the number of the days until a date, or None if invalid"""
    if not date_text or not is_valid_date(date_text):
        return None
    
    
    target_date = datetime.strptime(date_text, DATE_FORMAT).date()
    return (target_date, date.today()).days



def ask_text(prompt, allow_empty=False):
    """Ask for text and reject empty input unless allowed"""
    while True:
        value = input(prompt).strip()
        
        
        if value or allow_empty:
            return value
        
        
        print("This field cannot be empty. Please try again.")
        
        
def ask_choice(prompt, choices, default=None):
    """Ask until the user enters one of the allowed choices."""
    normalized_choices = tuple(choice.lower() for choice in choices)
    
    
    while True:
        value = input(prompt).strip().lower()
        
        if not value and default is not None:
            return default
        
        
        if value in normalized_choices:
            return value
        
        
        
        print("Please choose one of:", ",".join(normalized_choices))
        
        
def ask_date(prompt, allow_empty=True):
    """Ask for valid a date in YYYY-MM-DD format."""
    while True:
        value = input(prompt).strip()
        
        
        if not value and allow_empty:
            return ""
        
        
        if is_valid_date(value):
            return value
        
        
        print("Invalid date. Use YYYY-MM-DD, for example 2026-12-25.")
        
        
        
        
def ask_int(prompt, minimum=None, maximum=None):
    """Ask for an integer within optional minimum and maximum limits."""
    while True:
        value = input(prompt).strip()
        
        
        try:
            number = int(value)
            if minimum is not None and number < minimum:
                print(f"Enter a number greater than or equal to {minimum}.")
            if maximum is not None and number > maximum:
                print(f"Enter a number less than or equal to {maximum}.")  
                continue
            return number
        except ValueError:
            print("Please enter a valid whole.")                                     