/*===== file header =========================================================*/

/*===== includes ============================================================*/

#include <gtk/gtk.h>
#include <stdio.h>
#include "gui.uih"
#include "parameters.h"

/*===== private datatypes ===================================================*/

/*===== private symbols =====================================================*/

/*===== private constants ===================================================*/

/*===== public constants ====================================================*/

/*===== private variables ===================================================*/

static GtkBuilder*     builder;
static GtkCssProvider* css_provider;

/*----- exposed widgets -----*/

/*-- main window --*/
static GtkWidget* window;
static GtkEntry*  fec_entry;
static GtkEntry*  lnblo_entry;
static GtkEntry*  tune_entry;
static GtkEntry*  bandwidth_entry;
static GtkEntry*  symbolrate_entry;
static GtkEntry*  frequency_entry;

/*-- settings dialog --*/
static GtkDialog* settings_dialog;

/* settings DVB-S */
static GtkLabel*        constellation_label;
static GtkComboBoxText* constellation_combobox;
static GtkLabel*        coderate_label;
static GtkComboBoxText* coderate_combobox;
static GtkLabel*        viterbi_label;
static GtkSwitch*       viterbi_switch;
static GtkLabel*        hardmetric_label;
static GtkSwitch*       hardmetric_switch;

/* settings DVB-S2 */
static GtkLabel*      strongpls_label;
static GtkSwitch*     strongpls_switch;
static GtkLabel*      modcods_label;
static GtkEntry*      modcods_entry;
static GtkLabel*      framesizes_label;
static GtkEntry*      framesizes_entry;
static GtkLabel*      fastdrift_label;
static GtkSwitch*     fastdrift_switch;
static GtkLabel*      ldpcbf_label;
static GtkSpinButton* ldpcbf_spinbutton;
static GtkLabel*      nhelpers_label;
static GtkSpinButton* nhelpers_spinbutton;

/*===== public variables ====================================================*/

/*===== private functions ===================================================*/

static void parameters_to_gui (void)
{
    const char* s;
    int         i;
    float       f;
    bool        b;
    char      buf[20];

    parameters_get_string ("fec", &s);
    snprintf (buf,sizeof(buf), "%s", s);
    gtk_entry_set_text ((GtkEntry*)fec_entry, buf);

    parameters_get_float ("lnb_lo", &f);
    snprintf (buf,sizeof(buf), "%.3f", f);
    gtk_entry_set_text ((GtkEntry*)lnblo_entry, buf);

    parameters_get_int ("tune", &i);
    snprintf (buf,sizeof(buf), "%d", i);
    gtk_entry_set_text ((GtkEntry*)tune_entry, buf);

    parameters_get_int ("bandwidth", &i);
    snprintf (buf,sizeof(buf), "%d", i);
    gtk_entry_set_text ((GtkEntry*)bandwidth_entry, buf);

    parameters_get_int ("symbolrate", &i);
    snprintf (buf,sizeof(buf), "%d", i);
    gtk_entry_set_text ((GtkEntry*)symbolrate_entry, buf);

    parameters_get_float ("frequency", &f);
    snprintf (buf,sizeof(buf), "%.3f", f);
    gtk_entry_set_text ((GtkEntry*)frequency_entry, buf);
}

/*===== callback functions ==================================================*/

/*----- main window -----*/

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

void fec_combobox_changed_cb (GtkComboBox *widget, gpointer user_data)
{
    gchar* text;

    text = gtk_combo_box_text_get_active_text (GTK_COMBO_BOX_TEXT(widget));
    printf("fec changed to %s\n", text);
}

/*----- settings  files -----*/

gboolean leandvb_filechooser_query_tooltip_cb (GtkWidget* widget, gint x,  gint y, gboolean keyboard_mode, GtkTooltip* tooltip, gpointer user_data)
{
    gchar* filename;

    filename = gtk_file_chooser_get_filename (GTK_FILE_CHOOSER(widget));
    gtk_tooltip_set_text (tooltip, filename);
    return TRUE;
}

