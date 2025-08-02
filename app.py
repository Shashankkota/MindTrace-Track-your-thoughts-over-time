import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import json

from sentiment import SentimentAnalyzer
from utils import DataManager

# Page configuration
st.set_page_config(
    page_title="Mental Health Sentiment Journal",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def load_components():
    """Load sentiment analyzer and data manager"""
    return SentimentAnalyzer(), DataManager()

sentiment_analyzer, data_manager = load_components()

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sentiment-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid;
    }
    .positive-card {
        background-color: #d4edda;
        border-left-color: #28a745;
    }
    .neutral-card {
        background-color: #f8f9fa;
        border-left-color: #6c757d;
    }
    .negative-card {
        background-color: #f8d7da;
        border-left-color: #dc3545;
    }
    .stats-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .metric-card {
        text-align: center;
        padding: 1rem;
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🧠 Mental Health Sentiment Journal</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📊 Navigation")
    page = st.selectbox(
        "Choose a page:",
        ["📝 New Entry", "📈 Analytics", "📋 Journal History", "⚙️ Settings"]
    )
    
    st.markdown("---")
    st.markdown("### 💡 About")
    st.markdown("""
    This is your personal mental health journal that analyzes the emotional tone of your entries using AI.
    
    **Features:**
    - 📝 Daily journaling
    - 🧠 Sentiment analysis
    - 📊 Trend visualization
    - 🔒 100% offline & private
    """)

# Main content based on selected page
if page == "📝 New Entry":
    st.header("📝 Write Your Daily Entry")
    st.markdown("Share your thoughts, feelings, or experiences from today...")
    
    # Journal entry form
    with st.form("journal_entry"):
        entry_text = st.text_area(
            "Your Entry:",
            placeholder="How are you feeling today? What's on your mind?",
            height=200,
            help="Write freely about your day, emotions, or thoughts."
        )
        
        submitted = st.form_submit_button("💾 Save Entry & Analyze", type="primary")
        
        if submitted and entry_text.strip():
            # Analyze sentiment
            sentiment_result = sentiment_analyzer.analyze_sentiment(entry_text)
            
            # Save entry
            entry = data_manager.add_entry(
                entry_text, 
                sentiment_result["sentiment"], 
                sentiment_result["score"]
            )
            
            # Display results
            st.success("✅ Entry saved successfully!")
            
            # Show sentiment analysis
            sentiment_color = sentiment_analyzer.get_sentiment_color(sentiment_result["sentiment"])
            sentiment_emoji = sentiment_analyzer.get_sentiment_emoji(sentiment_result["sentiment"])
            
            st.markdown(f"""
            <div class="sentiment-card {sentiment_result['sentiment'].lower()}-card">
                <h3>{sentiment_emoji} Sentiment Analysis</h3>
                <p><strong>Mood:</strong> {sentiment_result['sentiment']}</p>
                <p><strong>Score:</strong> {sentiment_result['score']:.3f}</p>
                <p><strong>Time:</strong> {entry['timestamp']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show entry preview
            st.markdown("### 📝 Your Entry:")
            st.info(entry_text)
            
        elif submitted and not entry_text.strip():
            st.error("Please write something in your journal entry.")

elif page == "📈 Analytics":
    st.header("📈 Mental Health Analytics")
    
    # Get data
    df = data_manager.get_entries_as_dataframe()
    stats = data_manager.get_statistics()
    
    if df.empty:
        st.info("📝 No journal entries yet. Start writing to see your analytics!")
    else:
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Entries", stats["total_entries"])
        
        with col2:
            st.metric("Average Mood Score", f"{stats['average_score']:.3f}")
        
        with col3:
            positive_count = stats["sentiment_distribution"].get("Positive", 0)
            st.metric("Positive Days", positive_count)
        
        with col4:
            negative_count = stats["sentiment_distribution"].get("Negative", 0)
            st.metric("Challenging Days", negative_count)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Sentiment Distribution")
            if stats["sentiment_distribution"]:
                sentiment_data = pd.DataFrame([
                    {"Sentiment": k, "Count": v} 
                    for k, v in stats["sentiment_distribution"].items()
                ])
                
                fig = px.pie(
                    sentiment_data, 
                    values="Count", 
                    names="Sentiment",
                    color="Sentiment",
                    color_discrete_map={
                        "Positive": "#28a745",
                        "Neutral": "#6c757d", 
                        "Negative": "#dc3545"
                    }
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No sentiment data available yet.")
        
        with col2:
            st.subheader("📈 Mood Trends Over Time")
            if len(df) > 1:
                fig = px.line(
                    df, 
                    x="timestamp", 
                    y="score",
                    title="Your Emotional Journey",
                    labels={"score": "Sentiment Score", "timestamp": "Date"}
                )
                fig.add_hline(y=0, line_dash="dash", line_color="gray")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Need at least 2 entries to show trends.")
        
        # Best and worst days
        if stats["best_day"] and stats["worst_day"]:
            st.subheader("🌟 Highlights")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**😊 Best Day:**")
                best = stats["best_day"]
                st.markdown(f"""
                - **Date:** {best['timestamp']}
                - **Score:** {best['score']:.3f}
                - **Entry:** {best['text'][:100]}{'...' if len(best['text']) > 100 else ''}
                """)
            
            with col2:
                st.markdown("**😔 Most Challenging Day:**")
                worst = stats["worst_day"]
                st.markdown(f"""
                - **Date:** {worst['timestamp']}
                - **Score:** {worst['score']:.3f}
                - **Entry:** {worst['text'][:100]}{'...' if len(worst['text']) > 100 else ''}
                """)

elif page == "📋 Journal History":
    st.header("📋 Your Journal History")
    
    entries = data_manager.get_all_entries()
    
    if not entries:
        st.info("📝 No journal entries yet. Start writing to build your history!")
    else:
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            sentiment_filter = st.selectbox(
                "Filter by sentiment:",
                ["All", "Positive", "Neutral", "Negative"]
            )
        
        with col2:
            days_filter = st.selectbox(
                "Show entries from:",
                ["All time", "Last 7 days", "Last 30 days", "Last 90 days"]
            )
        
        # Apply filters
        filtered_entries = entries
        
        if sentiment_filter != "All":
            filtered_entries = [e for e in filtered_entries if e["sentiment"] == sentiment_filter]
        
        if days_filter != "All time":
            days_map = {"Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90}
            days = days_map[days_filter]
            recent_entries = data_manager.get_recent_entries(days)
            filtered_entries = [e for e in filtered_entries if e in recent_entries]
        
        # Display entries
        st.markdown(f"**Showing {len(filtered_entries)} entries**")
        
        for entry in reversed(filtered_entries):  # Most recent first
            sentiment_color = sentiment_analyzer.get_sentiment_color(entry["sentiment"])
            sentiment_emoji = sentiment_analyzer.get_sentiment_emoji(entry["sentiment"])
            
            st.markdown(f"""
            <div class="sentiment-card {entry['sentiment'].lower()}-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4>{sentiment_emoji} {entry['sentiment']} ({entry['score']:.3f})</h4>
                        <p><strong>{entry['timestamp']}</strong></p>
                    </div>
                </div>
                <p style="margin-top: 1rem;">{entry['text']}</p>
            </div>
            """, unsafe_allow_html=True)

elif page == "⚙️ Settings":
    st.header("⚙️ Settings & Data Management")
    
    # Data export
    st.subheader("📤 Export Your Data")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Export as JSON"):
            data = data_manager.export_data("json")
            st.download_button(
                label="💾 Download JSON",
                data=json.dumps(data, indent=2),
                file_name=f"mental_health_journal_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📊 Export as CSV"):
            csv_data = data_manager.export_data("csv")
            st.download_button(
                label="💾 Download CSV",
                data=csv_data,
                file_name=f"mental_health_journal_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    # Data management
    st.subheader("🗑️ Data Management")
    
    # Show current stats
    stats = data_manager.get_statistics()
    st.info(f"**Current Status:** {stats['total_entries']} entries stored locally")
    
    # Clear data (with confirmation)
    st.markdown("### ⚠️ Clear All Data")
    st.warning("This action cannot be undone. All your journal entries will be permanently deleted.")
    
    if st.button("🗑️ Clear All Data", type="secondary"):
        if st.checkbox("I understand this will delete all my data permanently"):
            data_manager.clear_all_data()
            st.success("✅ All data has been cleared.")
            st.rerun()
    
    # App information
    st.subheader("ℹ️ About This App")
    st.markdown("""
    **Mental Health Sentiment Journal** is a privacy-focused journaling app that helps you track your emotional well-being.
    
    **Features:**
    - 🔒 **100% Offline:** All data stays on your device
    - 🧠 **AI Analysis:** Understand your emotional patterns
    - 📊 **Visual Insights:** Track your mental health journey
    - 📱 **Simple & Clean:** Focus on what matters - your thoughts
    
    **Privacy:** Your journal entries are stored locally and never leave your device.
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "🧠 Built with ❤️ for mental health awareness | "
    "100% Offline & Private"
    "</div>",
    unsafe_allow_html=True
) 