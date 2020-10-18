#!/usr/bin/env python

# Simple UI voor LEANDVB, DVBS receiver.
# requires sudo apt-get install python-imaging-tk package
# keep everything in your home directory
# if you add a 180x180 pixels file called logo.png it will be
# showed in right corner.
# Leandvb by F4DAV (github leansdr)
# Wrapper by pe2jko@540.org

# TODO reorganize DVB-S / DVB-S2 checkbox evaluation
# TODO leandvb-run as function like leandvb-stop
# TODO leandvb: --tune is broken, use --derotate instead
# TODO streamline usage of viewer ffplay and mplayer
# TODO 'cancel' in settings not working propperly
# TODO add entries for path and filenames in settings

from Tkinter import *
import ttk
import os
import json

# set directory for lb3iliary files (settings, run, stop)
home            = os.path.expanduser("~/")
lb3_dir         = os.path.expanduser("~/") + ".leandvb-GUI/"
parameters_file = lb3_dir + "parameters.json"
run_script      = lb3_dir + "run.sh"
stop_script     = lb3_dir + "stop.sh"

if not os.path.exists(lb3_dir):
    print "create " + lb3_dir
    os.mkdir(lb3_dir)

print "Home directory      : " + home
print "lb3illiary directory: " + lb3_dir
print "run script          : " + run_script
print "stop script         : " + stop_script

# check max pipe size and adjust if needed

max_needed = 32000000

fd = open("/proc/sys/fs/pipe-max-size", "r")
max_current = int(fd.readline())
fd.close()

if (max_current < max_needed):
    print "max pipe size is", max_current, ", will be set to", max_needed
    cmd = "bash -c 'echo " + str(max_needed) + " > /proc/sys/fs/pipe-max-size'"
    os.system("pkexec " + cmd)
else:
    print "max pipe size is", max_current, ", this is ok"

#===== handle parameters (save, load, default) ================================

parameters = dict()

def parameters_save():
    print "save parameters to file"
    parameters["frequency"     ] = float(frequency.get())
    parameters["samplerate"    ] = int(samplerate.get())
    parameters["fec"           ] = fec.get()
    parameters["tune"          ] = int(tune.get())
    parameters["fastlock"      ] = bool(fastlock.get())
    parameters["bandwidth"     ] = int(bandwidth.get())
    parameters["viterbi"       ] = bool(viterbi.get())
    parameters["gui"           ] = bool(gui.get())
    parameters["maxprocess"    ] = bool(maxprocess.get())
    parameters["hardmetric"    ] = bool(hardmetric.get())
    parameters["leanpad"       ] = padlean.get()
    parameters["ppm"           ] = int(ppm.get())
    parameters["gain"          ] = gain.get()
    parameters["viewer"        ] = viewer.get()
    parameters["rolloff_factor"] = rolloff_factor.get()
    parameters["rrc_rej_factor"] = rrc_rej_factor.get()
    parameters["nhelpers"      ] = nhelpers.get()
    parameters["inpipe"        ] = inpipe.get()
    parameters["modcods"       ] = modcods.get()
    parameters["framesizes"    ] = framesizes.get()
    parameters["lnb_lo"        ] = lnblo.get()
    parameters["rtldongle"     ] = rtldongle.get()
    parameters["standard"      ] = standard.get()
    parameters["sampler"       ] = sampler.get()
    parameters["strongpls"     ] = bool(strongpls.get())
    parameters["fastdrift"     ] = bool(fastdrift.get())
    parameters["ldpc_bf"       ] = int(ldpc_bf.get())
    parameters["ldpc_helper"   ] = ldpc_helper.get()
    parameters["constellation" ] = const.get()

    file = open(parameters_file, "w")
    file.write(json.dumps(parameters, indent=4, sort_keys=True))
    file.close()

def parameters_load():
    global parameters
    print "load parameters from file"
    file = open(parameters_file, "r")
    parameters = json.load(file)
    file.close()

