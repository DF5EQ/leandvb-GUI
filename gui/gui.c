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
static GtkComboBoxText* tune_combobox;

/* data for entries */
static gchar* lnblo_value         = "9750.000";
static gchar* lnblo_value_default = "9750.000";

/* data for comboboxes */
static gchar* fec_list[]           = { "1/2", "2/3", "3/4", "4/5", "5/6", "6/7", "7/8" };
static gint   fec_list_default     = 3;
static gchar* tune_list[]          = { "10000", "5000", "2000", "1000", "500", "100", "0", "-100", "-500", "-1000", "-2000", "-5000", "-10000" };
static gint   tune_list_default    = 6;

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
    window        = GTK_WIDGET         (gtk_builder_get_object (builder, "main_window")  );
    fec_combobox  = GTK_COMBO_BOX_TEXT (gtk_builder_get_object (builder, "fec_combobox") );
    lnblo_entry   = GTK_ENTRY          (gtk_builder_get_object (builder, "lnblo_entry")  );
    tune_combobox = GTK_COMBO_BOX_TEXT (gtk_builder_get_object (builder, "tune_combobox"));
    
    /* populate lnblo entry */
    gtk_entry_set_text (lnblo_entry, lnblo_value_default);

    /* populate fec combobox */
    for( i=0; i<sizeof(fec_list)/sizeof(fec_list[0]); i++ )
    {
        gtk_combo_box_text_append_text (fec_combobox, fec_list[i]);
    }
    gtk_combo_box_set_active ((GtkComboBox*)fec_combobox, fec_list_default);

    /* populate tune combobox */
    for( i=0; i<sizeof(tune_list)/sizeof(tune_list[0]); i++ )
    {
        gtk_combo_box_text_append_text (tune_combobox, tune_list[i]);
    }
    gtk_combo_box_set_active ((GtkComboBox*)tune_combobox, tune_list_default);

    /* connect the signals */
    gtk_builder_connect_signals(builder, NULL);
 
    /* builder not needed any longer */
    g_object_unref(builder);
 
    /* start the gui */
    gtk_widget_show(window);                
 }

