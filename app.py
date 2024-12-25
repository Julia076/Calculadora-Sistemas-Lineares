from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask("solução de sistemas lineares por escalonamento:")

def escalonamento(A, b):
    # Verifica o tamanho da matriz A (número de linhas ou variáveis)
    n = len(A)

    # Criação da matriz aumentada [A|b] combinando a matriz A e o vetor b como uma última coluna de A
    A = np.hstack([A, b.reshape(-1, 1)])

    # Processo de escalonamento / transformar a matriz A em uma matriz Triangular Superior 
    for i in range(n):
        # Verificar se o elemento de pivô (A[i, i]) é zero 
        # Se o pivô é zero, o sistema pode não ter solução única ou ser não invertível
        if A[i, i] == 0:
            raise ValueError("A matriz tem uma linha de zeros, o sistema pode não ser invertível ou ter soluções infinitas.")

        # Tornar o elemento de pivô (A[i, i]) igual a 1 dividindo a linha a[i] inteira por A[i, i]
        A[i] = A[i] / A[i, i]

        # Eliminar as variáveis abaixo do elemento de pivô para criar zeros na coluna i
        for j in range(i + 1, n):
            fator = A[j, i] # Fator que multiplica a linha do pivô para zerar o elemento A[j, i] 
                              # Esse fator indica o valor pelo qual multiplicamos a linha do pivô i para eliminar o valor abaixo do pivô.
            A[j] -= fator * A[i]  # Subtrai a linha do pivô multiplicada pelo fator da linha j 
                                  # para cada linha j abaixo do pivô subt 1 multiplo da linha i
                                  # multiplicamos a linha i por 𝐴[𝑗,𝑖] e subtraímos de 𝐴[𝑗]
    # Substituição regressiva para encontrar as soluções
    x = np.zeros(n)
    # Começa na última linha e sobe até a primeira para resolver cada variável
    for i in range(n - 1, -1, -1):
        # Calcula o valor de x[i] subtraindo o produto dos valores já encontrados e o termo independente
        x[i] = A[i, -1] - np.dot(A[i, i+1:n], x[i+1:])        #xrepresenta os coeficientes das variáveis que já foram calculadas
                                                              # np.dot multp os coef pelos valores já encontrados
                                                              #calcula o produto entre os coeficientes e as variáveis já calculadas
        
    
    return x


































@app.route('/')
def index():
    return render_template('index.html')  # Serve o arquivo HTML
@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    A = np.array(data['A'], dtype=float)
    b = np.array(data['b'], dtype=float)
    try:
        solution = escalonamento(A, b).tolist() 
        variable_names = ['x', 'y', 'z', 'w']  # Adapte conforme o número de variáveis
        formatted_solution = [f"{var} = {value}" for var, value in zip(variable_names, solution)]
        return jsonify({"solution": formatted_solution})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000, debug=True)

