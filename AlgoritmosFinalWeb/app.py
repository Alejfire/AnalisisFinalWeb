from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def resolverSistema(coeficientes, constantes):
    try:
        solution = np.linalg.solve(coeficientes, constantes)
        return list(solution)
    except np.linalg.LinAlgError:
        return None 

def graficarEcuaciones(coeficientes, constantes, colors=None):
    x = np.linspace(-10, 10, 400)
    plt.figure(figsize=(8, 6))

    for i in range(len(coeficientes)):
        coef = coeficientes[i]
        const = constantes[i]
        color = colors[i] if colors else None
        if coef[1] != 0:
            m = -coef[0] / coef[1]
            b = const / coef[1]
            y = m * x + b
            plt.plot(x, y, label=f"Ecuacion {i+1}: y = {m:.2f}x + {b:.2f}", color=color)
        else:
            plt.axvline(x=const / coef[0], linestyle='--', label=f"Ecuacion {i+1}: x = {const / coef[0]:.2f}", color=color)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Grafico de las ecuaciones lineales')
    plt.grid(True)
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    img_base64 = base64.b64encode(img.getvalue()).decode()

    return img_base64

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    numEcuaciones = int(request.form['numEcuaciones'])
    numVariables = int(request.form['numVariables'])

    coeficientes = []
    constantes = []

    for i in range(numEcuaciones):
        coef = []
        for j in range(numVariables):
            value = float(request.form[f'coef_{i}_{j}'])
            coef.append(value)
        coeficientes.append(coef)

        constant = float(request.form[f'const_{i}'])
        constantes.append(constant)

    solution = resolverSistema(np.array(coeficientes), np.array(constantes))
    if solution:
        img_base64 = graficarEcuaciones(coeficientes, constantes, colors=['red', 'blue'])
        return render_template('result.html', solution=solution, img_base64=img_base64)
    else:
        return "No se resolvio el sistema de ecuaciones."

if __name__ == '__main__':
    app.run(debug=True)