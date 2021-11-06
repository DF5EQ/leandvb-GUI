/*===== file header =========================================================*/

/*===== includes ============================================================*/

#include <gtk/gtk.h>
#include <stdio.h>
#include "gui.uih"

/*===== private datatypes ===================================================*/

/*===== private symbols =====================================================*/

/*===== private constants ===================================================*/

/*===== public constants ====================================================*/

/*===== private variables ===================================================*/

static GtkBuilder*      builder;
static GtkCssProvider*  css_provider;
static GtkWidget*       window;
static GtkComboBoxText* fec_combobox;
static GtkEntry*        lnblo_entry;

/* data for entries */
static gfloat lnblo_value         = 0.0;
static gfloat lnblo_value_default = 9750.000;
static gchar  lnblo_string[11]    = "";

/* data for comboboxes */
static gchar* fec_list[]       = { "1/2", "2/3", "3/4", "4/5", "5/6", "6/7", "7/8" };
static gint   fec_list_default = 3;

/*===== public variables ====================================================*/

/*===== private functions ===================================================*/

/*===== callback functions ==================================================*/

void main_window_destroy_cb (GtkWidget* widget, gpointer data)
{
	gtk_main_quit();
}

void button_start_clicked_cb (GtkWidget* widget, gpointer data)
{
	gtk_main_quit();
}

void button_stop_clicked_cb (GtkWidget* widget, gpointer data)
{
	gtk_main_quit();
}

void button_settings_clicked_cb (GtkWidget* widget, gpointer data)
{
	gtk_main_quit();
}

/*===== public functions ====================================================*/

void gui_init (void)
{
    int i;

    /* load gui elements */
    builder = gtk_builder_new();
    gtk_builder_add_from_file (builder, "gui/gui.ui", NULL);
//    gtk_builder_add_from_string (builder, gui, -1, NULL);

    /* load gui theme */
    css_provider = gtk_css_provider_new(); 
    gtk_css_provider_load_from_path (css_provider, "gui/gui.css", NULL);
    gtk_style_context_add_provider_for_screen (gdk_screen_get_default(), GTK_STYLE_PROVIDER(css_provider), GTK_STYLE_PROVIDER_PRIORITY_USER);

    /* expose needed widgets */
    window       = GTK_WIDGET         (gtk_builder_get_object (builder, "main_window") );
    fec_combobox = GTK_COMBO_BOX_TEXT (gtk_builder_get_object (builder, "fec_combobox"));
    lnblo_entry  = GTK_ENTRY          (gtk_builder_get_object (builder, "lnblo_entry") );
    
    /* populate entries */
    sprintf (lnblo_string, "%6.3f", lnblo_value_default);
    gtk_entry_set_text (lnblo_entry, lnblo_string);

    /* populate comboboxes */
    for( i=0; i<sizeof(fec_list)/sizeof(gchar*); i++ )
    {
        gtk_combo_box_text_append_text (fec_combobox, fec_list[i]);
    }
    gtk_combo_box_set_active ((GtkComboBox*)fec_combobox, fec_list_default);

    gtk_builder_connect_signals(builder, NULL);
 
    g_object_unref(builder);
 
    gtk_widget_show(window);                
 }

