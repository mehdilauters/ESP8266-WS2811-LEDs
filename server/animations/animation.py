class Animation:
  def __init__(self):
    self.strip = None
    self.intensity = 1.
    self.nedd_update = False
    
  def set_max_intensity(self, _intensity):
    self.intensity = _intensity
    self.need_update = True
  
  def set_strip(self, _strip):
    self.strip = _strip
    self.need_update = True
  
  def run_once(self):
    pass
  
  def stop(self):
    pass