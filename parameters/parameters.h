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

void param_init        (void);
void param_deinit      (void);
void param_default_get (const char* key, void* val);
void param_get         (const char* key, void* val);
void param_set         (const char* key, void* val);

#endif
