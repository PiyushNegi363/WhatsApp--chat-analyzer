import re
import pandas as pd

def preprocess(data):
    # 1. Cleaning: Remove invisible Unicode characters that trip up regex
    # \u200e = LTR, \u200f = RTL, \u202f = Narrow No-Break Space
    data = data.replace('\u200e', '').replace('\u200f', '').replace('\u202f', ' ')
    
    # 2. Pattern Definition
    # Android Pattern: 01/01/24, 10:00 - User: message
    android_pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s?\d{1,2}:\d{2}(?::\d{2})?(?:\s?[apAP][mM])?\s?-\s'
    
    # iOS Pattern: [01/01/24, 10:00:00] User: message
    ios_pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s?\d{1,2}:\d{2}(?::\d{2})?(?:\s?[apAP][mM])?\]\s'
    
    # Combined Timestamp Regex
    timestamp_pattern = f'({android_pattern}|{ios_pattern})'

    # 3. Splitting logic
    parts = re.split(timestamp_pattern, data)
    
    if len(parts) < 3:
        # Fallback to even simpler date pattern if previous failed
        # Handles cases like "01/01/2024, 10:00 am User:" (missing hyphen or brackets)
        fallback_pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?[apAP][mM])?[\s-]*)'
        parts = re.split(fallback_pattern, data)

    messages = []
    dates = []
    
    # re.split(pattern with capture group) returns [leading, captured, trailing, captured, trailing]
    # In our case: [empty, date_string, message_content, date_string, message_content, ...]
    for i in range(1, len(parts), 2):
        dates.append(parts[i].strip('[]- '))
        messages.append(parts[i+1])

    if not messages:
        return pd.DataFrame()

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    
    # 4. Robust Date Parsing
    # Try multiple common formats
    formats = [
        '%d/%m/%y, %H:%M', '%m/%d/%y, %H:%M', 
        '%d/%m/%Y, %H:%M', '%m/%d/%Y, %H:%M',
        '%d/%m/%y, %I:%M %p', '%m/%d/%y, %I:%M %p',
        '%d/%m/%Y, %I:%M %p', '%m/%d/%Y, %I:%M %p',
        '%d/%m/%y, %H:%M:%S', '%m/%d/%y, %H:%M:%S', # iOS seconds
        '%d/%m/%Y, %H:%M:%S', '%m/%d/%Y, %H:%M:%S'
    ]
    
    # Default to standard coerce with format='mixed' to avoid warnings
    parsed_dates = pd.to_datetime(df['message_date'], errors='coerce', format='mixed')
    
    # Heuristic: If parsing failed for more than 20% of rows, try specific formats
    if parsed_dates.isna().sum() > len(df) * 0.2:
        for fmt in formats:
            temp_dates = pd.to_datetime(df['message_date'], format=fmt, errors='coerce')
            if temp_dates.notna().sum() > parsed_dates.notna().sum():
                parsed_dates = temp_dates
                if parsed_dates.isna().sum() == 0:
                    break

    df['date'] = parsed_dates
    df.dropna(subset=['date'], inplace=True)

    # 5. Extract User and Message
    users = []
    message_texts = []
    for msg in df['user_message']:
        # Split at the first ": " to separate user from message
        entry = re.split('^([\w\W]+?):\s', msg)
        if len(entry) >= 3: # Successfully matched "User: Message"
            users.append(entry[1])
            message_texts.append(entry[2])
        else: # Group notification (e.g., "User added User2")
            users.append('group_notification')
            message_texts.append(entry[0])

    df['user'] = users
    df['message'] = message_texts
    df.drop(columns=['user_message', 'message_date'], inplace=True)

    # 6. Time Features
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Heatmap period
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append(f"00-{hour + 1}")
        else:
            period.append(f"{hour}-{hour + 1}")
    df['period'] = period

    return df
