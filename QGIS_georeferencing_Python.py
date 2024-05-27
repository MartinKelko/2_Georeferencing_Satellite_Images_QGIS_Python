# read the blog here (https://medium.com/@martin2kelko/automating-georeferencing-of-satellite-images-in-qgis-using-python-837f3abef341) > article walks through the script, explaining each
# part and how it works to make the georeferencing process more efficient

from qgis.core import (
    QgsRasterLayer,
    QgsPointXY,
    QgsApplication
)
from osgeo import gdal

# Initialize QGIS Application
QgsApplication.setPrefixPath("C:/Program Files/QGIS 3.36.0", True)
qgs = QgsApplication([], False)
qgs.initQgis()

try:
    # Load the raster layer
    input_tiff = 'C:/Users/marti/PycharmProjects/8 QGIS_georeferencing_Python/bagana.jpg'
    raster_layer = QgsRasterLayer(input_tiff, "Input Raster")

    if not raster_layer.isValid():
        print("Layer failed to load!")
        qgs.exitQgis()
        exit()

    # Define control points (source_image_point, target_geo_point)
    control_points = [
        (QgsPointXY(100, 100), QgsPointXY(10.0, 20.0)),
        (QgsPointXY(500, 100), QgsPointXY(12.0, 20.0)),
        (QgsPointXY(100, 500), QgsPointXY(10.0, 22.0)),
        (QgsPointXY(500, 500), QgsPointXY(12.0, 22.0)),
    ]

    # Apply the transformation using gdal
    output_tiff = 'C:/Users/marti/PycharmProjects/8 QGIS_georeferencing_Python/georeferenced_bagana.tiff'

    # Define the GCPs (Ground Control Points)
    gcps = []
    for src_point, tgt_point in control_points:
        gcp = gdal.GCP(tgt_point.x(), tgt_point.y(), 0, src_point.x(), src_point.y())
        gcps.append(gcp)

    # Load the input raster
    src_ds = gdal.Open(input_tiff)
    if src_ds is None:
        print("Failed to open input TIFF.")
        qgs.exitQgis()
        exit()

    # Apply the GCPs
    driver = gdal.GetDriverByName('GTiff')
    dst_ds = driver.CreateCopy(output_tiff, src_ds, 0)

    # Set the GCPs and the target CRS (WGS84, EPSG:3857)
    dst_ds.SetGCPs(gcps, 'EPSG:3857')

    # Close the datasets
    src_ds = None
    dst_ds = None

    print("Georeferencing successful!")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Clean up
    qgs.exitQgis()