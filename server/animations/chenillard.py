from animation import Animation

class Chenillard(Animation):
  def __init__(self):
    Animation.__init__(self)
    self.r = 0
    self.g = 0
    self.b = 0
    self.id = 0
    self.idstep = 1
  
  def run_once(self):
    step = 0.01

    if self.r >= 1:
      self.g += step
    if self.g >= 1:
      self.b += step
      
    self.r = min(self.r, 1)
    self.g = min(self.g, 1)
    self.b = min(self.b, 1)
    if self.b >= 1:
      self.r = 0
      self.g = 0
      self.b = 0
    for i in range(0, self.id):
      p = self.strip.get_pixel(i)
      p.set_color(self.r,self.g,self.b)
      p.set_intensity(min(0.1,self.intensity))
    self.r += step
    self.id += self.idstep
    if self.id == self.strip.len:
      self.idstep = -1
    if self.id == 0:
      self.idstep = 1
    self.strip.has_changed()