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
    parameters["dvbs2"         ] = bool(dvbs.get())
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
    parameters["dvbs2"         ] = True
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

#===== settings dialog ========================================================

def dlg_settings():

    #----- action functions -----
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
    tab_leansdr = ttk.Frame (ntb, padding=10)

    ntb.add(tab_general, text="general")
    ntb.add(tab_files,   text="files")
    ntb.add(tab_rtlsdr,  text="rtl_sdr")
    ntb.add(tab_leansdr, text="leansdr")

    #----- tab_general -----
    lbl_general = ttk.Label(tab_general, text="General settings")
    lbl_viewer  = ttk.Label(tab_general,           text="Viewer : ")
    ent_viewer  = ttk.Entry(tab_general, width=10, textvariable=viewer)
    lbl_lnblo   = ttk.Label(tab_general,           text="LNB LO : ")
    ent_lnblo   = ttk.Entry(tab_general, width=10, textvariable=lnblo)

    #----- tab_files -----
    lbl_files        = ttk.Label(tab_files, text="Setting of files and directories")
    lbl_leansdr_file = ttk.Label(tab_files,           text="Path to leansdr : ")
    ent_leansdr_file = ttk.Entry(tab_files, width=40, textvariable=padlean)

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

    #----- tab_leansdr -----
    lbl_leansdr    = ttk.Label(tab_leansdr, text="Settings for leansdr program")
    lbl_inpipe     = ttk.Label(tab_leansdr,           text="Inpipe")
    lb2_inpipe     = ttk.Label(tab_leansdr,           text=" (--inpipe) : ")
    ent_inpipe     = ttk.Entry(tab_leansdr, width=10, textvariable=inpipe)
    lb3_inpipe     = ttk.Label(tab_leansdr,           text="DVBS2")
    lbl_rolloff    = ttk.Label(tab_leansdr,           text="Roll Off Factor")
    lb2_rolloff    = ttk.Label(tab_leansdr,           text=" (--roll-off) : ")
    ent_rolloff    = ttk.Entry(tab_leansdr, width=10, textvariable=rolloff_factor)
    lb3_rolloff    = ttk.Label(tab_leansdr,           text="DVBS2")
    lbl_rrcrej     = ttk.Label(tab_leansdr,           text="RRC Rej Factor")
    lb2_rrcrej     = ttk.Label(tab_leansdr,           text=" (--rrc-rej) : ")
    ent_rrcrej     = ttk.Entry(tab_leansdr, width=10, textvariable=rrc_rej_factor)
    lb3_rrcrej     = ttk.Label(tab_leansdr,           text="DVBS2")
    lbl_nhelpers   = ttk.Label(tab_leansdr,           text="Nhelpers")
    lb2_nhelpers   = ttk.Label(tab_leansdr,           text=" (--nhelpers) : ")
    ent_nhelpers   = ttk.Entry(tab_leansdr, width=10, textvariable=nhelpers)
    lb3_nhelpers   = ttk.Label(tab_leansdr,           text="DVBS2")
    lbl_modcods    = ttk.Label(tab_leansdr,           text="modcods")
    lb2_modcods    = ttk.Label(tab_leansdr,           text=" (--modcods) : ")
    ent_modcods    = ttk.Entry(tab_leansdr, width=10, textvariable=modcods)
    lb3_modcods    = ttk.Label(tab_leansdr,           text="empty entry omits parameter")
    lbl_framesizes = ttk.Label(tab_leansdr,           text="framesizes")
    lb2_framesizes = ttk.Label(tab_leansdr,           text=" (--framesizes) : ")
    ent_framesizes = ttk.Entry(tab_leansdr, width=10, textvariable=framesizes)
    lb3_framesizes = ttk.Label(tab_leansdr,           text="empty entry omits parameter")

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

    tab_files.columnconfigure((0,1), pad=4, weight=1)
    tab_files.rowconfigure   ((0,1), pad=4, weight=0)
    lbl_files       .grid (row=0, column=0, sticky=N, columnspan=4, pady=6)
    lbl_leansdr_file.grid (row=1, column=0, sticky=E)
    ent_leansdr_file.grid (row=1, column=1, sticky=W)

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

    tab_leansdr.columnconfigure((0,2,3),       pad=4, weight=1)
    tab_leansdr.rowconfigure   ((0,1,2,3,4,5), pad=4, weight=0)
    lbl_leansdr   .grid (row=0, column=0, sticky=N, columnspan=4, pady=6)
    lbl_inpipe    .grid (row=1, column=0, sticky=E)
    lb2_inpipe    .grid (row=1, column=1, sticky=E)
    ent_inpipe    .grid (row=1, column=2, sticky=W)
    lb3_inpipe    .grid (row=1, column=3, sticky=W)
    lbl_rolloff   .grid (row=2, column=0, sticky=E)
    lb2_rolloff   .grid (row=2, column=1, sticky=E)
    ent_rolloff   .grid (row=2, column=2, sticky=W)
    lb3_rolloff   .grid (row=2, column=3, sticky=W)
    lbl_rrcrej    .grid (row=3, column=0, sticky=E)
    lb2_rrcrej    .grid (row=3, column=1, sticky=E)
    ent_rrcrej    .grid (row=3, column=2, sticky=W)
    lb3_rrcrej    .grid (row=3, column=3, sticky=W)
    lbl_nhelpers  .grid (row=4, column=0, sticky=E)
    lb2_nhelpers  .grid (row=4, column=1, sticky=E)
    ent_nhelpers  .grid (row=4, column=2, sticky=W)
    lb3_nhelpers  .grid (row=4, column=3, sticky=W)
    lbl_modcods   .grid (row=5, column=0, sticky=E)
    lb2_modcods   .grid (row=5, column=1, sticky=E)
    ent_modcods   .grid (row=5, column=2, sticky=W)
    lb3_modcods   .grid (row=5, column=3, sticky=W)
    lbl_framesizes.grid (row=6, column=0, sticky=E)
    lb2_framesizes.grid (row=6, column=1, sticky=E)
    ent_framesizes.grid (row=6, column=2, sticky=W)
    lb3_framesizes.grid (row=6, column=3, sticky=W)

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
dvbs           = IntVar()
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

