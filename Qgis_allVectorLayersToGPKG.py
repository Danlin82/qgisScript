import os

extentRectangle = iface.mapCanvas().extent()
layers = QgsProject.instance().layerTreeRoot().layerOrder()

#homePath = QgsProject.instance().readPath("./")
homePath = 'c:/'    #Denna bör inte ligga på nätverket då det kan ta lång tid.
folders ='export'
fileName = 'test12.gpkg'


path = os.path.normcase(os.path.join(homePath, folders))
filePath = os.path.normcase(os.path.join(homePath, folders, fileName))

  
if not os.path.exists(path):
    os.makedirs(path)

def saving_gpkg(styled_layer, out_path):
    context = QgsProject.instance().transformContext()
    name = styled_layer.name()
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.layerName = name
    options.filterExtent = extentRectangle
    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
    options.EditionCapability = QgsVectorFileWriter.CanAddNewLayer
    options.fileEncoding = styled_layer.dataProvider().encoding()
    options.driverName = "GPKG"
    errorMessage = QgsVectorFileWriter.writeAsVectorFormatV3(styled_layer, out_path, context, options)
    print(errorMessage, out_path)
    doc = QDomDocument()
    # readWriteContext = context = QgsReadWriteContext()
    styled_layer.exportNamedStyle(doc)
    gpkg_layer = QgsVectorLayer(f"{out_path}|layername={name}", name, "ogr")
    gpkg_layer.importNamedStyle(doc)
    gpkg_layer.saveStyleToDatabase(name, "", True, "")

def create_gpkg(filePath):
    schema = QgsFields()
    schema.append(QgsField('id', QVariant.Int))

    crs = QgsCoordinateReferenceSystem('epsg:3006')
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.layerName = 'Polygon layer'
    options.driverName = "GPKG"
    options.fileEncoding = 'cp1251'

    fw = QgsVectorFileWriter.create(
        fileName=filePath,
        fields=schema,
        geometryType=QgsWkbTypes.Polygon,
        srs=crs,
        transformContext=QgsCoordinateTransformContext(),
        options=options)
    del fw


if not os.path.exists(filePath):
    create_gpkg(filePath)



for layer in layers:
    if layer.type() == QgsMapLayer.VectorLayer:
          
        saving_gpkg(layer, filePath)

    elif layer.type() == QgsMapLayerType.RasterLayer:
    #    print(layer.name(),layer.width(), layer.height(), layer.rasterType(),'type: 0 = GrayOrUndefined (single band), 1 = Palette (single band), 2 = Multiband')
    #    print(layer.name(),layer.renderer().type())
        pass
    else:
        print('pass')