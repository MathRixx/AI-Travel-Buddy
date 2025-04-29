import locale
from datetime import datetime, timedelta

def format_currency(amount, currency='USD'):
    """
    Format currency amount with appropriate symbol
    
    Args:
        amount: Numeric value
        currency: Currency code (default: USD)
        
    Returns:
        Formatted currency string
    """
    if currency == 'USD':
        return f"${amount:.2f}"
    elif currency == 'EUR':
        return f"€{amount:.2f}"
    elif currency == 'GBP':
        return f"£{amount:.2f}"
    elif currency == 'JPY':
        return f"¥{int(amount)}"  # No decimal places for Yen
    else:
        return f"{amount:.2f} {currency}"

def calculate_date_range(start_date, end_date):
    """
    Calculate a list of dates between start and end date
    
    Args:
        start_date: Start date (datetime.date object)
        end_date: End date (datetime.date object)
        
    Returns:
        List of date objects
    """
    days = (end_date - start_date).days + 1
    return [start_date + timedelta(days=i) for i in range(days)]

def get_time_period(hour):
    """
    Determine the time period (morning, afternoon, evening) based on hour
    
    Args:
        hour: Hour of the day (0-23)
        
    Returns:
        String representing time period
    """
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    else:
        return "evening"

def get_trip_duration_text(days):
    """
    Convert number of days to friendly text
    
    Args:
        days: Number of days
        
    Returns:
        Text description of duration
    """
    if days <= 3:
        return "short getaway"
    elif days <= 7:
        return "week-long trip"
    elif days <= 14:
        return "two-week vacation"
    else:
        return "extended journey"

def truncate_text(text, max_length=100):
    """
    Truncate text to specified length and add ellipsis
    
    Args:
        text: Text to truncate
        max_length: Maximum length before truncation
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
