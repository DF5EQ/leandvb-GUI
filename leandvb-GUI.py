#!/usr/bin/env python

# Simple UI voor LEANDVB, DVBS receiver.
# requires sudo apt-get install python-imaging-tk package
# keeps parameters file and helper scripts in ~/.leandvb-GUI (see parameters_path)
# if you add a file called logo.png it will be shown on the right side
# Leandvb by F4DAV (github leansdr)
# Wrapper by pe2jko@540.org

# TODO place main window on bottom right of screen
# TODO output all 'print' to text-widget, code before root=tk() needs to be placed in GUI
# TODO remember last 10 frequencies
# TODO remember last 10 sybolrates
# TODO leandvb: --tune is broken, use --derotate instead
# TODO provide fast switching between sets of changable favorite settings

from Tkinter import *
from tkFileDialog import *
import ttk
import os
import json
from subprocess import *
import select
from signal import *

# settings for auxiliary files (parameters, run, stop)
parameters_path = os.path.expanduser("~/") + ".leandvb-GUI/"
parameters_file = parameters_path + "parameters.json"

# show settings for auxiliary files (parameters, run, stop)
print "parameters path:", parameters_path
print "parameters file:",  parameters_file

# create parameters path if not existend
if not os.path.exists(parameters_path):
    print "create " + parameters_path
    os.mkdir(parameters_path)

# check max pipe size and adjust if needed

max_needed = 32000000

fd = open("/proc/sys/fs/pipe-max-size", "r")
max_current = int(fd.readline())
fd.close()

if (max_current < max_needed):
    print "max pipe size  :", max_current, ", will be set to", max_needed
    cmd = "bash -c 'echo " + str(max_needed) + " > /proc/sys/fs/pipe-max-size'"
    os.system("pkexec " + cmd)
else:
    print "max pipe size  :", max_current, ", this is ok"

#===== handle parameters (save, load, default) ================================

parameters = dict()

def parameters_save():
    print "save parameters to file"
    parameters["frequency"      ] = float(frequency.get())
    parameters["symbolrate"     ] = int(symbolrate.get())
    parameters["fec"            ] = fec.get()
    parameters["tune"           ] = int(tune.get())
    parameters["fastlock"       ] = bool(fastlock.get())
    parameters["bandwidth"      ] = int(bandwidth.get())
    parameters["viterbi"        ] = bool(viterbi.get())
    parameters["gui"            ] = bool(gui.get())
    parameters["maxsens"        ] = bool(maxsens.get())
    parameters["hardmetric"     ] = bool(hardmetric.get())
    parameters["leandvb_path"   ] = leandvb_path.get()
    parameters["leandvb_file"   ] = leandvb_file.get()
    parameters["ppm"            ] = int(ppm.get())
    parameters["gain"           ] = gain.get()
    parameters["viewer_path"    ] = viewer_path.get()
    parameters["viewer_file"    ] = viewer_file.get()
    parameters["rolloff"        ] = float(rolloff.get())
    parameters["rrcrej"         ] = float(rrcrej.get())
    parameters["nhelpers"       ] = int(nhelpers.get())
    parameters["inpipe"         ] = inpipe.get()
    parameters["modcods"        ] = modcods.get()
    parameters["framesizes"     ] = framesizes.get()
    parameters["lnb_lo"         ] = lnblo.get()
    parameters["rtldongle"      ] = rtldongle.get()
    parameters["standard"       ] = standard.get()
    parameters["sampler"        ] = sampler.get()
    parameters["strongpls"      ] = bool(strongpls.get())
    parameters["fastdrift"      ] = bool(fastdrift.get())
    parameters["ldpc_bf"        ] = int(ldpc_bf.get())
    parameters["ldpchelper_path"] = ldpchelper_path.get()
    parameters["ldpchelper_file"] = ldpchelper_file.get()
    parameters["constellation"  ] = const.get()
    parameters["debug"          ] = debug.get()
    parameters["rtlsdr_path"    ] = rtlsdr_path.get()
    parameters["rtlsdr_file"    ] = rtlsdr_file.get()

    file = open(parameters_file, "w")
    file.write(json.dumps(parameters, indent=4, sort_keys=True))
    file.close()

