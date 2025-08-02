import json
import os
import pandas as pd
from datetime import datetime
from pathlib import Path

class DataManager:
    def __init__(self, data_dir="data"):
        """Initialize data manager with specified directory"""
        self.data_dir = Path(data_dir)
        self.data_file = self.data_dir / "journal_log.json"
        self._ensure_data_directory()
        self._initialize_data_file()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        self.data_dir.mkdir(exist_ok=True)
    
    def _initialize_data_file(self):
        """Initialize the JSON file with empty structure if it doesn't exist"""
        if not self.data_file.exists():
            initial_data = {
                "entries": [],
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }
            self._save_data(initial_data)
    
    def _load_data(self):
        """Load data from JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"entries": [], "created_at": datetime.now().isoformat()}
    
    def _save_data(self, data):
        """Save data to JSON file"""
        data["last_updated"] = datetime.now().isoformat()
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def add_entry(self, text, sentiment, score):
        """Add a new journal entry"""
        data = self._load_data()
        
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "text": text,
            "sentiment": sentiment,
            "score": score
        }
        
        data["entries"].append(entry)
        self._save_data(data)
        return entry
    
    def get_all_entries(self):
        """Get all journal entries"""
        data = self._load_data()
        return data.get("entries", [])
    
    def get_entries_as_dataframe(self):
        """Get entries as pandas DataFrame for analysis"""
        entries = self.get_all_entries()
        if not entries:
            return pd.DataFrame()
        
        df = pd.DataFrame(entries)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        return df
    
    def get_statistics(self):
        """Get basic statistics about the journal entries"""
        entries = self.get_all_entries()
        
        if not entries:
            return {
                "total_entries": 0,
                "sentiment_distribution": {},
                "average_score": 0.0,
                "best_day": None,
                "worst_day": None
            }
        
        # Sentiment distribution
        sentiment_counts = {}
        for entry in entries:
            sentiment = entry["sentiment"]
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
        
        # Average score
        scores = [entry["score"] for entry in entries]
        avg_score = sum(scores) / len(scores) if scores else 0.0
        
        # Best and worst days
        best_entry = max(entries, key=lambda x: x["score"]) if entries else None
        worst_entry = min(entries, key=lambda x: x["score"]) if entries else None
        
        return {
            "total_entries": len(entries),
            "sentiment_distribution": sentiment_counts,
            "average_score": avg_score,
            "best_day": best_entry,
            "worst_day": worst_entry
        }
    
    def export_data(self, format="json"):
        """Export data in specified format"""
        if format.lower() == "json":
            return self._load_data()
        elif format.lower() == "csv":
            df = self.get_entries_as_dataframe()
            return df.to_csv(index=False)
        else:
            raise ValueError("Unsupported format. Use 'json' or 'csv'")
    
    def clear_all_data(self):
        """Clear all journal entries (use with caution!)"""
        initial_data = {
            "entries": [],
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        self._save_data(initial_data)
    
    def get_recent_entries(self, days=7):
        """Get entries from the last N days"""
        entries = self.get_all_entries()
        if not entries:
            return []
        
        # Convert to datetime for comparison
        recent_entries = []
        cutoff_date = datetime.now() - pd.Timedelta(days=days)
        
        for entry in entries:
            entry_date = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M")
            if entry_date >= cutoff_date:
                recent_entries.append(entry)
        
        return recent_entries 