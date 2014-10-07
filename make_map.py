#!/usr/bin/env python
import mapnik
stylesheet = "node_lens.xml"
image = "node_lens.png"
m = mapnik.Map(1200, 600)
mapnik.load_map(m, stylesheet)
m.zoom_all()
mapnik.render_to_file(m, image)
print "rendered image to '%s'" % image
