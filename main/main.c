/*===== file header =========================================================*/

/*===== includes ============================================================*/

#include <gtk/gtk.h>
#include "gui.h"
#include "parameters.h"
#include <locale.h>

/*===== private datatypes ===================================================*/

/*===== private symbols =====================================================*/

/*===== private constants ===================================================*/

/*===== public constants ====================================================*/

/*===== private variables ===================================================*/

/*===== public variables ====================================================*/

/*===== private functions ===================================================*/

/*===== callback functions ==================================================*/

/*===== public functions ====================================================*/

int main (int argc, char *argv[])
{
    gtk_init (&argc, &argv);
    setlocale(LC_ALL, "en_US.UTF-8");
    param_init("parameters.json");
    gui_init ();
    gtk_main ();
    param_deinit();

  return 0;
}