def parameters_default():
    print "load parameters with defaults"
    parameters["frequency"     ] = 10491.500
    parameters["samplerate"    ] = 1500
    parameters["fec"           ] = "1/2"
    parameters["tune"          ] = 0
    parameters["fastlock"      ] = False
    parameters["bandwidth"     ] = 2400
    parameters["viterbi"       ] = False
    parameters["gui"           ] = True
    parameters["maxprocess"    ] = False
    parameters["hardmetric"    ] = False
    parameters["leanpad"       ] = home+"leansdr/src/apps/"
    parameters["ppm"           ] = 0
    parameters["gain"          ] = 36
    parameters["viewer"        ] = "ffplay"
    parameters["rolloff_factor"] = "0.35"
    parameters["rrc_rej_factor"] = 30
    parameters["nhelpers"      ] = 6
    parameters["inpipe"        ] = 32000000
    parameters["modcods"       ] = "0x0040"
    parameters["framesizes"    ] = "0x01"
    parameters["lnb_lo"        ] = 9750.0
    parameters["rtldongle"     ] = 0
    parameters["standard"      ] = "DVB-S2"
    parameters["sampler"       ] = "rrc"
    parameters["strongpls"     ] = False
    parameters["fastdrift"     ] = False
    parameters["ldpc_bf"       ] = 0
    parameters["ldpc_helper"   ] = "ldpc_tool"
    parameters["constellation" ] = "QPSK"

#===== settings dialog ========================================================

