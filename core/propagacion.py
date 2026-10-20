# core/propagacion.py
import numpy as np

def calcular_derivadas(formula, vars_dict, valores_centrales):
    """
    Calcula las derivadas parciales numéricamente evaluando la fórmula con 
    pequeños incrementos (h) en cada variable.
    """
    h = 1e-6
    derivadas = {}
    y_base = evaluar_formula(formula, valores_centrales)
    
    for var in vars_dict.keys():
        valores_perturbados = valores_centrales.copy()
        valores_perturbados[var] += h
        y_perturbado = evaluar_formula(formula, valores_perturbados)
        
        # Derivada parcial aproximada: (f(x+h) - f(x)) / h
        derivadas[var] = (y_perturbado - y_base) / h
        
    return derivadas

def evaluar_formula(formula, variables):
    contexto = {
        'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
        'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
        'pi': np.pi, 'e': np.e
    }
    contexto.update(variables)
    return eval(formula, {"__builtins__": None}, contexto)