# Jython Script for ImageJ / Fiji

from ij import IJ
from ij.plugin import ZProjector
from ij.plugin import ChannelSplitter
from ij.measure import ResultsTable
import os
import sys
from java.awt.event import KeyAdapter, KeyEvent

neuron_channel = 1            
projection_method = "AVG"     
view_lut = "Green"            

do_display_autoscale = True
display_saturated = 0.01      

input_dir = IJ.getDirectory("Choose the folder containing your .czi images")
if not input_dir:
    sys.exit("No folder selected")

files = [f for f in os.listdir(input_dir) if f.lower().endswith(".czi")]
if not files:
    IJ.error("No .czi files found.")
    sys.exit()

rt = ResultsTable.getResultsTable()
if rt is None:
    rt = ResultsTable()

current_index = 0

def process_next_image():
    global current_index

    if current_index >= len(files):
        save_path = os.path.join(input_dir, "Quantification_Results.csv")
        rt.save(save_path)
        IJ.showMessage("Done!", "Processed {} images.\nSaved to: {}".format(len(files), save_path))
        return

    filename = files[current_index]
    path = os.path.join(input_dir, filename)
    current_index += 1

    # 1) Open CZI (Bio-Formats)
    IJ.run(
        "Bio-Formats Importer",
        "open=[" + path + "] autoscale color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT"
    )
    imp = IJ.getImage()

    nC = imp.getNChannels()
    IJ.log("Opened: {} | Channels detected: {}".format(filename, nC))

    if neuron_channel < 1 or neuron_channel > nC:
        imp.close()
        IJ.error("neuron_channel={} is out of range (image has {} channels).".format(neuron_channel, nC))
        process_next_image()
        return

    # 2) Force single-channel selection by splitting
    ch_imps = ChannelSplitter.split(imp)
    imp_ch = ch_imps[neuron_channel - 1] 

    imp.close()
    for i, tmp in enumerate(ch_imps):
        if tmp is not imp_ch:
            tmp.close()

    # 3) Z projection on the selected channel only
    zp = ZProjector(imp_ch)
    if projection_method == "SUM":
        zp.setMethod(ZProjector.SUM_METHOD)
    elif projection_method == "AVG":
        zp.setMethod(ZProjector.AVG_METHOD)
    else:
        zp.setMethod(ZProjector.MAX_METHOD)

    zp.doProjection()
    proj = zp.getProjection()

    imp_ch.close()

    # 4) Show projection 
    proj.show()

    if view_lut == "Green":
        IJ.run(proj, "Green", "")
    else:
        IJ.run(proj, "Grays", "")

    if do_display_autoscale:
        try:
            proj.resetDisplayRange()
        except:
            pass
        IJ.run(proj, "Enhance Contrast", "saturated={0}".format(display_saturated))

    IJ.setTool("freehand")

    win = proj.getWindow()
    canvas = win.getCanvas()
    listener = SpacebarListener(proj, filename)
    canvas.addKeyListener(listener)

    win.toFront()
    canvas.requestFocus()

    IJ.showStatus("Draw FREEHAND ROI on " + filename + " then press SPACEBAR")


class SpacebarListener(KeyAdapter):
    def __init__(self, imp, filename):
        self.imp = imp
        self.filename = filename
        self.processed = False

    def keyPressed(self, event):
        if event.getKeyCode() == KeyEvent.VK_SPACE and not self.processed:
            self.processed = True

            win = self.imp.getWindow()
            if win:
                canvas = win.getCanvas()
                canvas.removeKeyListener(self)

            roi = self.imp.getRoi()
            if roi is None:
                IJ.showStatus("No ROI found. Draw ROI first, then press SPACEBAR.")
                self.processed = False
                if win:
                    canvas.addKeyListener(self)
                    canvas.requestFocus()
                return

            stats = self.imp.getStatistics()

            rt.incrementCounter()
            rt.addValue("Label", self.filename)
            rt.addValue("Area", stats.area)
            rt.addValue("Mean", stats.mean)
            rt.addValue("Min", stats.min)
            rt.addValue("Max", stats.max)
            rt.addValue("IntDen", stats.area * stats.mean)
            rt.show("Results")

            self.imp.changes = False
            self.imp.close()

            process_next_image()


process_next_image()
