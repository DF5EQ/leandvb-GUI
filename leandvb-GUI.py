#!/usr/bin/env python

# Simple UI voor LEANDVB, DVBS receiver.
# requires sudo apt-get install python-imaging-tk package
# keep everything in your home directory
# if you add a 180x180 pixels file called logo.png it will be
# showed in right corner.
# Leandvb by F4DAV (github leansdr)
# Wrapper by pe2jko@540.org

# TODO store parameters in json file instead of simple list
# TODO change path for parameter file from ~/ to ~/.leandvb-GUI/
# TODO add entry (parameter) for local oscillator frequency
# TODO change checkbutton for LowSR(bandwith) in entry or list-entry
# TODO leandvb-run as function like leandvb-stop
# TODO leandvb: --tune is broken, use --derotate instead
# TODO change dutch names in english
# TODO streamline usage of viewer ffplay and mplayer
# TODO investigate usefullness of rtl0

from Tkinter import *
from PIL import ImageTk, Image
from os.path import expanduser
home = expanduser("~")
import os
import json

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
    leanpad = padlean.get()
    ppmwaarde = ppm.get()
    antennewaarde = ant.get()
    gain_rtlwaarde = gain_rtl.get()
    gain_limewaarde = gain_lime.get()
    viewer_waarde = viewer.get()
    rolloff_factorwaarde = rolloff_factor.get()
    rrc_rej_factorwaarde = rrc_rej_factor.get()
    bandwidth_limewaarde = bandwidth_lime.get()
    nhelpers_waarde = nhelpers.get()
    inpipe_waarde = inpipe.get()
    modcods_value = modcods.get()
    framesizes_value = framesizes.get()

    file = open(home+"/leandvb-last", "w")
    file.write("\n")    
    file.write("\n")
    file.write("\n")
    file.write("\n")
    file.write("\n")
    file.write("\n")
    file.write("\n")
    file.write("\n")
    file.write("\n")
    file.write("\n")
    file.write("\n")
    file.write("\n")
    file.write("\n")
    file.write(str(leanpad) + "\n")
    file.write(str(ppmwaarde) + "\n")
    file.write(str(antennewaarde) + "\n")
    file.write(str(gain_limewaarde) + "\n")
    file.write(str(bandwidth_limewaarde) + "\n")
    file.write(str(gain_rtlwaarde) + "\n")
    file.write(str(viewer_waarde) + "\n")
    file.write(str(rolloff_factorwaarde) + "\n")
    file.write(str(rrc_rej_factorwaarde) + "\n")
    file.write(str(nhelpers_waarde) + "\n")
    file.write(str(inpipe_waarde) + "\n")
    file.write("\n")
    file.write(str(modcods_value) + "\n")
    file.write(str(framesizes_value) + "\n")
    file.close()

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
    parameters["rtldongle0"    ] = bool(rtl0.get())
    parameters["leanpad"       ] = leanpad
    parameters["ppm"           ] = str(ppmwaarde)
    parameters["antenne"       ] = antennewaarde
    parameters["gain_lime"     ] = gain_limewaarde
    parameters["bandwidth_lime"] = bandwidth_limewaarde
    parameters["gain_rtl"      ] = gain_rtlwaarde
    parameters["viewer"        ] = viewer_waarde
    parameters["rolloff_factor"] = rolloff_factorwaarde
    parameters["rrc_rej_factor"] = rrc_rej_factorwaarde
    parameters["nhelpers"      ] = nhelpers_waarde
    parameters["inpipe"        ] = inpipe_waarde
    parameters["modcods"       ] = modcods_value
    parameters["framesizes"    ] = framesizes_value

    file = open(home + "/leandvb-last.json", "w")
    file.write(json.dumps(parameters, indent=4, sort_keys=True))
    file.close()

def parameters_load():
    global parameters
    print "loading parameters from json file"
    file = open(home + "/leandvb-last.json", "r")
    parameters = json.load(file)
    file.close()

def parameters_default():
    print "loading parameters with defaults"
    parameters["frequency"     ] = 741.500
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
    parameters["rtldongle0"    ] = True
    parameters["leanpad"       ] = ""
    parameters["ppm"           ] = "0"
    parameters["antenne"       ] = "1"
    parameters["gain_lime"     ] = "0.5"
    parameters["bandwidth_lime"] = "3500000"
    parameters["gain_rtl"      ] = "36"
    parameters["viewer"        ] = "ffplay"
    parameters["rolloff_factor"] = "0.35"
    parameters["rrc_rej_factor"] = "30"
    parameters["nhelpers"      ] = "6"
    parameters["inpipe"        ] = "32000000"
    parameters["modcods"       ] = "0x0040"
    parameters["framesizes"    ] = "0x01"

