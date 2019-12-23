#include <fftw3.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    int N = 8;
    fftw_complex *in, *out;
    fftw_plan p;
    int i;
    printf("\nForward transform:\n");
    in = (fftw_complex*) fftw_malloc(sizeof(fftw_complex)*N*N);
    out = (fftw_complex*) fftw_malloc(sizeof(fftw_complex)*N*N);

    // set everything to zero first
    memset(in, 0, sizeof(fftw_complex)*N*N);
    
    // change a few places to have non zero values
    in[10][0] = 70;
    in[11][0] = 80;
    in[12][0] = 90;
    in[18][0] = 90;
    in[19][0] = 100;
    in[20][0] = 110;
    in[26][0] = 110;
    in[27][0] = 120;
    in[28][0] = 130;
    in[34][0] = 130;
    in[35][0] = 140;
    in[36][0] = 150;
    
    printf("Input=\n");
    for (i = 0; i < N*N; i++) {
        printf("%3d %5.2f %+5.2fj,  ", i, in[i][0], in[i][1]);
        if ((i+1) % N == 0) printf("\n");
    }   
    printf("\n");
    p = fftw_plan_dft_2d(N, N, in, out, FFTW_FORWARD, FFTW_ESTIMATE);
    
    fftw_execute(p);
    printf("Output=\n");
    for (i = 0; i < N*N; i++) {
        printf("%3d %5.2f %+5.2fj,  ", i, out[i][0], out[i][1]);
        if ((i+1) % N == 0) printf("\n");
    }   
    
    fftw_destroy_plan(p);
    fftw_cleanup();
    return 0;
}

    