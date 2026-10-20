# core/reporte_pdf.py
from fpdf import FPDF
from core.formulas import generar_imagen_formula

class ReporteGUM(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'REPORTE DE CALIBRACIÓN E INCERTIDUMBRE', 0, 1, 'C')
        self.set_font('Arial', 'I', 9)
        self.cell(0, 8, 'Cálculo detallado basado en la GUM y Guías CENAM / EMA', 0, 1, 'C')
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def generar_pdf(datos_medicion, datos_reporte, resultado_final, unidad, derivadas, nombre_archivo="reporte_calibracion.pdf"):
    pdf = ReporteGUM()
    pdf.add_page()
    
    # ==========================================
    # PASO 1: MENSURANDO Y MODELO
    # ==========================================
    pdf.set_font("Arial", 'B', 11)
    pdf.set_fill_color(220, 230, 240)
    pdf.cell(0, 8, "1. Definición del Mensurando y Modelo Matemático", 0, 1, fill=True)
    pdf.set_font("Arial", size=9)
    pdf.multi_cell(0, 5, "El mensurando es el error de calibración del instrumento bajo calibración (IBC), el cual se define mediante el siguiente modelo matemático:")
    pdf.ln(2)
    
    # Insertar Imagen de la Fórmula Principal
    formula_principal = generar_imagen_formula(f"${datos_medicion['Formula Visual']}$", 16)
    pdf.image(formula_principal, x=60, w=80)
    
    pdf.set_font("Arial", size=8)
    pdf.cell(0, 6, f"Unidad de trabajo: {unidad} | Unidad del Patrón: {datos_medicion['Unidad del Patrón']}", 0, 1)
    pdf.ln(5)

    # ==========================================
    # PASO 2: COEFICIENTES DE SENSIBILIDAD (DERIVADAS)
    # ==========================================
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "2. Coeficientes de Sensibilidad (Derivadas Parciales)", 0, 1, fill=True)
    pdf.set_font("Arial", size=9)
    pdf.multi_cell(0, 5, "Aplicando la ley de propagación de incertidumbres, se calculan las derivadas parciales (c_i) de la función con respecto a cada variable de entrada, evaluadas en los valores promedio:")
    pdf.ln(3)
    
    for var, c_i in derivadas.items():
        formula_derivada = generar_imagen_formula(f"$c_{{{var}}} = \\frac{{\\partial E}}{{\\partial {var}}} = {c_i:.4f}$", 12)
        pdf.image(formula_derivada, x=70, w=60)
        pdf.ln(12)

    # ==========================================
    # PASO 3: TABLA DE PRESUPUESTO (ANEXO C)
    # ==========================================
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "3. Presupuesto de Incertidumbre (Anexo C)", 0, 1, fill=True)
    
    # Encabezados
    pdf.set_font("Arial", 'B', 7)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(15, 7, "Variable", border=1, align='C', fill=True)
    pdf.cell(45, 7, "Fuente", border=1, align='C', fill=True)
    pdf.cell(20, 7, "u(xi)", border=1, align='C', fill=True)
    pdf.cell(20, 7, "c_i", border=1, align='C', fill=True)
    pdf.cell(20, 7, "u_i(y)", border=1, align='C', fill=True)
    pdf.cell(25, 7, "% Contrib.", border=1, align='C', fill=True)
    pdf.cell(20, 7, "v", border=1, align='C', fill=True)
    pdf.ln()

    # Filas
    pdf.set_font("Arial", size=7)
    for index, row in datos_reporte.iterrows():
        pdf.cell(15, 6, str(row["Variable"]), border=1)
        fuente_texto = str(row["Fuente"])
        if len(fuente_texto) > 28: fuente_texto = fuente_texto[:25] + "..."
        pdf.cell(45, 6, fuente_texto, border=1)
        pdf.cell(20, 6, f"{row['u(xi)']:.4f}", border=1, align='C')
        pdf.cell(20, 6, f"{row['c_i']:.4f}", border=1, align='C')
        pdf.cell(20, 6, f"{row['u_i(y)']:.4f}", border=1, align='C')
        pdf.cell(25, 6, f"{row['% Contribución']:.1f} %", border=1, align='C')
        pdf.cell(20, 6, str(row["Grados v"]), border=1, align='C')
        pdf.ln()
    pdf.ln(4)

    # ==========================================
    # PASO 4: FORMULA DE PROPAGACIÓN
    # ==========================================
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "4. Cálculo de la Incertidumbre Combinada y Expandida", 0, 1, fill=True)
    pdf.set_font("Arial", size=9)
    
    pdf.multi_cell(0, 5, "La incertidumbre estándar combinada uc(y) se calcula sumando geométricamente las contribuciones individuales (es decir, la raíz cuadrada de la suma de los cuadrados de u_i(y)):")
    pdf.ln(2)
    
    # Insertar Fórmula de propagación general
    formula_uc = generar_imagen_formula(r"$u_c(y) = \sqrt{\sum_{i=1}^{N} [c_i \cdot u(x_i)]^2}$", 16)
    pdf.image(formula_uc, x=70, w=60)
    pdf.ln(12)

    pdf.multi_cell(0, 5, "Y la incertidumbre expandida U se obtiene multiplicando la incertidumbre estándar combinada por el factor de cobertura k:")
    pdf.ln(2)
    
    # Insertar Fórmula de U
    formula_U = generar_imagen_formula(r"$U = k \cdot u_c(y)$", 16)
    pdf.image(formula_U, x=80, w=40)
    pdf.ln(12)

    # Resultados Finales
    pdf.set_font("Arial", 'B', 10)
    for key, value in resultado_final.items():
        pdf.cell(70, 6, f"{key}:", border=0)
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 6, str(value), border=0, ln=1)
        pdf.set_font("Arial", 'B', 10)
    
    pdf.ln(8)

    # ==========================================
    # PASO 5: DECLARACIÓN Y FIRMAS
    # ==========================================
    pdf.set_font("Arial", size=8)
    pdf.multi_cell(0, 5, f"Declaración de Incertidumbre: Se reporta el resultado de la medición con una incertidumbre expandida U = {resultado_final['Incertidumbre Expandida U']}, utilizando un factor de cobertura k = {resultado_final['Factor de Cobertura (k)']} para un nivel de confianza aproximado del {resultado_final['Nivel de Confianza']}.")
    pdf.ln(15)

    pdf.cell(90, 8, "_________________________", 0, 0, 'C')
    pdf.cell(90, 8, "_________________________", 0, 1, 'C')
    pdf.cell(90, 5, "Realizó (Técnico)", 0, 0, 'C')
    pdf.cell(90, 5, "Autorizó (Responsable Técnico)", 0, 1, 'C')

    pdf.output(nombre_archivo)
    return nombre_archivo