#===== GUI ====================================================================

master = Tk()
master.title('LeanDVB DVBS + DVBS2 interface')

lengte=0
parameter2_conv2=0
parameter3_conv3= ""
print "Home directory = " + home

if os.path.isfile(home + "/leandvb-last.json"):
    parameters_load()
else:
    parameters_default()

print (json.dumps(parameters, sort_keys=True))

if os.path.isfile(home + "/leandvb-last"):
    file = open(home + "/leandvb-last", "r")
    file.readline()
    file.readline()
    file.readline()
    file.readline()
    file.readline()
    file.readline()
    file.readline()
    file.readline()
    file.readline()
    file.readline()
    file.readline()
    file.readline()
    file.readline()
    parameter14 = file.readline() #pad leandvb
    parameter15 = file.readline() #ppm
    parameter16 = file.readline() #ant
    parameter17 = file.readline() #gain_lime
    parameter18 = file.readline() #gain_lime_bandwidth
    parameter19 = file.readline() #gain_rtl
    parameter20 = file.readline() #viewer
    parameter21 = file.readline() #rolloff_factor
    parameter22 = file.readline() #rrc_rej
    parameter23 = file.readline() #nhelpers
    parameter24 = file.readline() #inpipe
    parameter25 = file.readline()
    parameter26 = file.readline() #modcods
    parameter27 = file.readline() #framesizes 

    parameter16_conv = str(parameter16[:-1])
    parameter17_conv = str(parameter17[:-1])
    parameter18_conv = str(parameter18[:-1])
    parameter19_conv = str(parameter19[:-1])
    parameter20_conv = str(parameter20[:-1])
    parameter21_conv = str(parameter21[:-1])
    parameter22_conv = str(parameter22[:-1])
    parameter23_conv = str(parameter23[:-1])
    parameter24_conv = str(parameter24[:-1])
    parameter26_conv = str(parameter26[:-1])
    parameter27_conv = str(parameter27[:-1])
    file.close()
else:
    parameter14 = home+"/leansdr/src/apps/ "
    parameter15 = 1
    parameter16_conv = 1
    parameter17_conv = "0.5"
    parameter18_conv = "3500000"
    parameter19_conv = "0"
    parameter20_conv = "ffplay"
    parameter21_conv = "0.35"
    parameter22_conv = "20"
    parameter23_conv = "4"
    parameter24_conv = "1000000"
    parameter26_conv = "0x0040"
    parameter27_conv = "0x01"

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

rtl0 = IntVar()
ppm = IntVar()
padlean = StringVar()
ant = StringVar()
gain_rtl = StringVar()
gain_lime = StringVar()
viewer = StringVar()
rolloff_factor = StringVar()
rrc_rej_factor = StringVar()
nhelpers = StringVar()
inpipe = StringVar()
bandwidth_lime = StringVar()
modcods = StringVar()
framesizes = StringVar()
var1.set(parameters["fastlock"])
var2.set(parameters["lowsr"])
var3.set(parameters["viterbi"])
var4.set(parameters["hardmetric"])
var5.set(parameters["gui"])
var6.set(parameters["dvbs2"])
var7.set(parameters["maxprocess"])
rtl0.set(parameters["rtldongle0"])
padlean.set(str(parameter14[:-1]))
ppm.set(int(parameter15))
ant.set(parameter16_conv)
gain_lime.set(parameter17_conv)
bandwidth_lime.set(parameter18_conv)
gain_rtl.set(parameter19_conv)
viewer.set(parameter20_conv)
rolloff_factor.set(parameter21_conv)
rrc_rej_factor.set(parameter22_conv)
nhelpers.set(parameter23_conv)
inpipe.set(parameter24_conv)
modcods.set(parameter26_conv)
framesizes.set(parameter27_conv)
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

def exit():
    parameters_save()
    stop()
    master.destroy()


def settings_window():

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

    save_button.grid      (row=9, column=2, sticky=EW)
    cancel_button.grid    (row=9, column=3, sticky=EW)

    settings_window.columnconfigure(0, weight=0)
    settings_window.columnconfigure(1, weight=0)
    settings_window.columnconfigure(2, weight=1)
    settings_window.columnconfigure(3, weight=1)

def stop():
    file = open(home + "/leandvb-stop", "w")
    file.write("#!/bin/sh \n")
    file.write("\n")
    file.write("killall rtl_sdr\n")
    file.write("killall ffplay\n")
    file.write("killall leandvb\n")
    file.write("killall basicRX\n")
    file.write("\n")
    file.write("exit 0\n")
    file.close()
    os.system("sh " + home + "/leandvb-stop")

