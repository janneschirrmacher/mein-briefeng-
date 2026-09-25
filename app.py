import streamlit as st
import feedparser
from datetime import datetime

# Seiten-Konfiguration
st.set_page_config(page_title="Global Briefing Hub", page_icon="📰", layout="wide")

# Design im Economist-Stil (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { background-color: #dc2626; color: white; border-radius: 6px; }
    .stButton>button:hover { background-color: #b91c1c; color: white; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("### 🔴 The Economist & Pro — Global Briefing Hub")
st.write(f"Tagesaktuelles Briefing vom: {datetime.now().strftime('%A, %d. %B %Y')}")
st.markdown("---")

# Morgen-Briefing (Automatische Highlights)
st.markdown("### ⚡ Morgen-Überblick (Live-Schlagzeilen)")
st.info("Das System liest im Hintergrund die wichtigsten Feeds ein. Hier sind die Top-Einträge des Tages:")

# 6 Kategorien definieren mit echten RSS-Feeds (kostenlos & zuverlässig)
feeds = {
    "Wirtschaft & Finanzen": "https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best",
    "Weltpolitik": "https://www.reutersagency.com/feed/?best-topics=political-general&post_type=best",
    "Sport": "https://feeds.bbci.co.uk/sport/rss.xml",
    "Weltgeschehen": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "Biologie, Pharma & Chemie": "https://www.sciencedaily.com/rss/top/science.xml",
    "Technologie & Zukunft": "https://www.technologyreview.com/feed/"
}

# Tabs für die 6 Kategorien in Streamlit
tabs = st.tabs(list(feeds.keys()))

for i, (category, url) in enumerate(feeds.items()):
    with tabs[i]:
        st.subheader(category)
        
        # RSS-Feed live auslesen
        try:
            feed = feedparser.parse(url)
            if not feed.entries:
                st.warning("Aktuell keine Artikel verfügbar oder Feed wird blockiert.")
            else:
                for entry in feed.entries[:5]: # Zeige die neuesten 5 Artikel
                    with st.container():
                        st.markdown(f"**{entry.title}**")
                        if 'summary' in entry:
                            st.write(entry.summary[:200] + "...")
                        elif 'description' in entry:
                            st.write(entry.description[:200] + "...")
                        
                        st.markdown(f"[Zum Originalartikel]({entry.link})")
                        st.markdown("---")
        except Exception as e:
            st.error(f"Fehler beim Laden der Nachrichten: {e}")
