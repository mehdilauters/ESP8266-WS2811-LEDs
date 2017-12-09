from animation import Animation

import time
import math
class Color(Animation):
  def __init__(self):
    Animation.__init__(self)
    r = 1.
    g = 1.
    b = 1.
    self.set_color(r, g, b)
  
  def set_color(self, _r, _g, _b):
    self.r = _r
    self.g = _g
    self.b = _b
    self.need_update = True
    
  def set_strip(self, _strip):
    Animation.set_strip(self, _strip)
    
  def run_once(self):
    if self.need_update:
      self.need_update = False
      for i in xrange(0,int(self.strip.len)):
        self.strip.get_pixel(i).set_color(self.r, self.g, self.b)
        self.strip.get_pixel(i).set_intensity(self.intensity)
      self.strip.has_changed()
    