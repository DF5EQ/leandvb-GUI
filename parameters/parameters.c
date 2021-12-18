/*===== file header =========================================================*/

/*===== includes ============================================================*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <json-c/json.h>
#include "parameters.h"

/*===== private datatypes ===================================================*/

/*===== private symbols =====================================================*/

/* default values for parameters */

#define PARAM_DEFAULT_BANDWIDTH       2400
#define PARAM_DEFAULT_CODERATE        "4/5"
#define PARAM_DEFAULT_CONSTELLATION   "QPSK"
#define PARAM_DEFAULT_DEBUG           "all"
#define PARAM_DEFAULT_FASTDRIFT       false
#define PARAM_DEFAULT_FASTLOCK        false
#define PARAM_DEFAULT_FEC             "1/2"
#define PARAM_DEFAULT_FRAMESIZES      "0x01"
#define PARAM_DEFAULT_FREQUENCY       10491.500
#define PARAM_DEFAULT_GAIN            36
#define PARAM_DEFAULT_GUI             true
#define PARAM_DEFAULT_HARDMETRIC      false
#define PARAM_DEFAULT_INPIPE          32000000
#define PARAM_DEFAULT_LDPCBF          0
#define PARAM_DEFAULT_LDPCHELPER_FILE "ldpc_tool"
#define PARAM_DEFAULT_LDPCHELPER_PATH "./"
#define PARAM_DEFAULT_LEANDVB_FILE    "leandvb"
#define PARAM_DEFAULT_LEANDVB_PATH    "./"
#define PARAM_DEFAULT_LNB_LO          9750.000
#define PARAM_DEFAULT_MAXSENS         false
#define PARAM_DEFAULT_MODCODS         "0x0040"
#define PARAM_DEFAULT_NHELPERS        6
#define PARAM_DEFAULT_PPM             0
#define PARAM_DEFAULT_ROLLOFF         0.35
#define PARAM_DEFAULT_RRCREJ          30.0
#define PARAM_DEFAULT_RTLDONGLE       0
#define PARAM_DEFAULT_RTLSDR_FILE     "rtl_sdr"
#define PARAM_DEFAULT_RTLSDR_PATH     "/usr/bin"
#define PARAM_DEFAULT_SAMPLER         "rrc"
#define PARAM_DEFAULT_STANDARD        "DVB-S2"
#define PARAM_DEFAULT_STRONGPLS       false
#define PARAM_DEFAULT_SYMBOLRATE      2000
#define PARAM_DEFAULT_TUNE            0
#define PARAM_DEFAULT_VIEWER_FILE     "ffplay -v 0"
#define PARAM_DEFAULT_VIEWER_PATH     "/usr/bin"
#define PARAM_DEFAULT_VITERBI         false

/*===== private constants ===================================================*/

/*===== public constants ====================================================*/

/*===== private variables ===================================================*/

/* parameters */

static       int   bandwidth;
static const char* coderate;
static const char* constellation;
static const char* debug;
static       bool  fastdrift;
static       bool  fastlock;
static const char* fec;
static const char* framesizes;
static       float frequency;
static       int   gain;
static       bool  gui;
static       bool  hardmetric;
static       int   inpipe;
static       int   ldpcbf;
static const char* ldpchelper_file;
static const char* ldpchelper_path;
static const char* leandvb_file;
static const char* leandvb_path;
static       float lnb_lo;
static       bool  maxsens;
static const char* modcods;
static       int   nhelpers;
static       int   ppm;
static       float rolloff;
static       float rrcrej;
static       int   rtldongle;
static const char* rtlsdr_file;
static const char* rtlsdr_path;
static const char* sampler;
static const char* standard;
static       bool  strongpls;
static       int   symbolrate;
static       int   tune;
static const char* viewer_file;
static const char* viewer_path;
static       bool  viterbi;

/*===== public variables ====================================================*/

/*===== private functions ===================================================*/

