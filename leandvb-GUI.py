#!/usr/bin/env python

from Tkinter import *
from PIL import ImageTk, Image
from os.path import expanduser
home = expanduser("~")
import os

# Simple UI voor LEANDVB, DVBS receiver.
# requires sudo apt-get install python-imaging-tk package
# keep everything in your home directory
# if you add a 180x180 pixels file called logo.png it will be
# showed in richt corner.
# Leandvb by F4DAV (github leansdr)
# Wrapper by pe2jko@540.org

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

# start the GUI

master = Tk()
master.title('LeanDVB DVBS + DVBS2 interface')

parameters = ""
lengte=0
parameter1_conv1=0
parameter2_conv2=0
parameter3_conv3= ""
print "Home directory = " + home
if os.path.isfile(home + "/leandvb-last"):
    file = open(home + "/leandvb-last", "r")
    parameter1 = file.readline() #freq
    parameter2 = file.readline() #samplerate
    parameter3 = file.readline() #fec
    parameter6 = file.readline() #tune
    parameter4 = file.readline() #fastlock
    parameter5 = file.readline() #lowsr
    parameter7 = file.readline() #viterbi
    parameter8 = file.readline() #Gui
    parameter9 = file.readline() #dvbs2
    parameter10 = file.readline() #max sensitive
    parameter11 = file.readline() #hard-metric
    parameter12 = file.readline() #rtl0
    parameter13 = file.readline() #rtl1
    parameter14 = file.readline() #pad leandvb
    parameter15 = file.readline() #ppm
    parameter16 = file.readline() #ant
    parameter17 = file.readline() #gain_lime
    parameter18 = file.readline() #gain_lime_bandbreedte
    parameter19 = file.readline() #gain_rtl
    parameter20 = file.readline() #viewer
    parameter21 = file.readline() #rolloff_factor
    parameter22 = file.readline() #rrc_rej
    parameter23 = file.readline() #nhelpers
    parameter24 = file.readline() #inpipe
    parameter25 = file.readline() 

    parameter1_conv1 = str(parameter1[:-1])
    parameter2_conv2 = int(parameter2)
    parameter3_conv3 = str(parameter3[:3])
    parameter4_conv4 = int (parameter6)
    parameter16_conv = str(parameter16[:-1])
    parameter17_conv = str(parameter17[:-1])
    parameter18_conv = str(parameter18[:-1])
    parameter19_conv = str(parameter19[:-1])
    parameter20_conv = str(parameter20[:-1])
    parameter21_conv = str(parameter21[:-1])
    parameter22_conv = str(parameter22[:-1])
    parameter23_conv = str(parameter23[:-1])
    parameter24_conv = str(parameter24[:-1])
    file.close()
else:
    parameter1_conv1 = 1252
    parameter2_conv2 = 2000
    parameter3_conv3 = "1/2"
    parameter4_conv4 = 0
    parameter1 = "1252"
    parameter2 = "2000"
    parameter3 = 1
    parameter4 = 1
    parameter5 = 1
    parameter6 = 0
    parameter7 = 0
    parameter8 = 1
    parameter9 = 1
    parameter10 = 0
    parameter11 = 0
    parameter12 = 1
    parameter13 = 0
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
rtl1 = IntVar()
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
bandbreedte_lime = StringVar()
var1.set(int(parameter4))
var2.set(int(parameter5))
var3.set(int(parameter7))
var4.set(int(parameter11))
var5.set(int(parameter8))
var6.set(int(parameter9))
var7.set(int(parameter10))
rtl0.set(int(parameter12))
rtl1.set(int(parameter13))
padlean.set(str(parameter14[:-1]))
ppm.set(int(parameter15))
ant.set(parameter16_conv)
gain_lime.set(parameter17_conv)
bandbreedte_lime.set(parameter18_conv)
gain_rtl.set(parameter19_conv)
viewer.set(parameter20_conv)
rolloff_factor.set(parameter21_conv)
rrc_rej_factor.set(parameter22_conv)
nhelpers.set(parameter23_conv)
inpipe.set(parameter24_conv)
e = Entry(master, font = "Verdana 15 bold")
f = Entry(master, font = "Verdana 15 bold")
g = Entry(master, font = "Verdana 15 bold")
h = Entry(master, font = "Verdana 15 bold")
e.insert(0, parameter1_conv1)
f.insert(0, parameter2_conv2)
g.insert(0, parameter3_conv3)
h.insert(0, parameter4_conv4)
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
    save_parms()
    stop()
    master.destroy()

