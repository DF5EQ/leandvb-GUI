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

/* settings/leandvc/DVB-S */
static GtkLabel*    constellation_label;
static GtkComboBox* constellation_combobox;
static GtkLabel*    coderate_label;
static GtkComboBox* coderate_combobox;
static GtkLabel*    viterbi_label;
static GtkSwitch*   viterbi_switch;
static GtkLabel*    hardmetric_label;
static GtkSwitch*   hardmetric_switch;

/* settings/leandvb/DVB-S2 */
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

/* settings/rtl_sdr */
static GtkSpinButton* rtldongle_spinbutton;
static GtkSpinButton* gain_spinbutton;
static GtkSpinButton* ppm_spinbutton;

/* settings/files */
static GtkEntry* leandvb_entry;
static GtkEntry* ldpchelper_entry;
static GtkEntry* rtlsdr_entry;
static GtkEntry* viewer_entry;     

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

    /* settings/leandvb/DVB-S */
    constellation_label    = GTK_LABEL     (gtk_builder_get_object (builder, "constellation_label"));
    constellation_combobox = GTK_COMBO_BOX (gtk_builder_get_object (builder, "constellation_combobox"));
    coderate_label         = GTK_LABEL     (gtk_builder_get_object (builder, "coderate_label"));
    coderate_combobox      = GTK_COMBO_BOX (gtk_builder_get_object (builder, "coderate_combobox"));
    viterbi_label          = GTK_LABEL     (gtk_builder_get_object (builder, "viterbi_label"));
    viterbi_switch         = GTK_SWITCH    (gtk_builder_get_object (builder, "viterbi_switch"));
    hardmetric_label       = GTK_LABEL     (gtk_builder_get_object (builder, "hardmetric_label"));
    hardmetric_switch      = GTK_SWITCH    (gtk_builder_get_object (builder, "hardmetric_switch"));

    /* settings/leandvb/DVB-S2 */
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

    /* settings/rtl_sdr */
    rtldongle_spinbutton = GTK_SPIN_BUTTON (gtk_builder_get_object (builder, "rtldongle_spinbutton"));
    gain_spinbutton      = GTK_SPIN_BUTTON (gtk_builder_get_object (builder, "gain_spinbutton"));
    ppm_spinbutton       = GTK_SPIN_BUTTON (gtk_builder_get_object (builder, "ppm_spinbutton"));

    /* settings/files */
    leandvb_entry    = GTK_ENTRY (gtk_builder_get_object (builder, "leandvb_entry"));
    ldpchelper_entry = GTK_ENTRY (gtk_builder_get_object (builder, "ldpchelper_entry"));
    rtlsdr_entry     = GTK_ENTRY (gtk_builder_get_object (builder, "rtlsdr_entry"));
    viewer_entry     = GTK_ENTRY (gtk_builder_get_object (builder, "viewer_entry"));
}

/*===== callback functions ==================================================*/

/*----- main window ---------------------------------------------------------*/

void main_window_show_cb (GtkWidget* widget, gpointer data)
{
    const char* s;
    float       f;
    int         i;
    char  buf[20];

    /* load main window parameters */

    param_get ("frequency", &f);
    snprintf (buf, sizeof(buf), "%.3f", f);
    gtk_entry_set_text (frequency_entry, buf);

    param_get ("symbolrate", &i);
    snprintf (buf, sizeof(buf), "%d", i);
    gtk_entry_set_text (symbolrate_entry, buf);

    param_get ("bandwidth", &i);
    snprintf (buf, sizeof(buf), "%d", i);
    gtk_entry_set_text (bandwidth_entry, buf);

    param_get ("tune", &i);
    snprintf (buf, sizeof(buf), "%d", i);
    gtk_entry_set_text (tune_entry, buf);

    param_get ("lnb_lo", &f);
    snprintf (buf, sizeof(buf), "%.3f", f);
    gtk_entry_set_text (lnblo_entry, buf);

    param_get ("fec", &s);
    snprintf (buf, sizeof(buf), "%s", s);
    gtk_entry_set_text (fec_entry, buf);
}

void main_window_destroy_cb (GtkWidget* widget, gpointer data)
{
    /* stop the gui */
    gtk_main_quit();
}

