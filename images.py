import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

EXCEL_FILE = "0. Final Data SDG Index.xlsx"
SHEET_NAME = "Modelo_final_tipificado"

OUTPUT_DIR = "figuras_tfg"
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.rcParams["figure.dpi"] = 120
plt.rcParams["savefig.dpi"] = 300
plt.rcParams["font.size"] = 11

df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

country_col = "País"

sdg_2021 = "SDG INDEX 2021"
sdg_2025 = "SDG INDEX 2025"
sdg_change = "SDG INDEX 2025 - 2021"

x_vars = [
    "z_ln_GDP_per_capita_PPP",
    "z_Government_Effectiveness",
    "z_Education_expenditure_pct_GDP",
    "z_ln_Patents_per_million_plus_1",
    "z_Research_expenditure_pct_GDP",
    "z_Trade_pct_GDP"
]

x_names = [
    "PIB per cápita PPP (log)",
    "Eficacia del gobierno",
    "Gasto en educación (% PIB)",
    "Patentes por millón (log)",
    "Gasto en I+D (% PIB)",
    "Trade (% PIB)"
]

boxplot_labels = [
    "ln PIB pc PPP (z)",
    "Eficacia gob. (z)",
    "Educación (z)",
    "Patentes (log, z)",
    "I+D (z)",
    "Trade (z)"
]

# GUARDADO DE FIGURAS

def save_fig(filename):
    path = os.path.join(OUTPUT_DIR, filename)
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"Figura guardada: {path}")

# FIGURA 1. DISTRIBUCIÓN DEL SDG INDEX 2021

plt.figure(figsize=(8, 4.5))

plt.hist(
    df[sdg_2021].dropna(),
    bins=12,
    edgecolor="black"
)

plt.title("Distribución del SDG Index 2021")
plt.xlabel("SDG Index 2021")
plt.ylabel("Número de países")
plt.grid(axis="y", alpha=0.25)

save_fig("figura_1_distribucion_sdg_2021.png")

# FIGURA 2. DISTRIBUCIÓN DE LA VARIACIÓN DEL SDG INDEX

plt.figure(figsize=(8, 4.5))

plt.hist(
    df[sdg_change].dropna(),
    bins=12,
    edgecolor="black"
)

plt.title("Distribución de la variación del SDG Index")
plt.xlabel("Variación del SDG Index 2021-2025")
plt.ylabel("Número de países")
plt.grid(axis="y", alpha=0.25)

save_fig("figura_2_distribucion_variacion_sdg.png")

# FIGURA 3. DIAGRAMAS DE CAJAS Y BIGOTES

plt.figure(figsize=(9, 5))

plt.boxplot(
    [df[col].dropna() for col in x_vars],
    labels=boxplot_labels,
    patch_artist=False
)

plt.title("Diagramas de cajas y bigotes de las variables estructurales")
plt.ylabel("Valor tipificado")
plt.xticks(rotation=30, ha="right")
plt.grid(axis="y", alpha=0.25)

save_fig("figura_3_boxplots_variables_estructurales.png")

# FIGURA 4. RELACIÓN ENTRE PIB PER CÁPITA Y SDG INDEX 2021

x_col = "z_ln_GDP_per_capita_PPP"
y_col = sdg_2021

df_scatter = df[[country_col, x_col, y_col]].dropna().copy()

x = df_scatter[x_col].values
y = df_scatter[y_col].values

X_simple = sm.add_constant(x)
model_simple = sm.OLS(y, X_simple).fit()

x_line = np.linspace(x.min(), x.max(), 100)
y_line = model_simple.predict(sm.add_constant(x_line))

r = np.corrcoef(x, y)[0, 1]
r2 = model_simple.rsquared

plt.figure(figsize=(8.5, 5.2))

plt.scatter(
    x,
    y,
    alpha=0.85,
    s=45
)

plt.plot(
    x_line,
    y_line,
    linewidth=2
)

countries_to_label = ["Singapore", "United States", "Tajikistan"]

for _, row in df_scatter.iterrows():
    if row[country_col] in countries_to_label:
        plt.text(
            row[x_col] + 0.05,
            row[y_col] + 0.3,
            row[country_col],
            fontsize=9
        )

plt.text(
    0.03,
    0.95,
    f"r = {r:.2f}\nR² = {r2:.3f}",
    transform=plt.gca().transAxes,
    va="top",
    ha="left",
    bbox=dict(boxstyle="round", facecolor="white", edgecolor="gray", alpha=0.9)
)

plt.title("Relación entre renta per cápita y SDG Index 2021")
plt.xlabel("PIB per cápita PPP (log, tipificado)")
plt.ylabel("SDG Index 2021")
plt.grid(alpha=0.3)

save_fig("figura_4_relacion_pib_sdg_2021.png")

# FUNCIONES AUXILIARES PARA MODELOS OLS

def fit_ols_model(data, y_var, x_vars):
    model_df = data[[y_var] + x_vars].dropna().copy()
    y = model_df[y_var]
    X = sm.add_constant(model_df[x_vars])
    model = sm.OLS(y, X).fit()
    return model, model_df


