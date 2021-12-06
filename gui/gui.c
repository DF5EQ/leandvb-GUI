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

/* settings/leandvb */
static GtkSpinButton* inpipe_spinbutton;
static GtkComboBox*   sampler_combobox;
static GtkSpinButton* rolloff_spinbutton;
static GtkSpinButton* rrcrej_spinbutton;
static GtkSwitch*     fastlock_switch;
static GtkSwitch*     maxsens_switch;
static GtkComboBox*   debug_combobox;
static GtkSwitch*     gui_switch;
static GtkComboBox*   standard_combobox;

/* settings/rtl_sdr */
static GtkSpinButton* rtldongle_spinbutton;
static GtkSpinButton* gain_spinbutton;
static GtkSpinButton* ppm_spinbutton;

/* settings/files */
static GtkEntry* leandvb_entry;
static GtkEntry* ldpchelper_entry;
static GtkEntry* rtlsdr_entry;
static GtkEntry* viewer_entry;     

/* settings DVB-S */
static GtkLabel*    constellation_label;
static GtkComboBox* constellation_combobox;
static GtkLabel*    coderate_label;
static GtkComboBox* coderate_combobox;
static GtkLabel*    viterbi_label;
static GtkSwitch*   viterbi_switch;
static GtkLabel*    hardmetric_label;
static GtkSwitch*   hardmetric_switch;

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
    settings_dialog = GTK_DIALOG (gtk_builder_get_object (builder, "settings_dialog"));

    /* settings/leandvb */
    inpipe_spinbutton  = GTK_SPIN_BUTTON (gtk_builder_get_object (builder, "inpipe_spinbutton"));
    sampler_combobox   = GTK_COMBO_BOX   (gtk_builder_get_object (builder, "sampler_combobox"));
    rolloff_spinbutton = GTK_SPIN_BUTTON (gtk_builder_get_object (builder, "rolloff_spinbutton"));
    rrcrej_spinbutton  = GTK_SPIN_BUTTON (gtk_builder_get_object (builder, "rrcrej_spinbutton"));
    fastlock_switch    = GTK_SWITCH      (gtk_builder_get_object (builder, "fastlock_switch"));
    maxsens_switch     = GTK_SWITCH      (gtk_builder_get_object (builder, "maxsens_switch"));
    debug_combobox     = GTK_COMBO_BOX   (gtk_builder_get_object (builder, "debug_combobox"));
    gui_switch         = GTK_SWITCH      (gtk_builder_get_object (builder, "gui_switch"));
    standard_combobox  = GTK_COMBO_BOX   (gtk_builder_get_object (builder, "standard_combobox"));

    /* settings/rtl_sdr */
    rtldongle_spinbutton = GTK_SPIN_BUTTON (gtk_builder_get_object (builder, "rtldongle_spinbutton"));
    gain_spinbutton      = GTK_SPIN_BUTTON (gtk_builder_get_object (builder, "gain_spinbutton"));
    ppm_spinbutton       = GTK_SPIN_BUTTON (gtk_builder_get_object (builder, "ppm_spinbutton"));

    /* settings/files */
    leandvb_entry    = GTK_ENTRY (gtk_builder_get_object (builder, "leandvb_entry"));
    ldpchelper_entry = GTK_ENTRY (gtk_builder_get_object (builder, "ldpchelper_entry"));
    rtlsdr_entry     = GTK_ENTRY (gtk_builder_get_object (builder, "rtlsdr_entry"));
    viewer_entry     = GTK_ENTRY (gtk_builder_get_object (builder, "viewer_entry"));

    /* settings DVB-S */
    constellation_label    = GTK_LABEL     (gtk_builder_get_object (builder, "constellation_label"));
    constellation_combobox = GTK_COMBO_BOX (gtk_builder_get_object (builder, "constellation_combobox"));
    coderate_label         = GTK_LABEL     (gtk_builder_get_object (builder, "coderate_label"));
    coderate_combobox      = GTK_COMBO_BOX (gtk_builder_get_object (builder, "coderate_combobox"));
    viterbi_label          = GTK_LABEL     (gtk_builder_get_object (builder, "viterbi_label"));
    viterbi_switch         = GTK_SWITCH    (gtk_builder_get_object (builder, "viterbi_switch"));
    hardmetric_label       = GTK_LABEL     (gtk_builder_get_object (builder, "hardmetric_label"));
    hardmetric_switch      = GTK_SWITCH    (gtk_builder_get_object (builder, "hardmetric_switch"));

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
    bool        b;
    char      buf[20];

    printf("TODO: %s - load parameters when showing the window/dialog, use the show signals\n", __FUNCTION__);

    /* load main window parameters */

    parameters_get_string ("fec", &s);
    snprintf (buf,sizeof(buf), "%s", s);
    gtk_entry_set_text (fec_entry, buf);

    parameters_get_float ("lnb_lo", &f);
    snprintf (buf,sizeof(buf), "%.3f", f);
    gtk_entry_set_text (lnblo_entry, buf);

    parameters_get_int ("tune", &i);
    snprintf (buf,sizeof(buf), "%d", i);
    gtk_entry_set_text (tune_entry, buf);

    parameters_get_int ("bandwidth", &i);
    snprintf (buf,sizeof(buf), "%d", i);
    gtk_entry_set_text (bandwidth_entry, buf);

    parameters_get_int ("symbolrate", &i);
    snprintf (buf,sizeof(buf), "%d", i);
    gtk_entry_set_text (symbolrate_entry, buf);

    parameters_get_float ("frequency", &f);
    snprintf (buf,sizeof(buf), "%.3f", f);
    gtk_entry_set_text (frequency_entry, buf);

    /* load settings/rtl_dongle parameters */

    parameters_get_int ("rtldongle", &i);
    gtk_spin_button_set_value (rtldongle_spinbutton, (float)i);

    parameters_get_int ("gain", &i);
    gtk_spin_button_set_value (gain_spinbutton, (float)i);

    parameters_get_int ("ppm", &i);
    gtk_spin_button_set_value (ppm_spinbutton, (float)i);

    /* load  settings/files parameters */

    parameters_get_string ("viewer_path", &s);
    gtk_widget_set_tooltip_text (GTK_WIDGET(viewer_entry), s);

    parameters_get_string ("viewer_file", &s);
    gtk_entry_set_text (viewer_entry, s);

    parameters_get_string ("rtlsdr_path", &s);
    gtk_widget_set_tooltip_text (GTK_WIDGET(rtlsdr_entry), s);

    parameters_get_string ("rtlsdr_file", &s);
    gtk_entry_set_text (rtlsdr_entry, s);

    parameters_get_string ("ldpchelper_path", &s);
    gtk_widget_set_tooltip_text (GTK_WIDGET(ldpchelper_entry), s);

    parameters_get_string ("ldpchelper_file", &s);
    gtk_entry_set_text (ldpchelper_entry, s);

    parameters_get_string ("leandvb_path", &s);
    gtk_widget_set_tooltip_text (GTK_WIDGET(leandvb_entry), s);

    parameters_get_string ("leandvb_file", &s);
    gtk_entry_set_text (leandvb_entry, s);

    /* load settings/leandvb parameters */

    parameters_get_int ("inpipe", &i);
    gtk_spin_button_set_value (inpipe_spinbutton, (float)i);

    parameters_get_string ("sampler", &s);
    gtk_combo_box_set_active_id (sampler_combobox, s);

    parameters_get_float ("rolloff", &f);
    gtk_spin_button_set_value (rolloff_spinbutton, f);

    parameters_get_float ("rrcrej", &f);
    gtk_spin_button_set_value (rrcrej_spinbutton, f);

    parameters_get_bool ("fastlock", &b);
    gtk_switch_set_state (fastlock_switch, b);

    parameters_get_bool ("maxsens", &b);
    gtk_switch_set_state (maxsens_switch, b);

    parameters_get_string ("debug", &s);
    gtk_combo_box_set_active_id (debug_combobox, s);

    parameters_get_bool ("gui", &b);
    gtk_switch_set_state (gui_switch, b);

    parameters_get_string ("standard", &s);
    gtk_combo_box_set_active_id (standard_combobox, s);

    /* load settings/leandvb/DVB-S parameters */

    parameters_get_string ("constellation", &s);
    gtk_combo_box_set_active_id (constellation_combobox, s);

    parameters_get_string ("coderate", &s);
    gtk_combo_box_set_active_id (coderate_combobox, s);

    parameters_get_bool ("viterbi", &b);
    gtk_switch_set_state (viterbi_switch, b);

    parameters_get_bool ("hardmetric", &b);
    gtk_switch_set_state (hardmetric_switch, b);

    /* load settings/leandvb/DVB-S2 parameters */

    parameters_get_bool ("strongpls", &b);
    gtk_switch_set_state (strongpls_switch, b);

    parameters_get_string ("modcods", &s);
    gtk_entry_set_text (modcods_entry, s);

    parameters_get_string ("framesizes", &s);
    gtk_entry_set_text (framesizes_entry, s);

    parameters_get_bool ("fastdrift", &b);
    gtk_switch_set_state (fastdrift_switch, b);

    parameters_get_int ("ldpcbf", &i);
    gtk_spin_button_set_value (ldpcbf_spinbutton, (float)i);

    parameters_get_int ("nhelpers", &i);
    gtk_spin_button_set_value (nhelpers_spinbutton, (float)i);
}

