/**
 * @file calculo.c
 * @brief Motor de calculo de Series de Fourier.
 * * Este modulo contem as implementacoes matematicas para aproximar 
 * os sinais de onda Quadrada, Dente de Serra e Triangular usando 
 * a somatoria da Serie de Fourier.
 */

#include <math.h>                                   // Importa a biblioteca de funções matemáticas (a função necessária é sin())
#include "calculo.h"                                // Importa o módulo .h contendo os protótipos das funções

// Definicao de PI com alta precisao para evitar erros de truncamento em N grandes
#define PI 3.141592653589793

/**
 * @brief Calcula a amplitude da Onda Quadrada em um dado instante de tempo.
 * * Utiliza apenas as harmonicas impares da Serie de Fourier.
 * * @param N Numero de harmonicas (termos da serie) a serem somadas.
 * @param A Amplitude de pico da onda.
 * @param t Instante de tempo (em segundos) a ser calculado.
 * @return double Valor da amplitude f(t) da onda quadrada.
 */
double squareWave(int N, int A, double t){
    int k;                                          // k => corresponde ao indice (termo/harmônica) da série
    double resultado = 0.0;                         // resultado => este valor, ao final das somas, será multiplicado por um fator (4 * A) / PI
    double n;                                       // n => variável auxiliar que contém o valor calculado de 2 * k - 1

    for(k = 1; k <=N; ++k){
        n = 2.0 * k - 1.0;
        resultado += sin(n * (2.0 * PI) * t) / n; 
    }

    // Aplica o ganho final da onda quadrada: (4A / PI)
    return (4 * A) / PI * resultado;
}

/**
 * @brief Calcula a amplitude da Onda Dente de Serra em um dado instante.
 * * Utiliza todas as harmonicas (pares e impares) com alternancia de sinal.
 * * @param N Numero de harmonicas (termos da serie) a serem somadas.
 * @param A Amplitude de pico da onda.
 * @param t Instante de tempo (em segundos) a ser calculado.
 * @return double Valor da amplitude f(t) da onda dente de serra.
 */
double sawtoothWave(int N, int A, double t){
    int k;                                          // k => corresponde ao indice (termo/harmônica) da série
    double resultado = 0.0;                         // resultado => este valor, ao final das somas, será multiplicado por um fator (4 * A) / PI

    for(k = 1; k <= N; ++k){
        // pow(-1, k+1) alterna o sinal (+, -, +, -...)
        // A divisao por 'k' garante o decaimento linear das harmonicas
        resultado += ((pow(-1.0, k + 1.0)) / k) * sin(k * (2.0 * PI) * t);
    }
    // Aplica o ganho final da dente de serra: (2A / PI)    
    return (2 * A) / PI * resultado;

}

/**
 * @brief Calcula a amplitude da Onda Triangular em um dado instante.
 * * Utiliza apenas harmonicas impares, com alternancia de sinal e decaimento quadratico.
 * * @param N Numero de harmonicas (termos da serie) a serem somadas.
 * @param A Amplitude de pico da onda.
 * @param t Instante de tempo (em segundos) a ser calculado.
 * @return double Valor da amplitude f(t) da onda triangular.
 */
double triangleWave(int N, int A, double t){
    int k;                                          // k => corresponde ao indice (termo/harmônica) da série
    double resultado = 0.0;                         // resultado => este valor, ao final das somas, será multiplicado por um fator (4 * A) / PI
    double n;                                       // n => variável auxiliar que contém o valor calculado de 2 * k - 1

    for(k = 1; k <= N; ++k){
        // n = 1, 3, 5, 7... (Apenas harmonicas impares)
        n = 2.0 * k - 1.0;
        
        // pow(-1, k-1) alterna o sinal a cada termo impar
        // pow(n, 2.0) gera um decaimento quadratico, tornando a onda mais suave
        resultado += (pow(-1.0, k - 1.0) / pow(n, 2.0)) * sin(n * (2.0 * PI) * t);
    }

    // Aplica o ganho final da onda triangular: (8A / PI^2)
    return (8 * A) / (pow(PI, 2)) * resultado;
}

