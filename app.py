# app.py
import streamlit as st
import pandas as pd
import re
import math
import numpy as np
import plotly.express as px
from core.plantillas import CATALOGO_SERVICIOS
from core.estadistica import calcular_veff, obtener_t_student
from core.propagacion import calcular_derivadas, evaluar_formula
from core.reporte_pdf import generar_pdf

st.set_page_config(page_title="Asistente de Incertidumbre", layout="wide", page_icon="📊")
st.title("📊 Asistente de Presupuestos de Incertidumbre")
st.markdown("Validación de hojas de cálculo bajo lineamientos GUM / CENAM.")

# --- DICCIONARIO DE UNIDADES DINÁMICAS ---
UNIDADES_POR_MAGNITUD = {
    "Presión": ["bar", "kPa", "MPa", "psi", "kgf/cm²"],
    "Temperatura (Contacto)": ["°C", "K", "°F"],
    "Humedad": ["%RH", "g/m³"],
    "Eléctrica (Medidores)": ["V", "mV", "A", "mA", "Ω", "kΩ", "MΩ"],
    "Eléctrica (Generadores)": ["Ω", "kΩ", "MΩ", "°C (simulado)"],
    "Tiempo / Frecuencia": ["s", "ms", "µs", "Hz", "kHz", "rpm"],
    "Par Torsional": ["Nm", "kNm", "lbf·ft", "kgf·m"],
    "Personalizado": ["u", "m", "kg", "s", "A", "K", "mol", "cd", "%"]
}

# --- BARRA LATERAL ---
st.sidebar.header("1. Contexto de la Medición")
magnitud_sel = st.sidebar.selectbox("Magnitud:", list(CATALOGO_SERVICIOS.keys()))
servicio_sel = st.sidebar.selectbox("Servicio:", list(CATALOGO_SERVICIOS[magnitud_sel].keys()))
info_servicio = CATALOGO_SERVICIOS[magnitud_sel][servicio_sel]

st.sidebar.header("2. Modelo Matemático")
formula = st.sidebar.text_area("Ecuación (Y = f(Xi)):", value=info_servicio['modelo_sugerido'])

variables_encontradas = re.findall(r'\b[A-Za-z_][A-Za-z0-9_]*\b', formula)
vars_limpias = [v for v in list(set(variables_encontradas)) if v not in ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'pi', 'e', 'rho']]

if not vars_limpias:
    st.info("👈 Define una ecuación con variables (ej. A, B).")