def dlg_settings():

    #----- local functions -----
    def set_visibility_dvb_options(dummy):

        # cover current options
        frm_blank.lift()

        # show options according to 'standard' widget
        if standard.get() == "DVB-S":
            for x in options_dvbs:
                x.lift()
        elif standard.get() == "DVB-S2":
            for x in options_dvbs2:
                x.lift()

    def on_save():
        parameters_save()
        dlg.destroy()

    def on_cancel():
        dlg.destroy()

    #----- dialog properties -----
    dlg = Toplevel(root, borderwidth=4)
    dlg.title("Settings")
    dlg.transient(root)
    dlg.resizable(height = False, width = False)
    dlg.grab_set()

    #----- tabs container -----
    ntb = ttk.Notebook (dlg)

    tab_general = ttk.Frame (ntb, padding=10)
    tab_files   = ttk.Frame (ntb, padding=10)
    tab_rtlsdr  = ttk.Frame (ntb, padding=10)
    tab_leandvb = ttk.Frame (ntb, padding=10)

    ntb.add(tab_general, text="general")
    ntb.add(tab_files,   text="files")
    ntb.add(tab_rtlsdr,  text="rtl_sdr")
    ntb.add(tab_leandvb, text="leandvb")

    #----- tab_general -----
    lbl_general = ttk.Label(tab_general, text="General settings")
    lbl_viewer  = ttk.Label(tab_general,           text="Viewer : ")
    ent_viewer  = ttk.Entry(tab_general, width=10, textvariable=viewer)
    lbl_lnblo   = ttk.Label(tab_general,           text="LNB LO : ")
    ent_lnblo   = ttk.Entry(tab_general, width=10, textvariable=lnblo)

    #----- tab_files -----
    lbl_files           = ttk.Label(tab_files, text="Setting of files and directories")
    lbl_leansdr_file    = ttk.Label(tab_files,           text="Path to leansdr : ")
    ent_leansdr_file    = ttk.Entry(tab_files, width=40, textvariable=padlean)
    lbl_ldpchelper_file = ttk.Label(tab_files,           text="LDPC helper : ")
    ent_ldpchelper_file = ttk.Entry(tab_files, width=40, textvariable=ldpc_helper)

     #----- tab_rtlsdr -----
    lbl_rtlsdr    = ttk.Label(tab_rtlsdr, text="Settings for rtl_sdr program")
    lbl_ppm       = ttk.Label(tab_rtlsdr,           text="ppm-error")
    lb2_ppm       = ttk.Label(tab_rtlsdr,           text=" (-p) : ")
    ent_ppm       = ttk.Entry(tab_rtlsdr, width=10, textvariable=ppm)
    lb3_ppm       = ttk.Label(tab_rtlsdr,           text="default 0")
    lbl_gain      = ttk.Label(tab_rtlsdr,           text="gain")
    lb2_gain      = ttk.Label(tab_rtlsdr,           text=" (-g) : ")
    ent_gain      = ttk.Entry(tab_rtlsdr, width=10, textvariable=gain)
    lb3_gain      = ttk.Label(tab_rtlsdr,           text="default 0 = Auto")
    lbl_rtldongle = ttk.Label(tab_rtlsdr,           text="rtldongle")
    lb2_rtldongle = ttk.Label(tab_rtlsdr,           text=" (-d) : ")
    ent_rtldongle = ttk.Entry(tab_rtlsdr, width=10, textvariable=rtldongle)
    lb3_rtldongle = ttk.Label(tab_rtlsdr,           text="default 0")

    #----- tab_leandvb -----
    tab_leandvb.columnconfigure((0,1,2),   pad=4, weight=1)
    tab_leandvb.rowconfigure   ((0,1,2,3), pad=4, weight=0)

        #----- label -----
    lbl_leandvb = ttk.Label (tab_leandvb, text="Settings for leandvb program")
    lbl_leandvb.grid (row=0, column=0, sticky=N, columnspan=3, pady=6)

        #----- frame 'common options' -----
    frm_common_options = ttk.Frame (tab_leandvb, borderwidth=4, padding=4)
    frm_common_options.grid (row=1, column=0, sticky=N)

        #----- frame 'dvb options' -----
    frm_dvb_options = ttk.Frame (tab_leandvb, borderwidth=4, padding=4)
    frm_dvb_options.grid (row=1, column=1, sticky=N)
    frm_dvb_options.columnconfigure((0,1), weight=1)
    options_dvbs  = [] # for collecting all DVB-S  options
    options_dvbs2 = [] # for collecting all DVB-S2 options

        #----- for covering current options when switching to new options -----
        #----- see set_visibility_dvb_options() -----
    frm_blank = ttk.Frame (frm_dvb_options)
    frm_blank.grid (row=1, column=0, rowspan=6, columnspan=3, sticky=NSEW)

    #----- tab_leandvb frm_common_options -----
    lbl_inpipe = ttk.Label (frm_common_options,           text="inpipe")
    ent_inpipe = ttk.Entry (frm_common_options, width=10, textvariable=inpipe)
    lbl_inpipe.grid (row=0, column=0, sticky=W)
    ent_inpipe.grid (row=0, column=1, sticky=W)

    lbl_sampler = ttk.Label (frm_common_options, text="sampler")
    cmb_sampler = ttk.Combobox(frm_common_options, width=10, textvariable=sampler, state="readonly")
    cmb_sampler ["values"] = ("nearest","linear","rrc")
    lbl_sampler.grid (row=1, column=0, sticky=W)
    cmb_sampler.grid (row=1, column=1, sticky=W)

    lbl_rolloff = ttk.Label (frm_common_options,           text="Roll Off")
    ent_rolloff = ttk.Entry (frm_common_options, width=10, textvariable=rolloff_factor)
    lbl_rolloff.grid (row=2, column=0, sticky=W)
    ent_rolloff.grid (row=2, column=1, sticky=W)

    lbl_rrcrej = ttk.Label (frm_common_options,           text="RRC Rej")
    ent_rrcrej = ttk.Entry (frm_common_options, width=10, textvariable=rrc_rej_factor)
    lbl_rrcrej.grid (row=3, column=0, sticky=W)
    ent_rrcrej.grid (row=3, column=1, sticky=W)

    lbl_fastlock = ttk.Label (frm_common_options, text="fastlock")
    chk_fastlock = Checkbutton (frm_common_options, variable=fastlock)
    lbl_fastlock.grid (row=4, column=0, sticky=E)
    chk_fastlock.grid (row=4, column=1, sticky=W)

    lbl_gui = ttk.Label (frm_common_options, text="GUI")
    chk_gui = Checkbutton (frm_common_options, variable=gui)
    lbl_gui.grid (row=5, column=0, sticky=E)
    chk_gui.grid (row=5, column=1, sticky=W)

    #----- tab_leandvb frm_dvb_options (control) -----
    lbl_standard = ttk.Label    (frm_dvb_options, text="DVB standard")
    cmb_standard = ttk.Combobox (frm_dvb_options, width=10, textvariable=standard, state="readonly")
    cmb_standard ["values"] = ("DVB-S","DVB-S2")
    cmb_standard.bind("<<ComboboxSelected>>", set_visibility_dvb_options)
    lbl_standard.grid (row=0, column=0, sticky=E)
    cmb_standard.grid (row=0, column=1, sticky=W)

    #----- tab_leandvb frm_dvb_options (DVB-S) -----
    lbl_const = ttk.Label    (frm_dvb_options, text="constellation")
    cmb_const = ttk.Combobox (frm_dvb_options, width=10, textvariable=const, state="readonly")
    cmb_const ["values"] = ("QPSK","BPSK")
    lbl_const.grid (row=1, column=0, sticky=E)
    cmb_const.grid (row=1, column=1, sticky=W)
    options_dvbs.append(lbl_const)
    options_dvbs.append(cmb_const)

    lbl_fec = ttk.Label   (frm_dvb_options, text="code rate")
    cmb_fec = ttk.Combobox(frm_dvb_options, width=10, textvariable=fec, state="readonly")
    cmb_fec ["values"] = ("1/2","2/3","3/4","5/6","6/7","7/8")
    lbl_fec.grid (row=2, column=0, sticky=E)
    cmb_fec.grid (row=2, column=1, sticky=W)
    options_dvbs.append(lbl_fec)
    options_dvbs.append(cmb_fec)

    lbl_viterbi = ttk.Label   (frm_dvb_options, text="Viterbi")
    chk_viterbi = Checkbutton (frm_dvb_options, variable=viterbi)
    lbl_viterbi.grid (row=3, column=0, sticky=E)
    chk_viterbi.grid (row=3, column=1, sticky=W)
    options_dvbs.append(lbl_viterbi)
    options_dvbs.append(chk_viterbi)

    lbl_hardmetric = ttk.Label   (frm_dvb_options, text="Hard-Metric")
    chk_hardmetric = Checkbutton (frm_dvb_options, variable=hardmetric)
    lbl_hardmetric.grid (row=4, column=0, sticky=E)
    chk_hardmetric.grid (row=4, column=1, sticky=W)
    options_dvbs.append(lbl_hardmetric)
    options_dvbs.append(chk_hardmetric)

    #----- tab_leandvb frm_dvb_options (DVB-S2) -----
    lbl_strongpls = ttk.Label   (frm_dvb_options, text="strongpls")
    chk_strongpls = Checkbutton (frm_dvb_options, variable=strongpls)
    lbl_strongpls.grid (row=1, column=0, sticky=E)
    chk_strongpls.grid (row=1, column=1, sticky=W)
    options_dvbs2.append(lbl_strongpls)
    options_dvbs2.append(chk_strongpls)

    lbl_modcods = ttk.Label (frm_dvb_options, text="modcods")
    ent_modcods = ttk.Entry (frm_dvb_options, width=10, textvariable=modcods)
    lb2_modcods = ttk.Label (frm_dvb_options, text="empty entry omits parameter")
    lbl_modcods.grid (row=2, column=0, sticky=E)
    ent_modcods.grid (row=2, column=1, sticky=W)
    lb2_modcods.grid (row=2, column=2, sticky=W)
    options_dvbs2.append(lbl_modcods)
    options_dvbs2.append(ent_modcods)
    options_dvbs2.append(lb2_modcods)

    lbl_framesizes = ttk.Label (frm_dvb_options, text="framesizes")
    ent_framesizes = ttk.Entry (frm_dvb_options, width=10, textvariable=framesizes)
    lb2_framesizes = ttk.Label (frm_dvb_options, text="empty entry omits parameter")
    lbl_framesizes.grid (row=3, column=0, sticky=E)
    ent_framesizes.grid (row=3, column=1, sticky=W)
    lb2_framesizes.grid (row=3, column=2, sticky=W)
    options_dvbs2.append(lbl_framesizes)
    options_dvbs2.append(ent_framesizes)
    options_dvbs2.append(lb2_framesizes)

    lbl_fastdrift = ttk.Label   (frm_dvb_options, text="fastdrift")
    chk_fastdrift = Checkbutton (frm_dvb_options, variable=fastdrift)
    lbl_fastdrift.grid (row=4, column=0, sticky=E)
    chk_fastdrift.grid (row=4, column=1, sticky=W)
    options_dvbs2.append(lbl_fastdrift)
    options_dvbs2.append(chk_fastdrift)

    lbl_ldpc_bf = ttk.Label (frm_dvb_options, text="max. LDPC bitflips")
    ent_ldpc_bf = ttk.Entry (frm_dvb_options, width=10, textvariable=ldpc_bf)
    lbl_ldpc_bf.grid (row=5, column=0, sticky=E)
    ent_ldpc_bf.grid (row=5, column=1, sticky=W)
    options_dvbs2.append(lbl_ldpc_bf)
    options_dvbs2.append(ent_ldpc_bf)

    lbl_nhelpers = ttk.Label (frm_dvb_options, text="Number of decoders")
    ent_nhelpers = ttk.Entry (frm_dvb_options, width=10, textvariable=nhelpers)
    lbl_nhelpers.grid (row=6, column=0, sticky=E)
    ent_nhelpers.grid (row=6, column=1, sticky=W)
    options_dvbs2.append(lbl_nhelpers)
    options_dvbs2.append(ent_nhelpers)

    #----- buttons -----
    btn_save   = ttk.Button (dlg, text="save",   command=on_save)
    btn_cancel = ttk.Button (dlg, text="cancel", command=on_cancel)

    #----- packing of widgets -----
    dlg.columnconfigure((0,1), pad=4, weight=1)
    dlg.rowconfigure   ((0,1), pad=4, weight=0)
    ntb       .grid (row=0, column=0, columnspan=2)
    btn_save  .grid (row=1, column=0)
    btn_cancel.grid (row=1, column=1)

    tab_general.columnconfigure((0,1),   pad=4, weight=1)
    tab_general.rowconfigure   ((0,1,2), pad=4, weight=0)
    lbl_general.grid(row=0, column=0, sticky=N, columnspan=4, pady=6)
    lbl_viewer .grid (row=1, column=0, sticky=E)
    ent_viewer .grid (row=1, column=1, sticky=W)
    lbl_lnblo  .grid (row=2, column=0, sticky=E)
    ent_lnblo  .grid (row=2, column=1, sticky=W)

    tab_files.columnconfigure((0,1,2), pad=4, weight=1)
    tab_files.rowconfigure   ((0,1,2), pad=4, weight=0)
    lbl_files          .grid (row=0, column=0, sticky=N, columnspan=4, pady=6)
    lbl_leansdr_file   .grid (row=1, column=0, sticky=E)
    ent_leansdr_file   .grid (row=1, column=1, sticky=W)
    lbl_ldpchelper_file.grid (row=2, column=0, sticky=E)
    ent_ldpchelper_file.grid (row=2, column=1, sticky=W)

    tab_rtlsdr.columnconfigure((0,2,3),     pad=4, weight=1)
    tab_rtlsdr.rowconfigure   ((0,1,2,3,4), pad=4, weight=0)
    lbl_rtlsdr   .grid (row=0, column=0, sticky=N, columnspan=4, pady=6)
    lbl_ppm      .grid (row=1, column=0, sticky=E)
    lb2_ppm      .grid (row=1, column=1, sticky=E)
    ent_ppm      .grid (row=1, column=2, sticky=W)
    lb3_ppm      .grid (row=1, column=3, sticky=W)
    lbl_gain     .grid (row=2, column=0, sticky=E)
    lb2_gain     .grid (row=2, column=1, sticky=E)
    ent_gain     .grid (row=2, column=2, sticky=W)
    lb3_gain     .grid (row=2, column=3, sticky=W)
    lbl_rtldongle.grid (row=3, column=0, sticky=E)
    lb2_rtldongle.grid (row=3, column=1, sticky=E)
    ent_rtldongle.grid (row=3, column=2, sticky=W)
    lb3_rtldongle.grid (row=3, column=3, sticky=W)

    set_visibility_dvb_options(None)

