import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Charger les données
df = pd.read_csv('./files/points.txt')

# Clustering
kmeans = KMeans(n_clusters=4)
df['cluster'] = kmeans.fit_predict(df[['x', 'y']])

# cluster center
df['center_x'] = kmeans.cluster_centers_[df['cluster'], 0]
df['center_y'] = kmeans.cluster_centers_[df['cluster'], 1]

# Affichage des clusters
plt.figure(figsize=(10, 10))
for cluster_id in df['cluster'].unique():
    cluster_data = df[df['cluster'] == cluster_id]
    plt.scatter(cluster_data['x'], cluster_data['y'], label=f'Cluster {cluster_id}')
    for i, row in cluster_data.iterrows():
        plt.text(row['x'], row['y'], row['char'], fontsize=12)

plt.ylabel('popcorn eating speed (grams per minute)')
plt.xlabel('time spent before the beginning of the movie (minutes)')
plt.legend()
plt.savefig('./solution/clusters.png')

# Reconstitution de la phrase
sentence_parts = []

for cluster_id in df['cluster'].unique():
    cluster_data = df[df['cluster'] == cluster_id]
    cluster_data["dist_to_center"] = np.sqrt((cluster_data['x'] - cluster_data['center_x'])**2 + (cluster_data['y'] - cluster_data['center_y'])**2)
    cluster_data = cluster_data.sort_values(by='dist_to_center')
    sentence_parts.append(''.join(cluster_data['char'].values))
    
print(sentence_parts)

