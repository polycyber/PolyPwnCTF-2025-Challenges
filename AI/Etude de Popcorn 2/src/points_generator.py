import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import string

# Phrase à encoder
phrase = "When there is noise, DBSCAN is your friend. Your flag is: polycyber{DB5c4nF0rClu57er1ng1SGr34t}"

# Nombre de clusters
nb_clusters = 8

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

np.random.seed(35)  # Pour reproductibilité

# Génération des clusters avec des points proches
cluster_centers_x = np.random.uniform(0, 100, nb_clusters)
cluster_centers_y = np.random.uniform(0, 100, nb_clusters)
cluster_centers = list(zip(cluster_centers_x, cluster_centers_y))

for idx, (part, center) in enumerate(zip(parts, cluster_centers)):
    num_chars = len(part)
    center_x, center_y = center
    
    # Génération de points autour du centre
    distances = np.linspace(0, 5, num_chars)  # Distances croissantes
    angles = np.random.uniform(0, 2 * np.pi, num_chars)  # Angles aléatoires
    x = center_x + distances * np.cos(angles)
    y = center_y + distances * np.sin(angles)
    
    # Ajouter les points générés au DataFrame
    df_cluster = pd.DataFrame({
        'x': x,
        'y': y,
        'type': 'point',
    })
    df_points = pd.concat([df_points, df_cluster], ignore_index=True)

# Ajout de points de bruit aléatoires
n_noise = 50  # Nombre de points bruités
noise_x = np.random.uniform(0, 100, n_noise)
noise_y = np.random.uniform(0, 100, n_noise)

df_noise = pd.DataFrame({'x': noise_x, 'y': noise_y, 'type': 'noise'})

# Supprime tous les points de bruit trop proches des clusters
for idx, center in enumerate(cluster_centers):
    center_x, center_y = center
    df_noise = df_noise[~((df_noise['x'] > center_x - 10) & (df_noise['x'] < center_x + 10) &
                          (df_noise['y'] > center_y - 10) & (df_noise['y'] < center_y + 10))]
    
df_points = pd.concat([df_points, df_noise], ignore_index=True)

# Application de DBSCAN
from sklearn.cluster import DBSCAN

# Paramètres de DBSCAN
eps = 5 
dbscan = DBSCAN(eps=eps)
df_points['cluster'] = dbscan.fit_predict(df_points[['x', 'y']])

# Print noise associated with a cluster
wrong1 = df_points[(df_points['cluster'] != -1) & (df_points['type'] == 'noise')]
wrong2 = df_points[(df_points['cluster'] == -1) & (df_points['type'] != 'noise')]

assert len(wrong1) == 0, f"Points bruités associés à un cluster: {wrong1}"
assert len(wrong2) == 0, f"Points de cluster associés au bruit: {wrong2}"

# Affichage des clusters, O pour le bruit
plt.figure(figsize=(10, 8))
colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown']
for cluster_id in df_points['cluster'].unique():
    cluster_points = df_points[df_points['cluster'] == cluster_id]
    plt.scatter(cluster_points['x'], cluster_points['y'],
                label=f"Cluster {cluster_id}" if cluster_id >= 0 else "Noise",
                alpha=0.7)
    

plt.title('Nuage de points avec bruit')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()

# Associer une lettre à chaque point
for i, part in enumerate(parts):
    cluster_data = df_points[df_points['cluster'] == i]
    cluster_data = cluster_data.sort_values(by='y')
    cluster_data["char"] = list(part)

    print(f"Cluster {i}:", ''.join(cluster_data['char'].values))
    df_points.loc[df_points['cluster'] == i, 'char'] = cluster_data['char']

# Assign random letters to noise
df_points.loc[df_points['cluster'] == -1, 'char'] = np.random.choice(list(string.ascii_letters), len(df_points[df_points['cluster'] == -1]), replace=False)

# Shuffle all
df_points = df_points.sample(frac=1).reset_index(drop=True)

# Save points
df_points[['x', 'y', 'char']].to_csv('./files/points.txt', index=False)



