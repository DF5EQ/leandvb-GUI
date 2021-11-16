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

static const char* parameters_file_name = "parameters.json";
static FILE*       parameters_file = NULL;

/*===== private variables ===================================================*/

static parameters_t parameters;
static json_object* parameters_json_object;

/*===== public variables ====================================================*/

/*===== private functions ===================================================*/

static int serializer_double(struct json_object* o, struct printbuf* pb, int level, int flags)
{
    char* format;
    double value;

    format = json_object_get_userdata(o);
    value  = json_object_get_double(o); 	
	sprintbuf(pb, format, value);
	return 0;
}

static int serializer_string(struct json_object* o, struct printbuf* pb, int level, int flags)
{
    const char* string;

    string = json_object_get_string(o);	
	sprintbuf(pb, "\"%s\"", string);
	return 0;
}

static void json_object_double_add(struct json_object* obj, char* key, double val, char* fmt)
{
    struct json_object*o;

    o = json_object_new_double(val);
    json_object_set_serializer(o, serializer_double, fmt, NULL);
    json_object_object_add(obj, key, o);
}

static void json_object_string_add(struct json_object* obj, char* key, char* val)
{
    struct json_object* o;

    o = json_object_new_string(val);
    json_object_set_serializer(o, serializer_string, NULL, NULL);
    json_object_object_add(obj, key, o);
}

static void json_object_int_add(struct json_object* obj, char* key, int val)
{
    struct json_object* o;

    o = json_object_new_int(val);
    json_object_object_add(obj, key, o);
}

static void json_object_boolean_add(struct json_object* obj, char* key, bool val)
{
    struct json_object* o;

    o = json_object_new_boolean(val);
    json_object_object_add(obj, key, o);
}

static void json_object_int_get(struct json_object* obj, const char* key, int* val)
{
    struct json_object* o;
    
    json_object_object_get_ex(parameters_json_object, key, &o);
    *val = json_object_get_int(o);
}

static void json_object_string_get(struct json_object* obj, const char* key, char** val)
{
    struct json_object* o;
    
    json_object_object_get_ex(parameters_json_object, key, &o);
    *val = (char*)json_object_get_string(o);
}

static void json_object_boolean_get(struct json_object* obj, const char* key, bool* val)
{
    struct json_object* o;
    
    json_object_object_get_ex(parameters_json_object, key, &o);
    *val = json_object_get_boolean(o);
}

static void json_object_double_get(struct json_object* obj, const char* key, float* val)
{
    struct json_object* o;
    
    json_object_object_get_ex(parameters_json_object, key, &o);
    *val = (float)json_object_get_double(o);
}

static void parameters_to_json_object (void)
{
    parameters_json_object = json_object_new_object();

    json_object_int_add     (parameters_json_object, "bandwidth",       parameters.bandwidth);
    json_object_string_add  (parameters_json_object, "constellation",   parameters.constellation);
    json_object_string_add  (parameters_json_object, "debug",           parameters.debug);
    json_object_boolean_add (parameters_json_object, "fastdrift",       parameters.fastdrift);
    json_object_boolean_add (parameters_json_object, "fastlock",        parameters.fastlock);
    json_object_string_add  (parameters_json_object, "fec",             parameters.fec);
    json_object_string_add  (parameters_json_object, "framesizes",      parameters.framesizes);
    json_object_double_add  (parameters_json_object, "frequency",       parameters.frequency, "%.3f");
    json_object_int_add     (parameters_json_object, "gain",            parameters.gain);
    json_object_boolean_add (parameters_json_object, "gui",             parameters.gui);
    json_object_boolean_add (parameters_json_object, "hardmetric",      parameters.hardmetric);
    json_object_int_add     (parameters_json_object, "inpipe",          parameters.inpipe);
    json_object_int_add     (parameters_json_object, "ldpc_bf",         parameters.ldpc_bf);
    json_object_string_add  (parameters_json_object, "ldpchelper_file", parameters.ldpchelper_file);
    json_object_string_add  (parameters_json_object, "ldpchelper_path", parameters.ldpchelper_path);
    json_object_string_add  (parameters_json_object, "leandvb_file",    parameters.leandvb_file);
    json_object_string_add  (parameters_json_object, "leandvb_path",    parameters.leandvb_path);
    json_object_double_add  (parameters_json_object, "lnb_lo",          parameters.lnb_lo, "%.3f");
    json_object_boolean_add (parameters_json_object, "maxsens",         parameters.maxsens);
    json_object_string_add  (parameters_json_object, "modcods",         parameters.modcods);
    json_object_int_add     (parameters_json_object, "nhelpers",        parameters.nhelpers);
    json_object_int_add     (parameters_json_object, "ppm",             parameters.ppm);
    json_object_double_add  (parameters_json_object, "rolloff",         parameters.rolloff, "%.2f");
    json_object_double_add  (parameters_json_object, "rrcrej",          parameters.rrcrej, "%.1f");
    json_object_int_add     (parameters_json_object, "rtldongle",       parameters.rtldongle);
    json_object_string_add  (parameters_json_object, "rtlsdr_file",     parameters.rtlsdr_file);
    json_object_string_add  (parameters_json_object, "rtlsdr_path",     parameters.rtlsdr_path);
    json_object_string_add  (parameters_json_object, "sampler",         parameters.sampler);
    json_object_string_add  (parameters_json_object, "standard",        parameters.standard);
    json_object_boolean_add (parameters_json_object, "strongpls",       parameters.strongpls);
    json_object_int_add     (parameters_json_object, "symbolrate",      parameters.symbolrate);
    json_object_int_add     (parameters_json_object, "tune",            parameters.tune);
    json_object_string_add  (parameters_json_object, "viewer_file",     parameters.viewer_file);
    json_object_string_add  (parameters_json_object, "viewer_path",     parameters.viewer_path);
    json_object_boolean_add (parameters_json_object, "viterbi",         parameters.viterbi);
}