def parameters_load():
    global parameters
    print "load parameters from file"
    file = open(parameters_file, "r")
    parameters = json.load(file)
    file.close()
    guivars_init()

def parameters_default():
    print "load parameters with defaults"
    parameters["frequency"      ] = 10491.500
    parameters["symbolrate"     ] = 1500
    parameters["fec"            ] = "1/2"
    parameters["tune"           ] = 0
    parameters["fastlock"       ] = False
    parameters["bandwidth"      ] = 2400
    parameters["viterbi"        ] = False
    parameters["gui"            ] = True
    parameters["maxsens"        ] = False
    parameters["hardmetric"     ] = False
    parameters["leandvb_path"   ] = "./"
    parameters["leandvb_file"   ] = "leandvb"
    parameters["ppm"            ] = 0
    parameters["gain"           ] = 36
    parameters["viewer_path"    ] = ""
    parameters["viewer_file"    ] = "ffplay -v 0"
    parameters["rolloff"        ] = 0.35
    parameters["rrcrej"         ] = 30.0
    parameters["nhelpers"       ] = 6
    parameters["inpipe"         ] = 32000000
    parameters["modcods"        ] = "0x0040"
    parameters["framesizes"     ] = "0x01"
    parameters["lnb_lo"         ] = 9750.0
    parameters["rtldongle"      ] = 0
    parameters["standard"       ] = "DVB-S2"
    parameters["sampler"        ] = "rrc"
    parameters["strongpls"      ] = False
    parameters["fastdrift"      ] = False
    parameters["ldpc_bf"        ] = 0
    parameters["ldpchelper_path"] = "./"
    parameters["ldpchelper_file"] = "ldpc_tool"
    parameters["constellation"  ] = "QPSK"
    parameters["debug"          ] = "all"
    parameters["rtlsdr_path"    ] = ""
    parameters["rtlsdr_file"    ] = "rtl_sdr"
    guivars_init()

