/**
 * @file calculo.h
 * @brief Interface da Biblioteca de Series de Fourier.
 * * Este arquivo define as assinaturas das funcoes que o Python 
 * podera chamar para calcular 
 * a amplitude das ondas matematicas em um determinado tempo.
 */

#ifndef CALCULO_H
#define CALCULO_H

/**
 * @brief Calcula o valor da Onda Quadrada via Serie de Fourier.
 * * @param N Numero de harmonicas (define a precisao da onda).
 * @param A Amplitude de pico da onda.
 * @param t Instante de tempo no eixo X (em segundos).
 * @return double Amplitude f(t) resultante para aquele instante.
 */
double squareWave(int, int, double);

/**
 * @brief Calcula o valor da Onda Dente de Serra via Serie de Fourier.
 * * @param N Numero de harmonicas (define a precisao da onda).
 * @param A Amplitude de pico da onda.
 * @param t Instante de tempo no eixo X (em segundos).
 * @return double Amplitude f(t) resultante para aquele instante.
 */
double sawtoothWave(int, int, double);

/**
 * @brief Calcula o valor da Onda Triangular via Serie de Fourier.
 * * @param N Numero de harmonicas (define a precisao da onda).
 * @param A Amplitude de pico da onda.
 * @param t Instante de tempo no eixo X (em segundos).
 * @return double Amplitude f(t) resultante para aquele instante.
 */
double triangleWave(int, int, double);

#endif // CALCULO_H