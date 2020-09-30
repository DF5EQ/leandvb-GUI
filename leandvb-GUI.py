#!/usr/bin/env python

# Simple UI voor LEANDVB, DVBS receiver.
# requires sudo apt-get install python-imaging-tk package
# keep everything in your home directory
# if you add a 180x180 pixels file called logo.png it will be
# showed in right corner.
# Leandvb by F4DAV (github leansdr)
# Wrapper by pe2jko@540.org

# TODO change checkbutton for LowSR(bandwith) in entry or list-entry
# TODO leandvb-run as function like leandvb-stop
# TODO leandvb: --tune is broken, use --derotate instead
# TODO change dutch names in english
# TODO streamline usage of viewer ffplay and mplayer
# TODO 'cancel' in settings not working propperly
# TODO add entries for path and filenames in settings

from Tkinter import *
from PIL import ImageTk, Image
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
print "Auxilliary directory: " + aux_dir
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
    parameters["frequency"     ] = float(ent_frequency.get())
    parameters["samplerate"    ] = int(ent_samplerate.get())
    parameters["fec"           ] = tkvar3.get()
    parameters["tune"          ] = int(h.get())
    parameters["fastlock"      ] = bool(var1.get())
    parameters["lowsr"         ] = bool(var2.get())
    parameters["viterbi"       ] = bool(var3.get())
    parameters["gui"           ] = bool(var5.get())
    parameters["dvbs2"         ] = bool(var6.get())
    parameters["maxprocess"    ] = bool(var7.get())
    parameters["hardmetric"    ] = bool(var4.get())
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
    parameters["lowsr"         ] = False
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
    dlg = Toplevel(master, borderwidth=4)
    dlg.title("Settings")
    dlg.transient(master)
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
    aux_ppm       = ttk.Label(tab_rtlsdr,           text="default 0")
    lbl_gain      = ttk.Label(tab_rtlsdr,           text="gain")
    lb2_gain      = ttk.Label(tab_rtlsdr,           text=" (-g) : ")
    ent_gain      = ttk.Entry(tab_rtlsdr, width=10, textvariable=gain)
    aux_gain      = ttk.Label(tab_rtlsdr,           text="default 0 = Auto")
    lbl_rtldongle = ttk.Label(tab_rtlsdr,           text="rtldongle")
    lb2_rtldongle = ttk.Label(tab_rtlsdr,           text=" (-d) : ")
    ent_rtldongle = ttk.Entry(tab_rtlsdr, width=10, textvariable=rtldongle)
    aux_rtldongle = ttk.Label(tab_rtlsdr,           text="default 0")

    #----- tab_leansdr -----
    lbl_leansdr    = ttk.Label(tab_leansdr, text="Settings for leansdr program")
    lbl_inpipe     = ttk.Label(tab_leansdr,           text="Inpipe")
    lb2_inpipe     = ttk.Label(tab_leansdr,           text=" (--inpipe) : ")
    ent_inpipe     = ttk.Entry(tab_leansdr, width=10, textvariable=inpipe)
    aux_inpipe     = ttk.Label(tab_leansdr,           text="DVBS2")
    lbl_rolloff    = ttk.Label(tab_leansdr,           text="Roll Off Factor")
    lb2_rolloff    = ttk.Label(tab_leansdr,           text=" (--roll-off) : ")
    ent_rolloff    = ttk.Entry(tab_leansdr, width=10, textvariable=rolloff_factor)
    aux_rolloff    = ttk.Label(tab_leansdr,           text="DVBS2")
    lbl_rrcrej     = ttk.Label(tab_leansdr,           text="RRC Rej Factor")
    lb2_rrcrej     = ttk.Label(tab_leansdr,           text=" (--rrc-rej) : ")
    ent_rrcrej     = ttk.Entry(tab_leansdr, width=10, textvariable=rrc_rej_factor)
    aux_rrcrej     = ttk.Label(tab_leansdr,           text="DVBS2")
    lbl_nhelpers   = ttk.Label(tab_leansdr,           text="Nhelpers")
    lb2_nhelpers   = ttk.Label(tab_leansdr,           text=" (--nhelpers) : ")
    ent_nhelpers   = ttk.Entry(tab_leansdr, width=10, textvariable=nhelpers)
    aux_nhelpers   = ttk.Label(tab_leansdr,           text="DVBS2")
    lbl_modcods    = ttk.Label(tab_leansdr,           text="modcods")
    lb2_modcods    = ttk.Label(tab_leansdr,           text=" (--modcods) : ")
    ent_modcods    = ttk.Entry(tab_leansdr, width=10, textvariable=modcods)
    aux_modcods    = ttk.Label(tab_leansdr,           text="empty entry omits parameter")
    lbl_framesizes = ttk.Label(tab_leansdr,           text="framesizes")
    lb2_framesizes = ttk.Label(tab_leansdr,           text=" (--framesizes) : ")
    ent_framesizes = ttk.Entry(tab_leansdr, width=10, textvariable=framesizes)
    aux_framesizes = ttk.Label(tab_leansdr,           text="empty entry omits parameter")

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
    aux_ppm      .grid (row=1, column=3, sticky=W)
    lbl_gain     .grid (row=2, column=0, sticky=E)
    lb2_gain     .grid (row=2, column=1, sticky=E)
    ent_gain     .grid (row=2, column=2, sticky=W)
    aux_gain     .grid (row=2, column=3, sticky=W)
    lbl_rtldongle.grid (row=3, column=0, sticky=E)
    lb2_rtldongle.grid (row=3, column=1, sticky=E)
    ent_rtldongle.grid (row=3, column=2, sticky=W)
    aux_rtldongle.grid (row=3, column=3, sticky=W)

    tab_leansdr.columnconfigure((0,2,3),       pad=4, weight=1)
    tab_leansdr.rowconfigure   ((0,1,2,3,4,5), pad=4, weight=0)
    lbl_leansdr   .grid (row=0, column=0, sticky=N, columnspan=4, pady=6)
    lbl_inpipe    .grid (row=1, column=0, sticky=E)
    lb2_inpipe    .grid (row=1, column=1, sticky=E)
    ent_inpipe    .grid (row=1, column=2, sticky=W)
    aux_inpipe    .grid (row=1, column=3, sticky=W)
    lbl_rolloff   .grid (row=2, column=0, sticky=E)
    lb2_rolloff   .grid (row=2, column=1, sticky=E)
    ent_rolloff   .grid (row=2, column=2, sticky=W)
    aux_rolloff   .grid (row=2, column=3, sticky=W)
    lbl_rrcrej    .grid (row=3, column=0, sticky=E)
    lb2_rrcrej    .grid (row=3, column=1, sticky=E)
    ent_rrcrej    .grid (row=3, column=2, sticky=W)
    aux_rrcrej    .grid (row=3, column=3, sticky=W)
    lbl_nhelpers  .grid (row=4, column=0, sticky=E)
    lb2_nhelpers  .grid (row=4, column=1, sticky=E)
    ent_nhelpers  .grid (row=4, column=2, sticky=W)
    aux_nhelpers  .grid (row=4, column=3, sticky=W)
    lbl_modcods   .grid (row=5, column=0, sticky=E)
    lb2_modcods   .grid (row=5, column=1, sticky=E)
    ent_modcods   .grid (row=5, column=2, sticky=W)
    aux_modcods   .grid (row=5, column=3, sticky=W)
    lbl_framesizes.grid (row=6, column=0, sticky=E)
    lb2_framesizes.grid (row=6, column=1, sticky=E)
    ent_framesizes.grid (row=6, column=2, sticky=W)
    aux_framesizes.grid (row=6, column=3, sticky=W)