static int serializer_double(struct json_object* obj, struct printbuf* pb, int level, int flags)
{
    /* helper for formatting double */

    char* format;
    double value;

    format = json_object_get_userdata(obj);
    value  = json_object_get_double(obj); 	
	sprintbuf(pb, format, value);

	return 0;
}

static void param_from_default (void)
{
    /* load parameters from defaults */

    printf("load parameters from defaults\n");

    bandwidth       = PARAM_DEFAULT_BANDWIDTH;
    coderate        = PARAM_DEFAULT_CODERATE;
    constellation   = PARAM_DEFAULT_CONSTELLATION;
    debug           = PARAM_DEFAULT_DEBUG;
    fastdrift       = PARAM_DEFAULT_FASTDRIFT;
    fastlock        = PARAM_DEFAULT_FASTLOCK;
    fec             = PARAM_DEFAULT_FEC;
    framesizes      = PARAM_DEFAULT_FRAMESIZES;
    frequency       = PARAM_DEFAULT_FREQUENCY;
    gain            = PARAM_DEFAULT_GAIN;
    gui             = PARAM_DEFAULT_GUI;
    hardmetric      = PARAM_DEFAULT_HARDMETRIC;
    inpipe          = PARAM_DEFAULT_INPIPE;
    ldpcbf          = PARAM_DEFAULT_LDPCBF;
    ldpchelper_file = PARAM_DEFAULT_LDPCHELPER_FILE;
    ldpchelper_path = PARAM_DEFAULT_LDPCHELPER_PATH;
    leandvb_file    = PARAM_DEFAULT_LEANDVB_FILE;
    leandvb_path    = PARAM_DEFAULT_LEANDVB_PATH;
    lnb_lo          = PARAM_DEFAULT_LNB_LO;
    maxsens         = PARAM_DEFAULT_MAXSENS;
    modcods         = PARAM_DEFAULT_MODCODS;
    nhelpers        = PARAM_DEFAULT_NHELPERS;
    ppm             = PARAM_DEFAULT_PPM;
    rolloff         = PARAM_DEFAULT_ROLLOFF;
    rrcrej          = PARAM_DEFAULT_RRCREJ;
    rtldongle       = PARAM_DEFAULT_RTLDONGLE;
    rtlsdr_file     = PARAM_DEFAULT_RTLSDR_FILE;
    rtlsdr_path     = PARAM_DEFAULT_RTLSDR_PATH;
    sampler         = PARAM_DEFAULT_SAMPLER;
    standard        = PARAM_DEFAULT_STANDARD;
    strongpls       = PARAM_DEFAULT_STRONGPLS;
    symbolrate      = PARAM_DEFAULT_SYMBOLRATE;
    tune            = PARAM_DEFAULT_TUNE;
    viewer_file     = PARAM_DEFAULT_VIEWER_FILE;
    viewer_path     = PARAM_DEFAULT_VIEWER_PATH;
    viterbi         = PARAM_DEFAULT_VITERBI;
}

