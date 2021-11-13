/*===== file header =========================================================*/

/*===== includes ============================================================*/
#include <stdio.h>
#include <stdlib.h>
#include <json-c/json.h>
#include "parameters.h"

/*===== private datatypes ===================================================*/

/*===== private symbols =====================================================*/

/*===== private constants ===================================================*/

/*===== public constants ====================================================*/

/*===== private variables ===================================================*/
static parameters_t parameters;

/*===== public variables ====================================================*/

/*===== private functions ===================================================*/

/*===== callback functions ==================================================*/

/*===== public functions ====================================================*/

void parameters_default(void)
{
    parameters.bandwidth       = 2400;
    parameters.constellation   = "QPSK";
    parameters.debug           = "all";
    parameters.fastdrift       = false;
    parameters.fastlock        = false;
    parameters.fec             = "1/2";
    parameters.framesizes      = "0x01";
    parameters.frequency       = 10491.500;
    parameters.gain            = 36;
    parameters.gui             = true;
    parameters.hardmetric      = false;
    parameters.inpipe          = 32000000;
    parameters.ldpc_bf         = 0;
    parameters.ldpchelper_file = "ldpc_tool";
    parameters.ldpchelper_path = "./";
    parameters.leandvb_file    = "leandvb";
    parameters.leandvb_path    = "./";
    parameters.lnb_lo          = 9750.000;
    parameters.maxsens         = false;
    parameters.modcods         = "0x0040";
    parameters.nhelpers        = 6;
    parameters.ppm             = 0;
    parameters.rolloff         = 0.35;
    parameters.rrcrej          = 30.0;
    parameters.rtldongle       = 0;
    parameters.rtlsdr_file     = "rtl_sdr";
    parameters.rtlsdr_path     = "";
    parameters.sampler         = "rrc";
    parameters.standard        = "DVB-S2";
    parameters.strongpls       = false;
    parameters.symbolrate      = 1500;
    parameters.tune            = 0;
    parameters.viewer_file     = "ffplay -v 0";
    parameters.viewer_path     = "";
    parameters.viterbi         = false;
}

void parameters_print (void)
{
    printf("bandwidth      : %u\n", parameters.bandwidth);
    printf("constellation  : %s\n", parameters.constellation);
    printf("debug          : %s\n", parameters.debug);
    printf("fastdrift      : %s\n", parameters.fastdrift == true ? "true" : "false");
    printf("fastlock       : %s\n", parameters.fastlock == true ? "true" : "false");
    printf("fec            : %s\n", parameters.fec);
    printf("framesizes     : %s\n", parameters.framesizes);
    printf("frequency      : %.3f\n", parameters.frequency);
    printf("gain           : %u\n", parameters.gain);
    printf("gui            : %s\n", parameters.gui == true ? "true" : "false");
    printf("hardmetric     : %s\n", parameters.hardmetric == true ? "true" : "false");
    printf("inpipe         : %u\n", parameters.inpipe);
    printf("ldpc bitflip   : %u\n", parameters.ldpc_bf);
    printf("ldpchelper file: %s\n", parameters.ldpchelper_file);
    printf("ldpchelper path: %s\n", parameters.ldpchelper_path);
    printf("leandvb file   : %s\n", parameters.leandvb_file);
    printf("leandvb path   : %s\n", parameters.leandvb_path);
    printf("lnb_lo         : %.3f\n", parameters.lnb_lo);
    printf("maxsens        : %s\n", parameters.maxsens == true ? "true" : "false");
    printf("modcods        : %s\n", parameters.modcods);
    printf("nhelpers       : %u\n", parameters.nhelpers);
    printf("ppm            : %u\n", parameters.ppm);
    printf("rolloff        : %.2f\n", parameters.rolloff);
    printf("rrcrej         : %.1f\n", parameters.rrcrej);
    printf("rtldongle      : %u\n", parameters.rtldongle);
    printf("rtlsdr file    : %s\n", parameters.rtlsdr_file);
    printf("rtlsdr path    : %s\n", parameters.rtlsdr_path);
    printf("sampler        : %s\n", parameters.sampler);
    printf("standard       : %s\n", parameters.standard);
    printf("strongpls      : %s\n", parameters.strongpls == true ? "true" : "false");
    printf("symbolrate     : %u\n", parameters.symbolrate);
    printf("tune           : %u\n", parameters.tune);
    printf("viewer file    : %s\n", parameters.viewer_file);
    printf("viewer path    : %s\n", parameters.viewer_path);
    printf("viterbi        : %s\n", parameters.viterbi == true ? "true" : "false");
}

void parameters_init (void)
{
    parameters_default();
    parameters_print();

    /*--- for testing ---*/
    char* string        = "{\"name\" : \"programming\"}";
    json_object* jobj   = json_tokener_parse(string);
    enum json_type type = json_object_get_type(jobj);

    printf("\ntype: ");
    switch (type)
    {
        case json_type_null:
            printf("json_type_null\n");
           break;
        case json_type_boolean:
            printf("json_type_boolean\n");
            break;
        case json_type_double:
            printf("json_type_double\n");
            break;
        case json_type_int:
            printf("json_type_int\n");
            break;
        case json_type_object:
            printf("json_type_object\n");
            break;
        case json_type_array:
            printf("json_type_array\n");
            break;
        case json_type_string:
            printf("json_type_string\n");
            break;
    }

    exit(0);
}

