#!/usr/bin/env python

# Simple UI voor LEANDVB, DVBS receiver.
# requires sudo apt-get install python-imaging-tk package
# keep everything in your home directory
# if you add a 180x180 pixels file called logo.png it will be
# showed in right corner.
# Leandvb by F4DAV (github leansdr)
# Wrapper by pe2jko@540.org

# TODO improve entries for path and filenames in settings
# TODO leandvb-run as function like leandvb-stop
# TODO leandvb: --tune is broken, use --derotate instead
# TODO streamline usage of viewer ffplay and mplayer
# TODO 'cancel' in settings not working propperly

from Tkinter import *
import ttk
import os
import json

# set directory for auxiliary files (settings, run, stop)
home            = os.path.expanduser("~/")
aux_dir         = os.path.expanduser("~/") + ".leandvb-GUI/"
parameters_file = aux_dir + "parameters.json"
run_script      = aux_dir + "run.sh"
stop_script     = aux_dir + "stop.sh"

if not os.path.exists(aux_dir):
    print "create " + aux_dir
    os.mkdir(aux_dir)

print "Home directory      : " + home
print "auxilliary directory: " + aux_dir
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
    parameters["symbolrate"    ] = int(symbolrate.get())
    parameters["fec"           ] = fec.get()
    parameters["tune"          ] = int(tune.get())
    parameters["fastlock"      ] = bool(fastlock.get())
    parameters["bandwidth"     ] = int(bandwidth.get())
    parameters["viterbi"       ] = bool(viterbi.get())
    parameters["gui"           ] = bool(gui.get())
    parameters["maxsens"       ] = bool(maxsens.get())
    parameters["hardmetric"    ] = bool(hardmetric.get())
    parameters["leandvb_path"  ] = leandvb_path.get()
    parameters["ppm"           ] = int(ppm.get())
    parameters["gain"          ] = gain.get()
    parameters["viewer"        ] = viewer.get()
    parameters["rolloff"       ] = float(rolloff.get())
    parameters["rrcrej"        ] = float(rrcrej.get())
    parameters["nhelpers"      ] = int(nhelpers.get())
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
    parameters["debug"         ] = debug.get()

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
    parameters["symbolrate"    ] = 1500
    parameters["fec"           ] = "1/2"
    parameters["tune"          ] = 0
    parameters["fastlock"      ] = False
    parameters["bandwidth"     ] = 2400
    parameters["viterbi"       ] = False
    parameters["gui"           ] = True
    parameters["maxsens"       ] = False
    parameters["hardmetric"    ] = False
    parameters["leanpad"       ] = home+"leansdr/src/apps/"
    parameters["ppm"           ] = 0
    parameters["gain"          ] = 36
    parameters["viewer"        ] = "ffplay"
    parameters["rolloff"       ] = 0.35
    parameters["rrcrej"        ] = 30.0
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
    parameters["debug"         ] = "all"

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
    tab_files.columnconfigure((0),     pad=4, weight=1)
    tab_files.rowconfigure   ((0,1,2), pad=4, weight=0)

        #----- label -----
    lbl_files = ttk.Label(tab_files, text="Setting of files and directories")
    lbl_files.grid (row=0, column=0, columnspan=2)

    lbl_files_separator = Frame (tab_files, height=1, bg="grey")
    lbl_files_separator.grid (row=1, column=0, columnspan=2, sticky=EW)

        #----- leandvb -----
    frm_files_leandvb = ttk.LabelFrame (tab_files, text="leandvb", borderwidth=2, padding=4)
    frm_files_leandvb.grid (row=2, column=0, sticky=N)

    lbl_leandvb_path = ttk.Label(frm_files_leandvb, text="Path : ")
    ent_leandvb_path = ttk.Entry(frm_files_leandvb, width=40, textvariable=leandvb_path)
    lbl_leandvb_path.grid (row=0, column=0, sticky=W)
    ent_leandvb_path.grid (row=0, column=1, sticky=W)

    lbl_leandvb_file = ttk.Label(frm_files_leandvb, text="File : ")
    ent_leandvb_file = ttk.Entry(frm_files_leandvb, width=20, textvariable=leandvb_file)
    lbl_leandvb_file.grid (row=1, column=0, sticky=W)
    ent_leandvb_file.grid (row=1, column=1, sticky=W)

        #----- LDCP helper -----
    frm_files_ldcphelper = ttk.LabelFrame (tab_files, text="LDCP helper", borderwidth=2, padding=4)
    frm_files_ldcphelper.grid (row=3, column=0, sticky=N)

    lbl_ldpchelper_path = ttk.Label(frm_files_ldcphelper, text="Path : ")
    ent_ldpchelper_path = ttk.Entry(frm_files_ldcphelper, width=40, textvariable=ldpchelper_path)
    lbl_ldpchelper_path.grid (row=0, column=0, sticky=W)
    ent_ldpchelper_path.grid (row=0, column=1, sticky=W)

    lbl_ldpchelper_file = ttk.Label(frm_files_ldcphelper, text="File : ")
    ent_ldpchelper_file = ttk.Entry(frm_files_ldcphelper, width=20, textvariable=ldpchelper_file)
    lbl_ldpchelper_file.grid (row=1, column=0, sticky=W)
    ent_ldpchelper_file.grid (row=1, column=1, sticky=W)

        #----- rtl_sdr -----

        #----- viewer -----

        #----- settings -----


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
    lbl_leandvb.grid (row=0, column=0, columnspan=3)

    lbl_leandvb_separator = Frame (tab_leandvb, height=1, bg="grey")
    lbl_leandvb_separator.grid (row=1, column=0, columnspan=3, sticky=EW)

        #----- frame 'common options' -----
    frm_common_options = ttk.Frame (tab_leandvb, borderwidth=4, padding=4)
    frm_common_options.grid (row=2, column=0, sticky=N)

        #----- frame 'dvb options' -----
    frm_dvb_options = ttk.Frame (tab_leandvb, borderwidth=4, padding=4)
    frm_dvb_options.grid (row=2, column=1, sticky=N)
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

    lbl_rolloff = ttk.Label (frm_common_options,           text="roll off")
    ent_rolloff = ttk.Entry (frm_common_options, width=10, textvariable=rolloff)
    lbl_rolloff.grid (row=2, column=0, sticky=W)
    ent_rolloff.grid (row=2, column=1, sticky=W)

    lbl_rrcrej = ttk.Label (frm_common_options,           text="rrc rej")
    ent_rrcrej = ttk.Entry (frm_common_options, width=10, textvariable=rrcrej)
    lbl_rrcrej.grid (row=3, column=0, sticky=W)
    ent_rrcrej.grid (row=3, column=1, sticky=W)

    lbl_fastlock = ttk.Label (frm_common_options, text="fastlock")
    chk_fastlock = Checkbutton (frm_common_options, variable=fastlock)
    lbl_fastlock.grid (row=4, column=0, sticky=W)
    chk_fastlock.grid (row=4, column=1, sticky=W)

    lbl_sensitivity = ttk.Label (frm_common_options, text="max sensitivity")
    chk_sensitivity = Checkbutton (frm_common_options, variable=maxsens)
    lbl_sensitivity.grid (row=5, column=0, sticky=W)
    chk_sensitivity.grid (row=5, column=1, sticky=W)

    lbl_debug = ttk.Label (frm_common_options, text="debug info")
    cmb_debug = ttk.Combobox(frm_common_options, width=10, textvariable=debug, state="readonly")
    cmb_debug ["values"] = ("all","operation","startup","none")
    lbl_debug.grid (row=6, column=0, sticky=W)
    cmb_debug.grid (row=6, column=1, sticky=W)

    lbl_gui = ttk.Label (frm_common_options, text="GUI")
    chk_gui = Checkbutton (frm_common_options, variable=gui)
    lbl_gui.grid (row=7, column=0, sticky=W)
    chk_gui.grid (row=7, column=1, sticky=W)

    #----- tab_leandvb frm_dvb_options (control) -----
    lbl_standard = ttk.Label    (frm_dvb_options, text="DVB standard")
    cmb_standard = ttk.Combobox (frm_dvb_options, width=10, textvariable=standard, state="readonly")
    cmb_standard ["values"] = ("DVB-S","DVB-S2")
    cmb_standard.bind("<<ComboboxSelected>>", set_visibility_dvb_options)
    lbl_standard.grid (row=0, column=0, sticky=W)
    cmb_standard.grid (row=0, column=1, sticky=W)

    #----- tab_leandvb frm_dvb_options (DVB-S) -----
    lbl_const = ttk.Label    (frm_dvb_options, text="constellation")
    cmb_const = ttk.Combobox (frm_dvb_options, width=10, textvariable=const, state="readonly")
    cmb_const ["values"] = ("QPSK","BPSK")
    lbl_const.grid (row=1, column=0, sticky=W)
    cmb_const.grid (row=1, column=1, sticky=W)
    options_dvbs.append(lbl_const)
    options_dvbs.append(cmb_const)

    lbl_fec = ttk.Label   (frm_dvb_options, text="code rate")
    cmb_fec = ttk.Combobox(frm_dvb_options, width=10, textvariable=fec, state="readonly")
    cmb_fec ["values"] = ("1/2","2/3","3/4","5/6","6/7","7/8")
    lbl_fec.grid (row=2, column=0, sticky=W)
    cmb_fec.grid (row=2, column=1, sticky=W)
    options_dvbs.append(lbl_fec)
    options_dvbs.append(cmb_fec)

    lbl_viterbi = ttk.Label   (frm_dvb_options, text="viterbi")
    chk_viterbi = Checkbutton (frm_dvb_options, variable=viterbi)
    lbl_viterbi.grid (row=3, column=0, sticky=W)
    chk_viterbi.grid (row=3, column=1, sticky=W)
    options_dvbs.append(lbl_viterbi)
    options_dvbs.append(chk_viterbi)

    lbl_hardmetric = ttk.Label   (frm_dvb_options, text="hard-metric")
    chk_hardmetric = Checkbutton (frm_dvb_options, variable=hardmetric)
    lbl_hardmetric.grid (row=4, column=0, sticky=W)
    chk_hardmetric.grid (row=4, column=1, sticky=W)
    options_dvbs.append(lbl_hardmetric)
    options_dvbs.append(chk_hardmetric)

    #----- tab_leandvb frm_dvb_options (DVB-S2) -----
    lbl_strongpls = ttk.Label   (frm_dvb_options, text="strongpls")
    chk_strongpls = Checkbutton (frm_dvb_options, variable=strongpls)
    lbl_strongpls.grid (row=1, column=0, sticky=W)
    chk_strongpls.grid (row=1, column=1, sticky=W)
    options_dvbs2.append(lbl_strongpls)
    options_dvbs2.append(chk_strongpls)

    lbl_modcods = ttk.Label (frm_dvb_options, text="modcods")
    ent_modcods = ttk.Entry (frm_dvb_options, width=10, textvariable=modcods)
    lb2_modcods = ttk.Label (frm_dvb_options, text="empty entry omits parameter")
    lbl_modcods.grid (row=2, column=0, sticky=W)
    ent_modcods.grid (row=2, column=1, sticky=W)
    lb2_modcods.grid (row=2, column=2, sticky=W)
    options_dvbs2.append(lbl_modcods)
    options_dvbs2.append(ent_modcods)
    options_dvbs2.append(lb2_modcods)

    lbl_framesizes = ttk.Label (frm_dvb_options, text="framesizes")
    ent_framesizes = ttk.Entry (frm_dvb_options, width=10, textvariable=framesizes)
    lb2_framesizes = ttk.Label (frm_dvb_options, text="empty entry omits parameter")
    lbl_framesizes.grid (row=3, column=0, sticky=W)
    ent_framesizes.grid (row=3, column=1, sticky=W)
    lb2_framesizes.grid (row=3, column=2, sticky=W)
    options_dvbs2.append(lbl_framesizes)
    options_dvbs2.append(ent_framesizes)
    options_dvbs2.append(lb2_framesizes)

    lbl_fastdrift = ttk.Label   (frm_dvb_options, text="fastdrift")
    chk_fastdrift = Checkbutton (frm_dvb_options, variable=fastdrift)
    lbl_fastdrift.grid (row=4, column=0, sticky=W)
    chk_fastdrift.grid (row=4, column=1, sticky=W)
    options_dvbs2.append(lbl_fastdrift)
    options_dvbs2.append(chk_fastdrift)

    lbl_ldpc_bf = ttk.Label (frm_dvb_options, text="max. LDPC bitflips")
    ent_ldpc_bf = ttk.Entry (frm_dvb_options, width=10, textvariable=ldpc_bf)
    lbl_ldpc_bf.grid (row=5, column=0, sticky=W)
    ent_ldpc_bf.grid (row=5, column=1, sticky=W)
    options_dvbs2.append(lbl_ldpc_bf)
    options_dvbs2.append(ent_ldpc_bf)

    lbl_nhelpers = ttk.Label (frm_dvb_options, text="number of decoders")
    ent_nhelpers = ttk.Entry (frm_dvb_options, width=10, textvariable=nhelpers)
    lbl_nhelpers.grid (row=6, column=0, sticky=W)
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