def preset1():
    top = Toplevel()
    top.title("Default Settings")
    top.geometry("400x400+30+30")    
    top.transient(master)
#    C1 = Checkbutton(top, font = "Verdana 11 italic", text="RTL=0", variable=rtl0)
#    C1.pack()
#    C2 = Checkbutton(top, font = "Verdana 11 italic", text="LimeSDR=1", variable=rtl1)
#    C2.pack()
    kk= Label(top, font = "Verdana 10", text="Path to Leansdr :")
    kk.pack()
    i = Entry(top, font = "Verdana 10", width=35, textvariable=padlean)
    i.pack()

#    kl= Label(top, font = "Verdana 10", text="------------")
#    kl.pack()

    kk= Label(top, font = "Verdana 10", text="PPM offset RTL0")
    kk.pack() 

    j = Entry(top, font = "Verdana 10", width=15, textvariable=ppm)
    j.pack()

#    kn= Label(top, font = "Verdana 10", text="Antenne Lime")
#    kn.pack() 

#    k= Entry(top, font = "Verdana 10", width=15, textvariable=ant)
#    k.pack()

#    km= Label(top, font = "Verdana 10", text="Gain Lime")
#    km.pack() 

#    l= Entry(top, font = "Verdana 10", width=15, textvariable=gain_lime)
#    l.pack()

#    lm= Label(top, font = "Verdana 10", text="Bandbreedte Lime")
#    lm.pack() 

#    kp= Entry(top, font = "Verdana 10", width=15, textvariable=bandbreedte_lime)
#    kp.pack() 

    noo= Label(top, font = "Verdana 10", text="Gain RTL (0=Auto)")
    noo.pack() 

    oo= Entry(top, font = "Verdana 10", width=15, textvariable=gain_rtl)
    oo.pack() 

    qoo= Label(top, font = "Verdana 10", text="Roll Off Factor (DVBS2)")
    qoo.pack() 

    qp= Entry(top, font = "Verdana 10", width=15, textvariable=rolloff_factor)
    qp.pack() 

    qooo= Label(top, font = "Verdana 10", text="RRC Rej Factor (DVBS2)")
    qooo.pack() 

    qpp= Entry(top, font = "Verdana 10", width=15, textvariable=rrc_rej_factor)
    qpp.pack() 

    qooop= Label(top, font = "Verdana 10", text="Nhelpers (DVBS2)")
    qooop.pack() 


    qppp= Entry(top, font = "Verdana 10", width=15, textvariable=nhelpers)
    qppp.pack() 


    oooop= Label(top, font = "Verdana 10", width=15, text="Inpipe (DVBS2)")
    oooop.pack() 

    qqppp= Entry(top, font = "Verdana 10",width=15, textvariable=inpipe)
    qqppp.pack() 

#    okl= Label(top, font = "Verdana 10", text="Viewer")
#    okl.pack()

#    okll= Entry(top, font = "Verdana 10", width=15, textvariable=viewer)
#    okll.pack() 


    kll= Label(top, font = "Verdana 10", text="------------")
    kll.pack()
    topButton0 = Button(top, bg="yellow", text="SAVE", command = lambda:[save_parms(),top.destroy()])
    topButton0.pack()


#    topButton = Button(top, text="CLOSE", command = top.destroy)
#    topButton.pack(side = BOTTOM )


