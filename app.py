import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# -------------------------
# CONFIGURATION DE LA PAGE
# -------------------------
st.set_page_config(page_title="Traducteur International Pro", page_icon="🗺️", layout="wide")

# Masquer la sidebar par défaut et injecter le style épuré
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

# -------------------------
# CONFIGURATION PAYPAL
# -------------------------
PAYPAL_CLIENT_ID = "DEMO"  # Mettez votre Client ID ici plus tard
PAYPAL_PLAN_ID = "DEMO"    # Mettez votre Plan ID ici plus tard

# -------------------------
# GESTION DE L'ACCÈS (SESSION STATE)
# -------------------------
if "est_abonne" not in st.session_state:
    st.session_state.est_abonne = False

try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    API_KEY = ""

# -------------------------
# INTERFACE SÉCURISÉE
# -------------------------
st.title("🗺️ Traducteur de Fiches Produits International — Version Pro")

# CAS 1 : L'UTILISATEUR N'A PAS PAYÉ
if not st.session_state.est_abonne:
    st.warning("🔒 Cette application est réservée aux membres de la version Premium.")
    
    col_offre, col_connexion = st.columns(2, gap="large")
    
    with col_offre:
        st.subheader("🚀 Débloquez l'IA pour 50 $/mois")
        st.write("Traduisez vos fiches produits en conservant un impact marketing maximal. L'IA adapte le copywriting et le SEO pour convertir instantanément à l'étranger.")
        st.write("Le paiement est entièrement sécurisé par **PayPal**.")
        
        if PAYPAL_CLIENT_ID == "DEMO":
            paypal_html = """
            <a href="https://paypal.com" target="_blank" style="text-decoration: none;">
                <div style="background-color: #ffc439; color: #003087; text-align: center; 
                            padding: 12px; font-family: Arial, sans-serif; font-weight: bold; 
                            border-radius: 4px; max-width: 300px; cursor: pointer; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    🟨 S'abonner avec PayPal (Démo)
                </div>
            </a>
            """
        else:
            paypal_html = f"""
            <div id="paypal-button-container-fixed" style="max-width: 350px; margin-top: 20px;"></div>
            <script src="https://paypal.com{PAYPAL_CLIENT_ID}&vault=true&intent=subscription" data-sdk-integration-source="button-factory"></script>
            <script>
              paypal.Buttons({{
                  style: {{ shape: 'rect', color: 'gold', layout: 'vertical', label: 'subscribe' }},
                  createSubscription: function(data, actions) {{
                    return actions.subscription.create({{ 'plan_id': '{PAYPAL_PLAN_ID}' }});
                  }},
                  onApprove: function(data, actions) {{
                    alert('Abonnement réussi ! ID : ' + data.subscriptionID);
                  }}
              }}).render('#paypal-button-container-fixed');
            </script>
            """
        
        components.html(paypal_html, height=150, scrolling=False)
        
    with col_connexion:
        st.subheader("🔑 Déjà abonné ?")
        st.write("Connectez-vous pour activer vos accès.")
        email = st.text_input("Adresse e-mail")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        
        if st.button("Se connecter", use_container_width=True):
            if email == "test@client.com" and mot_de_passe == "access50":
                st.session_state.est_abonne = True
                st.success("Accès accordé !")
                st.rerun()
            else:
                st.error("Identifiants incorrects ou abonnement PayPal inactif.")

# CAS 2 : L'UTILISATEUR EST ABONNÉ -> ACCÈS COMPLET
else:
    st.write("✨ **Bienvenue dans votre espace Premium.** Votre abonnement est actif.")
    if st.button("🚪 Se déconnecter", key="logout"):
        st.session_state.est_abonne = False
        st.rerun()
        
    st.write("---")

    with st.container(border=True):
        col_text, col_langs = st.columns(2)
        
        with col_text:
            texte_origine = st.text_area("Collez la fiche produit originale (Titre, description, caractéristiques...)", height=250, placeholder="Ex: Montre de luxe étanche. Idéale pour le quotidien...")
            
        with col_langs:
            langue_cible = st.selectbox("Langue de destination", [
                "🇺🇸 Anglais (USA)", 
                "🇬🇧 Anglais (UK)", 
                "🇩🇪 Allemand", 
                "🇪🇸 Espagnol", 
                "🇮🇹 Italien", 
                "🇳🇱 Néerlandais"
            ])
            optimisation = st.checkbox("Optimiser les expressions de vente pour la culture locale", value=True)

        generer = st.button("🚀 Lancer la Traduction Stratégique", use_container_width=True)

    if generer:
        if not API_KEY:
            st.error("⚠️ Erreur : La clé GROQ_API_KEY est manquante dans les Secrets du serveur.")
        elif not texte_origine:
            st.error("⚠️ Veuillez ajouter le texte à traduire.")
        else:
            with st.spinner("L'IA de Groq traduit et adapte votre contenu..."):
                try:
                    client = Groq(api_key=API_KEY)
                    
                    prompt_systeme = """Tu es un traducteur bilingue d'élite et un expert en copywriting e-commerce international.
                    Ton rôle est de traduire le texte fourni dans la langue cible demandée.
                    ATTENTION : Tu ne dois pas faire de la traduction mot-à-mot de base. Tu dois adapter le ton, les tournures de phrases et les expressions pour que le texte ait le même impact marketing et commercial que s'il avait été écrit directement par un natif du pays.
                    Ne fais aucun commentaire avant ou après, renvoie directement le texte entièrement traduit et mis en page en Markdown."""

                    reponse = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": prompt_systeme},
                            {"role": "user", "content": f"Texte à traduire : '{texte_origine}'. Langue cible : {langue_cible}. Adapter localement : {optimisation}."}
                        ],
                        temperature=0.4
                    )
                    
                    traduction_genere = reponse.choices.message.content
                    st.success("✨ Votre traduction optimisée est prête !")
                    st.markdown(traduction_genere)
                    st.text_area("Texte brut traduit :", value=traduction_genere, height=250)

                except Exception as e:
                    st.error(f"Erreur technique Groq : {str(e)}")