#===== root window ============================================================

root = Tk()

#----- window properties -----
root.title('LeanDVB DVBS + DVBS2 interface')
root.resizable(height = False, width = False)
frm_root = ttk.Frame(root, borderwidth=8)
frm_root.pack()

#----- initialize dictionary -----
if os.path.isfile(parameters_file):
    parameters_load()
else:
    parameters_default()

#----- user interface variables -----
fastlock       = IntVar()
viterbi        = IntVar()
hardmetric     = IntVar()
gui            = IntVar()
maxprocess     = IntVar()
ppm            = IntVar()
padlean        = StringVar()
gain           = IntVar()
rtldongle      = IntVar()
viewer         = StringVar()
rolloff_factor = StringVar()
rrc_rej_factor = IntVar()
nhelpers       = IntVar()
inpipe         = IntVar()
modcods        = StringVar()
framesizes     = StringVar()
lnblo          = DoubleVar()
frequency      = DoubleVar()
samplerate     = IntVar()
fec            = StringVar()
tune           = StringVar()
bandwidth      = IntVar()
standard       = StringVar()
sampler        = StringVar()
strongpls      = IntVar()
fastdrift      = IntVar()
ldpc_bf        = IntVar()
ldpc_helper    = StringVar()
const          = StringVar()

#----- user interface action functions -----
def on_start():
    opt_standard     = standard.get()
    ppmvalue         = int(ppm.get())
    leanpad          = padlean.get()
    gain_value       = gain.get()
    rolloff          = rolloff_factor.get()
    rrcrej           = rrc_rej_factor.get()
    nhelpers_value   = nhelpers.get()
    inpip            = inpipe.get()
    modcods_value    = modcods.get()
    framesizes_value = framesizes.get()
    bandwidth_value  = int(bandwidth.get()) * 1000
    if (viewer.get() == "ffplay"):
        view = "ffplay -v 0"
    else:
        view = "mplayer"
    if (fastlock.get() == True):
        opt_fastlock = " --fastlock"
    else:
        opt_fastlock = ""
    if (viterbi.get() == True):
        opt_viterbi = " --viterbi"
    else:
        opt_viterbi = ""
    if (gui.get() == True):
        opt_gui = " --gui"
    else:
        opt_gui = ""
    if (maxprocess.get() == True):
        opt_maxprocess = " --hq"
    else:
        opt_maxprocess = ""
    if (hardmetric.get() == True):
        opt_hardmetric = " --hard-metric"
    else:
        opt_hardmetric = ""
    if (modcods_value == ""):
        modcods_string = ""
    else:
        modcods_string = " --modcods " + modcods_value
    if (framesizes_value == ""):
        framesizes_string = ""
    else:
        framesizes_string = " --framesizes " + framesizes_value
    if (strongpls.get() == True):
        opt_strongpls = " --strongpls"
    else:
        opt_strongpls = ""
    if (fastdrift.get() == True):
        opt_fastdrift = " --fastdrift"
    else:
        opt_fastdrift = ""
    frequency_value   = int( ( float(frequency.get()) - float(lnblo.get()) ) * 1000000 )
    samplerate_value  = int(samplerate.get()) * 1000
    fec_value         = fec.get()
    tune_value        = tune.get()
    rtl               = rtldongle.get()
    ldpc_bf_value     = ldpc_bf.get()
    ldpc_helper_value = ldpc_helper.get()
    const_value       = const.get()
    if (opt_standard == "DVB-S2"):
        sub = "rtl_sdr" + \
              " -d " + str(rtl) + \
              " -f " + str(frequency_value) + \
              " -g " + str(gain_value) +  \
              " -s " + str(bandwidth_value) + \
              " -p " + str(ppmvalue) + \
              " -" + \
              " | " + \
              leanpad + "leandvb" + \
              opt_gui + \
              modcods_string + \
              framesizes_string + \
              opt_maxprocess + \
              opt_strongpls + \
              opt_fastdrift + \
              opt_hardmetric + \
              opt_fastlock + \
              " --tune " + tune_value + \
              " --standard " + opt_standard + \
              " --ldpc-bf " + str(ldpc_bf_value) + \
              " --ldpc-helper " + leanpad + ldpc_helper_value + \
              " --inpipe " + str(inpip) + \
              " --nhelpers " + str(nhelpers_value) + \
              " --sampler rrc" + \
              " --rrc-rej " + str(rrcrej) + \
              " -v" + \
              " --roll-off " + rolloff + \
              " --sr " + str(samplerate_value) + \
              " -f " + str(bandwidth_value) + \
              " | " + \
              "ffplay -v 0 -" + \
              " \n"
    else:
        sub = "rtl_sdr" + \
              " -d " + str(rtl) + \
              " -f " + str(frequency_value) + \
              " -g " + str(gain_value) +  \
              " -s " + str(bandwidth_value) + \
              " -p " + str(ppmvalue) + \
              " -" + \
              " | " + \
              leanpad + "leandvb" + \
              opt_gui + \
              opt_maxprocess + \
              opt_viterbi + \
              opt_hardmetric + \
              opt_fastlock + \
              " --tune " + tune_value + \
              " --standard " + opt_standard + \
              " --const " + const_value + \
              " --cr " + fec_value + \
              " -v" + \
              " --sr " + str(samplerate_value) + \
              " -f " + str(bandwidth_value) + \
              " | " + \
              view + " -" + \
              " \n"

    print sub

    parameters_save()

    file = open(run_script, "w")
    file.write("#!/bin/sh \n\n")
    file.write("\n\n")
    file.write(sub)
    file.close()
    os.system("sh " + run_script + " &")

