# 📈 ChatPulse Pro: WhatsApp Analyzer

**ChatPulse Pro** is a premium, high-performance analytics dashboard designed to turn raw WhatsApp exports into professional-grade insights. Built with a **modern glassmorphic design system**, it offers a seamless blend of data science and elite UI/UX.

---

## ✨ Premium UI/UX Features

ChatPulse Pro recently underwent a comprehensive **8-dimensional audit**, resulting in a significant upgrade to its visual and interactive core:

- **💎 Glassmorphic Design**: A sleek, dark-mode interface using transparency, blur effects, and vibrant glowing accents.
- **⚡ Zero-Friction Flow**: Automatic dashboard generation that refreshes instantly upon participant selection—no manual clicks required.
- **📈 High-Fidelity Interactivity**: Fully interactive Plotly charts with custom themes, hover effects, and smooth fade-in animations.
- **♿ Accessibility Optimized**: Enhanced with ARIA labels and semantic structure for screen reader support.
- **📱 Responsive Layout**: A mobile-first approach using fluid typography and stackable data grids for analysis on the go.

---

## 🏆 Analytics Dimensions

### 🥇 Performance Overview
Get high-level metrics at a glance, including total messages, word counts, media sharing habits, and link frequency—all rendered in glowing glassmorphic cards.

### 📈 Engagement Timelines
- **Monthly Velocity**: Visualize chat volume trends over months and years.
- **Daily Frequency**: Track consistent engagement patterns across individual days with interactive area charts.

### 🗓️ Activity Distribution
- **Weekly Intensity**: Identify the busiest days of the week.
- **Monthly Volume**: Understand seasonal chat spikes.
- **Hourly Pulse**: A sophisticated heatmap highlighting peak activity times during the day.

### 🔤 Semantic & Emotional Insights
- **Word Sentiment Cloud**: A visual lexical representation of your most frequent terms.
- **Top 10 Emotional Triggers**: Data-driven analysis of emoji usage patterns.
- **Lexical Trends**: Horizontal bar charts of common words with advanced Hinglish stop-word filtering.

### 👥 Community Dynamics
For group chats, analyze the "Share of Voice" to visualize contribution percentages and identify primary drivers of conversation.

---

## 🛡️ Security & Privacy

ChatPulse Pro is engineered with a **Privacy-First** philosophy:
- **Local Processing**: Your chat data never leaves your machine. All parsing and analysis happen entirely in-memory during your local session.
- **Hardened Security**: Includes built-in HTML sanitization and XSS protection for all user-generated content.
- **Media-Free**: Works exclusively with "Without Media" exports for maximum privacy and speed.

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
├── app.py                  # Premium Engine & Glassmorphic Dashboard
├── modules/                # Specialized Logic Layer
│   ├── preprocessor.py     # Regex-driven parsing & Unicode cleaning
│   └── helper.py           # Statistical engine & Visualization logic
├── assets/                 # Visual branding assets
├── data/                   # Resources (Hinglish stop-words, sample data)
├── requirements.txt        # Production dependencies (Streamlit 1.56.0+)
└── README.md               # Project Documentation
```

---

## 🛠️ Built With
- **Streamlit**: Core interactive engine.
- **Plotly**: Premium, high-fidelity visualizations.
- **Pandas**: Efficient data processing.
- **Matplotlib / WordCloud**: Detailed semantic analysis.

---

## 📬 Exporting Instructions
1. Open the WhatsApp chat you want to analyze.
2. Tap **Settings/More** > **Export Chat**.
3. Select **"Without Media"**.
4. Save the `.txt` file and upload it to the ChatPulse Pro sidebar!
