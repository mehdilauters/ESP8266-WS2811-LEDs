from animation import Animation
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
from gi.repository import GObject
import array
import time
import math
import threading
import re

magnitude = None

class Sceptrum(Animation):
  def __init__(self):
    Animation.__init__(self)
    self.magnitude = None
    self.min = -70
    self.max = -40
    self.band = 16
    self.pipeline = Gst.parse_launch('pulsesrc device=alsa_output.usb-0d8c_C-Media_USB_Headphone_Set-00-Set.analog-stereo.monitor ! audio/x-raw,format=S16LE,channels=1,rate=16000 ! spectrum interval=10000 bands=%s post-messages=true message-magnitude=true threshold=%s ! fakesink'%(self.band, self.min))
   
    bus = self.pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect('message::element', self.on_message)
   
    self.pipeline.set_state(Gst.State.PLAYING)
    g_loop = threading.Thread(target=GObject.MainLoop().run)
    g_loop.daemon = True
    g_loop.start()
   
    
  def on_message(self, bus, msg):
    global magnitude
    struct = msg.get_structure()
    if struct.get_name() == 'spectrum':
        struct_str = struct.to_string()
        print struct_str
        magnitude_str = re.match(r'.*magnitude=\(float\){(.*)}.*', struct_str)
        if magnitude_str:
            magnitude = []
            m = magnitude_str.groups()[0].split(',')
            for i in m:
              magnitude.append(float(i))
  
  def stop(self):
    self.pipeline.set_state(Gst.State.NULL)
  
  
  def run_once(self):
    global magnitude
    for i in range(0,self.strip.len):
      self.strip.get_pixel(i).set_intensity(0)
    ts = time.time()
    amplitude = 1/2.
    center = 1/2.
    frequency = 0.8
    for i in range(0,self.strip.len):
      self.strip.get_pixel(i).set_intensity(0)
    for i in xrange(0,self.strip.len):
      r = math.sin(i*frequency)*amplitude+center
      g = math.sin(i*frequency+2)*amplitude+center
      b = math.sin(i*frequency+3)*amplitude+center
      self.strip.get_pixel(i).set_color(r,g,b)
    
    c = float(self.band) / float(self.strip.len)
    if magnitude is None:
      return
    try:
      for i in xrange(0,self.strip.len):
        bandid = int(i * c)
        #bandid = 0
        intensity = (magnitude[bandid] - self.min) / (self.max - self.min)
        self.strip.get_pixel(i).set_intensity(intensity)
      #print magnitude
    except:
      pass
      
    