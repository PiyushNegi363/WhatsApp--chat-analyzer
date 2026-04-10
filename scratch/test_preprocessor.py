import sys
import os
sys.path.append(os.getcwd())
from modules import preprocessor
import html

def test_parsing():
    test_cases = [
        # Android 24h
        "01/01/24, 10:00 - User1: Hello\n01/01/24, 10:05 - User2: Hi",
        # Android 12h
        "01/01/24, 10:00 am - User1: Morning\n01/01/24, 10:05 PM - User2: Night",
        # iOS
        "[01/01/24, 10:00:00] User1: Hello iOS\n[01/01/24, 10:05:00] User2: Hi iOS",
        # Group notifications
        "01/01/24, 10:00 - User1 added User2\n01/01/24, 10:05 - User2 changed the group description",
        # Multi-line message
        "01/01/24, 10:00 - User1: Line 1\nLine 2\nLine 3\n01/01/24, 10:05 - User2: Done",
        # XSS Injection Case
        "01/01/24, 11:00 - <script>alert('xss')</script>: Hello XSS"
    ]
    
    for i, data in enumerate(test_cases):
        print(f"\n--- Test Case {i+1} ---")
        df = preprocessor.preprocess(data)
        if df.empty:
            print("FAILED: Empty DataFrame")
        else:
            print(f"SUCCESS: {len(df)} messages parsed")
            print(df[['user', 'message']].to_string(index=False))

if __name__ == "__main__":
    test_parsing()
