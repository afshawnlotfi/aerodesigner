#!/usr/bin/env python

import copy

try:
    import svgwrite
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.abspath(os.path.split(os.path.abspath(__file__))[0]+'/..'))
    import svgwrite

try:
    import airfoil
    import layout
except ImportError:
    # if airfoil is not 'installed' append parent dir of __file__ to sys.path
    import sys, os
    sys.path.insert(0, os.path.abspath(os.path.split(os.path.abspath(__file__))[0]+'/../lib'))
    import airfoil
    import layout

chord = 8.0

width = 8.5
height = 11

print "resampling and adaptive fit demo"
layout = layout.Layout( 'demo-fit', width, height )

root = airfoil.Airfoil("naca633618", 0, False)

rib = copy.deepcopy(root)
rib.scale( chord, chord )
tx = chord/3.0
ty = rib.simple_interp(rib.top, tx)
by = rib.simple_interp(rib.bottom, tx)
vd = (ty - by)
hy = by + vd / 2.0
rib.add_label( tx, hy, 14, 0, "Original Points" )
layout.draw_part_vertices( rib )

rib = copy.deepcopy(root)
rib.resample(1000, True)
rib.scale( chord, chord )
rib.fit( 200, 0.00005 )
tx = chord/3.0
ty = rib.simple_interp(rib.top, tx)
by = rib.simple_interp(rib.bottom, tx)
vd = (ty - by)
hy = by + vd / 2.0
rib.add_label( tx, hy, 14, 0, "Spline interpolation & adaptive fit to 0.00005\" tolerance" )
layout.draw_part_demo( rib )

rib = copy.deepcopy(root)
rib.resample(1000, True)
rib.scale( chord, chord )
rib.fit( 200, 0.0005 )
tx = chord/3.0
ty = rib.simple_interp(rib.top, tx)
by = rib.simple_interp(rib.bottom, tx)
vd = (ty - by)
hy = by + vd / 2.0
rib.add_label( tx, hy, 14, 0, "Spline interpolation & adaptive fit to 0.0005\" tolerance" )
layout.draw_part_demo( rib )

rib = copy.deepcopy(root)
rib.resample(1000, True)
rib.scale( chord, chord )
rib.fit( 200, 0.005 )
tx = chord/3.0
ty = rib.simple_interp(rib.top, tx)
by = rib.simple_interp(rib.bottom, tx)
vd = (ty - by)
hy = by + vd / 2.0
rib.add_label( tx, hy, 14, 0, "Spline interpolation & adaptive fit to 0.005\" tolerance" )
layout.draw_part_demo( rib )

rib = copy.deepcopy(root)
rib.resample(1000, True)
rib.scale( chord, chord )
rib.fit( 200, 0.01 )
tx = chord/3.0
ty = rib.simple_interp(rib.top, tx)
by = rib.simple_interp(rib.bottom, tx)
vd = (ty - by)
hy = by + vd / 2.0
rib.add_label( tx, hy, 14, 0, "Spline interpolation & adaptive fit to 0.01\" tolerance" )
layout.draw_part_demo( rib )

rib = copy.deepcopy(root)
rib.resample(1000, True)
rib.scale( chord, chord )
rib.fit( 200, 0.05 )
tx = chord/3.0
ty = rib.simple_interp(rib.top, tx)
by = rib.simple_interp(rib.bottom, tx)
vd = (ty - by)
hy = by + vd / 2.0
rib.add_label( tx, hy, 14, 0, "Spline interpolation & adaptive fit to 0.05\" tolerance" )
layout.draw_part_demo( rib )

rib = copy.deepcopy(root)
rib.resample(1000, True)
rib.scale( chord, chord )
rib.fit( 200, 0.15 )
tx = chord/3.0
ty = rib.simple_interp(rib.top, tx)
by = rib.simple_interp(rib.bottom, tx)
vd = (ty - by)
hy = by + vd / 2.0
rib.add_label( tx, hy, 14, 0, "Spline interpolation & adaptive fit to 0.15\" tolerance" )
layout.draw_part_demo( rib )

layout.save()
