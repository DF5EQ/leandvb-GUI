#!/usr/bin/env python

# Simple UI voor LEANDVB, DVBS receiver.
# requires sudo apt-get install python-imaging-tk package
# keep everything in your home directory
# if you add a 180x180 pixels file called logo.png it will be
# showed in right corner.
# Leandvb by F4DAV (github leansdr)
# Wrapper by pe2jko@540.org

# TODO introduce tabs in settings for 'general','rtl_sdr','leansdr','files'
# TODO leandvb-run as function like leandvb-stop
# TODO change checkbutton for LowSR(bandwith) in entry or list-entry
# TODO leandvb: --tune is broken, use --derotate instead
# TODO change dutch names in english
# TODO streamline usage of viewer ffplay and mplayer
# TODO 'cancel' in settings not working propperly
# TODO add rrc_rej_factor to settings
# TODO add entries for path and filenames in settings

from Tkinter import *
from PIL import ImageTk, Image
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

f = open("/proc/sys/fs/pipe-max-size", "r")
max_current = int(f.readline())
f.close()

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
    parameters["frequency"     ] = float(e.get())
    parameters["samplerate"    ] = int(f.get())
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
    parameters["antenne"       ] = ant.get()
    parameters["gain_lime"     ] = gain_lime.get()
    parameters["bandwidth_lime"] = bandwidth_lime.get()
    parameters["gain_rtl"      ] = gain_rtl.get()
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
    parameters["antenne"       ] = "1"
    parameters["gain_lime"     ] = "0.5"
    parameters["bandwidth_lime"] = 3500000
    parameters["gain_rtl"      ] = 36
    parameters["viewer"        ] = "ffplay"
    parameters["rolloff_factor"] = "0.35"
    parameters["rrc_rej_factor"] = 30
    parameters["nhelpers"      ] = 6
    parameters["inpipe"        ] = 32000000
    parameters["modcods"       ] = "0x0040"
    parameters["framesizes"    ] = "0x01"
    parameters["lnb_lo"        ] = 9750.0
    parameters["rtldongle"     ] = 0

#===== GUI ====================================================================

master = Tk()
master.title('LeanDVB DVBS + DVBS2 interface')

if os.path.isfile(parameters_file):
    parameters_load()
else:
    parameters_default()

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

rtldongle = IntVar()
ppm = IntVar()
padlean = StringVar()
ant = StringVar()
gain_rtl = IntVar()
gain_lime = StringVar()
viewer = StringVar()
rolloff_factor = StringVar()
rrc_rej_factor = IntVar()
nhelpers = IntVar()
inpipe = IntVar()
bandwidth_lime = IntVar()
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
rtldongle.set(parameters["rtldongle"])
padlean.set(parameters["leanpad"])
ppm.set(parameters["ppm"])
ant.set(parameters["antenne"])
gain_lime.set(parameters["gain_lime"])
bandwidth_lime.set(parameters["bandwidth_lime"])
gain_rtl.set(parameters["gain_rtl"])
viewer.set(parameters["viewer"])
rolloff_factor.set(parameters["rolloff_factor"])
rrc_rej_factor.set(parameters["rrc_rej_factor"])
nhelpers.set(parameters["nhelpers"])
inpipe.set(parameters["inpipe"])
modcods.set(parameters["modcods"])
framesizes.set(parameters["framesizes"])
lnblo.set(parameters["lnb_lo"])
e = Entry(master, font = "Verdana 15 bold")
f = Entry(master, font = "Verdana 15 bold")
g = Entry(master, font = "Verdana 15 bold")
h = Entry(master, font = "Verdana 15 bold")
e.insert(0, parameters["frequency"])
f.insert(0, parameters["samplerate"])
g.insert(0, parameters["fec"])
h.insert(0, parameters["tune"])
e.grid(row=0, column=1)
f.grid(row=1, column=1)
g.grid(row=2, column=1)
h.grid(row=3, column=1)


e.focus_set()
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