static int param_from_file (const char* file)
{
    /* load parameters from file */
    
    json_object* jobj;
    json_object* jitem;

    printf("load parameters from file %s\n", file);
    jobj = json_object_from_file(file);
    if (jobj == NULL)
    {
       /* failure while reading the file */
        return -1;
    }

    #define get_int(key,var)     json_object_object_get_ex(jobj,key,&jitem); \
                                 var = json_object_get_int(jitem)

    #define get_string(key,var)  json_object_object_get_ex(jobj,key,&jitem); \
                                 var = strdup(json_object_get_string(jitem))

    #define get_boolean(key,var) json_object_object_get_ex(jobj,key,&jitem); \
                                 var = json_object_get_boolean(jitem)

    #define get_double(key,var)  json_object_object_get_ex(jobj,key,&jitem); \
                                 var = json_object_get_double(jitem)

    get_int    ( "bandwidth",       bandwidth );
    get_string ( "coderate",        coderate );
    get_string ( "constellation",   constellation );
    get_string ( "debug",           debug );
    get_boolean( "fastdrift",       fastdrift );
    get_boolean( "fastlock",        fastlock );
    get_string ( "fec",             fec );
    get_string ( "framesizes",      framesizes );
    get_double ( "frequency",       frequency );
    get_int    ( "gain",            gain );
    get_boolean( "gui",             gui );
    get_boolean( "hardmetric",      hardmetric );
    get_int    ( "inpipe",          inpipe );
    get_int    ( "ldpcbf",          ldpcbf );
    get_string ( "ldpchelper_file", ldpchelper_file );
    get_string ( "ldpchelper_path", ldpchelper_path );
    get_string ( "leandvb_file",    leandvb_file );
    get_string ( "leandvb_path",    leandvb_path );
    get_double ( "lnb_lo",          lnb_lo );
    get_boolean( "maxsens",         maxsens );
    get_string ( "modcods",         modcods );
    get_int    ( "nhelpers",        nhelpers );
    get_int    ( "ppm",             ppm );
    get_double ( "rolloff",         rolloff );
    get_double ( "rrcrej",          rrcrej );
    get_int    ( "rtldongle",       rtldongle );
    get_string ( "rtlsdr_file",     rtlsdr_file );
    get_string ( "rtlsdr_path",     rtlsdr_path );
    get_string ( "sampler",         sampler );
    get_string ( "standard",        standard );
    get_boolean( "strongpls",       strongpls );
    get_int    ( "symbolrate",      symbolrate );
    get_int    ( "tune",            tune );
    get_string ( "viewer_file",     viewer_file );
    get_string ( "viewer_path",     viewer_path );
    get_boolean( "viterbi",         viterbi );

    #undef get_int
    #undef get_string
    #undef get_boolean
    #undef get_double

    /* destroy json object */
    json_object_put (jobj);

    return 0;
}

static void param_to_file (const char* file)
{
    /* save parameters to file */

    json_object* jobj;
    json_object* jitem;

    printf("save parameters to file %s\n", file);

    /* create new json object for parameters */
    jobj = json_object_new_object();

    /* add items to json object */

    #define add_int(key,val) jitem = json_object_new_int(val); \
                             json_object_object_add(jobj,key,jitem)

    #define add_string(key,val) jitem = json_object_new_string(val); \
                                json_object_object_add(jobj,key,jitem)

    #define add_boolean(key,val) jitem = json_object_new_boolean(val); \
                                 json_object_object_add(jobj,key,jitem)

    #define add_double(key,val,form) jitem = json_object_new_double(val); \
                                     json_object_set_serializer(jitem, serializer_double, form, NULL); \
                                     json_object_object_add(jobj,key,jitem)

    add_int    ( "bandwidth",       bandwidth );
    add_string ( "coderate",        coderate );
    add_string ( "constellation",   constellation );
    add_string ( "debug",           debug );
    add_boolean( "fastdrift",       fastdrift );
    add_boolean( "fastlock",        fastlock );
    add_string ( "fec",             fec );
    add_string ( "framesizes",      framesizes );
    add_double ( "frequency",       frequency, "%.3f" );
    add_int    ( "gain",            gain );
    add_boolean( "gui",             gui );
    add_boolean( "hardmetric",      hardmetric );
    add_int    ( "inpipe",          inpipe );
    add_int    ( "ldpcbf",          ldpcbf );
    add_string ( "ldpchelper_file", ldpchelper_file );
    add_string ( "ldpchelper_path", ldpchelper_path );
    add_string ( "leandvb_file",    leandvb_file );
    add_string ( "leandvb_path",    leandvb_path );
    add_double ( "lnb_lo",          lnb_lo, "%.3f" );
    add_boolean( "maxsens",         maxsens );
    add_string ( "modcods",         modcods );
    add_int    ( "nhelpers",        nhelpers );
    add_int    ( "ppm",             ppm );
    add_double ( "rolloff",         rolloff, "%.2f" );
    add_double ( "rrcrej",          rrcrej, "%.1f" );
    add_int    ( "rtldongle",       rtldongle );
    add_string ( "rtlsdr_file",     rtlsdr_file );
    add_string ( "rtlsdr_path",     rtlsdr_path );
    add_string ( "sampler",         sampler );
    add_string ( "standard",        standard );
    add_boolean( "strongpls",       strongpls );
    add_int    ( "symbolrate",      symbolrate );
    add_int    ( "tune",            tune );
    add_string ( "viewer_file",     viewer_file );
    add_string ( "viewer_path",     viewer_path );
    add_boolean( "viterbi",         viterbi );

    #undef add_int
    #undef add_string
    #undef add_boolean
    #undef add_double

    /* store json object */
    json_object_to_file_ext(file, jobj, JSON_C_TO_STRING_SPACED | JSON_C_TO_STRING_PRETTY | JSON_C_TO_STRING_NOSLASHESCAPE);

    /* destroy json object */
    json_object_put (jobj);
}

