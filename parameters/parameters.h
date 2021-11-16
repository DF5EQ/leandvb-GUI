#ifndef PARAMETERS_H
#define PARAMETERS_H

/*===== file header =========================================================*/

/*===== includes ============================================================*/

#include <stdint.h>
#include <stdbool.h>

/*===== public datatypes ====================================================*/

typedef struct
{
    int   bandwidth;
    char* constellation;
    char* debug;
    bool  fastdrift;
    bool  fastlock;
    char* fec;
    char* framesizes;
    float frequency;
    int   gain;
    bool  gui;
    bool  hardmetric;
    int   inpipe;
    int   ldpc_bf;
    char* ldpchelper_file;
    char* ldpchelper_path;
    char* leandvb_file;
    char* leandvb_path;
    float lnb_lo;
    bool  maxsens;
    char* modcods;
    int   nhelpers;
    int   ppm;
    float rolloff;
    float rrcrej;
    int   rtldongle;
    char* rtlsdr_file;
    char* rtlsdr_path;
    char* sampler;
    char* standard;
    bool  strongpls;
    int   symbolrate;
    int   tune;
    char* viewer_file;
    char* viewer_path;
    bool  viterbi;
}
parameters_t;

/*===== public symbols ======================================================*/

/*===== public constants ====================================================*/

/*===== public variables ====================================================*/

/*===== public functions ====================================================*/

void parameters_init    (void);
void parameters_print   (void);
void parameters_default (void);
void parameters_load    (void);
void parameters_save    (void);

#endif
