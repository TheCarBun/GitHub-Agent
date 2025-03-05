from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def format_duration(iso_date:str) -> str:
    """
    Formats the duration from the given ISO date to the current date in years, months, and days.

    Args:
        iso_date (str): The ISO formatted date string (e.g., "2023-02-07T12:34:56Z").

    Returns:
        str: The formatted duration string (e.g., "2 years 3 months 5 days").
    """
    created_at = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%SZ")
    now = datetime.now()
    delta = now - created_at

    years = delta.days // 365
    months = (delta.days % 365) // 30
    days = (delta.days % 365) % 30

    parts = []
    if years:
        parts.append(f"{years} year{'s' if years > 1 else ''}")
    if months:
        parts.append(f"{months} month{'s' if months > 1 else ''}")
    if days:
        parts.append(f"{days} day{'s' if days > 1 else ''}")

    return " ".join(parts) if parts else "0 days"

def format_date_ddmmyyyy(date:str) -> str:
    """
    Formats a date string from 'YYYY-MM-DD' to 'DDth MMM, YYYY'.

    Args:
        date (str): The date string in 'YYYY-MM-DD' format.

    Returns:
        str: The formatted date string (e.g., "7th Feb, 2025").
    """
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    formated_date = date_obj.strftime("{day} %b, %Y").replace("{day}", str(date_obj.day) + ("st" if date_obj.day in [1, 21, 31] else "nd" if date_obj.day in [2, 22] else "rd" if date_obj.day in [3, 23] else "th"))
    return formated_date

def format_iso_date(iso_date:str) -> str:
    """
    Formats an ISO date string to 'DDth MMM, YYYY'.

    Args:
        iso_date (str): The ISO date string (e.g., "2023-02-07T12:34:56Z").

    Returns:
        str: The formatted date string (e.g., "7th Feb, 202
    """
    dt = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%SZ")
    return dt.strftime("{day} %b, %Y").replace("{day}", str(dt.day) + ("st" if dt.day in [1, 21, 31] else "nd" if dt.day  in [2, 22] else "rd" if dt.day in [3, 23] else "th"))

def is_less_than_2_months_old(iso_date:str) -> bool:
    """
    Checks if the given ISO date is less than 2 months old from the current date.

    Args:
        iso_date (str): The ISO formatted date string (e.g., "2023-02-07T12:34:56Z").

    Returns:
        bool: True if the date is less than 2 months old, False otherwise.
    """
    created_date = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%SZ")
    two_months_ago = datetime.now() - relativedelta(months=2)
    return created_date > two_months_ago

def get_language_distribution(language_data:dict):
    """
    Calculate the distribution of programming languages based on the provided language data.
    Args:
        language_data (dict): A dictionary where keys are repository names and values are lists of dictionaries.
                                Each dictionary in the list represents a programming language and its size in the repository.
    Returns:
        dict: A dictionary where keys are programming language names and values are the total size of each language
                across all repositories.
    """

    lang_dist = {}
    for repo, language in language_data.items():
        for lang in language:
            for lang_name, size in lang.items():
                if lang_name not in lang_dist:
                    lang_dist[lang_name] = size
                else:
                    lang_dist[lang_name] += size
    
    return lang_dist

def get_langugage_percent(lang_dict:dict):
    """
    Calculate the percentage distribution of languages based on their sizes.
    Args:
        lang_dict (dict): A dictionary where keys are language names and values are their respective sizes.
    Returns:
        str: A formatted string showing each language and its percentage of the total size.
    """
    lang_dist = """"""
    total_size = sum(lang_dict.values())

    for lang, size in lang_dict.items():
        percent = round(((size/total_size)*100), 2)
        lang_dist += f"\n{lang}: {percent}%"
    
    return lang_dist