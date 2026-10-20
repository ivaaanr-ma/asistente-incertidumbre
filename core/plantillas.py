# core/plantillas.py

CATALOGO_SERVICIOS = {
    "Presión": {
        "Manómetros y Transductores": {
            "descripcion": "Comparación directa. Calcula la Corrección (C = P_patrón - P_IBC).",
            "modelo_sugerido": "P_patron - P_ibc",
            "formula_visual": "C = P_{Patrón} - P_{IBC}",
            "leyenda": "**C**: Corrección a aplicar al IBC.\n\n**P_{Patrón}**: Lectura del patrón (corregida por altura/temperatura).\n\n**P_{IBC}**: Lectura del instrumento.",
            "fuentes_patron_fijas": [
                {"Fuente": "Certificado del Patrón (k=2)", "Tipo": "B", "Distribución": "Normal (k=2)"},
                {"Fuente": "Deriva del Patrón", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_patron_opcionales": [
                {"Fuente": "Corrección por Altura (Columna)", "Tipo": "B", "Distribución": "Rectangular"},
                {"Fuente": "Efecto de Temperatura (Patrón)", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_ibc_fijas": [
                {"Fuente": "Repetibilidad (Calculada)", "Tipo": "A", "Distribución": "Normal (k=1)"},
                {"Fuente": "Resolución del IBC", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_ibc_opcionales": [
                {"Fuente": "Histéresis del IBC", "Tipo": "B", "Distribución": "Rectangular"},
                {"Fuente": "Error de Cero", "Tipo": "B", "Distribución": "Rectangular"}
            ]
        }
    },
    "Temperatura (Contacto)": {
        "Termómetros de Lectura Directa": {
            "descripcion": "Comparación directa en pozo seco o baño.",
            "modelo_sugerido": "t_patron - t_ibc",
            "formula_visual": "S = t_{ref} - (t_x + C)",
            "leyenda": "**S**: Sesgo instrumental.\n\n**t_{ref}**: Temperatura del patrón.\n\n**t_x**: Temperatura indicada por el IBC.",
            "fuentes_patron_fijas": [
                {"Fuente": "Certificado del Patrón (k=2)", "Tipo": "B", "Distribución": "Normal (k=2)"},
                {"Fuente": "Deriva del Patrón", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_patron_opcionales": [
                {"Fuente": "Incertidumbre del Baño/Pozo", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_ibc_fijas": [
                {"Fuente": "Repetibilidad (Calculada)", "Tipo": "A", "Distribución": "Normal (k=1)"},
                {"Fuente": "Resolución del IBC", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_ibc_opcionales": [
                {"Fuente": "Efecto de Temperatura Ambiente", "Tipo": "B", "Distribución": "Rectangular"},
                {"Fuente": "Histéresis Térmica", "Tipo": "B", "Distribución": "Rectangular"}
            ]
        },
        "Termómetros Bimetálicos": {
            "descripcion": "Comparación directa en pozo seco.",
            "modelo_sugerido": "T1 + C",
            "formula_visual": "T = T_I + C",
            "leyenda": "**T**: Temperatura corregida.\n\n**T_I**: Temperatura del pozo seco.\n\n**C**: Corrección del termómetro.",
            "fuentes_patron_fijas": [
                {"Fuente": "Certificado del Patrón (k=2)", "Tipo": "B", "Distribución": "Normal (k=2)"},
                {"Fuente": "Deriva del Patrón", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_patron_opcionales": [],
            "fuentes_ibc_fijas": [
                {"Fuente": "Repetibilidad (Calculada)", "Tipo": "A", "Distribución": "Normal (k=1)"},
                {"Fuente": "Resolución del IBC", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_ibc_opcionales": [
                {"Fuente": "Histéresis Bimetálica", "Tipo": "B", "Distribución": "Rectangular"}
            ]
        }
    },
    "Humedad": {
        "Higrómetros / Termohigrómetros": {
            "descripcion": "Comparación en cámara climática con 2 patrones y 10 mediciones.",
            "modelo_sugerido": "I_ibc - (P1 + P2)/2",
            "formula_visual": "E = I_{IBC} - \\frac{P_1 + P_2}{2}",
            "leyenda": "**E**: Error de indicación.\n\n**I_{IBC}**: Indicación del instrumento.\n\n**P_1, P_2**: Lecturas corregidas de los dos patrones.",
            "fuentes_patron_fijas": [
                {"Fuente": "Certificado Patrón 1 (k=2)", "Tipo": "B", "Distribución": "Normal (k=2)"},
                {"Fuente": "Certificado Patrón 2 (k=2)", "Tipo": "B", "Distribución": "Normal (k=2)"},
                {"Fuente": "Diferencia entre Patrones", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_patron_opcionales": [],
            "fuentes_ibc_fijas": [
                {"Fuente": "Variabilidad de Mediciones (10 lecturas)", "Tipo": "A", "Distribución": "Normal (k=1)"},
                {"Fuente": "Resolución del IBC", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_ibc_opcionales": [
                {"Fuente": "Variación de la Cámara", "Tipo": "B", "Distribución": "Triangular"},
                {"Fuente": "Fluctuación de la Cámara", "Tipo": "B", "Distribución": "Rectangular"}
            ]
        }
    },
    "Eléctrica (Medidores)": {
        "Medidores Tensión/Corriente/Resistencia": {
            "descripcion": "Comparación directa con generador patrón.",
            "modelo_sugerido": "V_ibc - V_patron",
            "formula_visual": "e = V_{IBC} - I_{Patrón}",
            "leyenda": "**e**: Error del IBC.\n\n**V_{IBC}**: Valor medido.\n\n**I_{Patrón}**: Valor de referencia.",
            "fuentes_patron_fijas": [
                {"Fuente": "Certificado del Generador (k=2)", "Tipo": "B", "Distribución": "Normal (k=2)"},
                {"Fuente": "Estabilidad del Generador", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_patron_opcionales": [
                {"Fuente": "Deriva del Generador", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_ibc_fijas": [
                {"Fuente": "Repetibilidad (Calculada)", "Tipo": "A", "Distribución": "Normal (k=1)"},
                {"Fuente": "Resolución del IBC", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_ibc_opcionales": [
                {"Fuente": "Error de Cero", "Tipo": "B", "Distribución": "Rectangular"}
            ]
        }
    },
    "Eléctrica (Generadores)": {
        "Generadores de Resistencia / Simuladores RTD": {
            "descripcion": "Calibración de simuladores de PT100, PT1000, etc.",
            "modelo_sugerido": "R_ibc - R_patron",
            "formula_visual": "e = V_{GM} - I_P",
            "leyenda": "**e**: Error del IBC.\n\n**V_{GM}**: Valor generado por el simulador.\n\n**I_P**: Valor de referencia del multímetro.",
            "fuentes_patron_fijas": [
                {"Fuente": "Certificado del Multímetro (k=2)", "Tipo": "B", "Distribución": "Normal (k=2)"},
                {"Fuente": "Estabilidad del Multímetro", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_patron_opcionales": [
                {"Fuente": "Deriva del Multímetro", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_ibc_fijas": [
                {"Fuente": "Repetibilidad (Calculada)", "Tipo": "A", "Distribución": "Normal (k=1)"},
                {"Fuente": "Resolución del IBC", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_ibc_opcionales": [
                {"Fuente": "Error de Cero", "Tipo": "B", "Distribución": "Rectangular"}
            ]
        }
    },
    "Tiempo / Frecuencia": {
        "Tacómetros": {
            "descripcion": "Generador de pulsos de luz.",
            "modelo_sugerido": "L_cal - L_pat",
            "formula_visual": "E = (L_{cal} + C_{res} + C_{temp}) - (L_{pat} + C_{base})",
            "leyenda": "**E**: Error del tacómetro.\n\n**L_{cal}**: Lectura del tacómetro (rpm).\n\n**L_{pat}**: Lectura del patrón (Hz x 60).",
            "fuentes_patron_fijas": [
                {"Fuente": "Calibración del Generador (k=2)", "Tipo": "B", "Distribución": "Normal (k=2)"},
                {"Fuente": "Deriva del Generador", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_patron_opcionales": [
                {"Fuente": "Ruido del Sistema de Pulsos", "Tipo": "A", "Distribución": "Normal (k=1)"}
            ],
            "fuentes_ibc_fijas": [
                {"Fuente": "Repetibilidad (Calculada)", "Tipo": "A", "Distribución": "Normal (k=1)"},
                {"Fuente": "Resolución del IBC", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_ibc_opcionales": [
                {"Fuente": "Base de Tiempo del Patrón", "Tipo": "B", "Distribución": "Rectangular"}
            ]
        },
        "Cronómetros": {
            "descripcion": "Comparación directa o totalización.",
            "modelo_sugerido": "T_ibc - T_patron",
            "formula_visual": "E = T_{IBC} - T_{Patrón}",
            "leyenda": "**E**: Error de tiempo.\n\n**T_{IBC}**: Tiempo del IBC.\n\n**T_{Patrón}**: Tiempo de referencia.",
            "fuentes_patron_fijas": [
                {"Fuente": "Incertidumbre de la Referencia", "Tipo": "B", "Distribución": "Rectangular"},
                {"Fuente": "Deriva del Patrón", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_patron_opcionales": [
                {"Fuente": "Tiempo de Reacción Humana", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_ibc_fijas": [
                {"Fuente": "Repetibilidad (Calculada)", "Tipo": "A", "Distribución": "Normal (k=1)"},
                {"Fuente": "Resolución del IBC", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_ibc_opcionales": [
                {"Fuente": "Estabilidad del Cristal (Base de Tiempo)", "Tipo": "B", "Distribución": "Rectangular"}
            ]
        }
    },
    "Par Torsional": {
        "Torquímetros": {
            "descripcion": "Calibración con analizador de par torsional.",
            "modelo_sugerido": "T_ibc - T_patron",
            "formula_visual": "E = T_{IBC} - T_{Patrón}",
            "leyenda": "**E**: Error de par torsional.\n\n**T_{IBC}**: Par indicado.\n\n**T_{Patrón}**: Par aplicado por el analizador.",
            "fuentes_patron_fijas": [
                {"Fuente": "Certificado del Analizador (k=2)", "Tipo": "B", "Distribución": "Normal (k=2)"},
                {"Fuente": "Deriva del Analizador", "Tipo": "B", "Distribución": "Rectangular"},
                {"Fuente": "Error del Brazo de Palanca", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_patron_opcionales": [
                {"Fuente": "Efecto de Temperatura (20±1°C)", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_ibc_fijas": [
                {"Fuente": "Repetibilidad (Calculada)", "Tipo": "A", "Distribución": "Normal (k=1)"},
                {"Fuente": "Resolución del IBC", "Tipo": "B", "Distribución": "Rectangular"}
            ],
            "fuentes_ibc_opcionales": [
                {"Fuente": "Histéresis del Torquímetro", "Tipo": "B", "Distribución": "Rectangular"},
                {"Fuente": "Error de Cero", "Tipo": "B", "Distribución": "Rectangular"}
            ]
        }
    },
    "Personalizado": {
        "Definir mi modelo": {
            "descripcion": "Modelo en blanco.",
            "modelo_sugerido": "I - P",
            "formula_visual": "Y = X_1 - X_2",
            "leyenda": "Escribe tu propia ecuación.",
            "fuentes_patron_fijas": [{"Fuente": "Certificado Patrón", "Tipo": "B", "Distribución": "Normal (k=2)"}],
            "fuentes_patron_opcionales": [{"Fuente": "Otra fuente Patrón", "Tipo": "B", "Distribución": "Rectangular"}],
            "fuentes_ibc_fijas": [{"Fuente": "Repetibilidad (Calculada)", "Tipo": "A", "Distribución": "Normal (k=1)"}],
            "fuentes_ibc_opcionales": [{"Fuente": "Otra fuente IBC", "Tipo": "B", "Distribución": "Rectangular"}]
        }
    }
}