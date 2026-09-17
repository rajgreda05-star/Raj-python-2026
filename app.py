import streamlit as st # Creation une  site WEBE
import pandas as pd # Pour faire un tableau 

st.set_page_config(
    layout="wide",
    page_title="Grossiste Site" # Pour faire une titre de ce site 
)
st.title("Mon site Grossiste") # Grand titre en haute de cet affichage
st.write("ON fait analyse des ventes") # Titre 2eme 

df=pd.read_csv("VENTES_1AN_Ar.csv")# Lire fichier CSV


st.success(f"Charger:{len(df)} lignes") # Afiicher le nombre de ligne de ce tableau 
st.dataframe(df.head())# Pour voir les  5 premiers lignes dans notre df

df.columns=df.columns.str.strip().str.lower() # Sup les espaces et fait les colonnes en miniscule
st.sidebar.header("FILTRES") # Titre en haute mais au côté gauche 
region=["Tous"] + list(df["region"].unique()) # Fitre des regions  tous avec les listes dans ce notre df

choix_region=st.sidebar.selectbox("choisis une region", region) # Choisir les noms de la region

#LOGIQUE sur les filtres 
if choix_region !="Tous":
    df_filtre=df[df["region"]==choix_region]
else:
    df_filtre=df

st.success(f"Charger={len(df_filtre)} lignes-Region:{choix_region}")
st.dataframe(df_filtre,use_container_width=True)

# On veut faire une courbe
df["date"]=pd.to_datetime(df["date"])

CA_Par_Jour=df_filtre.groupby("date")["total_ar"].sum()

st.subheader(f"Courbe CA - {choix_region}")
st.line_chart(CA_Par_Jour)

import altair as alt  # ajoute ça en haut avec tes autres import

# --- BARRES AVEC COULEURS DIFFÉRENTES ---
st.subheader(f"CA par Région - Filtre: {choix_region}")

# On prépare les données
ca_region = df_filtre.groupby("region")["total_ar"].sum().reset_index()

# On crée le graphique avec couleur = région
chart = alt.Chart(ca_region).mark_bar().encode(
    x=alt.X("region", title="Région"),
    y=alt.Y("total_ar", title="CA en Ar"),
    color=alt.Color("region", title="Région"),  # <-- C'est ça qui donne une couleur par barre
    tooltip=["region", "total_ar"] # affiche le chiffre quand tu passes la souris
)

st.altair_chart(chart, use_container_width=True)


# Filtre 2 : Type de produit (catégorie)
categories = ["Tous"] + list(df['categorie'].unique())
choix_categorie = st.sidebar.selectbox("Choisis type de produit", categories)

# On applique les 2 filtres en même temps
df_filtre = df.copy()

if choix_region != "Tous":
    df_filtre = df_filtre[df_filtre['region'] == choix_region]

if choix_categorie != "Tous":
    df_filtre = df_filtre[df_filtre['categorie'] == choix_categorie]

st.success(f"{len(df_filtre)} lignes - Région: {choix_region} | Type: {choix_categorie}")


import altair as alt

st.subheader(f"CA par Produit - {choix_region} | {choix_categorie}")

ca_produit = df_filtre.groupby("nom_produit")["total_ar"].sum().reset_index()
ca_produit = ca_produit.sort_values("total_ar", ascending=False) # du plus gros au plus petit

chart_produit = alt.Chart(ca_produit).mark_bar().encode(
    x=alt.X("nom_produit", sort="-y", title="Produit"),
    y=alt.Y("total_ar", title="CA en Ar"),
    color=alt.Color("nom_produit", legend=None), # une couleur par produit, sans légende
    tooltip=["nom_produit", "total_ar"]
)
st.altair_chart(chart_produit, use_container_width=True)



