from animation import Animation

import time
import math
class Rainbow(Animation):
  def set_strip(self,strip):
    Animation.set_strip(self,strip)
    
  def run_once(self):
    amplitude = 1/2.
    center = 1/2.
    frequency = 0.8
    frequency_intensity = 1
    ts = time.time()
    for i in xrange(0,int(self.strip.len)):
      r = math.sin(i*frequency)*amplitude+center
      g = math.sin(i*frequency+2)*amplitude+center
      b = math.sin(i*frequency+3)*amplitude+center
      self.strip.get_pixel(i).set_color(r,g,b)
      intensity =  1#max(0.3,math.sin(ts*frequency_intensity)*1/2.+1/2.)
      self.strip.get_pixel(i).set_intensity(min(intensity,self.intensity))
      
    j = math.sin(ts)*self.strip.len/2.+self.strip.len/2.
    self.strip.get_pixel(int(j)).set_intensity(self.intensity/2.)
      
    self.strip.has_changed()