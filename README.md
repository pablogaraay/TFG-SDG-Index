# Análisis econométrico y segmentación de países a partir del SDG Index

Este repositorio contiene el material asociado al Trabajo Fin de Grado titulado:

**“Factores estructurales del desempeño sostenible: análisis econométrico y segmentación de países a partir del SDG Index”**

El objetivo del proyecto es analizar qué factores económicos, institucionales, educativos, tecnológicos y comerciales se asocian con el desempeño sostenible de los países, medido a través del **SDG Index**. Para ello, el trabajo combina herramientas de econometría clásica con una técnica complementaria de aprendizaje no supervisado, **K-means**, con el fin de identificar perfiles estructurales diferenciados entre países.

---

## 1. Descripción general del proyecto

El proyecto parte de una pregunta económica central:

> ¿Qué factores estructurales ayudan a explicar por qué unos países presentan mejores niveles de sostenibilidad que otros?

A partir de esta cuestión, el análisis se organiza en tres planos complementarios:

1. **Nivel inicial de sostenibilidad**  
   Se estudia qué variables estructurales ayudan a explicar el valor del **SDG Index en 2021**.

2. **Cambio reciente en sostenibilidad**  
   Se analiza qué factores se asocian con la **variación del SDG Index entre 2021 y 2025**.

3. **Persistencia del desempeño sostenible**  
   Se evalúa hasta qué punto el valor del **SDG Index 2025** depende del nivel que cada país ya tenía en 2021.

Además, el trabajo incorpora una capa complementaria de segmentación mediante **clustering K-means**, con el objetivo de agrupar países según sus características estructurales.

---

## 2. Enfoque económico del análisis

El trabajo parte de la idea de que la sostenibilidad no puede explicarse mediante una única variable. El desempeño sostenible de un país depende de una combinación de factores estructurales, entre ellos:

- capacidad económica;
- calidad institucional;
- inversión educativa;
- capacidad innovadora;
- esfuerzo en investigación y desarrollo;
- grado de apertura comercial;
- trayectoria previa del país.

Por este motivo, el análisis combina modelos econométricos con una aproximación descriptiva y de segmentación. La econometría permite estimar asociaciones parciales entre variables, mientras que el clustering ayuda a identificar grupos de países con perfiles estructurales semejantes.

---

## 3. Base de datos

La base de datos utilizada se encuentra en el archivo:

```text
0. Final Data SDG Index.xlsx