#----- initialize parameters dictionary -----
if os.path.isfile(parameters_file):
    parameters_load()
else:
    parameters_default()

#----- user interface variables -----
fastlock       = IntVar()
viterbi        = IntVar()
hardmetric     = IntVar()
gui            = IntVar()
maxsens        = IntVar()
rolloff        = DoubleVar()
rrcrej         = DoubleVar()
nhelpers       = IntVar()
inpipe         = IntVar()
modcods        = StringVar()
framesizes     = StringVar()
fec            = StringVar()
tune           = IntVar()
bandwidth      = IntVar()
standard       = StringVar()
sampler        = StringVar()
strongpls      = IntVar()
fastdrift      = IntVar()
ldpc_bf        = IntVar()
ldpc_helper    = StringVar()
const          = StringVar()
debug          = StringVar()
ppm            = IntVar()
leandvb_path   = StringVar()
leandvb_file   = StringVar()
ldpchelper_path= StringVar()
ldpchelper_file= StringVar()
gain           = IntVar()
rtldongle      = IntVar()
frequency      = DoubleVar()
symbolrate     = IntVar()
lnblo          = DoubleVar()
viewer         = StringVar()

#----- user interface action functions -----
def on_start():
    opt_inpipe     = " --inpipe "   + str(inpipe.get())
    opt_sampler    = " --sampler "  + sampler.get()
    opt_rolloff    = " --roll-off " + str(rolloff.get())
    opt_rrcrej     = " --rrc-rej "  + str(rrcrej.get())
    opt_bandwidth  = " -f "         + str(bandwidth.get() * 1000)
    opt_symbolrate = " --sr "       + str(symbolrate.get() * 1000)
    opt_tune       = " --tune "     + str(tune.get())
    opt_standard   = " --standard " + standard.get()
    opt_fastlock   = " --fastlock" if fastlock.get() == True else ""
    opt_gui        = " --gui"      if gui.get()      == True else ""
    opt_maxsens    = " --hq"       if maxsens.get()  == True else ""
    opt_const      = (" --const " + const.get())                   if standard.get() == "DVB-S" else ""
    opt_fec        = (" --cr "    + fec.get()  )                   if standard.get() == "DVB-S" else ""
    opt_viterbi    = " --viterbi"     if viterbi.get()    == True and standard.get() == "DVB-S" else ""
    opt_hardmetric = " --hard-metric" if hardmetric.get() == True and standard.get() == "DVB-S" else ""
    opt_strongpls  = " --strongpls"   if strongpls.get()  == True and standard.get() == "DVB-S2" else ""
    opt_modcods    = (" --modcods "    + modcods.get())    if modcods.get()    != "" and standard.get() == "DVB-S2" else ""
    opt_framesizes = (" --framesizes " + framesizes.get()) if framesizes.get() != "" and standard.get() == "DVB-S2" else ""
    opt_fastdrift  = " --fastdrift" if fastdrift.get() == True and standard.get() == "DVB-S2" else ""
    opt_ldpc_bf    = (" --ldpc-bf " + str(ldpc_bf.get()))       if standard.get() == "DVB-S2" else ""
    opt_nhelpers   = (" --nhelpers " + str(nhelpers.get()))     if standard.get() == "DVB-S2" else ""
    opt_ldpc_helper= " --ldpc-helper " + "\"" + ldpchelper_path.get() + ldpchelper_file.get() + "\""
    opt_debug_v    = " -v" if debug.get() == "all" or debug.get() == "startup"   else ""
    opt_debug_d    = " -d" if debug.get() == "all" or debug.get() == "operation" else ""

    if (viewer.get() == "ffplay"):
        view = "ffplay -v 0"
    else:
        view = "mplayer"

    leandvb_opt = opt_inpipe + opt_sampler + opt_rolloff + opt_rrcrej \
                + opt_bandwidth + opt_symbolrate + opt_tune + opt_standard \
                + opt_fastlock + opt_gui + opt_maxsens \
                + opt_const + opt_fec + opt_viterbi + opt_hardmetric \
                + opt_strongpls + opt_modcods + opt_framesizes + opt_fastdrift \
                + opt_ldpc_bf + opt_nhelpers + opt_ldpc_helper \
                + opt_debug_v + opt_debug_d
    leandvb_sub = "\"" + leandvb_path.get() + leandvb_file.get() + "\"" + leandvb_opt
    print
    print "leandvb:" + leandvb_sub

    sub = "rtl_sdr" + \
          " -d " + str( rtldongle.get() ) + \
          " -f " + str( int( ( float(frequency.get()) - float(lnblo.get()) ) * 1000000 ) ) + \
          " -g " + str( gain.get() ) +  \
          " -s " + str( bandwidth.get() * 1000) + \
          " -p " + str( ppm.get() ) + \
          " -" + \
          " | " + \
          leandvb_sub + \
          " | " + \
          view + " -" + \
          " \n"

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
lbl_symbolrate = ttk.Label   (frm_root, text="Symbolrate")
cmb_symbolrate = ttk.Combobox(frm_root, width=10, textvariable=symbolrate)
cmb_symbolrate ["values"] = ("33","66","125","150","250","333","400","500","600","750","1000","1500","2000","2083","3000","4000","4340","5000")
lb2_symbolrate = ttk.Label   (frm_root, text="kHz")
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
lbl_separator  = Frame       (frm_root, height=1, bg="grey")
btn_start      = ttk.Button  (frm_root, text='START',         command=on_start)
btn_settings   = ttk.Button  (frm_root, text='Settings',      command=dlg_settings)
btn_stop       = ttk.Button  (frm_root, text='STOP',          command=on_stop)
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
lbl_symbolrate.grid (row=1, column=0, sticky=W, padx=5)
cmb_symbolrate.grid (row=1, column=1, sticky=W)
lb2_symbolrate.grid (row=1, column=2, sticky=W, padx=5)
lbl_fec       .grid (row=2, column=0, sticky=W, padx=5)
cmb_fec       .grid (row=2, column=1, sticky=W)
lb2_fec       .grid (row=2, column=2, sticky=W, padx=5)
lbl_tune      .grid (row=3, column=0, sticky=W, padx=5)
cmb_tune      .grid (row=3, column=1, sticky=W)
lb2_tune      .grid (row=3, column=2, sticky=W, padx=5)
lbl_bandwidth .grid (row=4, column=0, sticky=W, padx=5)
cmb_bandwidth .grid (row=4, column=1, sticky=W)
lb2_bandwidth .grid (row=4, column=2, sticky=W, padx=5)
lbl_separator .grid (row=5, column=0, sticky=EW, columnspan=6, pady=6)
btn_start     .grid (row=6, column=0)
btn_stop      .grid (row=6, column=1)
btn_settings  .grid (row=6, column=3, columnspan=2)

