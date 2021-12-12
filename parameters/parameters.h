#ifndef PARAMETERS_H
#define PARAMETERS_H

/*===== file header =========================================================*/

/*===== includes ============================================================*/

#include <stdint.h>
#include <stdbool.h>

/*===== public datatypes ====================================================*/

/*===== public symbols ======================================================*/

/*===== public constants ====================================================*/

/*===== public variables ====================================================*/

/*===== public functions ====================================================*/

void parameters_init    (void);
void parameters_deinit  (void);
void parameters_print   (void);
void parameters_default (void);
void parameters_load    (void);
void parameters_save    (void);

int parameters_get_int    (const char* key, int*   const  val);
int parameters_get_float  (const char* key, float* const  val);
int parameters_get_bool   (const char* key, bool*  const  val);
int parameters_get_string (const char* key, const  char** val);

int parameters_set_int    (const char* key, const int   val);
int parameters_set_float  (const char* key, const float val, char* format);
int parameters_set_bool   (const char* key, const bool  val);
int parameters_set_string (const char* key, const char* val);

int parameters_add_int    (const char* key, const int   val);
int parameters_add_float  (const char* key, const float val, char* format);
int parameters_add_bool   (const char* key, const bool  val);
int parameters_add_string (const char* key, const char* val);

#endif