def guivars_init():
    print "initialize GUI variables"
    bandwidth      .set(parameters["bandwidth"])
    const          .set(parameters["constellation"])
    debug          .set(parameters["debug"])
    fastdrift      .set(parameters["fastdrift"])
    fastlock       .set(parameters["fastlock"])
    fec            .set(parameters["fec"])
    framesizes     .set(parameters["framesizes"])
    frequency      .set(parameters["frequency"])
    gain           .set(parameters["gain"])
    gui            .set(parameters["gui"])
    hardmetric     .set(parameters["hardmetric"])
    inpipe         .set(parameters["inpipe"])
    ldpc_bf        .set(parameters["ldpc_bf"])
    ldpchelper_file.set(parameters["ldpchelper_file"])
    ldpchelper_path.set(parameters["ldpchelper_path"])
    leandvb_file   .set(parameters["leandvb_file"])
    leandvb_path   .set(parameters["leandvb_path"])
    lnblo          .set(parameters["lnb_lo"])
    maxsens        .set(parameters["maxsens"])
    modcods        .set(parameters["modcods"])
    nhelpers       .set(parameters["nhelpers"])
    ppm            .set(parameters["ppm"])
    rolloff        .set(parameters["rolloff"])
    rrcrej         .set(parameters["rrcrej"])
    rtldongle      .set(parameters["rtldongle"])
    rtlsdr_file    .set(parameters["rtlsdr_file"])
    rtlsdr_path    .set(parameters["rtlsdr_path"])
    sampler        .set(parameters["sampler"])
    standard       .set(parameters["standard"])
    strongpls      .set(parameters["strongpls"])
    symbolrate     .set(parameters["symbolrate"])
    tune           .set(parameters["tune"])
    viewer_file    .set(parameters["viewer_file"])
    viewer_path    .set(parameters["viewer_path"])
    viterbi        .set(parameters["viterbi"])

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

    def on_leandvb_path():
        d = askdirectory(parent=dlg, initialdir=leandvb_path.get())
        if len(d) > 0:
            leandvb_path.set(d)

    def on_leandvb_file():
        f = askopenfilename(parent=dlg, initialdir=leandvb_path.get(), initialfile=leandvb_file.get())
        if len(f) > 0:
            f = os.path.basename(f)
            leandvb_file.set(f)

    def on_ldpchelper_path():
        d = askdirectory(parent=dlg, initialdir=ldpchelper_path.get())
        if len(d) > 0:
            ldpchelper_path.set(d)

    def on_ldpchelper_file():
        f = askopenfilename(parent=dlg, initialdir=ldpchelper_path.get(), initialfile=ldpchelper_file.get())
        if len(f) > 0:
            f = os.path.basename(f)
            ldpchelper_file.set(f)

    def on_rtlsdr_path():
        d = askdirectory(parent=dlg, initialdir=rtlsdr_path.get())
        if len(d) > 0:
            rtlsdr_path.set(d)

    def on_rtlsdr_file():
        f = askopenfilename(parent=dlg, initialdir=rtlsdr_path.get(), initialfile=rtlsdr_file.get())
        if len(f) > 0:
            f = os.path.basename(f)
            rtlsdr_file.set(f)

    def on_viewer_path():
        d = askdirectory(parent=dlg, initialdir=viewer_path.get())
        if len(d) > 0:
            viewer_path.set(d)

    def on_viewer_file():
        f = askopenfilename(parent=dlg, initialdir=viewer_path.get(), initialfile=viewer_file.get())
        if len(f) > 0:
            f = os.path.basename(f)
            viewer_file.set(f)

    def on_save():
        parameters_save()
        dlg.destroy()

    def on_cancel():
        parameters_load()
        dlg.destroy()

    def on_default():
        parameters_default()

    #----- dialog properties -----
    dlg = Toplevel(root, borderwidth=4)
    dlg.title("Settings")
    dlg.transient(root)
    dlg.resizable(height = False, width = False)
    dlg.grab_set()

    #----- tabs container -----
    ntb = ttk.Notebook (dlg)
    ntb.grid (row=0, column=0, columnspan=3)

    tab_leandvb = ttk.Frame (ntb, padding=10)
    ntb.add(tab_leandvb, text="leandvb")

    tab_rtlsdr = ttk.Frame (ntb, padding=10)
    ntb.add(tab_rtlsdr, text="rtl_sdr")

    tab_files = ttk.Frame (ntb, padding=10)
    ntb.add(tab_files, text="files")

   #----- tab_files -----
    tab_files.columnconfigure((0,1),   pad=4, weight=1)
    tab_files.rowconfigure   ((0,1),   pad=4, weight=0)
    tab_files.rowconfigure   ((2,3,4), pad=4, weight=1)

        #----- label -----
    lbl_files = ttk.Label(tab_files, text="Setting of files and directories")
    lbl_files.grid (row=0, column=0, columnspan=2)

    lbl_files_separator = Frame (tab_files, height=1, bg="grey")
    lbl_files_separator.grid (row=1, column=0, columnspan=4, sticky=EW)

        #----- frame leandvb -----
    frm_files_leandvb = ttk.LabelFrame (tab_files, text="leandvb", borderwidth=2, padding=4)
    frm_files_leandvb.grid (row=2, column=0)

    lbl_leandvb_path = ttk.Label(frm_files_leandvb, text="Path : ")
    ent_leandvb_path = ttk.Entry(frm_files_leandvb, width=30, textvariable=leandvb_path)
    btn_leandvb_path = Button(frm_files_leandvb, padx=0, pady=0, text="...", command=on_leandvb_path)
    lbl_leandvb_path.grid (row=0, column=0, sticky=W)
    ent_leandvb_path.grid (row=0, column=1, sticky=W)
    btn_leandvb_path.grid (row=0, column=2)

    lbl_leandvb_file = ttk.Label(frm_files_leandvb, text="File : ")
    ent_leandvb_file = ttk.Entry(frm_files_leandvb, width=30, textvariable=leandvb_file)
    btn_leandvb_file = Button(frm_files_leandvb, padx=0, pady=0, text="...", command=on_leandvb_file)
    lbl_leandvb_file.grid (row=1, column=0, sticky=W)
    ent_leandvb_file.grid (row=1, column=1, sticky=W)
    btn_leandvb_file.grid (row=1, column=2)

        #----- frame LDCP helper -----
    frm_files_ldcphelper = ttk.LabelFrame (tab_files, text="LDCP helper", borderwidth=2, padding=4)
    frm_files_ldcphelper.grid (row=3, column=0)

    lbl_ldpchelper_path = ttk.Label(frm_files_ldcphelper, text="Path : ")
    ent_ldpchelper_path = ttk.Entry(frm_files_ldcphelper, width=30, textvariable=ldpchelper_path)
    btn_ldpchelper_path = Button(frm_files_ldcphelper, padx=0, pady=0, text="...", command=on_ldpchelper_path)
    lbl_ldpchelper_path.grid (row=0, column=0, sticky=W)
    ent_ldpchelper_path.grid (row=0, column=1, sticky=W)
    btn_ldpchelper_path.grid (row=0, column=2)

    lbl_ldpchelper_file = ttk.Label(frm_files_ldcphelper, text="File : ")
    ent_ldpchelper_file = ttk.Entry(frm_files_ldcphelper, width=30, textvariable=ldpchelper_file)
    btn_ldpchelper_file = Button(frm_files_ldcphelper, padx=0, pady=0, text="...", command=on_ldpchelper_file)
    lbl_ldpchelper_file.grid (row=1, column=0, sticky=W)
    ent_ldpchelper_file.grid (row=1, column=1, sticky=W)
    btn_ldpchelper_file.grid (row=1, column=2)

        #----- frame rtl_sdr -----
    frm_files_rtlsdr = ttk.LabelFrame (tab_files, text="rtl_sdr", borderwidth=2, padding=4)
    frm_files_rtlsdr.grid (row=2, column=1)

    lbl_rtlsdr_path = ttk.Label(frm_files_rtlsdr, text="Path : ")
    ent_rtlsdr_path = ttk.Entry(frm_files_rtlsdr, width=30, textvariable=rtlsdr_path)
    btn_rtlsdr_path = Button(frm_files_rtlsdr, padx=0, pady=0, text="...", command=on_rtlsdr_path)
    lbl_rtlsdr_path.grid (row=0, column=0, sticky=W)
    ent_rtlsdr_path.grid (row=0, column=1, sticky=W)
    btn_rtlsdr_path.grid (row=0, column=2)

    lbl_rtlsdr_file = ttk.Label(frm_files_rtlsdr, text="File : ")
    ent_rtlsdr_file = ttk.Entry(frm_files_rtlsdr, width=30, textvariable=rtlsdr_file)
    btn_rtlsdr_file = Button(frm_files_rtlsdr, padx=0, pady=0, text="...", command=on_rtlsdr_file)
    lbl_rtlsdr_file.grid (row=1, column=0, sticky=W)
    ent_rtlsdr_file.grid (row=1, column=1, sticky=W)
    btn_rtlsdr_file.grid (row=1, column=2)

        #----- frame viewer -----
    frm_files_viewer = ttk.LabelFrame (tab_files, text="viewer", borderwidth=2, padding=4)
    frm_files_viewer.grid (row=3, column=1)

    lbl_viewer_path = ttk.Label(frm_files_viewer, text="Path : ")
    ent_viewer_path = ttk.Entry(frm_files_viewer, width=30, textvariable=viewer_path)
    btn_viewer_path = Button(frm_files_viewer, padx=0, pady=0, text="...", command=on_viewer_path)
    lbl_viewer_path.grid (row=0, column=0, sticky=W)
    ent_viewer_path.grid (row=0, column=1, sticky=W)
    btn_viewer_path.grid (row=0, column=2)

    lbl_viewer_file = ttk.Label(frm_files_viewer, text="File : ")
    ent_viewer_file = ttk.Entry(frm_files_viewer, width=30, textvariable=viewer_file)
    btn_viewer_file = Button(frm_files_viewer, padx=0, pady=0, text="...", command=on_viewer_file)
    lbl_viewer_file.grid (row=1, column=0, sticky=W)
    ent_viewer_file.grid (row=1, column=1, sticky=W)
    btn_viewer_file.grid (row=1, column=2)

     #----- tab_rtlsdr -----
    tab_rtlsdr.columnconfigure((0,1),   pad=4, weight=1)
    tab_rtlsdr.rowconfigure   ((0,1,2), pad=4, weight=0)

        #----- label -----
    lbl_rtlsdr = ttk.Label(tab_rtlsdr, text="Settings for rtl_sdr program")
    lbl_rtlsdr.grid (row=0, column=0, columnspan=2)

    lbl_rtlsdr_separator = Frame (tab_rtlsdr, height=1, bg="grey")
    lbl_rtlsdr_separator.grid (row=1, column=0, columnspan=2, sticky=EW)

        #----- frame options -----
    frm_rtlsdr = ttk.Frame(tab_rtlsdr, borderwidth=4, padding=4)
    frm_rtlsdr.grid (row=2, column=0, columnspan=2)

        #----- options -----
    lbl_ppm = ttk.Label(frm_rtlsdr, text="ppm-error")
    ent_ppm = ttk.Entry(frm_rtlsdr, width=10, textvariable=ppm)
    lbl_ppm.grid (row=0, column=0, sticky=W)
    ent_ppm.grid (row=0, column=1, sticky=W)

    lbl_gain = ttk.Label(frm_rtlsdr, text="gain")
    ent_gain = ttk.Entry(frm_rtlsdr, width=10, textvariable=gain)
    lbl_gain.grid (row=1, column=0, sticky=W)
    ent_gain.grid (row=1, column=1, sticky=W)

    lbl_rtldongle = ttk.Label(frm_rtlsdr, text="rtldongle")
    ent_rtldongle = ttk.Entry(frm_rtlsdr, width=10, textvariable=rtldongle)
    lbl_rtldongle.grid (row=2, column=0, sticky=W)
    ent_rtldongle.grid (row=2, column=1, sticky=W)

    #----- tab_leandvb -----
    tab_leandvb.columnconfigure((0,1),   pad=4, weight=1)
    tab_leandvb.rowconfigure   ((0,1,2), pad=4, weight=0)

        #----- label -----
    lbl_leandvb = ttk.Label (tab_leandvb, text="Settings for leandvb program")
    lbl_leandvb.grid (row=0, column=0, columnspan=2)

    lbl_leandvb_separator = Frame (tab_leandvb, height=1, bg="grey")
    lbl_leandvb_separator.grid (row=1, column=0, columnspan=2, sticky=EW)

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
    btn_save    = ttk.Button (dlg, text="save",     command=on_save)
    btn_save   .grid (row=1, column=0)

    btn_cancel  = ttk.Button (dlg, text="cancel",   command=on_cancel)
    btn_cancel .grid (row=1, column=1)

    btn_default = ttk.Button (dlg, text="defaults", command=on_default)
    btn_default.grid (row=1, column=2)

    set_visibility_dvb_options(None)

