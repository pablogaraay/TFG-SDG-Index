import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

file_path = "0. Final Data SDG Index.xlsx"
df = pd.read_excel(file_path, sheet_name="Modelo_final_tipificado")

cluster_vars = [
    "z_ln_GDP_per_capita_PPP",
    "z_Government_Effectiveness",
    "z_Education_expenditure_pct_GDP",
    "z_ln_Patents_per_million_plus_1",
    "z_Research_expenditure_pct_GDP",
    "z_Trade_pct_GDP"
]

df_cluster = df[["País", "Código país"] + cluster_vars].copy()

df_cluster = df_cluster.dropna(subset=cluster_vars).reset_index(drop=True)

X = df_cluster[cluster_vars].values

kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

df_cluster["cluster"] = kmeans.fit_predict(X)

df_cluster["cluster"] = df_cluster["cluster"] + 1

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

df_cluster["PC1"] = X_pca[:, 0]
df_cluster["PC2"] = X_pca[:, 1]

print("Varianza explicada por PC1 y PC2:")
print(pca.explained_variance_ratio_)

print("\nVarianza explicada acumulada:")
print(pca.explained_variance_ratio_.sum())

plt.figure(figsize=(10, 7))

scatter = plt.scatter(
    df_cluster["PC1"],
    df_cluster["PC2"],
    c=df_cluster["cluster"],
    cmap="tab10",
    s=70,
    alpha=0.85,
    edgecolor="black"
)

countries_to_label = [
    "Luxembourg",
    "Singapore",
    "United States",
    "Finland",
    "Madagascar"
]

for _, row in df_cluster.iterrows():
    if row["País"] in countries_to_label:
        plt.text(
            row["PC1"] + 0.05,
            row["PC2"] + 0.05,
            row["País"],
            fontsize=9
        )

plt.title("Segmentación de países mediante K-means en proyección PCA")
plt.xlabel("Componente principal 1")
plt.ylabel("Componente principal 2")
plt.grid(True, alpha=0.3)

plt.legend(
    *scatter.legend_elements(),
    title="Clúster",
    loc="best"
)

plt.tight_layout()

plt.savefig("figura_clustering_pca.png", dpi=300, bbox_inches="tight")
plt.close()

print("\nFigura guardada como: figura_clustering_pca.png")

print("\nPaíses por clúster:")

for c in sorted(df_cluster["cluster"].unique()):
    countries = df_cluster.loc[df_cluster["cluster"] == c, "País"].tolist()
    print(f"\nClúster {c} ({len(countries)} países):")
    print(", ".join(countries))

cluster_profile = (
    df_cluster
    .groupby("cluster")[cluster_vars]
    .mean()
    .round(2)
)

print("\nPerfil medio de cada clúster:")
print(cluster_profile)

df_cluster.to_excel("resultados_clustering_kmeans.xlsx", index=False)
cluster_profile.to_excel("perfil_medio_clusters.xlsx")

print("\nArchivos guardados:")
print("- resultados_clustering_kmeans.xlsx")
print("- perfil_medio_clusters.xlsx")

print("\nClustering ejecutado correctamente.")