static void parameters_from_json_object (void)
{
    struct json_object* jso;

    json_object_int_get     (parameters_json_object, "bandwidth",       &parameters.bandwidth);
    json_object_string_get  (parameters_json_object, "constellation",   &parameters.constellation);
    json_object_string_get  (parameters_json_object, "debug",           &parameters.debug);
    json_object_boolean_get (parameters_json_object, "fastdrift",       &parameters.fastdrift);
    json_object_boolean_get (parameters_json_object, "fastlock",        &parameters.fastlock);
    json_object_string_get  (parameters_json_object, "fec",             &parameters.fec);
    json_object_string_get  (parameters_json_object, "framesizes",      &parameters.framesizes);
    json_object_double_get  (parameters_json_object, "frequency",       &parameters.frequency);
    json_object_int_get     (parameters_json_object, "gain",            &parameters.gain);
    json_object_boolean_get (parameters_json_object, "gui",             &parameters.gui);
    json_object_boolean_get (parameters_json_object, "hardmetric",      &parameters.hardmetric);
    json_object_int_get     (parameters_json_object, "inpipe",          &parameters.inpipe);
    json_object_int_get     (parameters_json_object, "ldpc_bf",         &parameters.ldpc_bf);
    json_object_string_get  (parameters_json_object, "ldpchelper_file", &parameters.ldpchelper_file);
    json_object_string_get  (parameters_json_object, "ldpchelper_path", &parameters.ldpchelper_path);
    json_object_string_get  (parameters_json_object, "leandvb_file",    &parameters.leandvb_file);
    json_object_string_get  (parameters_json_object, "leandvb_path",    &parameters.leandvb_path);
    json_object_double_get  (parameters_json_object, "lnb_lo",          &parameters.lnb_lo);
    json_object_boolean_get (parameters_json_object, "maxsens",         &parameters.maxsens);
    json_object_string_get  (parameters_json_object, "modcods",         &parameters.modcods);
    json_object_int_get     (parameters_json_object, "nhelpers",        &parameters.nhelpers);
    json_object_int_get     (parameters_json_object, "ppm",             &parameters.ppm);
    json_object_double_get  (parameters_json_object, "rolloff",         &parameters.rolloff);
    json_object_double_get  (parameters_json_object, "rrcrej",          &parameters.rrcrej);
    json_object_int_get     (parameters_json_object, "rtldongle",       &parameters.rtldongle);
    json_object_string_get  (parameters_json_object, "rtlsdr_file",     &parameters.rtlsdr_file);
    json_object_string_get  (parameters_json_object, "rtlsdr_path",     &parameters.rtlsdr_path);
    json_object_string_get  (parameters_json_object, "sampler",         &parameters.sampler);
    json_object_string_get  (parameters_json_object, "standard",        &parameters.standard);
    json_object_boolean_get (parameters_json_object, "strongpls",       &parameters.strongpls);
    json_object_int_get     (parameters_json_object, "symbolrate",      &parameters.symbolrate);
    json_object_int_get     (parameters_json_object, "tune",            &parameters.tune);
    json_object_string_get  (parameters_json_object, "viewer_file",     &parameters.viewer_file);
    json_object_string_get  (parameters_json_object, "viewer_path",     &parameters.viewer_path);
    json_object_boolean_get (parameters_json_object, "viterbi",         &parameters.viterbi);
}