cmb_frequency.focus_set()

bandwidth      .set(parameters["bandwidth"])
tune           .set(parameters["tune"])
fec            .set(parameters["fec"])
symbolrate     .set(parameters["symbolrate"])
frequency      .set(parameters["frequency"])
ppm            .set(parameters["ppm"])
leandvb_path   .set(parameters["leandvb_path"])
leandvb_file   .set(parameters["leandvb_file"])
gain           .set(parameters["gain"])
rtldongle      .set(parameters["rtldongle"])
fastlock       .set(parameters["fastlock"])
viterbi        .set(parameters["viterbi"])
hardmetric     .set(parameters["hardmetric"])
gui            .set(parameters["gui"])
maxsens        .set(parameters["maxsens"])
viewer         .set(parameters["viewer"])
rolloff        .set(parameters["rolloff"])
rrcrej         .set(parameters["rrcrej"])
nhelpers       .set(parameters["nhelpers"])
inpipe         .set(parameters["inpipe"])
modcods        .set(parameters["modcods"])
framesizes     .set(parameters["framesizes"])
lnblo          .set(parameters["lnb_lo"])
standard       .set(parameters["standard"])
sampler        .set(parameters["sampler"])
strongpls      .set(parameters["strongpls"])
fastdrift      .set(parameters["fastdrift"])
ldpc_bf        .set(parameters["ldpc_bf"])
ldpchelper_path.set(parameters["ldpchelper_path"])
ldpchelper_file.set(parameters["ldpchelper_file"])
const          .set(parameters["constellation"])
debug          .set(parameters["debug"])

#----- stop user interface -----
root.protocol("WM_DELETE_WINDOW", on_exit)

#----- start user interface -----
mainloop()

