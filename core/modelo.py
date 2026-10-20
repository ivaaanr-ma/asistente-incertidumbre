# core/modelo.py
import numpy as np

def evaluar_modelo(formula: str, variables: dict) -> dict:
    try:
        contexto = {
            'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
            'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
            'pi': np.pi, 'e': np.e
        }
        contexto.update(variables)
        resultado = eval(formula, {"__builtins__": None}, contexto)
        
        return {
            "valor": resultado.nominal_value,
            "incertidumbre_estandar": resultado.std_dev,
        }
    except Exception as e:
        return {"error": str(e)}