def on_stop():
    file = open(stop_script, "w")
    file.write("#!/bin/sh \n")
    file.write("\n")
    file.write("killall rtl_sdr\n")
    file.write("killall ffplay\n")
    file.write("killall leandvb\n")
    file.write("killall basicRX\n")
    file.write("\n")
    file.write("exit 0\n")
    file.close()
    os.system("sh " + stop_script)

def on_exit():
    parameters_save()
    on_stop()
    root.destroy()

#----- user interface content -----
lbl_frequency  = ttk.Label   (frm_root, text="Frequency")
cmb_frequency  = ttk.Combobox(frm_root, width=10, textvariable=frequency)
cmb_frequency  ["values"] = ("10491.500","1252","1257","1260","436","437","1255","1252.600","1280","1250","1253")
lb2_frequency  = ttk.Label   (frm_root, text="MHz")
lbl_samplerate = ttk.Label   (frm_root, text="Samplerate")
cmb_samplerate = ttk.Combobox(frm_root, width=10, textvariable=samplerate)
cmb_samplerate ["values"] = ("33","66","125","150","250","333","400","500","600","750","1000","1500","2000","2083","3000","4000","4340","5000")
lb2_samplerate = ttk.Label   (frm_root, text="S/R")
lbl_fec        = ttk.Label   (frm_root, text="FEC")
cmb_fec        = ttk.Combobox(frm_root, width=10, textvariable=fec)
cmb_fec        ["values"] = ("1/2","2/3","3/4","5/6","6/7","7/8")
lb2_fec        = ttk.Label   (frm_root, text="Div")
lbl_tune       = ttk.Label   (frm_root, text="Tune")
cmb_tune       = ttk.Combobox(frm_root, width=10, textvariable=tune)
cmb_tune       ["values"] = ("100","500","1000","2000","5000","10000","-100","-500","-1000","-2000","-5000","-10000")
lb2_tune       = ttk.Label   (frm_root, text="Hz")
lbl_bandwidth  = ttk.Label   (frm_root, text="Bandwidth")
cmb_bandwidth  = ttk.Combobox(frm_root, width=10, textvariable=bandwidth)
cmb_bandwidth  ["values"] = ("2400","2000","1000","500")
lb2_bandwidth  = ttk.Label   (frm_root, text="kHz")
lbl_separator  = Frame       (frm_root, height=1, bg="black")
chk_sensitive  = Checkbutton (frm_root, text="Max sensitive", variable=maxprocess)
btn_start      = ttk.Button  (frm_root, text='START',         command=on_start)
btn_settings   = ttk.Button  (frm_root, text='Settings',      command=dlg_settings)
btn_stop       = ttk.Button  (frm_root, text='STOP',          command=on_stop)
btn_exit       = ttk.Button  (frm_root, text='EXIT',          command=on_exit)
if os.path.isfile("logo.png"):
    img_logo = PhotoImage(file="logo.png")