#===== root window ============================================================

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
    opt_ldpc_helper= " --ldpc-helper " + "\"" + ldpchelper_path.get() + "/" + ldpchelper_file.get() + "\""
    opt_debug_v    = " -v" if debug.get() == "all" or debug.get() == "startup"   else ""
    opt_debug_d    = " -d" if debug.get() == "all" or debug.get() == "operation" else ""

    leandvb_opt = opt_inpipe + opt_sampler + opt_rolloff + opt_rrcrej \
                + opt_bandwidth + opt_symbolrate + opt_tune + opt_standard \
                + opt_fastlock + opt_gui + opt_maxsens \
                + opt_const + opt_fec + opt_viterbi + opt_hardmetric \
                + opt_strongpls + opt_modcods + opt_framesizes + opt_fastdrift \
                + opt_ldpc_bf + opt_nhelpers + opt_ldpc_helper \
                + opt_debug_v + opt_debug_d
    leandvb_sub = "\"" + leandvb_path.get() + "/" + leandvb_file.get() + "\"" + leandvb_opt

    opt_frequency  = " -f " + str(int((float(frequency.get()) - float(lnblo.get())) * 1000000))
    opt_samplerate = " -s " + str(bandwidth.get() * 1000)
    opt_device     = " -d " + str(rtldongle.get())
    opt_gain       = " -g " + str(gain.get())
    opt_ppm_error  = " -p " + str(ppm.get())
    opt_outfile    = " -"

    rtlsdr_opt = opt_frequency + opt_samplerate + opt_device + opt_gain + opt_ppm_error + opt_outfile
    rtlsdr_sub = "\"" + rtlsdr_path.get()  + rtlsdr_file.get()  + "\"" + rtlsdr_opt

    opt_infile = " -"
    viewer_opt = opt_infile
    viewer_sub = "\"" + viewer_path.get() + "\"" + viewer_file.get()  + viewer_opt

    print
    print "leandvb:", leandvb_sub
    print
    print "rtlsdr:", rtlsdr_sub
    print
    print "viewer:", viewer_sub
    print

    sub = rtlsdr_sub + \
          " -d " + str( rtldongle.get() ) + \
          " -f " + str( int( ( float(frequency.get()) - float(lnblo.get()) ) * 1000000 ) ) + \
          " -g " + str( gain.get() ) +  \
          " -s " + str( bandwidth.get() * 1000) + \
          " -p " + str( ppm.get() ) + \
          " -" + \
          " | " + \
          leandvb_sub + \
          " | " + \
          viewer_sub

    parameters_save()

    global proc_leandvb
    proc_leandvb = Popen(["/bin/sh","-c",sub], stderr=PIPE, preexec_fn=os.setsid)
    on_timeout()