#===== master window ==========================================================

master = Tk()

#----- window properties -----
master.title('LeanDVB DVBS + DVBS2 interface')

#----- initialize variables -----
if os.path.isfile(parameters_file):
    parameters_load()
else:
    parameters_default()

#----- user interface -----
lbl_frequency  = ttk.Label(master, text="Frequency")
ent_frequency  = ttk.Entry(master)
lb2_frequency  = ttk.Label(master, text="MHz")
lbl_samplerate = ttk.Label(master, text="Samplerate")
ent_samplerate = ttk.Entry(master)
lb2_samplerate = ttk.Label(master, text="S/R")

lbl_frequency .grid (row=0, column=0)
ent_frequency .grid (row=0, column=1)
lb2_frequency .grid (row=0, column=2, sticky=W)
lbl_samplerate.grid (row=1, column=0)
ent_samplerate.grid (row=1, column=1)
lb2_samplerate.grid (row=1, column=2, sticky=W)

ent_frequency.focus_set()

g = Entry(master, font = "Verdana 15 bold")
h = Entry(master, font = "Verdana 15 bold")
ent_frequency .insert(0, parameters["frequency"])
ent_samplerate.insert(0, parameters["samplerate"])
g.insert(0, parameters["fec"])
h.insert(0, parameters["tune"])
g.grid(row=2, column=1)
h.grid(row=3, column=1)

ppm = IntVar()
ppm.set(parameters["ppm"])

padlean = StringVar()
padlean.set(parameters["leanpad"])

gain = IntVar()
gain.set(parameters["gain"])

rtldongle = IntVar()
rtldongle.set(parameters["rtldongle"])

