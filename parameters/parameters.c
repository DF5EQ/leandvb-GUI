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

static void parameters_print_int (const char* key)
{
    int val;

    printf("%-15s: ", key);

    if( 0 > parameters_get_int(key, &val))
    {
        printf("<undefined>\n");
    }
    else
    {
        printf("%d\n", val);
    }
}

static void parameters_print_bool (const char* key)
{
    bool val;

    printf("%-15s: ", key);

    if( 0 > parameters_get_bool(key, &val))
    {
        printf("<undefined>\n");
    }
    else
    {
        printf("%s\n", val?"true":"false");
    }
}

static void parameters_print_string (const char* key)
{
    const char* val;

    printf("%-15s: ", key);

    if( 0 > parameters_get_string(key, &val))
    {
        printf("<undefined>\n");
    }
    else
    {
        printf("%s\n", val);
    }
}

static void parameters_print_float (const char* key, const char* format)
{
    float val;

    printf("%-15s: ", key);

    if( 0 > parameters_get_float(key, &val))
    {
        printf("<undefined>\n");
    }
    else
    {
        printf(format, val);
        printf("\n");
    }
}

/*===== callback functions ==================================================*/

/*===== public functions ====================================================*/

void parameters_default(void)
{
    /* load parameters with defaults */

    printf("load parameters with defaults\n");

    parameters_add_int    ("bandwidth", 2400);
    parameters_add_string ("constellation", "QPSK");
    parameters_add_string ("debug", "all");
    parameters_add_bool   ("fastdrift", false);
    parameters_add_bool   ("fastlock", false);
    parameters_add_string ("fec", "1/2");
    parameters_add_string ("framesizes", "0x01");
    parameters_add_float  ("frequency", 10491.500, "%.3f");
    parameters_add_int    ("gain", 36);
    parameters_add_bool   ("gui", true);
    parameters_add_bool   ("hardmetric", false);
    parameters_add_int    ("inpipe", 32000000);
    parameters_add_int    ("ldpc_bf", 0);
    parameters_add_string ("ldpchelper_file", "ldpc_tool");
    parameters_add_string ("ldpchelper_path", "./");
    parameters_add_string ("leandvb_file", "leandvb");
    parameters_add_string ("leandvb_path", "./");
    parameters_add_float  ("lnb_lo", 9750.000, "%.3f");
    parameters_add_bool   ("maxsens", false);
    parameters_add_string ("modcods", "0x0040");
    parameters_add_int    ("nhelpers", 6);
    parameters_add_int    ("ppm", 0);
    parameters_add_float  ("rolloff", 0.35, "%.2f");
    parameters_add_float  ("rrcrej", 30.0, "%.1f");
    parameters_add_int    ("rtldongle", 0);
    parameters_add_string ("rtlsdr_file", "rtl_sdr");
    parameters_add_string ("rtlsdr_path", "");
    parameters_add_string ("sampler", "rrc");
    parameters_add_string ("standard", "DVB-S2");
    parameters_add_bool   ("strongpls", false);
    parameters_add_int    ("symbolrate", 1500);
    parameters_add_int    ("tune", 0);
    parameters_add_string ("viewer_file", "ffplay -v 0");
    parameters_add_string ("viewer_path", "");
    parameters_add_bool   ("viterbi", false);
}

void parameters_print (void)
{
    /* print parameters to console */

    printf("print parameters\n");

    parameters_print_int    ("bandwidth");
    parameters_print_string ("constellation");
    parameters_print_string ("debug");
    parameters_print_bool   ("fastdrift");
    parameters_print_bool   ("fastlock");
    parameters_print_string ("fec");
    parameters_print_string ("framesizes");
    parameters_print_float  ("frequency","%.3f");
    parameters_print_int    ("gain");
    parameters_print_bool   ("gui");
    parameters_print_bool   ("hardmetric");
    parameters_print_int    ("inpipe");
    parameters_print_int    ("ldpc_bf");
    parameters_print_string ("ldpchelper_file");
    parameters_print_string ("ldpchelper_path");
    parameters_print_string ("leandvb_file");
    parameters_print_string ("leandvb_path");
    parameters_print_float  ("lnb_lo","%.3f");
    parameters_print_bool   ("maxsens");
    parameters_print_string ("modcods");
    parameters_print_int    ("nhelpers");
    parameters_print_int    ("ppm");
    parameters_print_float  ("rolloff","%.2f");
    parameters_print_float  ("rrcrej","%.1f");
    parameters_print_int    ("rtldongle");
    parameters_print_string ("rtlsdr_file");
    parameters_print_string ("rtlsdr_path");
    parameters_print_string ("sampler");
    parameters_print_string ("standard");
    parameters_print_bool   ("strongpls");
    parameters_print_int    ("symbolrate");
    parameters_print_int    ("tune");
    parameters_print_string ("viewer_file");
    parameters_print_string ("viewer_path");
    parameters_print_bool   ("viterbi");
}

void parameters_save (void)
{
    /* save parameters to file */

    printf("save parameters to file %s\n", parameters_file_name);
    json_object_to_file_ext(parameters_file_name, parameters_json_object, JSON_C_TO_STRING_SPACED | JSON_C_TO_STRING_PRETTY | JSON_C_TO_STRING_NOSLASHESCAPE);
}