/*===== callback functions ==================================================*/

/*===== public functions ====================================================*/

void param_init (void)
{
    /* load parameters from file or defaults */
    if( param_from_file("parameters.json") < 0)
    {
        /* file loading faild */
        printf("failure loading from file\n");
        param_from_default();
    }
}

void param_deinit (void)
{
    /* save parameters to file */

    param_to_file("parameters.json");
}

void param_default_get (const char* key, void* val)
{
          float* p_float = val;
          int*   p_int   = val;
    const char** p_char  = val;
          bool*  p_bool  = val;

    if (strcmp("inpipe", key) == 0)
        *p_int = PARAM_DEFAULT_INPIPE;
    else if (strcmp("sampler", key) == 0)
        *p_char = PARAM_DEFAULT_SAMPLER;
    else if (strcmp("rolloff", key) == 0)
        *p_float = PARAM_DEFAULT_ROLLOFF;
    else if (strcmp("rrcrej", key) == 0)
        *p_float = PARAM_DEFAULT_RRCREJ;
    else if (strcmp("fastlock", key) == 0)
        *p_bool = PARAM_DEFAULT_FASTLOCK;
    else if (strcmp("maxsens", key) == 0)
        *p_bool = PARAM_DEFAULT_MAXSENS;
    else if (strcmp("debug", key) == 0)
        *p_char = PARAM_DEFAULT_DEBUG;
    else if (strcmp("gui", key) == 0)
        *p_bool = PARAM_DEFAULT_GUI;
    else if (strcmp("standard", key) == 0)
        *p_char = PARAM_DEFAULT_STANDARD;
    else if (strcmp("constellation", key) == 0)
        *p_char = PARAM_DEFAULT_CONSTELLATION;
    else if (strcmp("coderate", key) == 0)
        *p_char = PARAM_DEFAULT_CODERATE;
    else if (strcmp("viterbi", key) == 0)
        *p_bool = PARAM_DEFAULT_VITERBI;
    else if (strcmp("hardmetric", key) == 0)
        *p_bool = PARAM_DEFAULT_HARDMETRIC;
    else if (strcmp("strongpls", key) == 0)
        *p_bool = PARAM_DEFAULT_STRONGPLS;
    else if (strcmp("modcods", key) == 0)
        *p_char = PARAM_DEFAULT_MODCODS;
    else if (strcmp("framesizes", key) == 0)
        *p_char = PARAM_DEFAULT_FRAMESIZES;
    else if (strcmp("fastdrift", key) == 0)
        *p_bool = PARAM_DEFAULT_FASTDRIFT;
    else if (strcmp("ldpcbf", key) == 0)
        *p_int = PARAM_DEFAULT_LDPCBF;
    else if (strcmp("nhelpers", key) == 0)
        *p_int = PARAM_DEFAULT_NHELPERS;
    else if (strcmp("ppm", key) == 0)
        *p_int = PARAM_DEFAULT_PPM;
    else if (strcmp("gain", key) == 0)
        *p_int = PARAM_DEFAULT_GAIN;
    else if (strcmp("rtldongle", key) == 0)
        *p_int = PARAM_DEFAULT_RTLDONGLE;
    else if (strcmp("leandvb_path", key) == 0)
        *p_char = PARAM_DEFAULT_LEANDVB_PATH;
    else if (strcmp("leandvb_file", key) == 0)
        *p_char = PARAM_DEFAULT_LEANDVB_FILE;
    else if (strcmp("ldpchelper_path", key) == 0)
        *p_char = PARAM_DEFAULT_LDPCHELPER_PATH;
    else if (strcmp("ldpchelper_file", key) == 0)
        *p_char = PARAM_DEFAULT_LDPCHELPER_FILE;
    else if (strcmp("rtlsdr_path", key) == 0)
        *p_char = PARAM_DEFAULT_RTLSDR_PATH;
    else if (strcmp("rtlsdr_file", key) == 0)
        *p_char = PARAM_DEFAULT_RTLSDR_FILE;
    else if (strcmp("viewer_path", key) == 0)
        *p_char = PARAM_DEFAULT_VIEWER_PATH;
    else if (strcmp("viewer_file", key) == 0)
        *p_char = PARAM_DEFAULT_VIEWER_FILE;
}