def on_stop():
    global timeout
    global proc_leandvb
    if timeout :
        root.after_cancel(timeout)
        timeout = None
    if proc_leandvb :
        os.killpg(proc_leandvb.pid, SIGKILL)
        proc_leandvb = None

def on_exit():
    parameters_save()
    on_stop()
    root.destroy()

def on_timeout():
    global timeout
    global proc_leandvb
    msg = ""
    # non-blocking read of stderr from proc_leandvb
    pipe = proc_leandvb.stderr
    while pipe in select.select([pipe], [], [], 0)[0]:
        msg = msg + pipe.read(1)
    if len(msg) > 0 :
        txt_terminal.insert(END, msg)
        txt_terminal.see(END)
    timeout = root.after(100, on_timeout)

#----- global variables -----
timeout = None
proc_leandvb = None

#----- create root window -----
root = Tk()
root.title('LeanDVB DVBS + DVBS2 interface')
root.resizable(height = False, width = False)
frm_root = ttk.Frame(root, borderwidth=8)
frm_root.pack()
root.protocol("WM_DELETE_WINDOW", on_exit)

#----- 'declare' user interface variables -----
bandwidth       = IntVar()
const           = StringVar()
debug           = StringVar()
fastdrift       = IntVar()
fastlock        = IntVar()
fec             = StringVar()
framesizes      = StringVar()
frequency       = DoubleVar()
gain            = IntVar()
gui             = IntVar()
hardmetric      = IntVar()
inpipe          = IntVar()
ldpc_bf         = IntVar()
ldpchelper_file = StringVar()
ldpchelper_path = StringVar()
leandvb_file    = StringVar()
leandvb_path    = StringVar()
lnblo           = DoubleVar()
maxsens         = IntVar()
modcods         = StringVar()
nhelpers        = IntVar()
ppm             = IntVar()
rolloff         = DoubleVar()
rrcrej          = DoubleVar()
rtldongle       = IntVar()
rtlsdr_file     = StringVar()
rtlsdr_path     = StringVar()
sampler         = StringVar()
standard        = StringVar()
strongpls       = IntVar()
symbolrate      = IntVar()
tune            = IntVar()
viewer_file     = StringVar()
viewer_path     = StringVar()
viterbi         = IntVar()