var1 = IntVar()
Checkbutton(master, font = "Verdana 13 italic", text="Fastlock", variable=var1).grid(row=5, sticky=W)
var2 = IntVar()
Checkbutton(master, font = "Verdana 13 italic" ,text="Low SR", variable=var2).grid(row=5, column=1, sticky=W)
var3 = IntVar()
Checkbutton(master, font = "Verdana 13 italic" ,text="Viterbi", variable=var3).grid(row=5, column=1, sticky=E)
var4 = IntVar()
#Checkbutton(master, font = "Verdana 13 italic" ,text="Hard-Metric", variable=var4).grid(row=5, column=1)

Label(master,font = "Verdana 10 italic", text="-----------------------").grid(row=4,column=0)
Label(master,font = "Verdana 10 italic", text="---------------------------------------------------------").grid(row=4,column=1)
var5 = IntVar()
Checkbutton(master, font = "Verdana 13 italic", text="Gui", variable=var5).grid(row=7, sticky=W)
var6 = IntVar()
Checkbutton(master, font = "Verdana 13 italic" ,text="DVBS-2", variable=var6).grid(row=7, column=1, sticky=W)
var7 = IntVar()
Checkbutton(master, font = "Verdana 13 italic" ,text="Max sensitive", variable=var7).grid(row=7, column=1, sticky=E)
Label(master,font = "Verdana 8 italic", text="").grid(row=6,column=0)
Label(master,font = "Verdana 8 italic", text="").grid(row=8,column=0)

viewer = StringVar()
rolloff_factor = StringVar()
rrc_rej_factor = IntVar()
nhelpers = IntVar()
inpipe = IntVar()
modcods = StringVar()
framesizes = StringVar()
lnblo = DoubleVar()
var1.set(parameters["fastlock"])
var2.set(parameters["lowsr"])
var3.set(parameters["viterbi"])
var4.set(parameters["hardmetric"])
var5.set(parameters["gui"])
var6.set(parameters["dvbs2"])
var7.set(parameters["maxprocess"])
viewer.set(parameters["viewer"])
rolloff_factor.set(parameters["rolloff_factor"])
rrc_rej_factor.set(parameters["rrc_rej_factor"])
nhelpers.set(parameters["nhelpers"])
inpipe.set(parameters["inpipe"])
modcods.set(parameters["modcods"])
framesizes.set(parameters["framesizes"])
lnblo.set(parameters["lnb_lo"])

if os.path.isfile("logo.png"):
    im = Image.open("logo.png")
    photo = ImageTk.PhotoImage(im)
    label = Label(image=photo)
    label.image = photo
    label.grid(row=0, column=3, columnspan=2, rowspan=3,sticky=W+E+N+S, padx=5, pady=5)

def on_exit():
    parameters_save()
    on_stop()
    master.destroy()

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

def on_start():
    ppmvalue = int(ppm.get())
    leanpad = padlean.get()
    gain_value = gain.get()
    rolloff = rolloff_factor.get()
    rrcrej = rrc_rej_factor.get()
    nhelp = nhelpers.get()
    inpip = inpipe.get()
    modcods_value = modcods.get()
    framesizes_value = framesizes.get()
    if (viewer.get() == "ffplay"):
        view = "ffplay -v 0"
    else:
        view = "mplayer"
    if (var2.get() == True):
        bandwidth = 1800000
    else:
        bandwidth = 2400000
    if (var1.get() == True):
        fastlock = " --fastlock"
    else:
        fastlock = ""
    if (var3.get() == True):
        viterbi = " --viterbi"
    else:
        viterbi = ""
    if (var5.get() == True):
        gui = " --gui"
    else:
        gui = ""
    if (var6.get() == True):
        dvbs = "DVB-S2"
    else:
        dvbs = "DVB-S"
    if (var7.get() == True):
        maxprocess = " --hq"
    else:
        maxprocess = ""
    if (var4.get() == True):
        hardmetric = " --hard-metric"
    else:
        hardmetric = ""
    if (modcods_value == ""):
        modcods_string = ""
    else:
        modcods_string = " --modcods " + modcods_value
    if (framesizes_value == ""):
        framesizes_string = ""
    else:
        framesizes_string = " --framesizes " + framesizes_value
    frequency = int( ( float(ent_frequency.get()) - float(lnblo.get()) ) * 1000000 )
    samplerate = int(ent_samplerate.get()) * 1000
    fec = tkvar3.get()
    tune = h.get()
    rtl = rtldongle.get()
    if (var6.get() == True): #dvbs2
        sub = "rtl_sdr" + \
              " -d " + str(rtl) + \
              " -f " + str(frequency) + \
              " -g " + str(gain_value) +  \
              " -s " + str(bandwidth) + \
              " -p " + str(ppmvalue) + \
              " -" + \
              " | " + \
              leanpad + "leandvb" + \
              gui + \
              modcods_string + \
              framesizes_string + \
              maxprocess + \
              viterbi + \
              hardmetric + \
              fastlock + \
              " --tune " + tune + \
              " --standard " + dvbs + \
              " --ldpc-helper " + leanpad + "ldpc_tool" + \
              " --inpipe " + str(inpip) + \
              " --nhelpers " + str(nhelp) + \
              " --sampler rrc" + \
              " --rrc-rej " + str(rrcrej) + \
              " -v" + \
              " --roll-off " + rolloff + \
              " --sr " + str(samplerate) + \
              " -f " + str(bandwidth) + \
              " | " + \
              "ffplay -v 0 -" + \
              " \n"
    else:
        sub = "rtl_sdr" + \
              " -d " + str(rtl) + \
              " -f " + str(frequency) + \
              " -g " + str(gain_value) +  \
              " -s " + str(bandwidth) + \
              " -p " + str(ppmvalue) + \
              " -" + \
              " | " + \
              leanpad + "leandvb" + \
              gui + \
              maxprocess + \
              viterbi + \
              hardmetric + \
              fastlock + \
              " --tune " + tune + \
              " --cr " + fec + \
              " --standard " + dvbs + \
              " -v" + \
              " --sr " + str(samplerate) + \
              " -f " + str(bandwidth) + \
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

