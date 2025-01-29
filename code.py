import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Génération d'un DataFrame fictif pour l'exemple
data = {
    "valeur": np.random.choice(["A", "B", "C", "D", "E"], 100),
    "date": pd.date_range(start="2023-01-01", periods=100, freq="D")
}
df = pd.DataFrame(data)

# Assurez-vous que la colonne 'date' est bien en datetime
df["date"] = pd.to_datetime(df["date"])

# Comptage total des occurrences de chaque grandeur
total_counts = df["valeur"].value_counts()

# Création d'une matrice pour stocker les quotients
grandeurs = total_counts.index
matrix = pd.DataFrame(0.0, index=grandeurs, columns=grandeurs)

# Calcul du nombre d'occurrences avec une autre grandeur à ±7 jours
for i, row in df.iterrows():
    grandeur_1 = row["valeur"]
    date_1 = row["date"]

    # Filtrer les occurrences dans la plage de 7 jours
    mask = (df["date"] >= date_1 - pd.Timedelta(days=7)) & (df["date"] <= date_1 + pd.Timedelta(days=7))
    proches = df[mask]

    # Compter les co-occurrences avec les autres grandeurs
    for grandeur_2 in proches["valeur"].unique():
        if grandeur_1 != grandeur_2:
            matrix.loc[grandeur_1, grandeur_2] += 1

# Normalisation par le nombre total d'apparitions de chaque grandeur
for grandeur in grandeurs:
    matrix.loc[grandeur] /= total_counts[grandeur]

# Tracer la heatmap avec seaborn
plt.figure(figsize=(8, 6))
sns.heatmap(matrix, annot=True, cmap="Blues", fmt=".2f", linewidths=0.5)
plt.title("Matrice des quotients des co-occurrences dans un intervalle de ±7 jours")
plt.xlabel("Grandeur 2")
plt.ylabel("Grandeur 1")
plt.show()