/*===== callback functions ==================================================*/

/*===== public functions ====================================================*/

void parameters_default(void)
{
    /* load parameters with defaults */

    printf("load parameters with defaults\n");

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

    parameters_to_json_object();
}

void parameters_print (void)
{
    /* print parameters to console */

    printf("bandwidth      : %u\n",   parameters.bandwidth);
    printf("constellation  : %s\n",   parameters.constellation);
    printf("debug          : %s\n",   parameters.debug);
    printf("fastdrift      : %s\n",   parameters.fastdrift == true ? "true" : "false");
    printf("fastlock       : %s\n",   parameters.fastlock == true ? "true" : "false");
    printf("fec            : %s\n",   parameters.fec);
    printf("framesizes     : %s\n",   parameters.framesizes);
    printf("frequency      : %.3f\n", parameters.frequency);
    printf("gain           : %u\n",   parameters.gain);
    printf("gui            : %s\n",   parameters.gui == true ? "true" : "false");
    printf("hardmetric     : %s\n",   parameters.hardmetric == true ? "true" : "false");
    printf("inpipe         : %u\n",   parameters.inpipe);
    printf("ldpc bitflip   : %u\n",   parameters.ldpc_bf);
    printf("ldpchelper file: %s\n",   parameters.ldpchelper_file);
    printf("ldpchelper path: %s\n",   parameters.ldpchelper_path);
    printf("leandvb file   : %s\n",   parameters.leandvb_file);
    printf("leandvb path   : %s\n",   parameters.leandvb_path);
    printf("lnb_lo         : %.3f\n", parameters.lnb_lo);
    printf("maxsens        : %s\n",   parameters.maxsens == true ? "true" : "false");
    printf("modcods        : %s\n",   parameters.modcods);
    printf("nhelpers       : %u\n",   parameters.nhelpers);
    printf("ppm            : %u\n",   parameters.ppm);
    printf("rolloff        : %.2f\n", parameters.rolloff);
    printf("rrcrej         : %.1f\n", parameters.rrcrej);
    printf("rtldongle      : %u\n",   parameters.rtldongle);
    printf("rtlsdr file    : %s\n",   parameters.rtlsdr_file);
    printf("rtlsdr path    : %s\n",   parameters.rtlsdr_path);
    printf("sampler        : %s\n",   parameters.sampler);
    printf("standard       : %s\n",   parameters.standard);
    printf("strongpls      : %s\n",   parameters.strongpls == true ? "true" : "false");
    printf("symbolrate     : %u\n",   parameters.symbolrate);
    printf("tune           : %u\n",   parameters.tune);
    printf("viewer file    : %s\n",   parameters.viewer_file);
    printf("viewer path    : %s\n",   parameters.viewer_path);
    printf("viterbi        : %s\n",   parameters.viterbi == true ? "true" : "false");
}

void parameters_save (void)
{
    /* save parameters to file */

    printf("save parameters to file %s\n", parameters_file_name);
    parameters_to_json_object();
    json_object_to_file_ext(parameters_file_name, parameters_json_object, JSON_C_TO_STRING_SPACED | JSON_C_TO_STRING_PRETTY);
}

void parameters_load (void)
{
    /* load parameters from file */

    printf("load parameters from file %s\n", parameters_file_name);
    parameters_json_object = json_object_from_file(parameters_file_name);
    parameters_from_json_object();
}

void parameters_init (void)
{
    /* load parameters from file or with defaults */

    parameters_file = fopen(parameters_file_name, "r");
    if (parameters_file == NULL)
    {   /* file does not exist */
        parameters_default();
    }
    else
    {   /* file exists */
        fclose(parameters_file);
        parameters_load();
    }
}

void parameters_deinit (void)
{
    /* save parameters to file */

    parameters_save();
}

