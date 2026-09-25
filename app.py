import streamlit as st
import feedparser
from datetime import datetime
from deep_translator import GoogleTranslator

# Seiten-Konfiguration
st.set_page_config(page_title="Global Briefing Hub", page_icon="📰", layout="wide")

# Design im Economist-Stil
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { background-color: #dc2626; color: white; border-radius: 6px; }
    .stButton>button:hover { background-color: #b91c1c; color: white; }
    </style>
""", unsafe_allow_html=True)

# Sidebar für Einstellungen (z.B. Übersetzung)
st.sidebar.markdown("### ⚙️ Einstellungen")
translate_german = st.sidebar.checkbox("Inhalte automatisch ins Deutsche übersetzen", value=True)

st.markdown("### 🔴 The Economist & Pro — Global Briefing Hub")
st.write(f"Tagesaktuelles Briefing vom: {datetime.now().strftime('%A, %d. %B %Y')}")
st.markdown("---")

# Zuverlässige RSS-Quellen für die 6 Kategorien
feeds = {
    "Wirtschaft & Finanzen": "https://www.ft.com/rss/home/uk",
    "Weltpolitik": "https://www.aljazeera.com/xml/rss/all.rss",
    "Sport": "https://feeds.bbci.co.uk/sport/rss.xml",
    "Weltgeschehen": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "Biologie, Pharma & Chemie": "https://www.sciencedaily.com/rss/top/science.xml",
    "Technologie & Zukunft": "https://www.technologyreview.com/feed/"
}

tabs = st.tabs(list(feeds.keys()))

translator = GoogleTranslator(source='auto', target='de')

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
                    content_text = entry.summary if 'summary' in entry else (entry.description if 'description' in entry else "")
                    
                    # Optional übersetzen
                    if translate_german:
                        try:
                            title = translator.translate(title)
                            if content_text:
                                # Wir übersetzen die ersten Zeichen, um es schnell zu halten
                                content_text = translator.translate(content_text[:500])
                        except Exception:
                            pass # Falls die Übersetzung fehlschlägt, Original anzeigen
                    
                    with st.container():
                        st.markdown(f"**{title}**")
                        
                        with st.expander("Vollständigen Text / Details anzeigen"):
                            st.write(content_text)
                            st.markdown(f"[Direkt zur Originalquelle öffnen]({entry.link})")
                            
                        st.markdown("---")
        except Exception as e:
            st.error(f"Fehler beim Laden: {e}")