void parameters_load (void)
{
    /* load parameters from file */

    printf("load parameters from file %s\n", parameters_file_name);
    parameters_json_object = json_object_from_file(parameters_file_name);
}

int parameters_get_int (const char* key, int* const val)
{
    struct json_object* jobj;
    enum   json_type    jtyp;
    bool                ret;

    ret = json_object_object_get_ex(parameters_json_object, key, &jobj);
    if (ret == false) return -1;

    jtyp = json_object_get_type(jobj);
    if (jtyp != json_type_int) return -2;

    *val = json_object_get_int(jobj);

    return 0;
}

int parameters_get_float (const char* key, float* const val)
{
    struct json_object* jobj;
    enum   json_type    jtyp;
    bool                ret;

    ret = json_object_object_get_ex(parameters_json_object, key, &jobj);
    if (ret == false) return -1;

    jtyp = json_object_get_type(jobj);
    if (jtyp != json_type_double) return -2;

    *val = json_object_get_double(jobj);

    return 0;
}

int parameters_get_bool (const char* key, bool* const val)
{
    struct json_object* jobj;
    enum   json_type    jtyp;
    bool                ret;

    ret = json_object_object_get_ex(parameters_json_object, key, &jobj);
    if (ret == false) return -1;

    jtyp = json_object_get_type(jobj);
    if (jtyp != json_type_boolean) return -2;

    *val = json_object_get_boolean(jobj);

    return 0;
}

int parameters_get_string (const char* key, const char** val)
{
    struct json_object* jobj;
    enum   json_type    jtyp;
    bool                ret;

    ret = json_object_object_get_ex(parameters_json_object, key, &jobj);
    if (ret == false) return -1;

    jtyp = json_object_get_type(jobj);
    if (jtyp != json_type_string) return -2;

    *val = json_object_get_string(jobj);

    return 0;
}

int parameters_set_int (const char* key, const int val)
{
    struct json_object* jobj;
    enum   json_type    jtyp;
    bool                ret;

    ret = json_object_object_get_ex(parameters_json_object, key, &jobj);
    if (ret == false) return -1;

    jtyp = json_object_get_type(jobj);
    if (jtyp != json_type_int) return -2;

    ret = json_object_set_int(jobj, val);
    if (ret == false) return -3;

    return 0;
}

int parameters_set_float (const char* key, const float val)
{
    struct json_object* jobj;
    enum   json_type    jtyp;
    bool                ret;

    ret = json_object_object_get_ex(parameters_json_object, key, &jobj);
    if (ret == false) return -1;

    jtyp = json_object_get_type(jobj);
    if (jtyp != json_type_double) return -2;

    ret = json_object_set_double(jobj, val);
    if (ret == false) return -3;

    return 0;
}

int parameters_set_bool (const char* key, const bool val)
{
    struct json_object* jobj;
    enum   json_type    jtyp;
    bool                ret;

    ret = json_object_object_get_ex(parameters_json_object, key, &jobj);
    if (ret == false) return -1;

    jtyp = json_object_get_type(jobj);
    if (jtyp != json_type_boolean) return -2;

    ret = json_object_set_boolean(jobj, val);
    if (ret == false) return -3;

    return 0;
}

int parameters_set_string (const char* key, const char* val)
{
    struct json_object* jobj;
    enum   json_type    jtyp;
    bool                ret;

    ret = json_object_object_get_ex(parameters_json_object, key, &jobj);
    if (ret == false) return -1;

    jtyp = json_object_get_type(jobj);
    if (jtyp != json_type_string) return -2;

    ret = json_object_set_string(jobj, val);
    if (ret == false) return -3;

    return 0;
}

int parameters_add_int (const char* key, const int val)
{
    struct json_object* jobj;
    int                 ret;

    jobj = json_object_new_int(val);
    if (jobj == NULL) return -1;

    ret = json_object_object_add(parameters_json_object, key, jobj);
    if (ret < 0) return -2;

    return 0;
}

int parameters_add_float (const char* key, const float val, char* format)
{
    struct json_object* jobj;
    int                 ret;

    jobj = json_object_new_double(val);
    if (jobj == NULL) return -1;

    json_object_set_serializer(jobj, serializer_double, format, NULL);

    ret = json_object_object_add(parameters_json_object, key, jobj);
    if (ret < 0) return -2;

    return 0;
}

int parameters_add_bool (const char* key, const bool val)
{
    struct json_object* jobj;
    int                 ret;

    jobj = json_object_new_boolean(val);
    if (jobj == NULL) return -1;

    ret = json_object_object_add(parameters_json_object, key, jobj);
    if (ret < 0) return -2;

    return 0;
}

int parameters_add_string (const char* key, const char* val)
{
    struct json_object* jobj;
    int                 ret;

    jobj = json_object_new_string(val);
    if (jobj == NULL) return -1;

    ret = json_object_object_add(parameters_json_object, key, jobj);
    if (ret < 0) return -2;

    return 0;
}

void parameters_init (void)
{
    /* create new json_object for parameters */
    parameters_json_object = json_object_new_object();

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

    /*--- for test ---*/

    parameters_print();
    parameters_save();
    exit(0);

}

void parameters_deinit (void)
{
    /* save parameters to file */

    parameters_save();
}

