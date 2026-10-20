# core/estadistica.py
import math

def calcular_veff(contribuciones):
    """
    Calcula los grados efectivos de libertad usando Welch-Satterthwaite.
    """
    # CORREGIDO: Ahora busca 'u_i(y)' que es como se llama en la tabla del Anexo C
    numerador = sum([c['u_i(y)']**2 for c in contribuciones])**2
    denominador = 0
    
    for c in contribuciones:
        v_i = c['Grados v']
        if v_i > 0 and v_i != float('inf'):
            denominador += (c['u_i(y)']**4) / v_i
    
    if denominador == 0:
        return float('inf')
    
    veff = numerador / denominador
    return math.floor(veff) if veff >= 1 else 1

def obtener_t_student(veff, nivel_confianza=95):
    tabla_95 = {1: 12.71, 2: 4.30, 3: 3.18, 4: 2.78, 5: 2.57, 6: 2.45, 7: 2.36, 8: 2.31, 9: 2.26, 10: 2.23, 
                15: 2.13, 20: 2.09, 30: 2.04, 50: 2.01, 100: 1.98}
    tabla_99 = {1: 63.66, 2: 9.92, 3: 5.84, 4: 4.60, 5: 4.03, 6: 3.71, 7: 3.50, 8: 3.36, 9: 3.25, 10: 3.17, 
                15: 2.95, 20: 2.85, 30: 2.75, 50: 2.68, 100: 2.63}
    
    tabla = tabla_95 if nivel_confianza == 95 else tabla_99

    if veff >= 100:
        return 2.0 if nivel_confianza == 95 else 2.576
    
    llaves = sorted(tabla.keys())
    for k in llaves:
        if veff <= k:
            return tabla[k]
    return 2.0