def callback():
    ppmwaarde = ppm.get()
    sub = ""
    sub1 = ""
    view = ""
    leanpad = padlean.get()
    antennewaarde = ant.get()
    gain_limewaarde = gain_lime.get()
    gain_rtlwaarde = gain_rtl.get()
    viewer_waarde = viewer.get()
    rolloff_factorwaarde = rolloff_factor.get()
    rrc_rej_factorwaarde = rrc_rej_factor.get()
    nhelpers_waarde = nhelpers.get()
    inpipe_waarde = inpipe.get()
    modcods_value = modcods.get()
    framesizes_value = framesizes.get()
    bandwidth_limewaarde = bandwidth_lime.get()
    if (viewer_waarde == "ffplay"):
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
    if (rtl0.get() == True):
        rtl = "0"
    else:
        rtl = "1"
    if (modcods_value == ""):
        modcods_string = ""
    else:
        modcods_string = " --modcods " + modcods_value
    if (framesizes_value == ""):
        framesizes_string = ""
    else:
        framesizes_string = " --framesizes " + framesizes_value
    frequency = int(float(e.get()) * 1000000 )
    samplerate = int(f.get()) * 1000
    fec = tkvar3.get()
    tune = h.get()
    if (rtl0.get() == True):
        if (var6.get() == True): #dvbs2
            sub = "rtl_sdr" + \
                  " -d " + rtl + \
                  " -f "  + str(frequency) + \
                  " -g " + gain_rtlwaarde +  \
                  " -s " + str(bandwidth) + \
                  " -p " + str(ppmwaarde) + \
                  " -" + \
                  " | " + \
                  str(leanpad) + "leandvb" + \
                  gui + \
                  modcods_string + \
                  framesizes_string + \
                  maxprocess + \
                  viterbi + \
                  hardmetric + \
                  fastlock + \
                  " --tune " + tune + \
                  " --standard " + dvbs + \
                  " --ldpc-helper " + str(leanpad) + "ldpc_tool" + \
                  " --inpipe " + str(inpipe_waarde) + \
                  " --nhelpers " +str(nhelpers_waarde) + \
                  " --sampler rrc" + \
                  " --rrc-rej " + str(rrc_rej_factorwaarde) + \
                  " -v" + \
                  " --roll-off " + str(rolloff_factorwaarde) + \
                  " --sr " + str(samplerate) + \
                  " -f " + str(bandwidth) + \
                  " | " + \
                  "ffplay -v 0 -" + \
                  " \n"
        else:
            sub = "rtl_sdr" + \
                  " -d " + rtl + \
                  " -f "  + str(frequency) + \
                  " -g " + gain_rtlwaarde +  \
                  " -s " + str(bandwidth) + \
                  " -p " + str(ppmwaarde) + \
                  " -" + \
                  " | " + \
                  str(leanpad) + "leandvb" + \
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
                  str(view) + " -" + \
                  " \n" 
    else:
        sub1 = home + "/LimeSuite/builddir/bin/basicRX" + \
               " -a " + antennewaarde + \
               " -r " + bandwidth_limewaarde + \
               " -g " + gain_limewaarde + \
               " -f " + "freq_lime" + \
               " -o 16" + \
               " -b 3000000" + \
               " &"
        sub = "cat ~/experiment" + \
              " | " + \
              str(leanpad) + \
              gui + \
              maxprocess + \
              viterbi + \
              hardmetric + \
              fastlock + \
              " --tune " + tune + \
              " --cr " + fec + \
              " --sr " + str(samplerate) + \
              " -f " + bandwidth_limewaarde + \
              " --s16" + \
              " | " + \
              "ffplay -v 0 - &"
    print "sub:\n",sub

    parameters_save()

    file = open(home + "/leandvb-run", "w")
    file.write("#!/bin/sh \n\n")
    file.write(sub1)
    file.write("\n\n")
    file.write(sub)
    file.close()
    os.system("sh " + home + "/leandvb-run &")

Button(master,font = "Verdana 11 italic", text='EXIT', command=exit).grid(row=7, column=3,sticky=E)
Button(master, font = "Verdana 11 italic",highlightbackground='red',text='START', command=callback).grid(row=7, column=3,sticky=W)
Button(master, font = "Verdana 11 italic",text='STOP', command=stop).grid(row=7, column=4,sticky=W)
Button(master, font = "Verdana 11 italic",fg='red',highlightbackground='blue',text='    Settings    ', command=settings_window).grid(row=5, column=3)

master.protocol("WM_DELETE_WINDOW", exit)

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

