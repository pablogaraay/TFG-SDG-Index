# Factores estructurales del desempeño sostenible

Repositorio asociado al Trabajo Fin de Grado:

**"Factores estructurales del desempeño sostenible: análisis econométrico y segmentación de países a partir del SDG Index"**

El proyecto estudia qué factores económicos, institucionales, educativos, tecnológicos y comerciales se asocian con el desempeño sostenible de los países, aproximado mediante el **SDG Index**. Para ello, combina análisis econométrico, visualización estadística y una fase complementaria de segmentación con **K-means**.

## Resumen

La investigación parte de una pregunta central: **qué rasgos estructurales ayudan a explicar por qué algunos países obtienen mejores resultados de sostenibilidad que otros**.

El análisis se organiza en tres bloques:

1. Explicación del **nivel del SDG Index en 2021**.
2. Estudio de la **variación del SDG Index entre 2021 y 2025**.
3. Evaluación de la **persistencia del desempeño sostenible**, analizando hasta qué punto el nivel de 2025 depende del registrado en 2021.

Como complemento, se aplica un algoritmo de **clustering K-means** para identificar grupos de países con perfiles estructurales similares.

## Metodología

El trabajo integra tres capas de análisis:

- **Análisis descriptivo**, para caracterizar la distribución del SDG Index y de las variables estructurales.
- **Modelos de regresión OLS**, para estimar asociaciones entre el SDG Index y un conjunto de variables explicativas tipificadas.
- **Clustering no supervisado**, para segmentar países según sus características estructurales y representar los resultados en un espacio bidimensional mediante **PCA**.

Las variables estructurales consideradas en el análisis incluyen:

- renta per cápita en PPP;
- eficacia del gobierno;
- gasto en educación;
- actividad innovadora aproximada por patentes;
- gasto en investigación y desarrollo;
- apertura comercial.

## Base de datos

La base de datos principal del proyecto se encuentra en:

```text
0. Final Data SDG Index.xlsx
```

Los scripts utilizan específicamente la hoja:

```text
Modelo_final_tipificado
```

## Estructura del repositorio

```text
.
|-- 0. Final Data SDG Index.xlsx
|-- README.md
|-- clustering.py
`-- images.py
```

### Archivos principales

- `images.py`: genera figuras descriptivas y gráficos asociados a los modelos econométricos estimados con OLS.
- `clustering.py`: ejecuta la segmentación de países mediante K-means, proyecta los resultados con PCA y exporta las tablas de salida.
- `0. Final Data SDG Index.xlsx`: base de datos utilizada por ambos scripts.

## Requisitos

El proyecto está desarrollado en Python y requiere, como mínimo, las siguientes librerías:

- `pandas`
- `numpy`
- `matplotlib`
- `statsmodels`
- `scikit-learn`
- `openpyxl`

Instalación sugerida:

```bash
pip install pandas numpy matplotlib statsmodels scikit-learn openpyxl
```

## Ejecución

### 1. Generación de figuras y resultados econométricos

```bash
python images.py
```

Este script:

- carga la base de datos desde Excel;
- genera histogramas, boxplots y gráficos de relación bivariada;
- estima tres modelos OLS;
- representa los coeficientes e intervalos de confianza;
- guarda las figuras en la carpeta `figuras_tfg`.

### 2. Segmentación de países con K-means

```bash
python clustering.py
```

Este script:

- selecciona las variables estructurales tipificadas;
- estima un modelo **K-means** con `n_clusters=4`;
- proyecta los resultados con **PCA**;
- genera una figura resumen del clustering;
- exporta tablas con la asignación de países y el perfil medio de cada clúster.

## Salidas generadas

Tras la ejecución de los scripts, se generan salidas como las siguientes:

- carpeta `figuras_tfg/` con las figuras del análisis descriptivo y econométrico;
- `figura_clustering_pca.png`;
- `resultados_clustering_kmeans.xlsx`;
- `perfil_medio_clusters.xlsx`.

## Alcance académico

Este repositorio documenta el componente empírico de un trabajo académico orientado al estudio comparado del desempeño sostenible entre países. Su objetivo principal es facilitar la trazabilidad del análisis, la reproducibilidad de los scripts y la organización del material cuantitativo utilizado en el TFG.

## Notas

- Los scripts asumen que el archivo Excel se encuentra en la raíz del proyecto.
- Los nombres de columnas y de hojas deben mantenerse sin cambios para garantizar la ejecución correcta.
- El repositorio puede ampliarse en el futuro con notebooks, tablas de resultados o documentación metodológica adicional.