#----- initialize parameters dictionary -----
if os.path.isfile(parameters_file):
    parameters_load()
else:
    parameters_default()

#----- create user interface -----
    #----- terminal -----
frm_terminal = ttk.Frame(frm_root)
frm_terminal.grid (row=0, column=0, rowspan=8, sticky=NS)
txt_terminal = Text(frm_terminal, width=40, height=0)
scb_terminal = Scrollbar(frm_terminal)
txt_terminal.config(yscrollcommand=scb_terminal.set)
scb_terminal.config(command=txt_terminal.yview)
txt_terminal.pack (side=LEFT, fill=Y)
scb_terminal.pack (side=RIGHT, fill=Y)

    #----- controls -----
lbl_frequency = ttk.Label (frm_root, text="Frequency")
cmb_frequency = ttk.Combobox (frm_root, width=10, textvariable=frequency)
cmb_frequency ["values"] = ("10491.500","1252","1257","1260","436","437","1255","1252.600","1280","1250","1253")
cmb_frequency.focus_set()
lb2_frequency = ttk.Label (frm_root, text="MHz")
lbl_frequency.grid (row=0, column=1, sticky=W, padx=5)
cmb_frequency.grid (row=0, column=2, sticky=W)
lb2_frequency.grid (row=0, column=3, sticky=W, padx=5)

