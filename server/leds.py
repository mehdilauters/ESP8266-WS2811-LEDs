#!/usr/bin/env python
from zeroconf import ServiceBrowser, Zeroconf

import copy
from threading import Lock,Thread
import time
import sys
import gi
import socket
import array
from random import randint
from xbmcjson import XBMC, PLAYER_VIDEO
import json
import urllib
import datetime
gi.require_version('Gst', '1.0')
from gi.repository import Gst
Gst.init(None)

import ephem
import webserver
from animations.rainbow import *
from animations.color import *
from animations.volumeBar import *
from animations.chenillard import *
from animations.sceptrum import *
from animations.tbm import *

default_baseurl='http://localhost:8080'
default_database='./kodi-rfid.db'
playlist_id = 0

UDP_PORT = 2711

nbLed = 50


class Pixel:
  def __init__(self):
    self.r = 0
    self.g = 0
    self.b = 0
    self.i = 0
    self.set_color(0,0,0,0)
  
  def set_color(self, _r, _g, _b, _i = None):
    if _r > 1:
      raise Exception('r > 1')
    if _g > 1:
      raise Exception('g > 1')
    if _b > 1:
      raise Exception('b > 1')
    self.r = _r
    self.g = _g
    self.b = _b
    if _i is not None:
      self.set_intensity(_i)
  
  def get_raw_color(self):
    return [
      int(self.r * self.i * 255),
      int(self.g * self.i * 255),
      int(self.b * self.i * 255)
      ]
  
  def set_intensity(self, _i):
    if _i > 1:
      raise Exception('i > 1')
    self.i = _i
    
  def get_buffer(self):
    return self.get_raw_color()

class MasterStrip():
  def __init__(self, _ip, _port, _len):
    self.sock = socket.socket(socket.AF_INET, # Internet
             socket.SOCK_DGRAM) # UDP
    self.len = _len
    self.ip = _ip
    self.port = _port
    self.pixels = []
    self.strips = []
    for i in range(0, _len):
      self.pixels.append(Pixel())
    self.write()
  
  def has_changed(self):
    for strip in self.strips:
      if strip.changed:
        return True
  
  def write(self):
    if self.has_changed():
      buf = [0,0,0,0,len(self.pixels)]
      for p in self.pixels:
        buf = buf + p.get_buffer()
      self.sock.sendto(str(bytearray(buf)), (self.ip, self.port))
      
      for strip in strips:
        strip.changed = False

class Strip():
  def __init__(self, _ms, _start, _len, reversed=False):
    self.len = _len
    self.animation = None
    self.masterStrip = _ms
    self.start = _start
    self.changed = True
    self.reversed = reversed
    self.masterStrip.strips.append(self)
  
  def write(self):
    return self.masterStrip.write()
  
  def has_changed(self):
    self.changed = True
  
  def clear(self, _apply = True):
    for i in range(0,self.len):
      self.get_pixel(i).set_intensity(0)
    if _apply:
      self.has_changed()
      self.write()
    
  def set_animation(self, _animation):
    if _animation is not None:
      _animation.set_strip(self)
    else:
      self.clear()
    self.animation = _animation

  def get_pixel(self, _i):
    p = self.start + _i
    if self.reversed:
      p = self.start + self.len - _i -1
    return self.masterStrip.pixels[p]

def is_night():
  o=ephem.Observer()
  o.lat='44'
  o.long='0'
  s=ephem.Sun()
  s.compute()
  sunrise = ephem.localtime(o.next_rising(s))
  sunset = ephem.localtime(o.next_setting(s))
  print sunset
  now = datetime.datetime.now()
  if now > sunset and now < sunrise:
    return True
  else:
    return False

class Kodi(Thread):
  def __init__(self, _url):
    Thread.__init__(self)
    self.kodi = XBMC("%s/jsonrpc"%_url)
    self.playing = False
  
  def get_active_player(self):
    players = self.kodi.Player.GetActivePlayers()
    return players['result']
  
  def is_playing(self):
    return self.playing
  
  def run(self):
    while True:
      try:
        #print self.get_active_player()[0]['type']
        playerid = self.get_active_player()[0]['playerid']
        r = self.kodi.Player.GetProperties(playerid=playerid, properties=['speed'])
        self.playing = r['result']['speed'] != 0
      except:
        self.playing = False
      time.sleep(1)



class App(Thread):
  def __init__(self, _strips):
    self.animations = ['none', 'color', 'rainbow', 'volumeBar', 'sceptrum', 'tbm']
    
    Thread.__init__(self)
    self.masterStrips = _strips
    self.ws = webserver.WebuiHTTPServer(('',7878), self, webserver.WebuiHTTPHandler)
    self.ws.start()
    self.max_intensity = 1
    self.pause = False

    self.k = Kodi(default_baseurl)
    self.k.start()
  
  def get_strips(self):
    strips = []
    for masterStrip in self.masterStrips:
      strips += masterStrip.strips
    return strips
  
  def run(self):
    while True:
      try:
        if self.pause:
          time.sleep(1)
        else:
          for masterStrip in self.masterStrips:
            for strip in masterStrip.strips:
              if strip.animation is not None:
                strip.animation.set_max_intensity(self.max_intensity)
                strip.animation.run_once()
              masterStrip.write()
          time.sleep(1/50.)

      except KeyboardInterrupt:
        print "ctrl+c"
        self.ws.stop()
      #except:
        #print "error"

      
  def set_animation(self, _id, _animation):
    strips = self.get_strips()
    for id, strip in enumerate(strips):
      if id == _id or _id == -1:
        if strip.animation is not None:
          strip.animation.stop()
        strip.set_animation(copy.copy(_animation))
      
  def get_max_intensity(self):
    return self.max_intensity
  
  def set_max_intensity(self, _max):
    self.max_intensity = _max
    
  def set_color(self, _r, _g, _b):
    for masterStrip in self.masterStrips:
      for strip in masterStrip.strips:
        if strip.animation.__class__.__name__ != 'Color':
          self.set_animation(Color())
        if strip.animation is not None:
          strip.animation.set_color(_r, _g, _b)
      
      

print "main"
strips = []


class MyListener(object):

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print("Service %s added, service info: %s:%s" % (name, info.name, info.port))
        count = int(info.properties['led_count'])
        ms = MasterStrip(info.server, info.port, count)
        if count > 50:
          strip = Strip(ms, 0, int(count/2))
          strip = Strip(ms, int(count/2), int(count/2), True)
          strip.set_animation( Color() )
        else:
          strip = Strip(ms, 0, count)
        strips.append(ms)
        
zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_fastled._udp.local.", listener)

#ms = MasterStrip('192.168.1.84', UDP_PORT, nbLed)
#strip = Strip(ms, 0, nbLed)
#strip = Strip(ms, 0, 62)
#strip = Strip(ms, 62, 38, True)
#strips.append(ms)

#strips.append(Strip('192.168.1.34', UDP_PORT, nbLed))
time.sleep(2)

app = App(strips)
app.start()
#time.sleep(2)
#app.set_animation(None)
app.join()