else:
    img_logo = None
lbl_logo = Label(frm_root, image=img_logo)

#----- user interface packing -----
lbl_frequency .grid (row=0, column=0, sticky=W, padx=5)
cmb_frequency .grid (row=0, column=1, sticky=W)
lb2_frequency .grid (row=0, column=2, sticky=W, padx=5)
lbl_logo      .grid (row=0, column=3, sticky=W+E+N+S, columnspan=2, rowspan=5, padx=5, pady=5)
lbl_samplerate.grid (row=1, column=0, sticky=W, padx=5)
cmb_samplerate.grid (row=1, column=1, sticky=W)
lb2_samplerate.grid (row=1, column=2, sticky=W, padx=5)
lbl_fec       .grid (row=2, column=0, sticky=W, padx=5)
cmb_fec       .grid (row=2, column=1, sticky=W)
lb2_fec       .grid (row=2, column=2, sticky=W, padx=5)
lbl_tune      .grid (row=3, column=0, sticky=W, padx=5)
cmb_tune      .grid (row=3, column=1, sticky=W)
lb2_tune      .grid (row=3, column=2, sticky=W, padx=5)
lbl_bandwidth .grid (row=4, column=0, sticky=W, padx=5)
cmb_bandwidth .grid (row=4, column=1, sticky=W)
lb2_bandwidth .grid (row=4, column=2, sticky=W, padx=5)
lbl_separator .grid (row=5, column=0, sticky=EW, columnspan=6, pady=8)
btn_start     .grid (row=6, column=3)
btn_settings  .grid (row=6, column=4)
chk_sensitive .grid (row=7, column=2, sticky=W)
btn_stop      .grid (row=7, column=3)
btn_exit      .grid (row=7, column=4)

