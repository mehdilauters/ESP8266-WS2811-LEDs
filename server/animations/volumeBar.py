from animation import Animation
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import array
import time
import math

volume = 0

class VolumeBar(Animation):
  def __init__(self):
    Animation.__init__(self)
    self.pipeline = Gst.parse_launch('pulsesrc device=alsa_output.usb-0d8c_C-Media_USB_Headphone_Set-00-Set.analog-stereo.monitor ! audio/x-raw,format=S16LE,channels=1,rate=16000 ! audioconvert ! audio/x-raw,format=S8,channels=1,rate=16000 ! audioresample  ! appsink name=sink caps=audio/x-raw,format=S8,channels=1,rate=16000 drop=TRUE')
    self.sink = self.pipeline.get_by_name('sink')
    self.sink.set_property('emit-signals', True)
    self.sink.connect('new-sample', self.on_new_buffer)
    self.pipeline.set_state(Gst.State.PLAYING)
    self.max_volume = 0
    self.min_volume = 100
    self.volume = 0
    self.last_volume = 0
    
  def stop(self):
    self.pipeline.set_state(Gst.State.NULL)
  
  def on_new_buffer(obj, data):
    global volume
    sample = data.emit("pull-sample")
    buf = sample.get_buffer()
    buffer = buf.extract_dup(0, buf.get_size())
    caps = sample.get_caps()
    format = caps.get_structure(0).get_value('format')
    rate = caps.get_structure(0).get_value('rate')
    b = array.array('B', buffer)
    volume = sum(b)/len(b)
    return Gst.FlowReturn.OK
  
  def run_once(self):
    #take it from global var
    self.volume = volume
    self.max_volume = max(self.volume, self.max_volume)
    if(self.max_volume == 0):
      return
    if self.last_volume == 0:
      self.last_volume = self.volume
      return
    
    self.min_volume = min(self.volume, self.min_volume)
    
    intensity = self.intensity
    if self.volume < self.min_volume:
      intensity = 0
    
    #print volume, self.min_volume
    #r = self.volume / float(self.last_volume)
    #if r < 0.9:
      #return
    #print r
    self.strip.has_changed()
    #print "min: %s, max: %s, vol: %s "%(self.min_volume, self.max_volume, self.volume)
    min_volume = (self.min_volume+15)
    volume_percent = 0
    try:
      volume_percent = (self.volume-min_volume) / float(self.max_volume-min_volume)
    except:
      pass
    max_led = volume_percent * self.strip.len
    max_led = min(max_led, self.strip.len)
    max_led = max(max_led,0)
    ts = time.time()
    amplitude = 1/2.
    center = 1/2.
    frequency = 0.8
    for i in range(0,self.strip.len):
      self.strip.get_pixel(i).set_intensity(0)
    for i in xrange(0,int(max_led)):
      r = math.sin(i*frequency)*amplitude+center
      g = math.sin(i*frequency+2)*amplitude+center
      b = math.sin(i*frequency+3)*amplitude+center
      self.strip.get_pixel(i).set_color(r,g,b)
      #intensity =  min(self.intensity,math.sin(ts)*amplitude+center)
      self.strip.get_pixel(i).set_intensity(intensity)
    self.last_volume = self.volume