#include <math.h>
#include "calculo.h"
#define PI 3.141592653589793

double squareWave(int N, int A, double t){
    int k;
    double resultado = 0.0;
    double n;

    for(k = 1; k <=N; ++k){
        n = 2.0 * k - 1.0;
        resultado += sin(n * (2.0 * PI) * t) / n; 

    }

    return (4 * A) / PI * resultado;

}

double sawtoothWave(int N, int A, double t){
    int k;
    double resultado = 0.0;

    for(k = 1; k <= N; ++k){
        resultado += ((pow(-1.0, k + 1.0)) / k) * sin(k * (2.0 * PI) * t);

    }
    
    return (2 * A) / PI * resultado;

}

double triangleWave(int N, int A, double t){
    int k;
    double resultado = 0.0;
    double n;

    for(k = 1; k <= N; ++k){
        n = 2.0 * k - 1.0;
        resultado += (pow(-1.0, k - 1.0) / pow(n, 2.0)) * sin(n * (2.0 * PI) * t);

    }

    return (8 * A) / (pow(PI, 2)) * resultado;

}

