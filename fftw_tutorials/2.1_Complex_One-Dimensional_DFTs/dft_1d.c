#include <fftw3.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    int N = 16;
    fftw_complex *in, *out;
    fftw_plan p;
    int i;
    printf("\nForward transform:\n");
    in = (fftw_complex*) fftw_malloc(sizeof(fftw_complex)*N);
    out = (fftw_complex*) fftw_malloc(sizeof(fftw_complex)*N);

    for (i = 0; i < N; i++) {
        in[i][0] = cos(3*2*M_PI*i/N);
        in[i][1] = 0.;
    }    

    /* alternative way of assigning value */
    /*
    fftw_complex *p_in = in;
    for (i = 0; i < N; i++) {
        double val = cos(3*2*M_PI*i/N);
        memcpy(*p_in, &val, sizeof(double));
        p_in++;
    }
    */    

    printf("Input=\n");
    for (i = 0; i < N; i++) {
        printf("%3d %5.2f %+5.2fj\n", i, in[i][0], in[i][1]);
    }   
    p = fftw_plan_dft_1d(N, in, out, FFTW_FORWARD, FFTW_ESTIMATE);
    
    fftw_execute(p);
    printf("Output=\n");
    for (i = 0; i < N; i++) {
        printf("%3d %5.2f %+5.2fj\n", i, out[i][0], out[i][1]);
    }   
    
    fftw_destroy_plan(p);
    
    printf("\nInverse transform:\n");
    fftw_complex* back;
    back = (fftw_complex*) fftw_malloc(sizeof(fftw_complex)*N);

    fftw_plan p_i = fftw_plan_dft_1d(N, out, back, FFTW_BACKWARD, FFTW_ESTIMATE);
    fftw_execute(p_i);
    
    for (i = 0; i < N; i++) {
        back[i][0] *= 1./N;
        back[i][1] *= 1./N;
    }
    
    printf("Output=\n");
    for (i = 0; i < N; i++) {
        printf("%3d %5.2f %+5.2fj\n", i, back[i][0], back[i][1]);
    }   
    fftw_destroy_plan(p_i);
    fftw_cleanup();
    return 0;
}

    