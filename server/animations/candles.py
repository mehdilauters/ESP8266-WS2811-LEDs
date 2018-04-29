from animation import Animation
from random import randint

class Candles(Animation): 
  def __init__(self):
    Animation.__init__(self)
  
  def set_strip(self, _strip):
    Animation.set_strip(self, _strip)
    for i in xrange(0, int(self.strip.len)):
      c = self.get_color()
      self.strip.get_pixel(i).set_color(c[0], c[1], c[2])
  
  def get_color(self):
    r = randint(60, 60)/100.
    g = randint(20, 80)/100.
    b = 0
    i = randint(1, self.intensity*100)/100.
    return [r,g,b,i]
  
  def run_once(self):
    for i in xrange(0, int(self.strip.len)/5):
      i = randint(0, int(self.strip.len))
      c = self.get_color()
      #self.strip.get_pixel(i).set_color(c[0], c[1], c[2])
      self.strip.get_pixel(i).set_intensity(c[3])
      self.strip.has_changed()