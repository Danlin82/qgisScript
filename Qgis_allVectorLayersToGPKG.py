import os
from datetime import datetime

now = datetime.now()

extentRectangle = iface.mapCanvas().extent()
layers = QgsProject.instance().layerTreeRoot().layerOrder()


#---------------------------------------------------------------
#Kan ändras till valfi mapp och filnamn

#homePath = QgsProject.instance().readPath("./")
homePath = 'c:/'                        #Denna bör inte ligga på nätverket då det kan ta lång tid.
folders ='export'                       #Mappstruktur ex huvudmapp/undermapp.
fileName = 'eget_data_vector.gpkg'                #Filnamn med filändelse

#---------------------------------------------------------------


  
if not os.path.exists(path):
    os.makedirs(path)

def saving_gpkg(styled_layer, out_path, layerPrefixString):
    context = QgsProject.instance().transformContext()
    name = styled_layer.name()
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.layerName = layerPrefixString+name
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
    gpkg_layer = QgsVectorLayer(f"{out_path}|layername={layerPrefixString+name}", name, "ogr")
    gpkg_layer.importNamedStyle(doc)
    gpkg_layer.saveStyleToDatabase(name, "", True, "")

def create_gpkg(filePath):
    schema = QgsFields()
    schema.append(QgsField('GPKG parent project', QVariant.String))
    schema.append(QgsField('GPKG skapad datum', QVariant.String))
    feature = QgsFeature(schema)
    feature[1] = now.strftime("%Y%m%d %H:%M:%S")
    feature[0] = QgsProject.instance().absoluteFilePath()

    crs = QgsCoordinateReferenceSystem('epsg:3006')
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.layerName = 'Metadata'
    options.driverName = "GPKG"
    options.fileEncoding = 'cp1251'

    fw = QgsVectorFileWriter.create(
        fileName=filePath,
        fields=schema,
        geometryType=QgsWkbTypes.NoGeometry,
        srs=crs,
        transformContext=QgsCoordinateTransformContext(),
        options=options)
    fw.addFeature(feature)
    del fw

path = os.path.normcase(os.path.join(homePath, folders))
filePath = os.path.normcase(os.path.join(homePath, folders, fileName))

create_gpkg(filePath)

layerPrefix = 1

for layer in layers:
    layerPrefixString = str(layerPrefix).zfill(2)+'-'
    if layer.type() == QgsMapLayer.VectorLayer:
        layerPrefix += 1
        saving_gpkg(layer, filePath, layerPrefixString)

    elif layer.type() == QgsMapLayerType.RasterLayer:
         pass
    else:
        pass