cmb_frequency.focus_set()

bandwidth     .set(parameters["bandwidth"])
tune          .set(parameters["tune"])
fec           .set(parameters["fec"])
samplerate    .set(parameters["samplerate"])
frequency     .set(parameters["frequency"])
ppm           .set(parameters["ppm"])
padlean       .set(parameters["leanpad"])
gain          .set(parameters["gain"])
rtldongle     .set(parameters["rtldongle"])
fastlock      .set(parameters["fastlock"])
viterbi       .set(parameters["viterbi"])
hardmetric    .set(parameters["hardmetric"])
gui           .set(parameters["gui"])
maxprocess    .set(parameters["maxprocess"])
viewer        .set(parameters["viewer"])
rolloff_factor.set(parameters["rolloff_factor"])
rrc_rej_factor.set(parameters["rrc_rej_factor"])
nhelpers      .set(parameters["nhelpers"])
inpipe        .set(parameters["inpipe"])
modcods       .set(parameters["modcods"])
framesizes    .set(parameters["framesizes"])
lnblo         .set(parameters["lnb_lo"])
standard      .set(parameters["standard"])
sampler       .set(parameters["sampler"])
strongpls     .set(parameters["strongpls"])
fastdrift     .set(parameters["fastdrift"])
ldpc_bf       .set(parameters["ldpc_bf"])
ldpc_helper   .set(parameters["ldpc_helper"])
const         .set(parameters["constellation"])

#----- stop user interface -----
root.protocol("WM_DELETE_WINDOW", on_exit)

#----- start user interface -----
mainloop()