#----- user interface action functions -----
def on_start():
    ppmvalue         = int(ppm.get())
    leanpad          = padlean.get()
    gain_value       = gain.get()
    rolloff          = rolloff_factor.get()
    rrcrej           = rrc_rej_factor.get()
    nhelp            = nhelpers.get()
    inpip            = inpipe.get()
    modcods_value    = modcods.get()
    framesizes_value = framesizes.get()
    bandwidthvalue   = int(bandwidth.get()) * 1000
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
    if (dvbs.get() == True):
        opt_dvbs = "DVB-S2"
    else:
        opt_dvbs = "DVB-S"
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
    frequency_value  = int( ( float(frequency.get()) - float(lnblo.get()) ) * 1000000 )
    samplerate_value = int(samplerate.get()) * 1000
    fec_value        = fec.get()
    tune_value       = tune.get()
    rtl        = rtldongle.get()
    if (dvbs.get() == True): #dvbs2
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
              opt_viterbi + \
              opt_hardmetric + \
              opt_fastlock + \
              " --tune " + tune_value + \
              " --standard " + opt_dvbs + \
              " --ldpc-helper " + leanpad + "ldpc_tool" + \
              " --inpipe " + str(inpip) + \
              " --nhelpers " + str(nhelp) + \
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
              " --cr " + fec_value + \
              " --standard " + opt_dvbs + \
              " -v" + \
              " --sr " + str(samplerate_value) + \
              " -f " + str(bandwidth_value) + \
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
chk_fastlock   = Checkbutton (frm_root, text="Fastlock",      variable=fastlock)
chk_viterbi    = Checkbutton (frm_root, text="Viterbi",       variable=viterbi)
chk_hardmetric = Checkbutton (frm_root, text="Hard-Metric",   variable=hardmetric)
chk_gui        = Checkbutton (frm_root, text="Gui",           variable=gui)
chk_dvbs2      = Checkbutton (frm_root, text="DVBS-2",        variable=dvbs)
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
chk_fastlock  .grid (row=6, column=0, sticky=W)
chk_viterbi   .grid (row=6, column=1, sticky=W)
chk_hardmetric.grid (row=6, column=2, sticky=W)
btn_start     .grid (row=6, column=3)
btn_settings  .grid (row=6, column=4)
chk_gui       .grid (row=7, column=0, sticky=W)
chk_dvbs2     .grid (row=7, column=1, sticky=W)
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
dvbs          .set(parameters["dvbs2"])
maxprocess    .set(parameters["maxprocess"])
viewer        .set(parameters["viewer"])
rolloff_factor.set(parameters["rolloff_factor"])
rrc_rej_factor.set(parameters["rrc_rej_factor"])
nhelpers      .set(parameters["nhelpers"])
inpipe        .set(parameters["inpipe"])
modcods       .set(parameters["modcods"])
framesizes    .set(parameters["framesizes"])
lnblo         .set(parameters["lnb_lo"])

#----- stop user interface -----
root.protocol("WM_DELETE_WINDOW", on_exit)

#----- start user interface -----
mainloop()