gboolean main_window_entry_focus_out_event_cb (GtkWidget *widget, GdkEvent *event, gpointer user_data)
{
    /* store main window parameter as requested */

    const char* s;
    float       f;
    int         i;

    s = gtk_entry_get_text (GTK_ENTRY(widget));
    f = atof(s);
    i = atoi(s);

    if (GTK_ENTRY(widget) == frequency_entry)
        param_set ("frequency", &f);
    else if (GTK_ENTRY(widget) == symbolrate_entry)
        param_set ("symbolrate", &i);
    else if (GTK_ENTRY(widget) == bandwidth_entry)
        param_set ("bandwidth", &i);
    else if (GTK_ENTRY(widget) == tune_entry)
        param_set ("tune", &i);
    else if (GTK_ENTRY(widget) == lnblo_entry)
        param_set ("lnb_lo", &f);
    else if (GTK_ENTRY(widget) == fec_entry)
        param_set ("fec", &s);

    return GDK_EVENT_PROPAGATE;
}

void main_window_combobox_changed_cb (GtkWidget* widget, gpointer data)
{
    /* when change was caused by selection from list */
    if ( gtk_combo_box_get_active (GTK_COMBO_BOX(widget)) != -1)
    {
        /* data must point to the entry of the combobox */
        main_window_entry_focus_out_event_cb (GTK_WIDGET(data), NULL, NULL);
    }
}

void main_window_start_button_clicked_cb (GtkWidget* widget, gpointer data)
{
    printf("TODO: %s\n", __FUNCTION__);
}

void main_window_stop_button_clicked_cb (GtkWidget* widget, gpointer data)
{
    printf("TODO: %s\n", __FUNCTION__);
}

void main_window_settings_button_clicked_cb (GtkWidget* widget, gpointer data)
{
	/* show the settings dialog and wait for closing */
    gtk_dialog_run (settings_dialog);

    /* hide the settingsdialog after it's closing */
    gtk_widget_hide (GTK_WIDGET(settings_dialog));
}

/*----- settings dialog -----------------------------------------------------*/

void settings_dialog_show_cb (GtkWidget* widget, gpointer data)
{
    const char* s;
    float       f;
    int         i;
    bool        b;

    /* load settings/leandvb parameters */

    param_get ("inpipe", &i);
    gtk_spin_button_set_value (inpipe_spinbutton, (float)i);

    param_get ("sampler", &s);
    gtk_combo_box_set_active_id (sampler_combobox, s);

    param_get ("rolloff", &f);
    gtk_spin_button_set_value (rolloff_spinbutton, f);

    param_get ("rrcrej", &f);
    gtk_spin_button_set_value (rrcrej_spinbutton, f);

    param_get ("fastlock", &b);
    gtk_switch_set_state (fastlock_switch, b);

    param_get ("maxsens", &b);
    gtk_switch_set_state (maxsens_switch, b);

    param_get ("debug", &s);
    gtk_combo_box_set_active_id (debug_combobox, s);

    param_get ("gui", &b);
    gtk_switch_set_state (gui_switch, b);

    param_get ("standard", &s);
    gtk_combo_box_set_active_id (standard_combobox, s);

    /* load settings/leandvb/DVB-S parameters */

    param_get ("constellation", &s);
    gtk_combo_box_set_active_id (constellation_combobox, s);

    param_get ("coderate", &s);
    gtk_combo_box_set_active_id (coderate_combobox, s);

    param_get ("viterbi", &b);
    gtk_switch_set_state (viterbi_switch, b);

    param_get ("hardmetric", &b);
    gtk_switch_set_state (hardmetric_switch, b);

    /* load settings/leandvb/DVB-S2 parameters */

    param_get ("strongpls", &b);
    gtk_switch_set_state (strongpls_switch, b);

    param_get ("modcods", &s);
    gtk_entry_set_text (modcods_entry, s);

    param_get ("framesizes", &s);
    gtk_entry_set_text (framesizes_entry, s);

    param_get ("fastdrift", &b);
    gtk_switch_set_state (fastdrift_switch, b);

    param_get ("ldpcbf", &i);
    gtk_spin_button_set_value (ldpcbf_spinbutton, (float)i);

    param_get ("nhelpers", &i);
    gtk_spin_button_set_value (nhelpers_spinbutton, (float)i);

    /* load settings/rtl_dongle parameters */

    param_get ("ppm", &i);
    gtk_spin_button_set_value (ppm_spinbutton, (float)i);

    param_get ("gain", &i);
    gtk_spin_button_set_value (gain_spinbutton, (float)i);

    param_get ("rtldongle", &i);
    gtk_spin_button_set_value (rtldongle_spinbutton, (float)i);

    /* load  settings/files parameters */

    param_get ("leandvb_path", &s);
    gtk_widget_set_tooltip_text (GTK_WIDGET(leandvb_entry), s);

    param_get ("leandvb_file", &s);
    gtk_entry_set_text (leandvb_entry, s);

    param_get ("ldpchelper_path", &s);
    gtk_widget_set_tooltip_text (GTK_WIDGET(ldpchelper_entry), s);

    param_get ("ldpchelper_file", &s);
    gtk_entry_set_text (ldpchelper_entry, s);

    param_get ("rtlsdr_path", &s);
    gtk_widget_set_tooltip_text (GTK_WIDGET(rtlsdr_entry), s);

    param_get ("rtlsdr_file", &s);
    gtk_entry_set_text (rtlsdr_entry, s);

    param_get ("viewer_path", &s);
    gtk_widget_set_tooltip_text (GTK_WIDGET(viewer_entry), s);

    param_get ("viewer_file", &s);
    gtk_entry_set_text (viewer_entry, s);
}

