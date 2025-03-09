import sys
import os

#Usage command line arguments to use in command line
#in_txt = r'C:\acgis\gis4207_prog\data\Week11\canada.txt'
#out_shp = r'C:\acgis\gis4207_prog\data\Week11\outputs\canada.shp'

def main():

    if len(sys.argv) != 3:
        print('Usage geom_obj01.py in_txt out_shp')
        sys.exit()
    
    in_txt = sys.argv[1] 
    out_shp = sys.argv[2]
    
    if not os.path.exists(in_txt):
        print(f"{in_txt} text file does not exist.")
        sys.exit()
    
    #Time it takes to create feature class
    import time
    start = time.perf_counter()
    _creating_polyline_geometries(in_txt, out_shp)
    end = time.perf_counter()
    print(f"Elapsed using feature class as output: {end - start} s")


def _txt_to_dict(in_txt):
    """Reading in the text file and converting it to a dictionnary with 
    polyline ID as keys and a list of coordinates of polyline vertices as values

    Args:
        in_txt (path): text file with polyline ID and coordinates

    Returns:
        dictionary: dictionary of polyline ID (keys) and list of coordinates of polyline vertices (values)
    """
    with open (in_txt) as infile:
        dict_polylines = {}
        key_dict = None
        for line in infile:
            line_stripped = line.rstrip('\n')
            if line_stripped.isdigit() == True:
                if key_dict is not None: # Check if we are not reading the first line of the txt file
                    dict_polylines[key_dict] = polyline_coordinates
                key_dict = int(line_stripped)
                polyline_coordinates = []
            else:
                point_coordinates = []
                for coordinate in line_stripped.split():
                    point_coordinates.append(float(coordinate))
                polyline_coordinates.append(point_coordinates)
        if key_dict is not None: # Save the last set of coordinates to the dictionary
            dict_polylines[key_dict] = polyline_coordinates
                
    return dict_polylines

def _creating_polyline_geometries(in_txt, out_shp):
    """Creating polyline geometries as a feature class than can be opened in ArcGIS Pro
    """
    dict_polylines = _txt_to_dict(in_txt)
    raw_polylines = []
    polylines = []

    import arcpy

    arcpy.env.overwriteOutput = True

    #Using dictionary to create polylines
    for item in dict_polylines.values():
        raw_polylines.append(item)
    
    #Creating empty feature class 
    out_name = os.path.basename(out_shp)
    out_path = os.path.dirname(out_shp)
    geometry_type = 'POLYLINE'
    WKID = '4326'
    fcPoly = arcpy.management.CreateFeatureclass(out_path, out_name, geometry_type, spatial_reference = WKID)[0]
    
    #Using InsertCursor to add polylines to new feature class
    for raw_polyline in raw_polylines:
        polylines.append(arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in raw_polyline])))
    
    with arcpy.da.InsertCursor(fcPoly, ['SHAPE@']) as cursor:
        for polyline in polylines:
            cursor.insertRow([polyline])

if __name__ == '__main__':
    main()