/*===== callback functions ==================================================*/

/*----- main window -----*/

void main_window_destroy_cb (GtkWidget* widget, gpointer data)
{
    const char* s;
    int         i;
    float       f;

    /* store main window parameters */

    s = gtk_entry_get_text (fec_entry);
    parameters_set_string ("fec", s);

    s = gtk_entry_get_text (lnblo_entry);
    f = atof(s);
    parameters_set_float ("lnb_lo", f, "%.3f");

    s = gtk_entry_get_text (tune_entry);
    i = atoi(s);
    parameters_set_int ("tune", i);

    s = gtk_entry_get_text (bandwidth_entry);
    i = atoi(s);
    parameters_set_int ("bandwidth", i);

    s = gtk_entry_get_text (symbolrate_entry);
    i = atoi(s);
    parameters_set_int ("symbolrate", i);

    s = gtk_entry_get_text (frequency_entry);
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
    bool        b;

    /* store settings/rtl_dongle parameters */

    i = gtk_spin_button_get_value_as_int (rtldongle_spinbutton);
    parameters_set_int ("rtldongle", i);

    i = gtk_spin_button_get_value_as_int (gain_spinbutton);
    parameters_set_int ("gain", i);

    i = gtk_spin_button_get_value_as_int (ppm_spinbutton);
    parameters_set_int ("ppm", i);

    /* store settings/files parameters */

    s = gtk_widget_get_tooltip_text (GTK_WIDGET(viewer_entry));
    parameters_set_string ("viewer_path", s);
    s = gtk_entry_get_text (viewer_entry);
    parameters_set_string ("viewer_file", s);

    s = gtk_widget_get_tooltip_text (GTK_WIDGET(rtlsdr_entry));
    parameters_set_string ("rtlsdr_path", s);
    s = gtk_entry_get_text (rtlsdr_entry);
    parameters_set_string ("rtlsdr_file", s);

    s = gtk_widget_get_tooltip_text (GTK_WIDGET(ldpchelper_entry));
    parameters_set_string ("ldpchelper_path", s);
    s = gtk_entry_get_text (ldpchelper_entry);
    parameters_set_string ("ldpchelper_file", s);

    s = gtk_widget_get_tooltip_text (GTK_WIDGET(leandvb_entry));
    parameters_set_string ("leandvb_path", s);
    s = gtk_entry_get_text (leandvb_entry);
    parameters_set_string ("leandvb_file", s);

    /* store settings/leandvb parameters */

    i = gtk_spin_button_get_value_as_int (inpipe_spinbutton);
    parameters_set_int ("inpipe", i);

    s = gtk_combo_box_get_active_id (sampler_combobox);
    parameters_set_string ("sampler", s);

    f = gtk_spin_button_get_value (rolloff_spinbutton);
    parameters_set_float ("rolloff", f, "%.2f");

    f = gtk_spin_button_get_value (rrcrej_spinbutton);
    parameters_set_float ("rrcrej", f, "%.1f");

    b = gtk_switch_get_state (fastlock_switch);
    parameters_set_bool ("fastlock", b);

    b = gtk_switch_get_state (maxsens_switch);
    parameters_set_bool ("maxsens", b);

    s = gtk_combo_box_get_active_id (debug_combobox);
    parameters_set_string ("debug", s);

    b = gtk_switch_get_state (gui_switch);
    parameters_set_bool ("gui", b);
 
    s = gtk_combo_box_get_active_id (standard_combobox);
    parameters_set_string ("standard", s);

   /* store settings/leandvb/DVB-S parameters */
 
    s = gtk_combo_box_get_active_id (constellation_combobox);
    parameters_set_string ("constellation", s);
 
    s = gtk_combo_box_get_active_id (coderate_combobox);
    parameters_set_string ("coderate", s);

    b = gtk_switch_get_state (viterbi_switch);
    parameters_set_bool ("viterbi", b);

    b = gtk_switch_get_state (hardmetric_switch);
    parameters_set_bool ("hardmetric", b);

   /* store settings/leandvb/DVB-S2 parameters */

    b = gtk_switch_get_state (strongpls_switch);
    parameters_set_bool ("strongpls", b);

    s = gtk_entry_get_text (modcods_entry);
    parameters_set_string ("modcods", s);

    s = gtk_entry_get_text (framesizes_entry);
    parameters_set_string ("framesizes", s);

    b = gtk_switch_get_state (fastdrift_switch);
    parameters_set_bool ("fastdrift", b);

    i = gtk_spin_button_get_value_as_int (ldpcbf_spinbutton);
    parameters_set_int ("ldpcbf", i);

    i = gtk_spin_button_get_value_as_int (nhelpers_spinbutton);
    parameters_set_int ("nhelpers", i);
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

void filechooser_button_clicked_cb (GtkWidget* widget, gpointer data)
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

    path = gtk_widget_get_tooltip_text (GTK_WIDGET(data));
    file = gtk_entry_get_text (GTK_ENTRY(data));

    if (path != NULL) gtk_file_chooser_set_current_folder (GTK_FILE_CHOOSER (dialog), path);
    if (file != NULL) gtk_file_chooser_set_current_name (GTK_FILE_CHOOSER (dialog), file);

    /* run the dialog */
    res = gtk_dialog_run (GTK_DIALOG (dialog));
    if (res == GTK_RESPONSE_ACCEPT)
    {
        /* store the choosen path/file */

        path = gtk_file_chooser_get_current_folder (GTK_FILE_CHOOSER (dialog));
        file = gtk_file_chooser_get_current_name   (GTK_FILE_CHOOSER (dialog));
 
        gtk_widget_set_tooltip_text (GTK_WIDGET(data), path);
        gtk_entry_set_text          (GTK_ENTRY (data), file);
    }

    /* destroy the dialog */
    gtk_widget_destroy (dialog);
}

/*----- settings/leandvb -----*/

void standard_combobox_changed_cb (GtkComboBox *widget, gpointer user_data)
{
    const char* text;

    text = gtk_combo_box_get_active_id (standard_combobox);

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

