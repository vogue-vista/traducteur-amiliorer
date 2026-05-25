import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# -------------------------
# CONFIGURATION DE LA PAGE
# -------------------------
st.set_page_config(page_title="Traducteur International Pro", page_icon="🗺️", layout="wide")

st.markdown("""
<style>
[data-testid="stSidebar"] {display: none !important;}
[data-testid="stSidebarNav"] {display: none !important;}
@import url('https://googleapis.com');
html, body, div, p, h1, h2, h3, h4, h5, h6, span {
    font-family: 'Poppins', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

PAYPAL_CLIENT_ID = "DEMO"
PAYPAL_PLAN_ID = "DEMO"

if "est_abonne" not in st.session_state:
    st.session_state.est_abonne = False

try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    API_KEY = ""

st.title("🗺️ Traducteur de Fiches Produits International")

if not st.session_state.est_abonne:
    st.warning("🔒 Application réservée aux membres Premium.")
    col_offre, col_connexion = st.columns(2, gap="large")
    
    with col_offre:
        st.subheader("🚀 Débloquez l'IA pour 50 $/mois")
        paypal_html = """
        <a href="https://paypal.com" target="_blank" style="text-decoration: none;">
            <div style="background-color: #ffc439; color: #003087; text-align: center; padding: 12px; font-weight: bold; border-radius: 4px; max-width: 300px;">
                🟨 S'abonner avec PayPal (Démo)
            </div>
        </a>
        """
        components.html(paypal_html, height=150, scrolling=False)
        
    with col_connexion:
        st.subheader("🔑 Déjà abonné ?")
        email = st.text_input("Adresse e-mail")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter", use_container_width=True):
            if email == "test@client.com" and mot_de_passe == "access50":
                st.session_state.est_abonne = True
                st.rerun()
            else:
                st.error("Identifiants incorrects.")
else:
    st.write("✨ Espace Premium Actif.")
    if st.button("🚪 Se déconnecter"):
        st.session_state.est_abonne = False
        st.rerun()

    with st.container(border=True):
        col_text, col_langs = st.columns(2)
        with col_text:
            texte_origine = st.text_area("Fiche produit originale", height=200, placeholder="Texte à traduire...")
        with col_langs:
            langue_cible = st.selectbox("Langue cible", ["🇺🇸 Anglais (USA)", "🇩🇪 Allemand", "🇪🇸 Espagnol", "🇮🇹 Italien"])
            optimisation = st.checkbox("Optimiser le copywriting local", value=True)

        generer = st.button("🚀 Lancer la Traduction Stratégique", use_container_width=True)

    if generer:
        if not API_KEY:
            st.error("⚠️ Clé manquante.")
        elif not text_origine if 'text_origine' in locals() else not texte_origine:
            st.error("⚠️ Ajoutez du texte.")
        else:
            with st.spinner("Traduction en cours..."):
                try:
                    client = Groq(api_key=API_KEY)
                    prompt_systeme = "Tu es un traducteur expert. Adapte le ton marketing et renvoie directement le texte traduit en Markdown, sans introduction."
                    reponse = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": prompt_systeme},
                            {"role": "user", "content": f"Traduire en {langue_cible}. Texte : {texte_origine}. Optimisation locale: {optimisation}"}
                        ],
                        temperature=0.4
                    )
                    traduction_genere = reponse.choices[0].message.content
                    st.success("✨ Traduction prête !")
                    st.markdown(traduction_genere)
                except Exception as e:
                    st.error(f"Erreur : {str(e)}")

