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

/* settings/rtl_dongle */
static GtkSpinButton* rtldongle_spinbutton;
static GtkSpinButton* gain_spinbutton;
static GtkSpinButton* ppm_spinbutton;
static GtkEntry*      test_entry;

/* settings/files */
static GtkFileChooser* viewer_filechooser;
static GtkFileChooser* rtlsdr_filechooser;
static GtkFileChooser* ldpchelper_filechooser;
static GtkFileChooser* leandvb_filechooser;

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

static void expose_widgets (void)
{
    /* main window */
    window           = GTK_WIDGET (gtk_builder_get_object (builder, "main_window"));
    fec_entry        = GTK_ENTRY  (gtk_builder_get_object (builder, "fec_entry"));
    lnblo_entry      = GTK_ENTRY  (gtk_builder_get_object (builder, "lnblo_entry"));
    tune_entry       = GTK_ENTRY  (gtk_builder_get_object (builder, "tune_entry"));
    bandwidth_entry  = GTK_ENTRY  (gtk_builder_get_object (builder, "bandwidth_entry"));
    symbolrate_entry = GTK_ENTRY  (gtk_builder_get_object (builder, "symbolrate_entry"));
    frequency_entry  = GTK_ENTRY  (gtk_builder_get_object (builder, "frequency_entry"));

    /* settings dialog */
    settings_dialog     = GTK_DIALOG (gtk_builder_get_object (builder, "settings_dialog"));

    /* settings/rtl_sdr */
    rtldongle_spinbutton = GTK_SPIN_BUTTON (gtk_builder_get_object (builder, "rtldongle_spinbutton"));
    gain_spinbutton      = GTK_SPIN_BUTTON (gtk_builder_get_object (builder, "gain_spinbutton"));
    ppm_spinbutton       = GTK_SPIN_BUTTON (gtk_builder_get_object (builder, "ppm_spinbutton"));

    /* settings/files */
    viewer_filechooser     = GTK_FILE_CHOOSER (gtk_builder_get_object (builder, "viewer_filechooser"));
    rtlsdr_filechooser     = GTK_FILE_CHOOSER (gtk_builder_get_object (builder, "rtlsdr_filechooser"));
    ldpchelper_filechooser = GTK_FILE_CHOOSER (gtk_builder_get_object (builder, "ldpchelper_filechooser"));
    leandvb_filechooser    = GTK_FILE_CHOOSER (gtk_builder_get_object (builder, "leandvb_filechooser"));
    test_entry             = GTK_ENTRY        (gtk_builder_get_object (builder, "test_entry"));

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
}

static void parameters_to_gui (void)
{
    const char* s;
    int         i;
    float       f;
    char      buf[20];

    /* load settings/leandvb parameters */
    printf("TODO: %s - load settings/leandvb parameters\n", __FUNCTION__);

    /* load main window parameters */

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

    /* load settings/rtl_dongle parameters */

    parameters_get_int ("rtldongle", &i);
    gtk_spin_button_set_value (rtldongle_spinbutton, (float)i);

    parameters_get_int ("gain", &i);
    gtk_spin_button_set_value (gain_spinbutton, (float)i);

    parameters_get_int ("ppm", &i);
    gtk_spin_button_set_value (ppm_spinbutton, (float)i);

    /* load  settings/files parameters */

    parameters_get_string ("viewer_file", &s);
    printf("%s: %s\n", __FUNCTION__, s);
//    gtk_file_chooser_set_filename (viewer_filechooser, "makefile");
//    gtk_file_chooser_set_current_name (viewer_filechooser, "makefile");
}

/*===== callback functions ==================================================*/

/*----- main window -----*/

