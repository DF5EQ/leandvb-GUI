#ifndef PARAMETERS_H
#define PARAMETERS_H

/*===== file header =========================================================*/

/*===== includes ============================================================*/
#include <stdint.h>
#include <stdbool.h>

/*===== public datatypes ====================================================*/
typedef struct
{
    uint16_t bandwidth;
    char*    constellation;
    char*    debug;
    bool     fastdrift;
    bool     fastlock;
    char*    fec;
    char*    framesizes;
    float    frequency;
    uint16_t gain;
    bool     gui;
    bool     hardmetric;
    uint32_t inpipe;
    uint16_t ldpc_bf;
    char*    ldpchelper_file;
    char*    ldpchelper_path;
    char*    leandvb_file;
    char*    leandvb_path;
    float    lnb_lo;
    bool     maxsens;
    char*    modcods;
    uint8_t  nhelpers;
    uint16_t ppm;
    float    rolloff;
    float    rrcrej;
    uint8_t  rtldongle;
    char*    rtlsdr_file;
    char*    rtlsdr_path;
    char*    sampler;
    char*    standard;
    bool     strongpls;
    uint16_t symbolrate;
    int16_t  tune;
    char*    viewer_file;
    char*    viewer_path;
    bool     viterbi;
}
parameters_t;

/*===== public symbols ======================================================*/

/*===== public constants ====================================================*/

/*===== public variables ====================================================*/

/*===== public functions ====================================================*/
void parameters_init    (void);
void parameters_print   (void);
void parameters_default (void);

#endif