Button(master, font = "Verdana 11 italic", text='EXIT', command=on_exit).grid(row=7, column=3,sticky=E)
Button(master, font = "Verdana 11 italic",highlightbackground='red',text='START', command=on_start).grid(row=7, column=3,sticky=W)
Button(master, font = "Verdana 11 italic",text='STOP', command=on_stop).grid(row=7, column=4,sticky=W)
Button(master, font = "Verdana 11 italic",fg='red',highlightbackground='blue',text='    Settings    ', command=dlg_settings).grid(row=5, column=3)

master.protocol("WM_DELETE_WINDOW", on_exit)

tkvar1 = StringVar(master)

# Frequency Dropdown
choices1 = { '1252','1257','1260','436','437','1255','1252.600','1280','1250','1253'}

tkvar1.set(str(parameters["frequency"])) # set the default option

popupMenu = OptionMenu(master, tkvar1, *choices1)
popupMenu.grid(row = 0, column =1, sticky=E)

# on change dropdown value
def change_dropdown1(*args):
    print( tkvar1.get() )
    ent_frequency.delete(0, END)
    ent_frequency.insert(0, tkvar1.get())

# link function to change dropdown
tkvar1.trace('w', change_dropdown1)

tkvar2 = StringVar(master)

# SampleRate
choices2 = { '33', '66','125','150','250','333','400','500','600','750','1000','1500','2000','2083','3000','4000','4340','5000'}

tkvar2.set(str(parameters["samplerate"])) # set the default option

popupMenu = OptionMenu(master, tkvar2, *choices2)
popupMenu.grid(row = 1, column =1, sticky=E)

# on change dropdown value
def change_dropdown2(*args):
    print( tkvar2.get() )
    ent_samplerate.delete(0, END)
    ent_samplerate.insert(0, tkvar2.get())

# link function to change dropdown
tkvar2.trace('w', change_dropdown2)

tkvar3 = StringVar(master)
# Fec
choices3 = { '1/2','2/3','3/4','5/6','6/7','7/8' }
tkvar3.set(parameters["fec"])
popupMenu = OptionMenu(master, tkvar3, *choices3)
Label(master, text="FEC (auto@dvbs2)", font = "Verdana 14 italic").grid(row = 2, column = 0)
Label(master, text="Div", font = "Verdana 14 italic").grid(row = 2, column = 2,sticky=W)
popupMenu.grid(row = 2, column =1, sticky=E)

# on change dropdown value
def change_dropdown3(*args):
    print( tkvar3.get() )
    g.delete(0, END)
    g.insert(0, tkvar3.get())

# link function to change dropdown
tkvar3.trace('w', change_dropdown3)

tkvar4 = StringVar(master)
# Tune
choices4 = { '100','500','1000','2000','5000','10000','-100','-500','-1000','-2000','-5000','-10000'}
tkvar4.set(parameters["tune"]) # set the default option

popupMenu = OptionMenu(master, tkvar4, *choices4)
Label(master, text="Tune", font = "Verdana 14 italic").grid(row = 3, column = 0)
Label(master, text="Hz", font = "Verdana 14 italic").grid(row = 3, column = 2,sticky=W)
popupMenu.grid(row = 3, column =1, sticky=E)

# on change dropdown value
def change_dropdown4(*args):
    print(  )
    h.delete(0, END)
    h.insert(0, tkvar4.get())

# link function to change dropdown
tkvar4.trace('w', change_dropdown4)


mainloop()

