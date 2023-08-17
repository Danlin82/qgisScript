nessesaryPlugins = ['mgrs','latlontools','brand_gis']
installdPlugins = qgis.utils.plugins.keys()
print(installdPlugins)

def neededPlugins(nessesaryList,InstalldList):
    #returnerar en lista med [True/False,[plugin som fattas]]
    if list(set(nessesaryList).intersection(set(InstalldList))) == sorted(nessesaryList):
        
        return [True,list(set(nessesaryList).difference(set(InstalldList)))]
    else:
        
        return [False,list(set(nessesaryList).difference(set(InstalldList)))]
        

print(neededPlugins(nessesaryPlugins,installdPlugins)[0])