void param_get (const char* key, void* val)
{
          float* p_float = val;
          int*   p_int   = val;
    const char** p_char  = val;
          bool*  p_bool  = val;

    if (strcmp("frequency", key) == 0)
        *p_float = frequency;
    else if (strcmp("symbolrate", key) == 0)
        *p_int = symbolrate;
    else if (strcmp("bandwidth", key) == 0)
        *p_int = bandwidth;
    else if (strcmp("tune", key) == 0)
        *p_int = tune;
    else if (strcmp("lnb_lo", key) == 0)
        *p_float = lnb_lo;
    else if (strcmp("fec", key) == 0)
        *p_char = fec;
    else if (strcmp("inpipe", key) == 0)
        *p_int = inpipe;
    else if (strcmp("sampler", key) == 0)
        *p_char = sampler;
    else if (strcmp("rolloff", key) == 0)
        *p_float = rolloff;
    else if (strcmp("rrcrej", key) == 0)
        *p_float = rrcrej;
    else if (strcmp("fastlock", key) == 0)
        *p_bool = fastlock;
    else if (strcmp("maxsens", key) == 0)
        *p_bool = maxsens;
    else if (strcmp("debug", key) == 0)
        *p_char = debug;
    else if (strcmp("gui", key) == 0)
        *p_bool = gui;
    else if (strcmp("standard", key) == 0)
        *p_char = standard;
    else if (strcmp("constellation", key) == 0)
        *p_char = constellation;
    else if (strcmp("coderate", key) == 0)
        *p_char = coderate;
    else if (strcmp("viterbi", key) == 0)
        *p_bool = viterbi;
    else if (strcmp("hardmetric", key) == 0)
        *p_bool = hardmetric;
    else if (strcmp("strongpls", key) == 0)
        *p_bool = strongpls;
    else if (strcmp("modcods", key) == 0)
        *p_char = modcods;
    else if (strcmp("framesizes", key) == 0)
        *p_char = framesizes;
    else if (strcmp("fastdrift", key) == 0)
        *p_bool = fastdrift;
    else if (strcmp("ldpcbf", key) == 0)
        *p_int = ldpcbf;
    else if (strcmp("nhelpers", key) == 0)
        *p_int = nhelpers;
    else if (strcmp("ppm", key) == 0)
        *p_int = ppm;
    else if (strcmp("gain", key) == 0)
        *p_int = gain;
    else if (strcmp("rtldongle", key) == 0)
        *p_int = rtldongle;
    else if (strcmp("leandvb_path", key) == 0)
        *p_char = leandvb_path;
    else if (strcmp("leandvb_file", key) == 0)
        *p_char = leandvb_file;
    else if (strcmp("ldpchelper_path", key) == 0)
        *p_char = ldpchelper_path;
    else if (strcmp("ldpchelper_file", key) == 0)
        *p_char = ldpchelper_file;
    else if (strcmp("rtlsdr_path", key) == 0)
        *p_char = rtlsdr_path;
    else if (strcmp("rtlsdr_file", key) == 0)
        *p_char = rtlsdr_file;
    else if (strcmp("viewer_path", key) == 0)
        *p_char = viewer_path;
    else if (strcmp("viewer_file", key) == 0)
        *p_char = viewer_file;
}