else:
    # --- MOSTRAR ECUACIÓN ---
    st.markdown("### Modelo Matemático Identificado")
    col_ec1, col_ec2, col_ec3 = st.columns([1, 2, 1])
    with col_ec2:
        st.latex(info_servicio.get('formula_visual', formula))
    with st.expander("ℹ️ ¿Qué significa cada variable?", expanded=False):
        st.markdown(info_servicio.get('leyenda', ''))

    st.markdown("---")
    
    # --- ASIGNACIÓN DE ROLES Y UNIDADES DINÁMICAS ---
    st.markdown("#### Asignación de Roles y Unidades")
    col_rol1, col_rol2, col_rol3, col_rol4 = st.columns(4)
    
    with col_rol1:
        var_ibc = st.selectbox("Variable IBC:", vars_limpias, index=0)
    with col_rol2:
        otras_vars = [v for v in vars_limpias if v != var_ibc]
        var_patron = st.selectbox("Variable Patrón:", otras_vars if otras_vars else vars_limpias, index=0)
    
    # Unidades dinámicas basadas en la magnitud seleccionada
    opciones_unidades = UNIDADES_POR_MAGNITUD.get(magnitud_sel, ["u"])
    
    with col_rol3:
        unidad_ibc = st.selectbox(f"Unidad IBC ({var_ibc}):", opciones_unidades)
    with col_rol4:
        unidad_patron = st.selectbox(f"Unidad Patrón ({var_patron}):", opciones_unidades)

    # Factores de conversión (simplificados para el ejemplo, puedes expandirlos)
    factores = {"bar": 100, "kPa": 1, "MPa": 1000, "psi": 6.89476, "kgf/cm²": 98.0665,
                "°C": 1, "K": 1, "°F": 0.5555, "%RH": 1, "g/m³": 1,
                "V": 1, "mV": 0.001, "A": 1, "mA": 0.001, "Ω": 1, "kΩ": 1000, "MΩ": 1000000,
                "s": 1, "ms": 0.001, "µs": 0.000001, "Hz": 1, "kHz": 1000, "rpm": 1,
                "Nm": 1, "kNm": 1000, "lbf·ft": 1.3558, "kgf·m": 9.80665,
                "°C (simulado)": 1, "u": 1, "m": 1, "kg": 1, "mol": 1, "cd": 1, "%": 1}
    
    factor_ibc = factores.get(unidad_ibc, 1)
    factor_patron = factores.get(unidad_patron, 1)

    st.markdown("---")
    st.subheader("3. Datos de Medición")
    
    num_mediciones = st.number_input("Número de mediciones:", min_value=1, max_value=20, value=3, key="n_ibc")
    
    df_mediciones = pd.DataFrame({
        "No.": range(1, num_mediciones + 1),
        f"Valor Patrón ({unidad_patron})": [0.0] * num_mediciones,
        f"Lectura IBC ({unidad_ibc})": [0.0] * num_mediciones
    })
    col_tabla, _ = st.columns([2, 1])
    with col_tabla:
        df_med = st.data_editor(df_mediciones, hide_index=True, width='stretch', key="med_ibc")
        
    promedio_ibc_global = 0.0
    promedio_patron_global = 0.0
    u_tipo_a_global = 0.0
    
    if num_mediciones > 1 and not df_med[f"Lectura IBC ({unidad_ibc})"].eq(0).all():
        patron_en_ibc = df_med[f"Valor Patrón ({unidad_patron})"] * (factor_patron / factor_ibc)
        ibc_en_ibc = df_med[f"Lectura IBC ({unidad_ibc})"]
        
        promedio_ibc_global = ibc_en_ibc.mean()
        promedio_patron_global = patron_en_ibc.mean()
        u_tipo_a_global = (ibc_en_ibc - patron_en_ibc).std(ddof=1) / math.sqrt(num_mediciones)
        
        st.info(f"**Resumen:** Promedio IBC: {promedio_ibc_global:.4f} | Promedio Patrón: {promedio_patron_global:.4f} | u(A): {u_tipo_a_global:.4f}")

    st.markdown("---")
    
    # ================= CONTRIBUCIONES =================
    st.subheader("4. Contribuciones de Incertidumbre")
    
    if "fuentes_patron_activas" not in st.session_state:
        st.session_state["fuentes_patron_activas"] = pd.DataFrame(info_servicio.get("fuentes_patron_fijas", []))
        st.session_state["fuentes_patron_activas"]["Valor Base"] = 0.0
        st.session_state["fuentes_patron_activas"]["u(xi) Calculada"] = 0.0
        
    if "fuentes_ibc_activas" not in st.session_state:
        st.session_state["fuentes_ibc_activas"] = pd.DataFrame(info_servicio.get("fuentes_ibc_fijas", []))
        st.session_state["fuentes_ibc_activas"]["Valor Base"] = 0.0
        st.session_state["fuentes_ibc_activas"]["u(xi) Calculada"] = 0.0

    datos_para_reporte = []
    valores_centrales = {var_ibc: promedio_ibc_global, var_patron: promedio_patron_global}
    vars_u_estandar = {}
    datos_ishikawa = []

    col_patron, col_ibc = st.columns(2)
    
    # ---------- PATRÓN ----------
    with col_patron:
        st.markdown(f"##### 🟨 Patrón ({var_patron})")
        
        df_fuentes_patron = st.data_editor(
            st.session_state["fuentes_patron_activas"], num_rows="dynamic",
            column_config={
                "Tipo": st.column_config.SelectboxColumn("Tipo", options=["A", "B"]),
                "Distribución": st.column_config.SelectboxColumn("Distribución", options=["Normal (k=1)", "Normal (k=2)", "Rectangular", "Triangular"]),
                "u(xi) Calculada": st.column_config.NumberColumn("u(xi)", disabled=True, format="%.4f")
            }, key="editor_patron_activas", width='stretch'
        )
        st.session_state["fuentes_patron_activas"] = df_fuentes_patron
        
        with st.expander("➕ Añadir otra fuente al Patrón"):
            opciones_pat = [f["Fuente"] for f in info_servicio.get("fuentes_patron_opcionales", [])]
            opciones_pat = [o for o in opciones_pat if o not in df_fuentes_patron["Fuente"].values]
            if opciones_pat:
                nueva_fuente_pat = st.selectbox("Selecciona la fuente:", opciones_pat, key="sel_nueva_pat")
                if st.button("Agregar al Patrón", key="btn_add_pat"):
                    info_nueva = next(f for f in info_servicio["fuentes_patron_opcionales"] if f["Fuente"] == nueva_fuente_pat)
                    nueva_fila = pd.DataFrame([{**info_nueva, "Valor Base": 0.0, "u(xi) Calculada": 0.0}])
                    st.session_state["fuentes_patron_activas"] = pd.concat([st.session_state["fuentes_patron_activas"], nueva_fila], ignore_index=True)
                    st.rerun()
            else:
                st.write("Todas las fuentes disponibles ya están agregadas.")

        suma_cuadrados_patron = 0.0
        fuentes_var_patron = []
        for index, row in df_fuentes_patron.iterrows():
            if pd.isna(row["Fuente"]) or str(row["Fuente"]).strip() == "" or row["Fuente"] == "None":
                continue
            val_base = float(row["Valor Base"]) * (factor_patron / factor_ibc) if pd.notna(row["Valor Base"]) else 0.0
            dist = str(row["Distribución"])
            
            if "Normal (k=1)" in dist: u_std = val_base / 1.0
            elif "Normal (k=2)" in dist: u_std = val_base / 2.0
            elif "Rectangular" in dist: u_std = val_base / math.sqrt(3)
            elif "Triangular" in dist: u_std = val_base / math.sqrt(6)
            else: u_std = val_base
            
            df_fuentes_patron.at[index, "u(xi) Calculada"] = u_std
            suma_cuadrados_patron += u_std ** 2
            fuentes_var_patron.append({'Fuente': row["Fuente"], 'u_i': u_std, 'v_i': float('inf')})
            datos_ishikawa.append({"Variable": var_patron, "Fuente": row["Fuente"], "Valor": u_std})
        
        u_combinada_patron = math.sqrt(suma_cuadrados_patron)
        st.success(f"**u({var_patron}) combinada:** {u_combinada_patron:.4f} {unidad_ibc}")
        vars_u_estandar[var_patron] = u_combinada_patron
        datos_para_reporte.append({"Variable": var_patron, "Fuentes": fuentes_var_patron})
        
        df_ish_pat = pd.DataFrame([d for d in datos_ishikawa if d["Variable"] == var_patron])
        if not df_ish_pat.empty:
            st.plotly_chart(px.pie(df_ish_pat, values='Valor', names='Fuente', hole=0.4), width='stretch')

    # ---------- IBC ----------
    with col_ibc:
        st.markdown(f"##### 🟦 Instrumento ({var_ibc})")
        
        df_fuentes_ibc = st.data_editor(
            st.session_state["fuentes_ibc_activas"], num_rows="dynamic",
            column_config={
                "Tipo": st.column_config.SelectboxColumn("Tipo", options=["A", "B"]),
                "Distribución": st.column_config.SelectboxColumn("Distribución", options=["Normal (k=1)", "Normal (k=2)", "Rectangular", "Triangular"]),
                "u(xi) Calculada": st.column_config.NumberColumn("u(xi)", disabled=True, format="%.4f")
            }, key="editor_ibc_activas", width='stretch'
        )
        st.session_state["fuentes_ibc_activas"] = df_fuentes_ibc
        
        with st.expander("➕ Añadir otra fuente al IBC"):
            opciones_ibc = [f["Fuente"] for f in info_servicio.get("fuentes_ibc_opcionales", [])]
            opciones_ibc = [o for o in opciones_ibc if o not in df_fuentes_ibc["Fuente"].values]
            if opciones_ibc:
                nueva_fuente_ibc = st.selectbox("Selecciona la fuente:", opciones_ibc, key="sel_nueva_ibc")
                if st.button("Agregar al IBC", key="btn_add_ibc"):
                    info_nueva = next(f for f in info_servicio["fuentes_ibc_opcionales"] if f["Fuente"] == nueva_fuente_ibc)
                    nueva_fila = pd.DataFrame([{**info_nueva, "Valor Base": 0.0, "u(xi) Calculada": 0.0}])
                    st.session_state["fuentes_ibc_activas"] = pd.concat([st.session_state["fuentes_ibc_activas"], nueva_fila], ignore_index=True)
                    st.rerun()
            else:
                st.write("Todas las fuentes disponibles ya están agregadas.")

        suma_cuadrados_ibc = 0.0
        fuentes_var_ibc = []
        for index, row in df_fuentes_ibc.iterrows():
            if pd.isna(row["Fuente"]) or str(row["Fuente"]).strip() == "" or row["Fuente"] == "None":
                continue
            val_base = float(row["Valor Base"]) if pd.notna(row["Valor Base"]) else 0.0
            if "Repetibilidad" in str(row["Fuente"]): 
                val_base = u_tipo_a_global
                
            dist = str(row["Distribución"])
            if "Normal (k=1)" in dist: u_std = val_base / 1.0
            elif "Normal (k=2)" in dist: u_std = val_base / 2.0
            elif "Rectangular" in dist: u_std = val_base / math.sqrt(3)
            elif "Triangular" in dist: u_std = val_base / math.sqrt(6)
            else: u_std = val_base
            
            df_fuentes_ibc.at[index, "u(xi) Calculada"] = u_std
            df_fuentes_ibc.at[index, "Valor Base"] = val_base
            
            suma_cuadrados_ibc += u_std ** 2
            fuentes_var_ibc.append({'Fuente': row["Fuente"], 'u_i': u_std, 'v_i': float('inf')})
            datos_ishikawa.append({"Variable": var_ibc, "Fuente": row["Fuente"], "Valor": u_std})
            
        u_combinada_ibc = math.sqrt(suma_cuadrados_ibc)
        st.success(f"**u({var_ibc}) combinada:** {u_combinada_ibc:.4f} {unidad_ibc}")
        vars_u_estandar[var_ibc] = u_combinada_ibc
        datos_para_reporte.append({"Variable": var_ibc, "Fuentes": fuentes_var_ibc})
        
        df_ish_ibc = pd.DataFrame([d for d in datos_ishikawa if d["Variable"] == var_ibc])
        if not df_ish_ibc.empty:
            st.plotly_chart(px.pie(df_ish_ibc, values='Valor', names='Fuente', hole=0.4), width='stretch')

    # --- CÁLCULO FINAL Y PDF ---
    st.sidebar.header("4. Configuración del Reporte")
    rigor = st.sidebar.radio("Cálculo del factor k:", ["Riguroso (Welch-Satterthwaite)", "Aproximación Normal (k=2)"])
    nivel_confianza = st.sidebar.radio("Nivel de Confianza:", [95, 99])
    
    if st.button("🚀 Calcular y Generar Reporte", type="primary"):
        try:
            derivadas = calcular_derivadas(formula, vars_u_estandar, valores_centrales)
            y_valor = evaluar_formula(formula, valores_centrales)
        except Exception as e:
            st.error(f"Error en el modelo matemático: {e}")
            st.stop()

        tabla_anexo_c = []
        suma_var_total = 0.0
        for item in datos_para_reporte:
            var = item['Variable']
            c_i = derivadas[var]
            for f in item['Fuentes']:
                contribucion = (f['u_i'] * c_i) ** 2
                suma_var_total += contribucion
                tabla_anexo_c.append({
                    "Variable": var, "Fuente": f['Fuente'], "u(xi)": f['u_i'],
                    "c_i": c_i, "u_i(y)": abs(f['u_i'] * c_i), "Contribución²": contribucion, "Grados v": f['v_i']
                })
        
        uc_y = math.sqrt(suma_var_total)
        for fila in tabla_anexo_c:
            fila["% Contribución"] = (fila["Contribución²"] / suma_var_total * 100) if suma_var_total > 0 else 0

        if "Riguroso" in rigor:
            v_efectivos = calcular_veff(tabla_anexo_c)
            k_factor = obtener_t_student(v_efectivos, nivel_confianza)
        else:
            k_factor = 2.0 if nivel_confianza == 95 else 2.576
        U_exp = uc_y * k_factor

        st.subheader("Resultados")
        st.success(f"**Error (Y) = {y_valor:.4f} ± {U_exp:.4f} {unidad_ibc}** (k={k_factor:.2f}, {nivel_confianza}%)")
        
        df_anexo_c = pd.DataFrame(tabla_anexo_c).drop(columns=["Contribución²"])
        st.dataframe(df_anexo_c, width='stretch')

        # PDF DETALLADO
        datos_medicion = {
            "Magnitud": magnitud_sel, 
            "Servicio": servicio_sel, 
            "Ecuación": formula, 
            "Formula Visual": info_servicio.get('formula_visual', formula),
            "Unidad del Patrón": unidad_patron
        }
        resultado_final = {
            "Error de Indicación (y)": f"{y_valor:.4f} {unidad_ibc}",
            "Incertidumbre Estándar uc(y)": f"{uc_y:.4f} {unidad_ibc}",
            "Factor de Cobertura (k)": f"{k_factor:.2f}",
            "Incertidumbre Expandida U": f"{U_exp:.4f} {unidad_ibc}",
            "Nivel de Confianza": f"{nivel_confianza}%"
        }
        
        nombre_pdf = "reporte_auditoria.pdf"
        generar_pdf(datos_medicion, df_anexo_c, resultado_final, unidad_ibc, derivadas, nombre_pdf)
        
        with open(nombre_pdf, "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        st.download_button("⬇️ Descargar Reporte PDF Detallado", PDFbyte, nombre_pdf, "application/pdf", type="primary")