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
static GtkWidget*      window;
static GtkEntry*       entry;

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
    /* load gui elements */
    builder = gtk_builder_new();
    gtk_builder_add_from_file (builder, "gui/gui.ui", NULL);
//    gtk_builder_add_from_string (builder, gui, -1, NULL);

    /* load gui theme */
    css_provider = gtk_css_provider_new(); 
    gtk_css_provider_load_from_path (css_provider, "gui/gui.css", NULL);
    gtk_style_context_add_provider_for_screen (gdk_screen_get_default(), GTK_STYLE_PROVIDER(css_provider), GTK_STYLE_PROVIDER_PRIORITY_USER);

    /* expose needed widgets */
    window = GTK_WIDGET (gtk_builder_get_object (builder, "main_window"));
    entry  = GTK_ENTRY  (gtk_builder_get_object (builder, "entry_show" ));

    gtk_builder_connect_signals(builder, NULL);
 
    g_object_unref(builder);
 
    gtk_widget_show(window);                
 }

