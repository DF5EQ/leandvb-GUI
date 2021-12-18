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
    const char* param_file;

    gtk_init (&argc, &argv);
    setlocale(LC_ALL, "en_US.UTF-8");

    if (argc > 1)
    {
        param_file = argv[1];
    }
    else
    {
        param_file = "parameters.json";
    }
    param_init(param_file);

    gui_init ();
    gtk_main ();

    param_deinit();

  return 0;
}