void main_window_destroy_cb (GtkWidget* widget, gpointer data)
{
    const char* s;
    int         i;
    float       f;

    /* store main window parameters */

    s = gtk_entry_get_text ((GtkEntry*)fec_entry);
    parameters_set_string ("fec", s);

    s = gtk_entry_get_text ((GtkEntry*)lnblo_entry);
    f = atof(s);
    parameters_set_float ("lnb_lo", f, "%.3f");

    s = gtk_entry_get_text ((GtkEntry*)tune_entry);
    i = atoi(s);
    parameters_set_int ("tune", i);

    s = gtk_entry_get_text ((GtkEntry*)bandwidth_entry);
    i = atoi(s);
    parameters_set_int ("bandwidth", i);

    s = gtk_entry_get_text ((GtkEntry*)symbolrate_entry);
    i = atoi(s);
    parameters_set_int ("symbolrate", i);

    s = gtk_entry_get_text ((GtkEntry*)frequency_entry);
    f = atof(s);
    parameters_set_float ("frequency", f, "%.3f");

    /* stop the gui */
	gtk_main_quit();
}

void start_button_clicked_cb (GtkWidget* widget, gpointer data)
{
    printf("TODO: %s\n", __FUNCTION__);
}

void stop_button_clicked_cb (GtkWidget* widget, gpointer data)
{
    printf("TODO: %s\n", __FUNCTION__);
}

void settings_button_clicked_cb (GtkWidget* widget, gpointer data)
{
	/* show the settings dialog and wait for closing */
    gtk_dialog_run (settings_dialog);

    /* hide the settingsdialog after it's closing */
    gtk_widget_hide (GTK_WIDGET(settings_dialog));
}

void settings_save_button_clicked_cb (GtkWidget* widget, gpointer data)
{
    const char* s;
    int         i;
    float       f;

    /* store settings/rtl_dongle parameters */

    i = gtk_spin_button_get_value_as_int (rtldongle_spinbutton);
    parameters_set_int ("rtldongle", i);

    i = gtk_spin_button_get_value_as_int (gain_spinbutton);
    parameters_set_int ("gain", i);

    i = gtk_spin_button_get_value_as_int (ppm_spinbutton);
    parameters_set_int ("ppm", i);

    printf("TODO: %s - store settings/leandvb parameters\n", __FUNCTION__);
    printf("TODO: %s - store settings/files parameters\n", __FUNCTION__);
}

void settings_cancel_button_clicked_cb (GtkWidget* widget, gpointer data)
{
    printf("TODO: %s\n", __FUNCTION__);
}

void settings_defaults_button_clicked_cb (GtkWidget* widget, gpointer data)
{
    printf("TODO: %s\n", __FUNCTION__);
}

/*----- settings/files -----*/

void test_button_clicked_cb (GtkWidget* widget, gpointer data)
{
    /* 'data' is set up in GLADE to point to the corresponding entry */

    GtkWidget* dialog;
    const char* file;
    const char* path;
    int res;
    
    /* create a new dialog */
    dialog = gtk_file_chooser_dialog_new ("Choose File", NULL, GTK_FILE_CHOOSER_ACTION_SAVE,
                                          "Cancel", GTK_RESPONSE_CANCEL,
                                          "Open", GTK_RESPONSE_ACCEPT,
                                          NULL);

    /* prepare dialog with current path/file */

    path = gtk_widget_get_tooltip_text ((GtkWidget*)data);
    file = gtk_entry_get_text ((GtkEntry*)data);

    if (path != NULL) gtk_file_chooser_set_current_folder (GTK_FILE_CHOOSER (dialog), path);
    if (file != NULL) gtk_file_chooser_set_current_name (GTK_FILE_CHOOSER (dialog), file);

    /* run the dialog */
    res = gtk_dialog_run (GTK_DIALOG (dialog));
    if (res == GTK_RESPONSE_ACCEPT)
    {
        /* store the choosen path/file */

        path = gtk_file_chooser_get_current_folder (GTK_FILE_CHOOSER (dialog));
        file = gtk_file_chooser_get_current_name   (GTK_FILE_CHOOSER (dialog));
 
        gtk_widget_set_tooltip_text ((GtkWidget*)data, path);
        gtk_entry_set_text          ((GtkEntry*) data, file);
    }

    /* destroy the dialog */
    gtk_widget_destroy (dialog);
}

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

    /* expose needed widgets */
    expose_widgets();

    /* load parameters */
    parameters_to_gui();

    /* connect the signals */
    gtk_builder_connect_signals(builder, NULL);
 
    /* builder not longer needed */ 
    g_object_unref(builder);
 
    /* start the gui */
    gtk_widget_show(window);                
 }

