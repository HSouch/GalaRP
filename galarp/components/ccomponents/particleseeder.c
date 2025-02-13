#include <math.h>
#include <stdlib.h>
#include <stdio.h>

typedef struct {
    double* R;
    double* z;
    size_t count;
} ParticleSet;


float genRandom(float a, float b) {
    return a + (b - a) * ((float) rand() / (float) RAND_MAX);
}


ParticleSet* seed_particles(int NParticles, float hR, float hz) {
    ParticleSet* particles = (ParticleSet*) malloc(sizeof(ParticleSet));
    
    if (!particles) {
        fprintf(stderr, "Failed to allocate memory for Particle Set.\n");
    }

    particles->R = (double*) malloc(NParticles * sizeof(double));
    particles->z = (double*) malloc(NParticles * sizeof(double));

    if (!particles->R || !particles->z) {
        fprintf(stderr, "Failed to allocate memory for particle arrays.\n");
        free(particles->R);
        free(particles->z);
        free(particles);
        return NULL;
    }

    particles-> count = 0;

    float Rmax = hR * 5;
    float zmax = hz * 5;
    float PI = 3.1415926;

    double n0 = 1. / (4. * PI * hR * hR * hz);
    //  printf("%f %f \n", PI, n0);
    
    int maxAttempts = 100000;

    for (int i = 0; i < NParticles; i++) {
        for (int j = 0; j < maxAttempts; j++) {
            
            float r_attempt = genRandom(0, Rmax);
            float z_attempt = genRandom(-zmax, zmax);
            
            float p = n0 * exp(-(r_attempt / hR)) * exp(-(fabs(z_attempt) / hz));
            float rand_prob = genRandom(0, 1);
            
            if (rand_prob <= p) {
                float theta = genRandom(0, 2 * M_PI);
                
                particles->R[particles->count] = r_attempt;
                particles->z[particles->count] = z_attempt;
                particles->count++;
                break;
            }
            // printf("BAH %f %f %f %f %f \n", hR, hz, n0, p, rand_prob);
        }
    }
    
    return particles;

}

void free_particles(ParticleSet* particles) {
    if (particles) {
        free(particles->R);
        free(particles->z);
        free(particles);
    }
}
