"""Provides a scripting component.
    Inputs:
        imagePath:  String - Path to input image, e.g. "E:\\Pictures\\Paul.png"
        xSpacing:   int     pixel spacing of panels in horizontal-direction, e.g. 30
        YSpacing:   int     pixel spacing of panels in vertical-direction, e.g. 30
        Resolution  int     number if pixels to skip in image to reduce resolution (and run-time), e.g. 10 => Draw every 10 pixels
    Outputs:
        None (but some nicely coloured Panels appear on the canvas)
"""

__author__ = "Paul Shepherd"
__version__ = "2020.10.02"

import rhinoscriptsyntax as rs
import Grasshopper as gh
import System.Drawing as sd

NICKNAME = ""  # All panels called this get deleted every time it is run, so be careful

aComponent = ghenv.Component
theDoc = aComponent.OnPingDocument()

def remove_old():
    try:
        listToRemove = list()
        for aObj in theDoc.Objects:
            if type(aObj) is gh.Kernel.Special.GH_Panel:
                if aObj.NickName == NICKNAME:
                    listToRemove.append(aObj)
        print "Removing %d old panels" % len(listToRemove)
        for aObj in listToRemove:
            theDoc.RemoveObject(aObj,False)
    except Exception, ex:
        ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning,str(ex))

def make_new(aBitmap, x_spacing, y_spacing, resolution):
    try:
        for x in range(aBitmap.Width//resolution) :
            for y in range(aBitmap.Height//resolution) :
                aColour = aBitmap.GetPixel(x*resolution,y*resolution)
                if (aColour.A > 128) :  #  Make a panel for non-transparent pixels only
                    aPanel = gh.Kernel.Special.GH_Panel()
                    aPanel.NickName = NICKNAME
                    aPanel.UserText = ""
                    aPanel.Properties.Colour = aColour
                    aPanel.Properties.Font = sd.Font("Trebuchet MS", 4)
                    aPanel.Properties.Multiline = False
                    theDoc.AddObject(aPanel,False,theDoc.ObjectCount+1)
                    aPanel.Attributes.Pivot = sd.PointF(x*x_spacing,y*y_spacing)
                    aPanel.Attributes.Bounds = sd.RectangleF(0,0,x_spacing,y_spacing)
    except Exception, ex:
        ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning,str(ex))
        

try:
    theBitmap = sd.Bitmap(imagePath)
    remove_old()
    print "Creating {:d}x{:d} Image".format(theBitmap.Width,theBitmap.Height)
    make_new(theBitmap, xSpacing, ySpacing, Resolution)
except Exception, ex:
    ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning,str(ex))