def save_parms():
    sub = ""
    samplerate = 0
    freq = 0
    tune = 0
    fastlock = var1.get()
    lowsr = var2.get()
    viterbi = var3.get()
    gui = var5.get()
    dvbs2 = var6.get()
    maxprocess = var7.get()
    hardmetric = var4.get()
    rtldongle0 = rtl0.get()
    rtldongle1 = rtl1.get()
    leanpad = padlean.get()
    srsubstring = f.get()
    tunesubstring = str(1)
    opslaanfreq= e.get()
    fsubstring = float(e.get())
    tunesubstring = str(1)
    freq = fsubstring * 1000000
    freqfinal=int(freq)
    freq_lime=str(fsubstring)+"M"
    samplerate = int(srsubstring) * 1000
    fec = tkvar3.get()
    tune = h.get()
    ppmwaarde = ppm.get()
    antennewaarde = ant.get()
    gain_rtlwaarde = gain_rtl.get()
    gain_limewaarde = gain_lime.get()
    viewer_waarde = viewer.get()
    rolloff_factorwaarde = rolloff_factor.get()
    rrc_rej_factorwaarde = rrc_rej_factor.get()
    bandbreedte_limewaarde = bandbreedte_lime.get()
    nhelpers_waarde = nhelpers.get()
    inpipe_waarde = inpipe.get()
    file = open(home + "/leandvb-run", "w")
    file.write("#!/bin/sh \n\n")
    file.write(sub)
    file.close()
    file = open(home+"/leandvb-last", "w")
    file.write(str(opslaanfreq) + "\n")    
    file.write(srsubstring + "\n")
    file.write(fec + "\n")
    file.write(tune + "\n")
    file.write(str(fastlock) + "\n")
    file.write(str(lowsr) + "\n")
    file.write(str(viterbi) + "\n")
    file.write(str(gui) + "\n")
    file.write(str(dvbs2) + "\n")
    file.write(str(maxprocess) + "\n")
    file.write(str(hardmetric) + "\n")
    file.write(str(rtldongle0) + "\n")
    file.write(str(rtldongle1) + "\n")
    file.write(str(leanpad) + "\n")
    file.write(str(ppmwaarde) + "\n")
    file.write(str(antennewaarde) + "\n")
    file.write(str(gain_limewaarde) + "\n")
    file.write(str(bandbreedte_limewaarde) + "\n")
    file.write(str(gain_rtlwaarde) + "\n")
    file.write(str(viewer_waarde) + "\n")
    file.write(str(rolloff_factorwaarde) + "\n")
    file.write(str(rrc_rej_factorwaarde) + "\n")
    file.write(str(nhelpers_waarde) + "\n")
    file.write(str(inpipe_waarde) + "\n")
    file.write(tunesubstring + "\n")
    file.close()

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
    dvbs2string = ""
    samplerate = 0
    freq = 0
    tune = 0
    fastlock = var1.get()
    lowsr = var2.get()
    viterbi = var3.get()
    gui = var5.get()
    dvbs2 = var6.get()
    maxprocess = var7.get()
    hardmetric = var4.get()
    rtldongle0 = rtl0.get()
    rtldongle1 = rtl1.get()
    leanpad = padlean.get()
    antennewaarde = ant.get()
    gain_limewaarde = gain_lime.get()
    gain_rtlwaarde = gain_rtl.get()
    viewer_waarde = viewer.get()
    rolloff_factorwaarde = rolloff_factor.get()
    rrc_rej_factorwaarde = rrc_rej_factor.get()
    nhelpers_waarde = nhelpers.get()
    inpipe_waarde = inpipe.get()
    bandbreedte_limewaarde = bandbreedte_lime.get()
    if (viewer_waarde == "ffplay"):
	view = "ffplay -v 0"
    else:
	view = "mplayer"
    if (lowsr == 1):
        bandbreedte = 1800000
    else:
        bandbreedte = 2400000
    if (fastlock == 1):
        fastlockstring = "--fastlock"
    else:
        fastlockstring = ""
    if (viterbi == 1):
        viterbistring = "--viterbi"
    else:
        viterbistring = ""
    if (gui == 1):
        guistring = "--gui"
    else:
        guistring = ""
    if (dvbs2 == 1):
        dvbs2string = "-S2"
    else:
        dvbs2string = "-S"
    if (maxprocess == 1):
        maxprocessstring = "--hq"
    else:
        maxprocessstring = ""
    if (hardmetric == 1):
        hardmetricstring = "--hard-metric"
    else:
        hardmetricstring = ""
    if (rtldongle0 == 1):
        rtlstring = "0"
    else:
        rtlstring = "1"
    srsubstring = f.get()
    opslaanfreq= e.get()
    fsubstring = float(e.get())
    tunesubstring = str(1)
    freq = fsubstring * 1000000
    freqfinal=int(freq)
    freq_lime=str(fsubstring)+"M"
    samplerate = int(srsubstring) * 1000
    fec = tkvar3.get()
    tune = h.get( )
    if (rtldongle0 == 1):
	if (dvbs2 == 1):
            # TODO move modcods and framesizes to settings to be compatible to all versions of leandvb. A value of 0 shall remove them from the parameterlist in the call
    		sub = "rtl_sdr -d " + rtlstring + " -f "  + str(freqfinal) + " -g " + gain_rtlwaarde +  " -s " + str(bandbreedte) + " -p " + str(ppmwaarde) + " - | " + str(leanpad) + "leandvb" + " " + guistring + " --modcods 0x0040 --framesizes 0x01 " + maxprocessstring + " " + viterbistring + " " + hardmetricstring + " " + fastlockstring + " --tune " + tune + " --standard DVB" + dvbs2string + " --ldpc-helper " + str(leanpad) + "ldpc_tool  --inpipe " + str(inpipe_waarde) + " --nhelpers " +str(nhelpers_waarde) + " --sampler rrc --rrc-rej " + str(rrc_rej_factorwaarde) + " -v --roll-off " + str(rolloff_factorwaarde) + " --sr " + str(samplerate) + " -f " + str(bandbreedte) + " | ffplay -v 0  - \n" 
	else:
		sub = "rtl_sdr -d " + rtlstring + " -f "  + str(freqfinal) + " -g " + gain_rtlwaarde +  " -s " + str(bandbreedte) + " -p " + str(ppmwaarde) + " - | " + str(leanpad) + "leandvb" + " " + guistring + " " + maxprocessstring + " " + viterbistring + " " + hardmetricstring + " " + fastlockstring + " --tune " + tune + " --cr " + str(fec) + " --standard DVB" + dvbs2string + " -v --sr " + str(samplerate) + " -f " + str(bandbreedte) + " | " + str(view) + " - \n" 
    else:
        sub1 = home+"/LimeSuite/builddir/bin/basicRX -a " + antennewaarde + " -r " + bandbreedte_limewaarde + " -g " + gain_limewaarde + " -f " + freq_lime + " -o 16 -b 3000000 &"
        sub = "cat ~/experiment | " + str(leanpad) + " " + guistring + " " + maxprocessstring + " " + viterbistring + " " + hardmetricstring + " " + fastlockstring + " --tune " + tune + " --cr " + str(fec) + " --sr " + str(samplerate) + " -f " +bandbreedte_limewaarde + " --s16 | ffplay -v 0 - &"
    file = open(home + "/leandvb-run", "w")
    file.write("#!/bin/sh \n\n")
    file.write(sub1)
    file.write("\n\n")
    file.write(sub)
    file.close()
    file = open(home + "/leandvb-last", "w")
    file.write(str(opslaanfreq) + "\n")    
    file.write(srsubstring + "\n")
    file.write(fec + "\n")
    file.write(tune + "\n")
    file.write(str(fastlock) + "\n")
    file.write(str(lowsr) + "\n")
    file.write(str(viterbi) + "\n")
    file.write(str(gui) + "\n")
    file.write(str(dvbs2) + "\n")
    file.write(str(maxprocess) + "\n")
    file.write(str(hardmetric) + "\n")
    file.write(str(rtldongle0) + "\n")
    file.write(str(rtldongle1) + "\n")
    file.write(str(leanpad) + "\n")
    file.write(str(ppmwaarde) + "\n")
    file.write(str(antennewaarde) +"\n")
    file.write(str(gain_limewaarde) +"\n")
    file.write(str(bandbreedte_limewaarde) +"\n")
    file.write(str(gain_rtlwaarde) + "\n")
    file.write(str(viewer_waarde) + "\n")
    file.write(str(rolloff_factorwaarde) + "\n")
    file.write(str(rrc_rej_factorwaarde) + "\n")
    file.write(str(nhelpers_waarde) + "\n")
    file.write(str(inpipe_waarde) + "\n")
    file.write(tunesubstring + "\n")
    file.close()
    os.system("sh " + home + "/leandvb-run &")