def on_settings():

    def on_settings_save():
        parameters_save()
        settings_window.destroy()

    def on_settings_cancel():
        settings_window.destroy()

    settings_window = Toplevel(master, borderwidth=4)
    settings_window.title("Settings")
    settings_window.transient(master)
    settings_window.resizable(height = False, width = False)

    leansdr_label    = Label(settings_window,           text="Path to leansdr :")
    leansdr_entry    = Entry(settings_window, width=40, textvariable=padlean)

    ppmrtl_label     = Label(settings_window,           text="PPM offset RTL :")
    ppmrtl_entry     = Entry(settings_window, width=10, textvariable=ppm)

    gainrtl_label    = Label(settings_window,           text="Gain RTL :")
    gainrtl_entry    = Entry(settings_window, width=10, textvariable=gain_rtl)
    gainrtl_extra    = Label(settings_window,           text="0 = Auto")

    rolloff_label    = Label(settings_window,           text="Roll Off Factor (DVBS2) :")
    rolloff_entry    = Entry(settings_window, width=10, textvariable=rolloff_factor)

    rrcrej_label     = Label(settings_window,           text="RRC Rej Factor (DVBS2) :")
    rrcrej_entry     = Entry(settings_window, width=10, textvariable=rrc_rej_factor)

    nhelpers_label   = Label(settings_window,           text="Nhelpers (DVBS2) :")
    nhelpers_entry   = Entry(settings_window, width=10, textvariable=nhelpers)

    inpipe_label     = Label(settings_window,           text="Inpipe (DVBS2) :")
    inpipe_entry     = Entry(settings_window, width=10, textvariable=inpipe)

    modcods_label    = Label(settings_window,           text="modcods :")
    modcods_entry    = Entry(settings_window, width=10, textvariable=modcods)
    modcods_extra    = Label(settings_window,           text="empty entry omits parameter")

    framesizes_label = Label(settings_window,           text="framesizes :")
    framesizes_entry = Entry(settings_window, width=10, textvariable=framesizes)
    framesizes_extra = Label(settings_window,           text="empty entry omits parameter")

    viewer_label     = Label(settings_window,           text="Viewer :")
    viewer_entry     = Entry(settings_window, width=10, textvariable=viewer)

    lnblo_label      = Label(settings_window,           text="LNB LO :")
    lnblo_entry      = Entry(settings_window, width=10, textvariable=lnblo)

    rtldongle_label  = Label(settings_window,           text="rtldongle :")
    rtldongle_entry  = Entry(settings_window, width=10, textvariable=rtldongle)

    save_button      = Button(settings_window, highlightbackground='green', text="SAVE",   command = on_settings_save)
    cancel_button    = Button(settings_window, highlightbackground='red',   text="CANCEL", command = on_settings_cancel)

    leansdr_label.grid    (row=0, column=0, sticky=E)
    leansdr_entry.grid    (row=0, column=1, sticky=W, columnspan=3)

    ppmrtl_label.grid     (row=1, column=0, sticky=E)
    ppmrtl_entry.grid     (row=1, column=1, sticky=W)

    gainrtl_label.grid    (row=2, column=0, sticky=E)
    gainrtl_entry.grid    (row=2, column=1, sticky=W)
    gainrtl_extra.grid    (row=2, column=2, sticky=W, columnspan=2)

    rolloff_label.grid    (row=3, column=0, sticky=E)
    rolloff_entry.grid    (row=3, column=1, sticky=W)

    nhelpers_label.grid   (row=4, column=0, sticky=E)
    nhelpers_entry.grid   (row=4, column=1, sticky=W)

    inpipe_label.grid     (row=5, column=0, sticky=E)
    inpipe_entry.grid     (row=5, column=1, sticky=W)

    modcods_label.grid    (row=6, column=0, sticky=E)
    modcods_entry.grid    (row=6, column=1, sticky=W)
    modcods_extra.grid    (row=6, column=2, sticky=W, columnspan=2)

    framesizes_label.grid (row=7, column=0, sticky=E)
    framesizes_entry.grid (row=7, column=1, sticky=W)
    framesizes_extra.grid (row=7, column=2, sticky=W, columnspan=2)

    viewer_label.grid     (row=8, column=0, sticky=E)
    viewer_entry.grid     (row=8, column=1, sticky=W)

    lnblo_label.grid      (row=9, column=0, sticky=E)
    lnblo_entry.grid      (row=9, column=1, sticky=W)

    rtldongle_label.grid  (row=10, column=0, sticky=E)
    rtldongle_entry.grid  (row=10, column=1, sticky=W)

    save_button.grid      (row=11, column=2, sticky=EW)
    cancel_button.grid    (row=11, column=3, sticky=EW)

    settings_window.columnconfigure(0, weight=0)
    settings_window.columnconfigure(1, weight=0)
    settings_window.columnconfigure(2, weight=1)
    settings_window.columnconfigure(3, weight=1)

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
    antenne = ant.get()
    gainlime = gain_lime.get()
    gainrtl = gain_rtl.get()
    rolloff = rolloff_factor.get()
    rrcrej = rrc_rej_factor.get()
    nhelp = nhelpers.get()
    inpip = inpipe.get()
    modcods_value = modcods.get()
    framesizes_value = framesizes.get()
    bandwidthlime = bandwidth_lime.get()
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
    frequency = int( ( float(e.get()) - float(lnblo.get()) ) * 1000000 )
    samplerate = int(f.get()) * 1000
    fec = tkvar3.get()
    tune = h.get()
    rtl = rtldongle.get()
    if (var6.get() == True): #dvbs2
        sub = "rtl_sdr" + \
              " -d " + str(rtl) + \
              " -f " + str(frequency) + \
              " -g " + str(gainrtl) +  \
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
              " -g " + str(gainrtl) +  \
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

    print sub

    parameters_save()

    file = open(run_script, "w")
    file.write("#!/bin/sh \n\n")
    file.write("\n\n")
    file.write(sub)
    file.close()
    os.system("sh " + run_script + " &")