lbl_symbolrate = ttk.Label (frm_root, text="Symbolrate")
cmb_symbolrate = ttk.Combobox (frm_root, width=10, textvariable=symbolrate)
cmb_symbolrate ["values"] = ("33","66","125","150","250","333","400","500","600","750","1000","1500","2000","2083","3000","4000","4340","5000")
lb2_symbolrate = ttk.Label (frm_root, text="kHz")
lbl_symbolrate.grid (row=1, column=1, sticky=W, padx=5)
cmb_symbolrate.grid (row=1, column=2, sticky=W)
lb2_symbolrate.grid (row=1, column=3, sticky=W, padx=5)

lbl_bandwidth = ttk.Label (frm_root, text="Bandwidth")
cmb_bandwidth = ttk.Combobox (frm_root, width=10, textvariable=bandwidth)
cmb_bandwidth ["values"] = ("2400","2000","1000","500")
lb2_bandwidth = ttk.Label (frm_root, text="kHz")
lbl_bandwidth.grid (row=2, column=1, sticky=W, padx=5)
cmb_bandwidth.grid (row=2, column=2, sticky=W)
lb2_bandwidth.grid (row=2, column=3, sticky=W, padx=5)

lbl_tune = ttk.Label (frm_root, text="Tune")
cmb_tune = ttk.Combobox (frm_root, width=10, textvariable=tune)
cmb_tune ["values"] = ("100","500","1000","2000","5000","10000","-100","-500","-1000","-2000","-5000","-10000")
lb2_tune = ttk.Label (frm_root, text="Hz")
lbl_tune.grid (row=3, column=1, sticky=W, padx=5)
cmb_tune.grid (row=3, column=2, sticky=W)
lb2_tune.grid (row=3, column=3, sticky=W, padx=5)

lbl_lnblo = ttk.Label (frm_root, text="LNB LO")
ent_lnblo = ttk.Entry (frm_root, width=10, textvariable=lnblo)
lb2_lnblo = ttk.Label (frm_root, text="MHz")
lbl_lnblo.grid (row=4, column=1, sticky=W)
ent_lnblo.grid (row=4, column=2, sticky=W)
lb2_lnblo.grid (row=4, column=3, sticky=W, padx=5)

lbl_fec = ttk.Label (frm_root, text="FEC")
cmb_fec = ttk.Combobox (frm_root, width=10, textvariable=fec)
cmb_fec ["values"] = ("1/2","2/3","3/4","5/6","6/7","7/8")
lb2_fec = ttk.Label (frm_root, text="Div")
lbl_fec.grid (row=5, column=1, sticky=W, padx=5)
cmb_fec.grid (row=5, column=2, sticky=W)
lb2_fec.grid (row=5, column=3, sticky=W, padx=5)

    #----- separator -----
lbl_separator = Frame (frm_root, height=1, bg="grey")
lbl_separator.grid (row=6, column=1, sticky=EW, columnspan=5, pady=6)

    #----- buttons -----
rdb_dummy = StringVar()
rdb_dummy.set("stop")
rdb_start = Radiobutton (frm_root, text="START", indicatoron=0, width=10, pady=4, variable=rdb_dummy, value="start", command=on_start)
rdb_start.grid (row=7, column=1)
rdb_stop = Radiobutton (frm_root, text="STOP", indicatoron=0, width=10, pady=4, variable=rdb_dummy, value="stop", command=on_stop)
rdb_stop.grid (row=7, column=2)

btn_settings = ttk.Button (frm_root, text='Settings', command=dlg_settings)
btn_settings.grid (row=7, column=4)

    #----- logo -----
if os.path.isfile("logo.png"):
    img_logo = PhotoImage(file="logo.png")
else:
    img_logo = None
lbl_logo = Label(frm_root, image=img_logo)
lbl_logo.grid (row=0, column=4, sticky=W+E+N+S, rowspan=6, padx=5, pady=5)

#----- start user interface -----
mainloop()