void param_set (const char* key, void* val)
{
          float* p_float = val;
          int*   p_int   = val;
    const char** p_char  = val;
          bool*  p_bool  = val;

    if (strcmp("frequency", key) == 0)
        frequency = *p_float;
    else if (strcmp("symbolrate", key) == 0)
        symbolrate = *p_int; 
    else if (strcmp("bandwidth", key) == 0)
        bandwidth = *p_int;
    else if (strcmp("tune", key) == 0)
        tune = *p_int;
    else if (strcmp("lnb_lo", key) == 0)
        lnb_lo = *p_float;
    else if (strcmp("fec", key) == 0)
        fec = strdup(*p_char);
    else if (strcmp("inpipe", key) == 0)
        inpipe = *p_int;
    else if (strcmp("sampler", key) == 0)
        sampler = strdup(*p_char);
    else if (strcmp("rolloff", key) == 0)
        rolloff = *p_float;
    else if (strcmp("rrcrej", key) == 0)
        rrcrej = *p_float;
    else if (strcmp("fastlock", key) == 0)
        fastlock = *p_bool;
    else if (strcmp("maxsens", key) == 0)
        maxsens = *p_bool;
    else if (strcmp("debug", key) == 0)
        debug = strdup(*p_char);
    else if (strcmp("gui", key) == 0)
        gui = *p_bool;
    else if (strcmp("standard", key) == 0)
        standard = strdup(*p_char);
    else if (strcmp("constellation", key) == 0)
        constellation = strdup(*p_char);
    else if (strcmp("coderate", key) == 0)
        coderate = strdup(*p_char);
    else if (strcmp("viterbi", key) == 0)
        viterbi = *p_bool;
    else if (strcmp("hardmetric", key) == 0)
        hardmetric = *p_bool;
    else if (strcmp("strongpls", key) == 0)
        strongpls = *p_bool;
    else if (strcmp("modcods", key) == 0)
        modcods = strdup(*p_char);
    else if (strcmp("framesizes", key) == 0)
        framesizes = strdup(*p_char);
    else if (strcmp("fastdrift", key) == 0)
        fastdrift = *p_bool;
    else if (strcmp("ldpcbf", key) == 0)
        ldpcbf = *p_int;
    else if (strcmp("nhelpers", key) == 0)
        nhelpers = *p_int;
    else if (strcmp("ppm", key) == 0)
        ppm = *p_int;
    else if (strcmp("gain", key) == 0)
        gain = *p_int;
    else if (strcmp("rtldongle", key) == 0)
        rtldongle = *p_int;
    else if (strcmp("leandvb_path", key) == 0)
        leandvb_path = strdup(*p_char);
    else if (strcmp("leandvb_file", key) == 0)
        leandvb_file = strdup(*p_char);
    else if (strcmp("ldpchelper_path", key) == 0)
        ldpchelper_path = strdup(*p_char);
    else if (strcmp("ldpchelper_file", key) == 0)
        ldpchelper_file = strdup(*p_char);
    else if (strcmp("rtlsdr_path", key) == 0)
        rtlsdr_path = strdup(*p_char);
    else if (strcmp("rtlsdr_file", key) == 0)
        rtlsdr_file = strdup(*p_char);
    else if (strcmp("viewer_path", key) == 0)
        viewer_path = strdup(*p_char);
    else if (strcmp("viewer_file", key) == 0)
        viewer_file = strdup(*p_char);
}