gboolean ldpchelper_filechooser_query_tooltip_cb (GtkWidget* widget, gint x,  gint y, gboolean keyboard_mode, GtkTooltip* tooltip, gpointer user_data)
{
    gchar* filename;

    filename = gtk_file_chooser_get_filename (GTK_FILE_CHOOSER(widget));
    gtk_tooltip_set_text (tooltip, filename);
    return TRUE;
}

gboolean rtlsdr_filechooser_query_tooltip_cb (GtkWidget* widget, gint x,  gint y, gboolean keyboard_mode, GtkTooltip* tooltip, gpointer user_data)
{
    gchar* filename;

    filename = gtk_file_chooser_get_filename (GTK_FILE_CHOOSER(widget));
    gtk_tooltip_set_text (tooltip, filename);
    return TRUE;
}

gboolean viewer_filechooser_query_tooltip_cb (GtkWidget* widget, gint x,  gint y, gboolean keyboard_mode, GtkTooltip* tooltip, gpointer user_data)
{
    gchar* filename;

    filename = gtk_file_chooser_get_filename (GTK_FILE_CHOOSER(widget));
    gtk_tooltip_set_text (tooltip, filename);
    return TRUE;
}

/*----- settings leandvb -----*/

void standard_combobox_changed_cb (GtkComboBox *widget, gpointer user_data)
{
    gchar* text;

    text = gtk_combo_box_text_get_active_text (GTK_COMBO_BOX_TEXT(widget));

    if (strcmp(text,"DVB-S")==0)
    {
        gtk_widget_hide (GTK_WIDGET(strongpls_label));
        gtk_widget_hide (GTK_WIDGET(strongpls_switch));
        gtk_widget_hide (GTK_WIDGET(modcods_label));
        gtk_widget_hide (GTK_WIDGET(modcods_entry));
        gtk_widget_hide (GTK_WIDGET(framesizes_label));
        gtk_widget_hide (GTK_WIDGET(framesizes_entry));
        gtk_widget_hide (GTK_WIDGET(fastdrift_label));
        gtk_widget_hide (GTK_WIDGET(fastdrift_switch));
        gtk_widget_hide (GTK_WIDGET(ldpcbf_label));
        gtk_widget_hide (GTK_WIDGET(ldpcbf_spinbutton));
        gtk_widget_hide (GTK_WIDGET(nhelpers_label));
        gtk_widget_hide (GTK_WIDGET(nhelpers_spinbutton));

        gtk_widget_show (GTK_WIDGET(constellation_label));
        gtk_widget_show (GTK_WIDGET(constellation_combobox));
        gtk_widget_show (GTK_WIDGET(coderate_label));
        gtk_widget_show (GTK_WIDGET(coderate_combobox));
        gtk_widget_show (GTK_WIDGET(viterbi_label));
        gtk_widget_show (GTK_WIDGET(viterbi_switch));
        gtk_widget_show (GTK_WIDGET(hardmetric_label));
        gtk_widget_show (GTK_WIDGET(hardmetric_switch));
    }

    if (strcmp(text,"DVB-S2")==0)
    {
        gtk_widget_hide (GTK_WIDGET(constellation_label));
        gtk_widget_hide (GTK_WIDGET(constellation_combobox));
        gtk_widget_hide (GTK_WIDGET(coderate_label));
        gtk_widget_hide (GTK_WIDGET(coderate_combobox));
        gtk_widget_hide (GTK_WIDGET(viterbi_label));
        gtk_widget_hide (GTK_WIDGET(viterbi_switch));
        gtk_widget_hide (GTK_WIDGET(hardmetric_label));
        gtk_widget_hide (GTK_WIDGET(hardmetric_switch));

        gtk_widget_show (GTK_WIDGET(strongpls_label));
        gtk_widget_show (GTK_WIDGET(strongpls_switch));
        gtk_widget_show (GTK_WIDGET(modcods_label));
        gtk_widget_show (GTK_WIDGET(modcods_entry));
        gtk_widget_show (GTK_WIDGET(framesizes_label));
        gtk_widget_show (GTK_WIDGET(framesizes_entry));
        gtk_widget_show (GTK_WIDGET(fastdrift_label));
        gtk_widget_show (GTK_WIDGET(fastdrift_switch));
        gtk_widget_show (GTK_WIDGET(ldpcbf_label));
        gtk_widget_show (GTK_WIDGET(ldpcbf_spinbutton));
        gtk_widget_show (GTK_WIDGET(nhelpers_label));
        gtk_widget_show (GTK_WIDGET(nhelpers_spinbutton));
    }
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

    /*--- expose needed widgets ---*/

    /* main window */
    window           = GTK_WIDGET (gtk_builder_get_object (builder, "main_window"));
    fec_entry        = GTK_ENTRY  (gtk_builder_get_object (builder, "fec_entry"));
    lnblo_entry      = GTK_ENTRY  (gtk_builder_get_object (builder, "lnblo_entry"));
    tune_entry       = GTK_ENTRY  (gtk_builder_get_object (builder, "tune_entry"));
    bandwidth_entry  = GTK_ENTRY  (gtk_builder_get_object (builder, "bandwidth_entry"));
    symbolrate_entry = GTK_ENTRY  (gtk_builder_get_object (builder, "symbolrate_entry"));
    frequency_entry  = GTK_ENTRY  (gtk_builder_get_object (builder, "symbolrate_entry"));

    /* settings dialog */
    settings_dialog     = GTK_DIALOG (gtk_builder_get_object (builder, "settings_dialog"));

        /* settings DVB-S */
        constellation_label    = GTK_LABEL          (gtk_builder_get_object (builder, "constellation_label"));
        constellation_combobox = GTK_COMBO_BOX_TEXT (gtk_builder_get_object (builder, "constellation_combobox"));
        coderate_label         = GTK_LABEL          (gtk_builder_get_object (builder, "coderate_label"));
        coderate_combobox      = GTK_COMBO_BOX_TEXT (gtk_builder_get_object (builder, "coderate_combobox"));
        viterbi_label          = GTK_LABEL          (gtk_builder_get_object (builder, "viterbi_label"));
        viterbi_switch         = GTK_SWITCH         (gtk_builder_get_object (builder, "viterbi_switch"));
        hardmetric_label       = GTK_LABEL          (gtk_builder_get_object (builder, "hardmetric_label"));
        hardmetric_switch      = GTK_SWITCH         (gtk_builder_get_object (builder, "hardmetric_switch"));

        /* settings DVB-S2 */
        strongpls_label     = GTK_LABEL       (gtk_builder_get_object (builder, "strongpls_label"));
        strongpls_switch    = GTK_SWITCH      (gtk_builder_get_object (builder, "strongpls_switch"));
        modcods_label       = GTK_LABEL       (gtk_builder_get_object (builder, "modcods_label"));
        modcods_entry       = GTK_ENTRY       (gtk_builder_get_object (builder, "modcods_entry"));
        framesizes_label    = GTK_LABEL       (gtk_builder_get_object (builder, "framesizes_label"));
        framesizes_entry    = GTK_ENTRY       (gtk_builder_get_object (builder, "framesizes_entry"));
        fastdrift_label     = GTK_LABEL       (gtk_builder_get_object (builder, "fastdrift_label"));
        fastdrift_switch    = GTK_SWITCH      (gtk_builder_get_object (builder, "fastdrift_switch"));
        ldpcbf_label        = GTK_LABEL       (gtk_builder_get_object (builder, "ldpcbf_label"));
        ldpcbf_spinbutton   = GTK_SPIN_BUTTON (gtk_builder_get_object (builder, "ldpcbf_spinbutton"));
        nhelpers_label      = GTK_LABEL       (gtk_builder_get_object (builder, "nhelpers_label"));
        nhelpers_spinbutton = GTK_SPIN_BUTTON (gtk_builder_get_object (builder, "nhelpers_spinbutton"));

    /* load parameters */
    parameters_to_gui();

    /* connect the signals */
    gtk_builder_connect_signals(builder, NULL);
 
    /* builder not longer needed */ 
    g_object_unref(builder);
 
    /* start the gui */
    gtk_widget_show(window);                
 }

