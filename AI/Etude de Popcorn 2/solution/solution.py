import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

# Charger les données
df = pd.read_csv('./files/points.txt')

# Clustering
kmeans = DBSCAN(eps=5)
df['cluster'] = kmeans.fit_predict(df[['x', 'y']])

# Affichage des clusters
plt.figure(figsize=(10, 10))
for cluster_id in df['cluster'].unique():
    cluster_data = df[df['cluster'] == cluster_id]
    plt.scatter(cluster_data['x'], cluster_data['y'], label=f'Cluster {cluster_id}' if cluster_id != -1 else 'Noise')
    for i, row in cluster_data.iterrows():
        plt.text(row['x'], row['y'], row['char'], fontsize=12)

plt.ylabel('popcorn crispiness (%)')
plt.xlabel('moviegoer leaving before the end of the movie (%)')
plt.legend()
plt.show()

# Reconstitution de la phrase
sentence_parts = []

for cluster_id in df['cluster'].unique():
    if cluster_id == -1:
        continue
    cluster_data = df[df['cluster'] == cluster_id]
    cluster_data = cluster_data.sort_values(by='y')
    sentence_parts.append(''.join(cluster_data['char'].values))
    
print(sentence_parts)

