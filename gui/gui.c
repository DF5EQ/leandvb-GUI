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

static GtkBuilder*     builder;
static GtkCssProvider* css_provider;

/* exposed widgets */
static GtkWidget* window;
static GtkDialog* settings_dialog;

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
	/* show the settings dialog and wait for closing */
    gtk_dialog_run (settings_dialog);

    /* hide the settingsdialog after it's closing */
    gtk_widget_hide (GTK_WIDGET(settings_dialog));
}

/*===== public functions ====================================================*/

void gui_init (void)
{
    /* load gui elements */
    builder = gtk_builder_new();
    gtk_builder_add_from_file (builder, "gui/gui.ui", NULL);
//    gtk_builder_add_from_string (builder, gui, -1, NULL);

    /* load gui theme */
    css_provider = gtk_css_provider_new(); 
    gtk_css_provider_load_from_path (css_provider, "gui/gui.css", NULL);
    gtk_style_context_add_provider_for_screen (gdk_screen_get_default(), GTK_STYLE_PROVIDER(css_provider), GTK_STYLE_PROVIDER_PRIORITY_USER);

    /* expose needed widgets */
    window          = GTK_WIDGET (gtk_builder_get_object (builder, "main_window"));
    settings_dialog = GTK_DIALOG (gtk_builder_get_object (builder, "settings_dialog"));

    /* connect the signals */
    gtk_builder_connect_signals(builder, NULL);
 
    /* builder not longer needed */ 
    g_object_unref(builder);
 
    /* start the gui */
    gtk_widget_show(window);                
 }