void settings_save_button_clicked_cb (GtkWidget* widget, gpointer data)
{
    const char* s;
    int         i;
    float       f;
    bool        b;

    /* store settings/leandvb parameters */

    i = gtk_spin_button_get_value_as_int (inpipe_spinbutton);
    param_set ("inpipe", &i);

    s = gtk_combo_box_get_active_id (sampler_combobox);
    param_set ("sampler", &s);

    f = gtk_spin_button_get_value (rolloff_spinbutton);
    param_set ("rolloff", &f);

    f = gtk_spin_button_get_value (rrcrej_spinbutton);
    param_set ("rrcrej", &f);

    b = gtk_switch_get_state (fastlock_switch);
    param_set ("fastlock", &b);

    b = gtk_switch_get_state (maxsens_switch);
    param_set ("maxsens", &b);

    s = gtk_combo_box_get_active_id (debug_combobox);
    param_set ("debug", &s);

    b = gtk_switch_get_state (gui_switch);
    param_set ("gui", &b);
 
    s = gtk_combo_box_get_active_id (standard_combobox);
    param_set ("standard", &s);

   /* store settings/leandvb/DVB-S parameters */
 
    s = gtk_combo_box_get_active_id (constellation_combobox);
    param_set ("constellation", &s);
 
    s = gtk_combo_box_get_active_id (coderate_combobox);
    param_set ("coderate", &s);

    b = gtk_switch_get_state (viterbi_switch);
    param_set ("viterbi", &b);

    b = gtk_switch_get_state (hardmetric_switch);
    param_set ("hardmetric", &b);

   /* store settings/leandvb/DVB-S2 parameters */

    b = gtk_switch_get_state (strongpls_switch);
    param_set ("strongpls", &b);

    s = gtk_entry_get_text (modcods_entry);
    param_set ("modcods", &s);

    s = gtk_entry_get_text (framesizes_entry);
    param_set ("framesizes", &s);

    b = gtk_switch_get_state (fastdrift_switch);
    param_set ("fastdrift", &b);

    i = gtk_spin_button_get_value_as_int (ldpcbf_spinbutton);
    param_set ("ldpcbf", &i);

    i = gtk_spin_button_get_value_as_int (nhelpers_spinbutton);
    param_set ("nhelpers", &i);

    /* store settings/rtl_dongle parameters */

    i = gtk_spin_button_get_value_as_int (ppm_spinbutton);
    param_set ("ppm", &i);

    i = gtk_spin_button_get_value_as_int (gain_spinbutton);
    param_set ("gain", &i);

    i = gtk_spin_button_get_value_as_int (rtldongle_spinbutton);
    param_set ("rtldongle", &i);

    /* store settings/files parameters */

    s = gtk_widget_get_tooltip_text (GTK_WIDGET(leandvb_entry));
    param_set ("leandvb_path", &s);

    s = gtk_entry_get_text (leandvb_entry);
    param_set ("leandvb_file", &s);

    s = gtk_widget_get_tooltip_text (GTK_WIDGET(ldpchelper_entry));
    param_set ("ldpchelper_path", &s);

    s = gtk_entry_get_text (ldpchelper_entry);
    param_set ("ldpchelper_file", &s);

    s = gtk_widget_get_tooltip_text (GTK_WIDGET(rtlsdr_entry));
    param_set ("rtlsdr_path", &s);

    s = gtk_entry_get_text (rtlsdr_entry);
    param_set ("rtlsdr_file", &s);

    s = gtk_widget_get_tooltip_text (GTK_WIDGET(viewer_entry));
    param_set ("viewer_path", &s);

    s = gtk_entry_get_text (viewer_entry);
    param_set ("viewer_file", &s);
}

void settings_cancel_button_clicked_cb (GtkWidget* widget, gpointer data)
{
    printf("TODO: %s\n", __FUNCTION__);
}

