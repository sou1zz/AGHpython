import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_blobs, make_circles
from sklearn.cluster import DBSCAN as SklearnDBSCAN
import unittest

# Własna implementacja DBSCAN
def dbscan(data, eps, min_samples):
    #Implementacja algorytmu DBSCAN (Density-Based Spatial Clustering of Applications with Noise)

    n = data.shape[0]  # Liczba punktów danych
    labels = -np.ones(n)  # Inicjalizacja etykiet (-1 oznacza szum)
    cluster_id = 0  # Identyfikator pierwszego klastra
    visited = np.zeros(n, dtype=bool)  # Tablica śledząca, czy punkt został odwiedzony

    def region_query(point_idx):
        #Znajduje sąsiadów danego punktu w promieniu eps.

        distances = np.linalg.norm(data - data[point_idx], axis=1)  # Odległości euklidesowe
        return np.where(distances <= eps)[0]  # Indeksy punktów spełniających warunek odległości

    def expand_cluster(point_idx, neighbors):
        #Rozszerza klaster, przypisując punkty do niego na podstawie sąsiedztwa.

        nonlocal cluster_id
        labels[point_idx] = cluster_id  # Przypisanie punktu do klastra
        i = 0
        while i < len(neighbors):  # Przechodzenie po sąsiadach
            neighbor_idx = neighbors[i]
            if not visited[neighbor_idx]:
                visited[neighbor_idx] = True  # Oznaczenie sąsiada jako odwiedzonego
                new_neighbors = region_query(neighbor_idx)  # Znajdowanie sąsiadów sąsiada
                if len(new_neighbors) >= min_samples:
                    neighbors = np.append(neighbors, new_neighbors)  # Dodanie nowych sąsiadów
            if labels[neighbor_idx] == -1:  # Punkt wcześniej oznaczony jako szum
                labels[neighbor_idx] = cluster_id  # Przypisanie do obecnego klastra
            i += 1

    for i in range(n):
        if visited[i]:  # Jeśli punkt był już odwiedzony, pomijamy go
            continue
        visited[i] = True  # Oznaczenie punktu jako odwiedzonego
        neighbors = region_query(i)  # Znajdowanie sąsiadów
        if len(neighbors) < min_samples:
            labels[i] = -1  # Punkt oznaczony jako szum
        else:
            cluster_id += 1  # Inkrementacja identyfikatora klastra
            expand_cluster(i, neighbors)  # Rozszerzenie klastra

    return labels

# Generowanie danych
data, _ = make_moons(n_samples=300, noise=0.05, random_state=42)  # Przykładowe dane (kształt półksiężyców)
#data, _ = make_circles(n_samples=300, noise=0.05, factor=0.5, random_state=42)
#data, _ = make_blobs(n_samples=1000, centers=5, cluster_std=0.6, random_state=42)

# Parametry DBSCAN
eps = 0.25  # Maksymalna odległość między sąsiadami
min_samples = 7  # Minimalna liczba punktów w klastrze

# Klasyfikacja z użyciem własnej implementacji
custom_labels = dbscan(data, eps, min_samples)

# Klasyfikacja z użyciem sklearn
sklearn_labels = SklearnDBSCAN(eps=eps, min_samples=min_samples).fit_predict(data)

# Porównanie wyników
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Wykres własnej implementacji
axs[0].scatter(data[:, 0], data[:, 1], c=custom_labels, cmap="viridis", s=10)
axs[0].set_title("Własna implementacja DBSCAN")

# Wykres implementacji sklearn
axs[1].scatter(data[:, 0], data[:, 1], c=sklearn_labels, cmap="viridis", s=10)
axs[1].set_title("Sklearn DBSCAN")

plt.show()



'''=================================UNITTESTY=========================='''
# Testy jednostkowe
class TestDBSCAN(unittest.TestCase):
    def setUp(self):
        #Przygotowanie danych testowych

        self.data, _ = make_moons(n_samples=300, noise=0.05, random_state=42)
        self.eps = 0.2
        self.min_samples = 5

    def test_cluster_count(self):
        #Test porównujący liczbę klastrów między implementacjami

        custom_labels = dbscan(self.data, self.eps, self.min_samples)
        sklearn_labels = SklearnDBSCAN(eps=self.eps, min_samples=self.min_samples).fit_predict(self.data)
        custom_cluster_count = len(set(custom_labels)) - (1 if -1 in custom_labels else 0)
        sklearn_cluster_count = len(set(sklearn_labels)) - (1 if -1 in sklearn_labels else 0)
        self.assertEqual(custom_cluster_count, sklearn_cluster_count)

    def test_noise_points(self):
        #Test sprawdzający, czy liczba punktów szumu jest zgodna między implementacjami

        custom_labels = dbscan(self.data, self.eps, self.min_samples)
        sklearn_labels = SklearnDBSCAN(eps=self.eps, min_samples=self.min_samples).fit_predict(self.data)
        custom_noise_count = np.sum(custom_labels == -1)
        sklearn_noise_count = np.sum(sklearn_labels == -1)
        self.assertEqual(custom_noise_count, sklearn_noise_count)

    def test_label_consistency(self):
        #Test sprawdzający, czy etykiety są spójne między implementacjami dla tych samych danych

        custom_labels = dbscan(self.data, self.eps, self.min_samples)
        sklearn_labels = SklearnDBSCAN(eps=self.eps, min_samples=self.min_samples).fit_predict(self.data)

        # Mapowanie etykiet między implementacjami
        custom_labels_mapped = self.map_labels(custom_labels, sklearn_labels)
        self.assertTrue(np.array_equal(custom_labels_mapped, sklearn_labels))

    @staticmethod
    def map_labels(custom_labels, sklearn_labels):
        # Mapuje etykiety klastrów z implementacji własnej na etykiety z implementacji sklearn.
        unique_custom = set(custom_labels)
        unique_sklearn = set(sklearn_labels)

        label_map = {}
        for custom_label in unique_custom:
            if custom_label == -1:
                label_map[custom_label] = -1
                continue
            matching_labels = [sklearn_label for sklearn_label in unique_sklearn
                               if np.sum((custom_labels == custom_label) & (sklearn_labels == sklearn_label)) > 0]
            label_map[custom_label] = matching_labels[0] if matching_labels else -1

        return np.array([label_map[label] for label in custom_labels])

if __name__ == "__main__":
    unittest.main()