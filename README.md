# WhatsApp Chat Analyzer

A comprehensive Streamlit dashboard to visualize and analyze WhatsApp chat data.

## 📁 Project Structure

```text
whatsapp-analyzer/
├── app.py                  # Main Streamlit application
├── modules/                # Core logic components
│   ├── preprocessor.py     # Regex parsing and cleaning
│   └── helper.py           # Analysis and visualization functions
├── data/                   # Data files and resources
│   ├── stop_hinglish.txt   # Stop words for NLP
│   └── [Exported Chat].txt # Your WhatsApp chat exports
├── notebooks/              # Exploratory work
│   └── preprocessing.ipynb # Original development notebook
├── requirements.txt        # List of dependencies
└── README.md               # This file
```

## 🚀 Getting Started

1.  **Clone the repository** (or navigate to the folder).
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application**:
    ```bash
    streamlit run app.py
    ```
4.  **Analyze your chat**: Export your WhatsApp chat (without media) as a `.txt` file and upload it in the sidebar.

## ✨ Features
- **Statistics**: Total messages, words, media, and links.
- **Timelines**: Monthly and daily activity trends.
- **Activity Maps**: Weekly activity pulse and monthly distributions.
- **WordCloud**: Visual representation of frequently used words.
- **Emoji Analysis**: Distribution of emojis used in the chat.