Button(master,font = "Verdana 11 italic", text='EXIT', command=exit).grid(row=7, column=3,sticky=E)
Button(master, font = "Verdana 11 italic",highlightbackground='red',text='START', command=callback).grid(row=7, column=3,sticky=W)
Button(master, font = "Verdana 11 italic",text='STOP', command=stop).grid(row=7, column=4,sticky=W)
Button(master, font = "Verdana 11 italic",fg='red',highlightbackground='blue',text='    Settings    ', command=preset1).grid(row=5, column=3)
#Button(master, font = "Verdana 11 italic",fg='red',highlightbackground='blue',text='  Save Settings ', command=save_parms).grid(row=5, column=3)
#Button(master, font = "Verdana 9 italic",fg='red',highlightbackground='blue',text='UI options', command=preset3).grid(row=2, column=5, ipady=5,sticky=E, ipadx=5)
#Button(master, font = "Verdana 9 italic",fg='red',highlightbackground='blue',text='General Options', command=preset4).grid(row=3, column=5, ipady=5,sticky=E,ipadx=5)

tkvar1 = StringVar(master)
 
# Frequency Dropdown
choices1 = { '1252','1257','1260','436','437','1255','1252.600','1280','1250','1253'}

tkvar1.set(parameter1[:-1]) # set the default option
 
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

tkvar2.set(parameter2[:-1]) # set the default option
 
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
tkvar3.set(parameter3_conv3)
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
tkvar4.set(parameter4_conv4) # set the default option
 
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
