"""
Csabagyöngye – Streamlit Cloud
Ez a fájl a Streamlit Cloud-on futó fő alkalmazás
"""

import streamlit as st

st.set_page_config(
    page_title="Csabagyöngye",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# PWA meta tagek injekciója – iOS és Android home screen támogatáshoz
st.markdown("""
<script>
(function() {
    function injectPWATags() {
        const head = document.head;

        const metas = [
            { name: "apple-mobile-web-app-capable",           content: "yes" },
            { name: "apple-mobile-web-app-status-bar-style",  content: "default" },
            { name: "apple-mobile-web-app-title",             content: "Csabagyöngye" },
            { name: "mobile-web-app-capable",                 content: "yes" },
            { name: "theme-color",                            content: "#2c3e50" },
            { name: "application-name",                       content: "Csabagyöngye" },
        ];

        metas.forEach(function(m) {
            if (!document.querySelector('meta[name="' + m.name + '"]')) {
                var el = document.createElement("meta");
                el.name = m.name;
                el.content = m.content;
                head.appendChild(el);
            }
        });

        var iconSizes = ["57x57","60x60","72x72","76x76","114x114","120x120","144x144","152x152","180x180"];
        iconSizes.forEach(function(sz) {
            if (!document.querySelector('link[rel="apple-touch-icon"][sizes="' + sz + '"]')) {
                var link = document.createElement("link");
                link.rel = "apple-touch-icon";
                link.sizes = sz;
                link.href = "/app/static/icon-192.png";
                head.appendChild(link);
            }
        });

        if (!document.querySelector('link[rel="apple-touch-icon"]:not([sizes])')) {
            var link = document.createElement("link");
            link.rel = "apple-touch-icon";
            link.href = "/app/static/icon-192.png";
            head.appendChild(link);
        }

        if (!document.querySelector('link[rel="manifest"]')) {
            var link = document.createElement("link");
            link.rel = "manifest";
            link.href = "/app/static/manifest.json";
            head.appendChild(link);
        }

        var viewport = document.querySelector('meta[name="viewport"]');
        if (viewport) {
            viewport.content = "width=device-width, initial-scale=1.0, viewport-fit=cover";
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", injectPWATags);
    } else {
        injectPWATags();
    }
})();
</script>
""", unsafe_allow_html=True)

# Import és futtatás a quiz_app_advanced.py-ból
from quiz_app_advanced import main

if __name__ == "__main__":
    main()
