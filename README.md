# Série de Fourier - Integração Python-C

Projeto que implementa o cálculo de Séries de Fourier para aproximação de ondas (quadrada, dente de serra, triangular) com integração entre Python e C.

## Arquitetura

### C (`calculo.c` e `calculo.h`)
- **squareWave(N, A, t)**: Calcula a aproximação de onda quadrada
- **sawtoothWave(N, A, t)**: Calcula a aproximação de onda dente de serra  
- **triangleWave(N, A, t)**: Calcula a aproximação de onda triangular

Cada função recebe:
- `N`: número de harmônicas (precisão)
- `A`: amplitude de pico
- `t`: valor do tempo (double)

E retorna `f(t)`: a amplitude da onda no instante t

### Python (`interface.py`)
- Carrega a biblioteca C compilada via `ctypes`
- Itera sobre um array de valores de tempo (0 a 2π)
- Para cada tempo `t`, chama a função C correspondente
- Coleta os resultados em um array NumPy
- Visualiza o resultado com Matplotlib

## Como usar

### 1. Compilar a biblioteca C

```bash
make compilar_lib
```

Gera `libcalculo.so` (Linux/macOS) ou `libcalculo.dll` (Windows)

### 2. Criar virtual environment (recomendado)

```bash
python3 -m venv venv  # No Windows: python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install matplotlib numpy PyQt5
```

### 3. Executar o programa

**Opção A: Com janela interativa (requer display gráfico)**
```bash
./run.sh 20 1.0 square
./run.sh 15 1.5 sawtooth
./run.sh 10 0.8 triangle
```

**Opção B: Salvar em arquivo PNG**
```bash
./run.sh 20 1.0 square --save grafico.png
./run.sh 15 1.5 sawtooth --save onda.png
./run.sh 10 0.8 triangle --save triangulo.png
```

**Parâmetros:**
- `N`: Número de harmônicas (padrão: 10)
- `A`: Amplitude (padrão: 1.0)
- `wave_type`: Tipo de onda - `square`, `sawtooth` ou `triangle` (padrão: square)
- `--save arquivo.png`: Salva gráfico em arquivo (opcional)

## Integração Python-C

A integração é feita via `ctypes`, que permite chamar funções de bibliotecas C dinâmicas diretamente do Python:

### 1. Carregando a biblioteca C

```python
import ctypes

# Carrega a biblioteca C compilada
fourier_lib = ctypes.CDLL("./libcalculo.so")  # Linux/macOS
# fourier_lib = ctypes.CDLL("./libcalculo.dll")  # Windows
```

`CDLL` (C Dynamic-Link Library) carrega o arquivo `.so`/`.dll` que contém as funções compiladas em C.

### 2. Definindo as assinaturas das funções

```python
# Define os tipos de argumentos e tipo de retorno
fourier_lib.squareWave.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double]
fourier_lib.squareWave.restype = ctypes.c_double
```

Isso informa ao Python:
- **`argtypes`**: A função C recebe 3 argumentos: `int`, `int`, `double`
- **`restype`**: A função C retorna um `double`

Sem isso, Python não saberia como converter os dados corretamente.

### 3. Chamando a função C

```python
import numpy as np

# Cria array de 1000 pontos de tempo de 0 a 2π
x_values = np.linspace(0, 2 * np.pi, 1000)
y_values = np.zeros_like(x_values)

# Para cada tempo t, chama a função C
for i, t in enumerate(x_values):
    # Converte valores Python para tipos C
    N = ctypes.c_int(20)          # número de harmônicas
    A = ctypes.c_int(1)            # amplitude inteira
    time = ctypes.c_double(t)      # tempo em double
    
    # Chama função C e armazena resultado
    y_values[i] = fourier_lib.squareWave(N, A, time)
```

### Resumo do fluxo

```
Python (ctypes)
    ↓
    Converte dados para tipos C
    ↓
    Chama função C via CDLL
    ↓
C (libcalculo.so)
    ↓
    Calcula série de Fourier
    ↓
    Retorna double para Python
    ↓
Python (ctypes)
    ↓
    Converte double para float Python
    ↓
    Armazena em array NumPy
```

### Exemplo completo

```python
import ctypes
import numpy as np
import matplotlib.pyplot as plt

# 1. Carregar biblioteca
lib = ctypes.CDLL("./libcalculo.so")

# 2. Definir assinatura
lib.squareWave.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double]
lib.squareWave.restype = ctypes.c_double

# 3. Gerar dados
x = np.linspace(0, 2 * np.pi, 1000)
y = np.zeros_like(x)

# 4. Chamar função C para cada ponto
for i, t in enumerate(x):
    y[i] = lib.squareWave(ctypes.c_int(20), ctypes.c_int(1), ctypes.c_double(t))

# 5. Plotar resultado
plt.plot(x, y)
plt.show()
```

### Vantagens dessa abordagem

- ✅ **Performance**: Cálculos em C são muito mais rápidos
- ✅ **Simplicidade**: Não precisa compilar wrappers C
- ✅ **Flexibilidade**: Podemos chamar qualquer função C
- ✅ **Portabilidade**: `ctypes` funciona em Linux, Windows, macOS

## Exemplo de saída

```
Teste da integração Python-C:
Valores de t (tempo): [0.0, 1.0, 2.0, 3.0, 4.0]
Valores f(t): [0.0, -3.79e-15, -7.58e-15, -1.32e-14, -1.52e-14]
✓ Integração bem-sucedida!
```

## Estrutura dos arquivos

```
.
├── calculo.c           # Implementação das funções em C
├── calculo.h           # Headers das funções
├── interface.py        # Interface Python com integração C
├── libcalculo.so       # Biblioteca compilada (gerada por make)
├── Makefile            # Targets para compilação e execução
└── README.md           # Este arquivo
```

## Performance

A integração C-Python permite:
- Cálculos mais rápidos (operações em C são compiladas)
- Aproveitamento da precisão de ponto flutuante em C
- Array processing eficiente com NumPy

## Notas técnicas

- Usa `#define PI 3.141592653589793` para alta precisão
- Funções trigonométricas via `math.h`
- Compilação com `-shared -fPIC -lm` para biblioteca dinâmica
- ctypes para interface sem dependências externas
