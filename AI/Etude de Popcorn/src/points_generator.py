import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Phrase à encoder
phrase = "K-means clustering unveils patterns like magic. Your flag is: polycyber{Km34nF0rClu57er1ng}"

# Nombre de clusters
nb_clusters = 4

# Division de la phrase en parties pour chaque cluster
def split_phrase(phrase, nb_clusters):
    length = len(phrase)
    part_size = length // nb_clusters
    parts = []
    for i in range(nb_clusters):
        start_index = i * part_size
        if i != nb_clusters - 1:
            end_index = (i + 1) * part_size
        else:
            end_index = length
        parts.append(phrase[start_index:end_index])
    return parts

parts = split_phrase(phrase, nb_clusters)

# Création d'un DataFrame pour stocker les points
df_points = pd.DataFrame(columns=['x', 'y'])

np.random.seed(30)  # Pour reproductibilité

# Génération aléatoire des points
for i, part in enumerate(parts):
    nb_points = len(part)
    center_x = np.random.uniform(0, 30)
    center_y = np.random.uniform(5, 50)
    x = np.random.normal(center_x, 2, nb_points)

    # On ajoute un peu de bruit pour rendre les points moins alignés
    y = np.random.normal(center_y, 2, nb_points)

    df_part = pd.DataFrame({'x': x, 'y': y})
    df_points = pd.concat([df_points, df_part])


# plot des points
plt.figure(figsize=(10, 10))
plt.scatter(df_points['x'], df_points['y'])
for i, row in df_points.iterrows():
    plt.text(row['x'], row['y'], phrase[i], fontsize=12)
plt.show()

# Application de K-means pour regrouper les points en clusters
kmeans = KMeans(n_clusters=nb_clusters)
df_points['cluster'] = kmeans.fit_predict(df_points[['x', 'y']])

# Ajout des centres trouvés par K-means
cluster_centers = kmeans.cluster_centers_

# Attribution des caractères en fonction de la distance au centre
df_points['distance_to_center'] = df_points.apply(
    lambda row: np.sqrt(
        (row['x'] - cluster_centers[int(row['cluster']), 0])**2 +
        (row['y'] - cluster_centers[int(row['cluster']), 1])**2
    ),
    axis=1
)

# Tri des points par cluster et par distance au centre
df_points_sorted = df_points.sort_values(['cluster', 'distance_to_center'], ascending=[True, True])
# Attribution des caractères triés par cluster
chars = list(phrase)
df_points_sorted['char'] = chars
print(df_points_sorted)

# Mélange des points pour le challenge (les caractères restent fixés aux points)
df_points_shuffled = df_points_sorted.sample(frac=1, random_state=42).reset_index(drop=True)

# Sauvegarde des données pour les participants (coordonnées et caractères)
df_points_shuffled[['x', 'y', 'char']].to_csv('./files/points.txt', index=False)