def plot_coefficients(model, x_vars, readable_names, title, filename):
    """
    Representa los coeficientes estimados del modelo junto con sus intervalos
    de confianza al 95%.

    Cada punto representa el coeficiente estimado.
    Cada línea horizontal representa el intervalo de confianza.
    La línea vertical en cero permite ver si el intervalo cruza el cero.
    """

    # Extraer coeficientes estimados
    params = model.params[x_vars]

    # Extraer intervalos de confianza al 95%
    conf = model.conf_int().loc[x_vars]

    coef_df = pd.DataFrame({
        "variable": readable_names,
        "coef": params.values,
        "lower": conf[0].values,
        "upper": conf[1].values
    })

    # Ordenar de mayor a menor coeficiente
    coef_df = coef_df.sort_values("coef", ascending=False)

    # Invertir para que el mayor aparezca arriba en el gráfico horizontal
    coef_df_plot = coef_df.iloc[::-1]

    plt.figure(figsize=(8.5, 5))

    y_pos = np.arange(len(coef_df_plot))

    # Punto = coeficiente
    # Línea horizontal = intervalo de confianza
    plt.errorbar(
        coef_df_plot["coef"],
        y_pos,
        xerr=[
            coef_df_plot["coef"] - coef_df_plot["lower"],
            coef_df_plot["upper"] - coef_df_plot["coef"]
        ],
        fmt="o",
        capsize=4
    )

    # Línea vertical en cero
    plt.axvline(0, linestyle="--", linewidth=1)

    plt.yticks(y_pos, coef_df_plot["variable"])
    plt.title(title)
    plt.xlabel("Coeficiente estimado")
    plt.grid(axis="x", alpha=0.25)

    save_fig(filename)


# FIGURA 5. COEFICIENTES MODELO 1: SDG INDEX 2021

model_1, df_model_1 = fit_ols_model(
    data=df,
    y_var=sdg_2021,
    x_vars=x_vars
)

print("\nMODELO 1: SDG INDEX 2021")
print(model_1.summary())

plot_coefficients(
    model=model_1,
    x_vars=x_vars,
    readable_names=x_names,
    title="Coeficientes del modelo OLS para el SDG Index 2021",
    filename="figura_5_coeficientes_modelo_1_sdg_2021.png"
)

# FIGURA 6. COEFICIENTES MODELO 2: VARIACIÓN SDG 2021-2025

model_2, df_model_2 = fit_ols_model(
    data=df,
    y_var=sdg_change,
    x_vars=x_vars
)

print("\nMODELO 2: VARIACIÓN SDG INDEX 2021-2025")
print(model_2.summary())

plot_coefficients(
    model=model_2,
    x_vars=x_vars,
    readable_names=x_names,
    title="Coeficientes del modelo OLS para la variación del SDG Index",
    filename="figura_6_coeficientes_modelo_2_variacion_sdg.png"
)

# FIGURA 7. COEFICIENTES MODELO 3: PERSISTENCIA SDG 2025

x_vars_persistence = [
    "SDG INDEX 2021",
    "z_ln_GDP_per_capita_PPP",
    "z_Government_Effectiveness",
    "z_Education_expenditure_pct_GDP",
    "z_ln_Patents_per_million_plus_1",
    "z_Research_expenditure_pct_GDP",
    "z_Trade_pct_GDP"
]

x_names_persistence = [
    "SDG Index 2021",
    "PIB per cápita PPP (log)",
    "Eficacia del gobierno",
    "Gasto en educación (% PIB)",
    "Patentes por millón (log)",
    "Gasto en I+D (% PIB)",
    "Trade (% PIB)"
]

model_3, df_model_3 = fit_ols_model(
    data=df,
    y_var=sdg_2025,
    x_vars=x_vars_persistence
)

print("\nMODELO 3: PERSISTENCIA SDG INDEX 2025")
print(model_3.summary())

plot_coefficients(
    model=model_3,
    x_vars=x_vars_persistence,
    readable_names=x_names_persistence,
    title="Coeficientes del modelo OLS para el SDG Index 2025",
    filename="figura_7_coeficientes_modelo_3_persistencia.png"
)

# FIGURA 8. PERSISTENCIA SDG INDEX 2021 vs 2025

df_persist = df[[country_col, sdg_2021, sdg_2025]].dropna().copy()

x_persist = df_persist[sdg_2021].values
y_persist = df_persist[sdg_2025].values

model_persist_simple = sm.OLS(
    y_persist,
    sm.add_constant(x_persist)
).fit()

x_line = np.linspace(x_persist.min(), x_persist.max(), 100)
y_line = model_persist_simple.predict(sm.add_constant(x_line))

r_persist = np.corrcoef(x_persist, y_persist)[0, 1]
r2_persist = model_persist_simple.rsquared

plt.figure(figsize=(8.5, 5.2))

plt.scatter(
    x_persist,
    y_persist,
    alpha=0.85,
    s=45
)

plt.plot(
    x_line,
    y_line,
    linewidth=2
)

min_val = min(x_persist.min(), y_persist.min())
max_val = max(x_persist.max(), y_persist.max())

plt.plot(
    [min_val, max_val],
    [min_val, max_val],
    linestyle="--",
    linewidth=1,
    alpha=0.7
)

plt.text(
    0.03,
    0.95,
    f"r = {r_persist:.2f}\nR² = {r2_persist:.3f}",
    transform=plt.gca().transAxes,
    va="top",
    ha="left",
    bbox=dict(boxstyle="round", facecolor="white", edgecolor="gray", alpha=0.9)
)

countries_to_label = ["Finland", "Madagascar", "Singapore"]

for _, row in df_persist.iterrows():
    if row[country_col] in countries_to_label:
        plt.text(
            row[sdg_2021] + 0.15,
            row[sdg_2025] + 0.15,
            row[country_col],
            fontsize=9
        )

plt.title("Persistencia del desempeño sostenible")
plt.xlabel("SDG Index 2021")
plt.ylabel("SDG Index 2025")
plt.grid(alpha=0.3)

save_fig("figura_8_persistencia_sdg_2021_2025.png")

print("\nProceso terminado correctamente.")
print(f"Todas las figuras se han guardado en la carpeta: {OUTPUT_DIR}")