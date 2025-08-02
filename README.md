# 🧠 MindTrace

A privacy-focused, offline journaling application that helps you track your emotional well-being using AI-powered sentiment analysis.

## ✨ Features

- **📝 Daily Journaling**: Write about your day, thoughts, and feelings
- **🧠 AI Sentiment Analysis**: Understand the emotional tone of your entries using VADER
- **📊 Visual Analytics**: Track your mental health trends over time
- **🔒 100% Offline & Private**: All data stays on your device
- **📈 Trend Visualization**: See your emotional journey through charts and graphs
- **📋 Entry History**: Browse and filter your past entries
- **📤 Data Export**: Export your data in JSON or CSV format

## 🛠️ Tech Stack

- **UI Framework**: Streamlit
- **Sentiment Analysis**: VADER (NLTK)
- **Data Storage**: Local JSON files
- **Visualization**: Plotly
- **Language**: Python 3.x

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd mental-health-journal
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, manually navigate to the URL

## 📱 How to Use

### 1. Write Your First Entry
- Navigate to the "📝 New Entry" page
- Write about your day, feelings, or thoughts
- Click "💾 Save Entry & Analyze"
- View your sentiment analysis results

### 2. Explore Your Analytics
- Go to the "📈 Analytics" page
- View your emotional trends over time
- See sentiment distribution charts
- Check your best and most challenging days

### 3. Browse Your History
- Visit the "📋 Journal History" page
- Filter entries by sentiment or time period
- Read through your past entries

### 4. Manage Your Data
- Access the "⚙️ Settings" page
- Export your data in JSON or CSV format
- Clear all data if needed (with confirmation)

## 📊 Understanding Sentiment Analysis

The app uses VADER (Valence Aware Dictionary and sEntiment Reasoner) to analyze your entries:

- **Positive** (Score ≥ 0.05): Happy, optimistic, or uplifting content
- **Neutral** (-0.05 < Score < 0.05): Balanced or factual content
- **Negative** (Score ≤ -0.05): Sad, anxious, or challenging content

**Note**: Sentiment analysis is a tool for self-reflection, not a clinical diagnosis.

## 🔒 Privacy & Data Security

- **100% Offline**: No internet connection required
- **Local Storage**: All data stored in `data/journal_log.json`
- **No Cloud Services**: Your entries never leave your device
- **No User Accounts**: No login or authentication required
- **Export Control**: You control when and how to export your data

## 📁 Project Structure

```
mental-health-journal/
├── app.py                    # Main Streamlit application
├── sentiment.py             # Sentiment analysis logic
├── utils.py                 # Data management utilities
├── data/
│   └── journal_log.json     # Your journal entries (created automatically)
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🎯 Sample Data Format

Your journal entries are stored in this format:

```json
{
  "entries": [
    {
      "timestamp": "2025-01-15 19:30",
      "text": "I had a great day today! Met with friends and felt really happy.",
      "sentiment": "Positive",
      "score": 0.7234
    }
  ],
  "created_at": "2025-01-15T10:00:00",
  "last_updated": "2025-01-15T19:30:00"
}
```

## 🛠️ Customization

### Adding Custom Sentiment Analysis
You can modify `sentiment.py` to use different sentiment analysis models:

```python
# Example: Using a custom model
def analyze_sentiment(self, text):
    # Your custom sentiment analysis logic here
    return {"sentiment": "Custom", "score": 0.5}
```


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## ⚠️ Disclaimer

This application is designed for personal use and self-reflection. It is not a substitute for professional mental health care. If you're experiencing mental health challenges, please consider reaching out to a qualified mental health professional.

## 🆘 Troubleshooting

### Common Issues

**1. "Module not found" errors**
```bash
pip install -r requirements.txt
```

**2. NLTK data not found**
The app will automatically download required NLTK data on first run.

**3. Port already in use**
```bash
streamlit run app.py --server.port 8502
```

**4. Data not saving**
- Check that the `data/` directory exists
- Ensure you have write permissions in the project directory

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the error messages in the terminal
3. Ensure all dependencies are installed correctly

---

**Built with ❤️ for mental health awareness**

*Remember: Your mental health matters. This tool is here to help you reflect and grow.*
