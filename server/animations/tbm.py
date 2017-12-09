import time
from animation import Animation
import urllib
import xml.etree.ElementTree

station_color = [0.5,0.5,0, 0.01]

class Tbm(Animation):
  def __init__(self):
    Animation.__init__(self)
    self.line = 60 # B
    self.key = '2EBR7OCLQ0'
    self.way = 'RETOUR'
    
    self.namespaces = {'ms': 'http://mapserver.gis.umn.edu/mapserver',
              'gml': 'http://www.opengis.net/gml',
              'wfs': 'http://www.opengis.net/wfs',
              'ogc': 'http://www.opengis.net/ogc',
              'cub': 'http://data.bordeaux-metropole.fr',
              'wps': 'http://www.opengis.net/wps/1.0.0',
              'bm' : "http://data.bordeaux-metropole.fr/wfs"}
    
    self.uri = "http://data.bordeaux-metropole.fr/wfs?key=%s&REQUEST=GetFeature&SERVICE=WFS&SRSNAME=EPSG%%3A3945&TYPENAME=SV_VEHIC_P&VERSION=1.1.0&Filter=%%3CFilter%%3E%%3CAND%%3E%%3CPropertyIsEqualTo%%3E%%3CPropertyName%%3ERS_SV_LIGNE_A%%3C%%2FPropertyName%%3E%%3CLiteral%%3E%d%%3C%%2FLiteral%%3E%%3C%%2FPropertyIsEqualTo%%3E%%3CPropertyIsEqualTo%%3E%%3CPropertyName%%3ESENS%%3C%%2FPropertyName%%3E%%3CLiteral%%3E%s%%3C%%2FLiteral%%3E%%3C%%2FPropertyIsEqualTo%%3E%%3C%%2FAND%%3E%%3C%%2FFilter%%3E"%(self.key, self.line, self.way)
    self.stations = self.get_stations()
    print self.stations
  
  def get_stations(self):
    ##line = 267447291
    ##uri = "https://data.bordeaux-metropole.fr/wps?key=%s&service=WPS&version=1.0.0&request=Execute&Identifier=saeiv_arrets_chemin&DataInputs=GID%%3D%s"%(self.key,line)
    
    uri = "https://data.bordeaux-metropole.fr/wps?key=%s&service=WPS&version=1.0.0&request=Execute&Identifier=saeiv_arrets_sens&DataInputs=GID%%3D%s;SENS%%3DALLER&_=1509997771598"%(self.key,self.line)
    print uri
    #handler = urllib.urlopen(uri)
    #data = handler.read()
    ##print data
    #root = xml.etree.ElementTree.fromstring(data)
    #raw_stations = root.findall("wps:ProcessOutputs/wps:Output/wps:Data/wps:ComplexData/gml:featureMember/cub:SV_ARRET_P", self.namespaces)
    #stations = []
    #for station in raw_stations:
      #gid = int(station.find('cub:GID', self.namespaces).text)
      #libelle = station.find('cub:LIBELLE', self.namespaces).text
      #stations.append({gid :  libelle})
    #return stations
    return [{'id':[4311, 3862], 'name': 'France.Alouette'}, {'id':[1628, 3114], 'name': 'Gare.P.Alouette'}, {'id':[1775, 1776], 'name': 'Hop.H.Leveque'}, {'id':[913, 914], 'name': 'Cap Metiers'}, {'id':[835, 836], 'name': 'Chataigneraie'}, {'id':[480, 481], 'name': 'Bougnard'}, {'id':[481], 'name': 'Bougnard'}, {'id':[3627, 3628], 'name': 'Saige'}, {'id':[3977, 3979], 'name': 'Unitec'}, {'id':[2843, 2846, 2849], 'name': 'Montaigne'}, {'id':[2849], 'name': 'Montaigne'}, {'id':[1509, 1510], 'name': 'Francois Bordes'}, {'id':[1265, 1266], 'name': 'Doyen Brus'}, {'id':[152,154], 'name': 'Arts Et Metiers'}, {'id':[403, 404], 'name': 'Bethanie'}, {'id':[3072, 3073], 'name': 'Peixotto'}, {'id':[1485, 1486], 'name': 'Forum'}, {'id':[3528, 3531], 'name': 'Roustaing'}, {'id':[281, 283], 'name': 'St Genes'}, {'id':[369, 370], 'name': 'Bergonie'},  {'id':[3646, 3647], 'name': 'St Nicolas'}, {'id':[4020, 4021], 'name': 'Victoire'}, {'id':[2905, 2908], 'name': 'Musee Aquitaine'}, {'id':[1844, 1847], 'name': 'Hotel De Ville'}, {'id':[1573, 1574], 'name': 'Gambetta'}, {'id':[1716, 1717], 'name': 'Grand Theatre'}, {'id':[3402, 3403], 'name': 'Quinconces'}, {'id':[3403], 'name': 'Quinconces'}, {'id':[668, 669], 'name': "Capc Musee D'Art"}, {'id':[833, 834], 'name': 'Chartrons'}, {'id':[1110, 1111], 'name': 'Cours Du Medoc'}, {'id':[2372, 2374], 'name': 'Les Hangars'}, {'id':[294, 299], 'name': 'La Cite Du Vin'}, {'id':[3555, 3557], 'name': 'Achard'}, {'id':[2928, 2927], 'name': 'New York'}, {'id':[527, 531], 'name': 'Brandenburg'}, {'id':[938,939], 'name': 'Claveau'}, {'id':[364], 'name': 'Berge De Garonne'}]
  
  def get_station_index(self, _id):
    i = 0
    for s in self.stations:
      if _id in s['id']:
        return i
      i += 1
    return None
  
  def get_led_station(self, _index):
    count = len(self.stations)
    lcount = self.strip.len
    offset = lcount/float(count)
    j = _index*offset
    return int(j)
  
  def draw_station(self, _index, _color):
    try:
      j = self.get_led_station(_index)
      self.strip.get_pixel(j).set_color(*_color)
    except:
      print "error ", _index, ' ', _color
  
  def draw_stations(self):
    count = len(self.stations)
    for i in range(0, count):
      self.draw_station(i, station_color)
  
  def run_once(self):
    self.strip.clear(False)
    self.draw_stations()
    self.draw_station(self.get_station_index(2905), [0,0,1])
    handler = urllib.urlopen(self.uri)
    data = handler.read()
    #print self.uri
    #print data
    root = xml.etree.ElementTree.fromstring(data)
    buses = root.findall("gml:featureMember/bm:SV_VEHIC_P", self.namespaces)
    print '===!!!!!'
    for bus in buses:
      print '==='
      busid = bus.get('{http://www.opengis.net/gml}id')
      terminus = bus.find("bm:TERMINUS",self.namespaces).text
      current_stop = int(bus.find("bm:RS_SV_ARRET_P_ACTU",self.namespaces).text)
      next_stop = int(bus.find("bm:RS_SV_ARRET_P_SUIV",self.namespaces).text)
      retard = int(bus.find("bm:RETARD",self.namespaces).text)
      etat = bus.find("bm:ETAT",self.namespaces).text
      print busid, current_stop
      try:
        i = self.get_led_station(self.get_station_index(int(current_stop)))
        j = self.get_led_station(self.get_station_index(int(next_stop)))

        start = min(i,j)
        stop = max(i,j)

        if current_stop == next_stop:
          color = station_color
          color[1]=1
          color[3]=1
          self.draw_station(i, color)
        else:
          for x in range(start,stop-1):
            color = [1,0,0,0.01]
            if terminus == "France.Alouette":
              color[3]=1
            self.strip.get_pixel(start).set_color(*color)
            
      except Exception as e:
        print 'error %s'%e
      for s in self.stations:
        if current_stop in s['id']:
          print s['name']
    self.strip.has_changed()
    time.sleep(3)
          