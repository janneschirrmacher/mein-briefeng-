import streamlit as st
import feedparser
from datetime import datetime
import re

# Seiten-Konfiguration
st.set_page_config(page_title="Global Briefing Hub", page_icon="📰", layout="wide")

# Custom CSS für das saubere Design im Economist-Stil
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    h1, h2, h3 { color: #111827; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
    .top-briefing {
        background-color: #ffffff;
        border-left: 5px solid #dc2626;
        padding: 20px;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("## 🔴 The Economist & Pro — Global Briefing Hub")
st.caption(f"Tagesaktuelles Briefing vom: {datetime.now().strftime('%A, %d. %B %Y')}")
st.markdown("---")

# Morgen-Briefing Sektion (wie in der Prototyp-Variante)
st.markdown("""
<div class="top-briefing">
    <h3>⚡ Morgen-Briefing des Tages</h3>
    <p>Willkommen zu Ihrem täglichen Intelligence-Briefing. Das Dashboard bündelt die wichtigsten Entwicklungen aus Wirtschaft, Politik und Technologie übersichtlich für Sie.</p>
</div>
""", unsafe_allow_html=True)

# Die 6 Kategorien und ihre Feeds
feeds = {
    "Wirtschaft & Finanzen": "https://www.ft.com/rss/home/uk",
    "Weltpolitik": "https://www.aljazeera.com/xml/rss/all.rss",
    "Sport": "https://feeds.bbci.co.uk/sport/rss.xml",
    "Weltgeschehen": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "Biologie, Pharma & Chemie": "https://www.sciencedaily.com/rss/top/science.xml",
    "Technologie & Zukunft": "https://www.technologyreview.com/feed/"
}

tabs = st.tabs(list(feeds.keys()))

for i, (category, url) in enumerate(feeds.items()):
    with tabs[i]:
        st.subheader(category)
        
        try:
            feed = feedparser.parse(url)
            if not feed.entries:
                st.warning("Aktuell keine Artikel verfügbar.")
            else:
                for entry in feed.entries[:5]:
                    title = entry.title
                    summary_text = ""
                    if 'summary' in entry:
                        summary_text = entry.summary
                    elif 'description' in entry:
                        summary_text = entry.description
                    
                    clean_summary = re.sub('<.*?>', '', summary_text)
                    
                    # Schöne, gerahmte Karten-Optik für jeden Artikel
                    with st.container(border=True):
                        st.markdown(f"#### {title}")
                        if clean_summary:
                            st.markdown(clean_summary[:280] + "..." if len(clean_summary) > 280 else clean_summary)
                        st.markdown(f"🔗 [Zum Originalartikel]({entry.link})")
        except Exception as e:
            st.error(f"Fehler beim Laden der Nachrichten: {e}")
