# arcpy-geometry
Samples of the use of arcpy Geometry

geom_obj01: Read coordinates from a text file, use arcpy.Array and arcpy.Point to construct arcpy.Polyline geometries and use an arcpy.da.InsertCursor to add the polylines to the new feature class.

geom_obj02: Reading coordinates from a text file, reformat the text into WKT LINESTRINGs and use arcpy.FromWKT to create arcpy.Polyline geometries and use an arcpy.da.InsertCursor to add the polylines to the new feature class.
