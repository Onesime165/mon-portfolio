import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "Onesime165"  # Remplacez par votre nom d'utilisateur GitHub
REPO_NAME = "mon-portfolio"  # Remplacez par le nom de votre dépôt

# Configuration de la page Streamlit
st.set_page_config(page_title="Mon Portfolio", page_icon="📁", layout="wide")

# En-tête
st.title("Mon Portfolio")
st.markdown("Bienvenue sur mon portfolio ! Retrouvez ici mes travaux et projets.")

# Fonction pour récupérer les fichiers depuis GitHub
def get_github_files(folder):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{folder}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erreur lors de la récupération des fichiers depuis {folder}")
        return []

# Afficher les images
st.header("Galerie d'images")
image_files = get_github_files("images")
cols = st.columns(3)  # Afficher les images en 3 colonnes

for idx, file in enumerate(image_files):
    if file["name"].lower().endswith(('.png', '.jpg', '.jpeg')):
        with cols[idx % 3]:
            image_url = file["download_url"]
            st.image(image_url, caption=file["name"], use_column_width=True)

# Afficher les travaux (PDF)
st.header("Mes travaux")
pdf_files = get_github_files("works")

for file in pdf_files:
    if file["name"].lower().endswith('.pdf'):
        with st.expander(f"Projet: {file['name']}"):
            st.write(f"**Nom du fichier**: {file['name']}")
            st.markdown(f"[Télécharger le PDF]({file['download_url']})")

# Pied de page
st.markdown("---")
st.write("Portfolio mis à jour automatiquement depuis mon dépôt GitHub.")