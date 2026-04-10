# 📈 ChatPulse Pro: WhatsApp Analyzer

**ChatPulse Pro** is a high-performance, privacy-first analytics dashboard designed to turn raw WhatsApp exports into professional-grade insights. Built with a premium SaaS design system, it offers a seamless blend of data science and elegant UI.

---

## ✨ Key Features

### 🏆 Performance Overview
Get high-level metrics at a glance, including total messages, word counts, media sharing habits, and link frequency.

### 📈 Engagement Timelines
- **Monthly Velocity**: Visualize chat volume trends over months and years.
- **Daily Frequency**: Track consistent engagement patterns across individual days.

### 🗓️ Activity Distribution
- **Weekly Intensity**: identify the busiest days of the week.
- **Monthly Volume**: Understand seasonal chat spikes.
- **Hourly Pulse**: A sophisticated heatmap highlighting peak activity times during the day.

### 🔤 Semantic & Emotional Insights
- **Word Sentiment Cloud**: A lexical visualization of the most utilized terms.
- **Top 10 Emotional Triggers**: Data-driven analysis of emoji usage patterns.
- **Lexical Trends**: Horizontal bar charts of most common words (with Hinglish stop-word filtering).

### 👥 Community Dynamics
For group chats, analyze "Share of Voice" to see who the primary contributors are.

---

## 🛡️ Security & Privacy

ChatPulse Pro is engineered with a **Privacy-First** philosophy:
- **Local Processing**: Your chat data never leaves your machine. All parsing and analysis happen in-memory during the Streamlit session.
- **Hardened Security**: Includes built-in HTML sanitization and XSS protection for all user-generated content (like names and message bodies).
- **No Media Required**: Works entirely with "Without Media" exports for maximum privacy.

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Python 3.10+ installed.

### 2. Installation
```powershell
# Clone the repository
git clone https://github.com/PiyushNegi363/WhatsApp--chat-analyzer.git
cd WhatsApp--chat-analyzer

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the App
```powershell
streamlit run app.py
```

---

## 📁 Repository Structure

```text
whatsapp-analyzer/
├── app.py                  # Main Engine & SaaS Dashboard UI
├── modules/                # Specialized Logic Layer
│   ├── preprocessor.py     # Regex-driven parsing & Unicode cleaning
│   └── helper.py           # Statistical analysis & Visualization logic
├── assets/                 # Branding & Visual Assets
├── data/                   # Resources (Hinglish stop-words, sample chats)
├── requirements.txt        # Production dependencies (Streamlit 1.35.0+)
└── README.md               # Project Documentation
```

---

## 🛠️ Built With
- **Streamlit**: The core interactive framework.
- **Plotly**: For high-fidelity, interactive data visualizations.
- **Pandas**: Efficient time-series and data manipulation.
- **WordCloud / Matplotlib**: Semantic content analysis.

---

## 📬 Exporting Instructions
1. Open the WhatsApp chat you want to analyze.
2. Tap **Settings/More** > **Export Chat**.
3. Select **"Without Media"**.
4. Save the `.txt` file and upload it to the ChatPulse Pro sidebar!
