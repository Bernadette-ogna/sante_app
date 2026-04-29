import streamlit as st
import psycopg2
from datetime import datetime

# ================= CONFIG =================
DB_NAME = st.secrets["DB_NAME"]
DB_USER = st.secrets["DB_USER"]
DB_PASS = st.secrets["DB_PASS"]
DB_HOST = st.secrets["DB_HOST"]
DB_PORT = "5432"

ADMIN_USER = "admin"
ADMIN_PASS = "1234"

BG = "https://images.unsplash.com/photo-1576091160550-2173dba999ef"

# ================= STYLE =================
def set_bg():
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{BG}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    .box {{
        background: rgba(0,0,0,0.65);
        padding: 20px;
        border-radius: 15px;
        color: white;
    }}
    </style>
    """, unsafe_allow_html=True)

# ================= DATABASE =================
def get_conn():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
        sslmode="require"
    )

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS recensement(
        id SERIAL PRIMARY KEY,
        nom TEXT,
        prenom TEXT,
        ville TEXT,
        alimentation TEXT,
        sport TEXT,
        sommeil TEXT,
        stress TEXT,
        tabac TEXT,
        alcool TEXT,
        eau TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

# ================= INIT =================
set_bg()
init_db()

if "page" not in st.session_state:
    st.session_state.page = "home"

# ================= HOME =================
if st.session_state.page == "home":
    st.markdown('<div class="box">', unsafe_allow_html=True)

    st.title("🏥 BIENVENUE SUR HEALTH FACTS")
    st.write("Collecte intelligente des facteurs de santé")

    col1, col2 = st.columns(2)

    if col1.button("COMMENCER"):
        st.session_state.page = "form"

    if col2.button("ADMIN"):
        st.session_state.page = "login"

    st.markdown('</div>', unsafe_allow_html=True)

# ================= FORMULAIRE =================
elif st.session_state.page == "form":
    st.markdown('<div class="box">', unsafe_allow_html=True)

    st.title("Formulaire Santé")

    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    ville = st.text_input("Ville")

    alimentation = st.selectbox("Alimentation", ["Mauvaise", "Moyenne", "Bonne"])
    sport = st.selectbox("Sport", ["Jamais", "Parfois", "Régulière"])
    sommeil = st.selectbox("Sommeil", ["Mauvais", "Moyen", "Bon"])
    stress = st.selectbox("Stress", ["Faible", "Moyen", "Élevé"])
    tabac = st.selectbox("Tabac", ["Oui", "Non"])
    alcool = st.selectbox("Alcool", ["Oui", "Non"])
    eau = st.selectbox("Hydratation", ["Faible", "Correcte"])

    if st.button("Enregistrer"):
        try:
            conn = get_conn()
            cur = conn.cursor()

            cur.execute("""
            INSERT INTO recensement(
                nom, prenom, ville, alimentation, sport,
                sommeil, stress, tabac, alcool, eau, created_at
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                nom, prenom, ville,
                alimentation, sport,
                sommeil, stress,
                tabac, alcool,
                eau,
                datetime.now().isoformat()
            ))

            conn.commit()
            conn.close()

            st.success("Données enregistrées avec succès ✅")

        except Exception as e:
            st.error(f"Erreur : {e}")

    if st.button("⬅ Retour"):
        st.session_state.page = "home"

    st.markdown('</div>', unsafe_allow_html=True)

# ================= LOGIN ADMIN =================
elif st.session_state.page == "login":
    st.markdown('<div class="box">', unsafe_allow_html=True)

    st.title("Connexion Admin")

    user = st.text_input("Utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Connexion"):
        if user == ADMIN_USER and password == ADMIN_PASS:
            st.session_state.page = "dashboard"
        else:
            st.error("Accès refusé")

    if st.button("⬅ Retour"):
        st.session_state.page = "home"

    st.markdown('</div>', unsafe_allow_html=True)

# ================= DASHBOARD =================
elif st.session_state.page == "dashboard":
    st.markdown('<div class="box">', unsafe_allow_html=True)

    st.title("Dashboard Santé")

    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
        SELECT nom, prenom, ville, stress, tabac, alcool
        FROM recensement
        ORDER BY id DESC
        """)

        data = cur.fetchall()
        conn.close()

        st.write(f"Nombre total de participants : {len(data)}")
        st.table(data)

    except Exception as e:
        st.error(f"Erreur : {e}")

    if st.button("Déconnexion"):
        st.session_state.page = "home"

    st.markdown('</div>', unsafe_allow_html=True)
