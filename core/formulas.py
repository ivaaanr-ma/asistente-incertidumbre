# core/formulas.py
import matplotlib.pyplot as plt
import io

def generar_imagen_formula(latex_formula, tamaño_letra=14):
    """
    Toma una fórmula en formato LaTeX (ej. r'$E = I - P$') 
    y devuelve un objeto BytesIO con la imagen en formato PNG.
    """
    # Configurar matplotlib para que no muestre ejes ni bordes
    fig = plt.figure(figsize=(6, 1))
    fig.patch.set_facecolor('white')
    
    # Escribir la fórmula
    fig.text(0.5, 0.5, latex_formula, ha='center', va='center', fontsize=tamaño_letra, color='black')
    
    # Guardar la imagen en memoria
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1, dpi=300, transparent=False)
    plt.close(fig)
    buf.seek(0)
    return buf