void settings_defaults_button_clicked_cb (GtkWidget* widget, gpointer data)
{
          float f;
          int   i;
    const char* s;
          bool  b;
    const char* tab_text;

    tab_text = gtk_notebook_get_tab_label_text(
                   GTK_NOTEBOOK(data),
                   gtk_notebook_get_nth_page(
                       GTK_NOTEBOOK(data),
                       gtk_notebook_get_current_page(
                           GTK_NOTEBOOK(data) ) ) );

    if (strcmp("leandvb", tab_text) == 0)
    {
        /* load settings/leandvb parameters */

        param_default_get ("inpipe", &i);
        gtk_spin_button_set_value (inpipe_spinbutton, i);

        param_default_get ("sampler", &s);
        gtk_combo_box_set_active_id (sampler_combobox, s);

        param_default_get ("rolloff", &f);
        gtk_spin_button_set_value (rolloff_spinbutton, f);

        param_default_get ("rrcrej", &f);
        gtk_spin_button_set_value (rrcrej_spinbutton, f);

        param_default_get ("fastlock", &b);
        gtk_switch_set_state (fastlock_switch, b);

        param_default_get ("maxsens", &b);
        gtk_switch_set_state (maxsens_switch, b);

        param_default_get ("debug", &s);
        gtk_combo_box_set_active_id (debug_combobox, s);

        param_default_get ("gui", &b);
        gtk_switch_set_state (gui_switch, b);

        param_default_get ("standard", &s);
        gtk_combo_box_set_active_id (standard_combobox, s);

        /* load settings/leandvb/DVB-S parameters */

        param_default_get ("constellation", &s);
        gtk_combo_box_set_active_id (constellation_combobox, s);

        param_default_get ("coderate", &s);
        gtk_combo_box_set_active_id (coderate_combobox, s);

        param_default_get ("viterbi", &b);
        gtk_switch_set_state (viterbi_switch, b);

        param_default_get ("hardmetric", &b);
        gtk_switch_set_state (hardmetric_switch, b);

        /* load settings/leandvb/DVB-S2 parameters */

        param_default_get ("strongpls", &b);
        gtk_switch_set_state (strongpls_switch, b);

        param_default_get ("modcods", &s);
        gtk_entry_set_text (modcods_entry, s);

        param_default_get ("framesizes", &s);
        gtk_entry_set_text (framesizes_entry, s);

        param_default_get ("fastdrift", &b);
        gtk_switch_set_state (fastdrift_switch, b);

        param_default_get ("ldpcbf", &i);
        gtk_spin_button_set_value (ldpcbf_spinbutton, i);

        param_default_get ("nhelpers", &i);
        gtk_spin_button_set_value (nhelpers_spinbutton, i);
    }
    else if (strcmp("rtl_sdr", tab_text) == 0)
    {
        /* load settings/rtl_dongle parameters */

        param_default_get ("ppm", &i);
        gtk_spin_button_set_value (ppm_spinbutton, i);

        param_default_get ("gain", &i);
        gtk_spin_button_set_value (gain_spinbutton, i);

        param_default_get ("rtldongle", &i);
        gtk_spin_button_set_value (rtldongle_spinbutton, i);
    }
    else if (strcmp("files", tab_text) == 0)
    {
        /* load  settings/files parameters */

        param_default_get ("leandvb_path", &s);
        gtk_widget_set_tooltip_text (GTK_WIDGET(leandvb_entry), s);

        param_default_get ("leandvb_file", &s);
        gtk_entry_set_text (leandvb_entry, s);

        param_default_get ("ldpchelper_path", &s);
        gtk_widget_set_tooltip_text (GTK_WIDGET(ldpchelper_entry), s);

        param_default_get ("ldpchelper_file", &s);
        gtk_entry_set_text (ldpchelper_entry, s);

        param_default_get ("rtlsdr_path", &s);
        gtk_widget_set_tooltip_text (GTK_WIDGET(rtlsdr_entry), s);

        param_default_get ("rtlsdr_file", &s);
        gtk_entry_set_text (rtlsdr_entry, s);

        param_default_get ("viewer_path", &s);
        gtk_widget_set_tooltip_text (GTK_WIDGET(viewer_entry), s);

        param_default_get ("viewer_file", &s);
        gtk_entry_set_text (viewer_entry, s);
    }
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

    text = gtk_combo_box_get_active_id (widget);

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

    /* connect the signals */
    gtk_builder_connect_signals(builder, NULL);
 
    /* builder not longer needed */ 
    g_object_unref(builder);

    /* start the gui */
    gtk_widget_show(window);                
 }

