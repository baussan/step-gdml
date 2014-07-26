#!/usr/bin/env python2

from __future__ import division, print_function, absolute_import

import sys
if len(sys.argv) != 3:
    print("Usage: step-gdml path/to/FreeCAD/lib filename.stp")
    quit()

sys.path.append(sys.argv[1])
filename = sys.argv[2]

import os,time
import FreeCAD
import Part
from fast_export import export_to_gdml
import resource

def print_memusage():
    print("MEMORY: "+str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0))

class block():
    def __init__(self, text):
        self.text = text
    def __enter__(self):
        print("\n\n      ENTER {}\n\n".format(self.text))
        self.time = time.time()
    def __exit__(self, x,y,z):
        print("\n\n      LEAVE {}; t={}\n\n".format(self.text,time.time()-self.time))

print_memusage()

with block("READ"):
    Part.open(filename)

print_memusage()

# Precision is a float in (0,1]
# 1 is fast, 10^-8 will OOM you.
# Does NOT improve triangle quality
precision = 1

doc = FreeCAD.getDocument("Unnamed")

def unpack(doc):
    objs = doc.findObjects()

    things = []
    for idx, obj in enumerate(objs):
        verts, tris = obj.Shape.tessellate(precision)

        print_memusage()

        yield ([(v.x,v.y,v.z) for v in verts], tris, str(idx), "ALUMINUM")

# clean out FreeCAD

with block("EXPORT"):
    export_to_gdml("output.gdml", unpack(doc))

print_memusage()