Button(master,font = "Verdana 11 italic", text='EXIT', command=on_exit).grid(row=7, column=3,sticky=E)
Button(master, font = "Verdana 11 italic",highlightbackground='red',text='START', command=on_start).grid(row=7, column=3,sticky=W)
Button(master, font = "Verdana 11 italic",text='STOP', command=on_stop).grid(row=7, column=4,sticky=W)
Button(master, font = "Verdana 11 italic",fg='red',highlightbackground='blue',text='    Settings    ', command=on_settings).grid(row=5, column=3)

master.protocol("WM_DELETE_WINDOW", on_exit)

tkvar1 = StringVar(master)
 
# Frequency Dropdown
choices1 = { '1252','1257','1260','436','437','1255','1252.600','1280','1250','1253'}

tkvar1.set(str(parameters["frequency"])) # set the default option

popupMenu = OptionMenu(master, tkvar1, *choices1)
Label(master, text=" Frequency ", font = "Verdana 14 italic").grid(row = 0, column = 0)
Label(master, text="MHz", font = "Verdana 14 italic").grid(row = 0, column = 2,sticky=W)
popupMenu.grid(row = 0, column =1, sticky=E)
 
# on change dropdown value
def change_dropdown1(*args):
    print( tkvar1.get() )
    e.delete(0, END)
    e.insert(0, tkvar1.get())
    
 
# link function to change dropdown
tkvar1.trace('w', change_dropdown1)

tkvar2 = StringVar(master)
 
# SampleRate
choices2 = { '33', '66','125','150','250','333','400','500','600','750','1000','1500','2000','2083','3000','4000','4340','5000'}

tkvar2.set(str(parameters["samplerate"])) # set the default option
 
popupMenu = OptionMenu(master, tkvar2, *choices2)
Label(master, text=" Samplerate ", font = "Verdana 14 italic").grid(row = 1, column = 0)
Label(master, text="S/R", font = "Verdana 14 italic").grid(row = 1, column = 2,sticky=W)
popupMenu.grid(row = 1, column =1, sticky=E)
 
# on change dropdown value
def change_dropdown2(*args):
    print( tkvar2.get() )
    f.delete(0, END)
    f.insert(0, tkvar2.get())
    
 
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

