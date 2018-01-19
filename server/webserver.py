from animations.rainbow import *
from animations.color import *
from animations.volumeBar import *
from animations.sceptrum import *
from animations.tbm import *

import urlparse

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import json
from threading import Thread
import threading
import os
import re
import urllib

class WebuiHTTPHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
      pass
    
    def _parse_url(self):
        # parse URL
        path = self.path.strip('/')
        sp = path.split('?')
        if len(sp) == 2:
            path, params = sp
        else:
            path, = sp
            params = None
        args = path.split('/')

        return path,params,args
    
    def _send_json(self, obj):
      data = json.dumps(obj, ensure_ascii=False).encode('utf8')
      
      self.send_response(200)
      self.send_header('Content-Type','application/json')
      self.send_header('Cache-Control','no-cache, no-store, must-revalidate')
      self.send_header('Pragma','no-cache')
      self.send_header('Expires','0')
      self.send_header('Access-Control-Allow-Origin','*')

      #if self.is_gzip_accepted():
        #data = self.gzip_compress(data)
        #self.send_header('Content-Encoding','gzip')
      
      self.end_headers()
      
      try:
        self.wfile.write(data)
      except Exception as e:
        raise
    
    def _get_animation(self, _id, _name, _params):
      if _name == 'next':
        self.server.animation_index += 1
        self.server.animation_index = self.server.animation_index % len(self.server.app.animations)
        return self._get_animation(_id, self.server.app.animations[self.server.animation_index], _params)
      else:
        print "set_animation %s"%_name
      if _name == 'rainbow':
        self.server.app.set_animation(_id, Rainbow())
      elif _name == 'color':
        animation = Color()
        animation.set_color(_params['r']/255., _params['g']/255., _params['b']/255.,)
        self.server.app.set_animation(_id, animation)
      elif _name == 'volumeBar':
        self.server.app.set_animation(_id, VolumeBar())
      elif _name == 'sceptrum':
        self.server.app.set_animation(_id, Sceptrum())
      elif _name == 'tbm':
        self.server.app.set_animation(_id, Tbm())
      elif _name == 'none':
        self.server.app.set_animation(_id, None)
      
      return self._send_json({'result':'OK'})
    
    def _get_status(self):
      strips = self.server.app.get_strips()
      _strips = []
      for s in strips:
        pixels = []
        for i in range(0, s.len):
          pixels.append(s.get_pixel(i).get_buffer_rgb())
        _strips.append({
            'pixel_count': s.len,
            'reversed': s.reversed,
            'animation': s.animation.__class__.__name__,
            'pixels':pixels
          })
      status = {
          'strips': _strips,
          'max_intensity': self.server.app.get_max_intensity(),
          'animations': self.server.app.animations
        }
      return self._send_json(status)
    
    def _get_file(self, path):
      _path = os.path.join(self.server.www_directory,path)
      if os.path.exists(_path):
          try:
          # open asked file
              data = open(_path,'r').read()

              # send HTTP OK
              self.send_response(200)
              self.end_headers()

              # push data
              self.wfile.write(data)
          except IOError as e:
                self.send_500(str(e))
                
    def _get_intensity(self, _min, _max):
      if _max.isdigit():
        _max = int(_max)/100.
      else:
        if _max == 'plus':
          _max = self.server.app.get_max_intensity() + 0.05
          _max = min(_max, 1.)
        else:
          _max = self.server.app.get_max_intensity() - 0.05
          _max = max(_max, 0.)
      self.server.app.set_max_intensity(_max)
      #self.server.app.set_min_intensity(_min)
      return self._send_json({'result':'OK'})
    
    def do_GET(self):
        path,params,args = self._parse_url()
        dparams = {} if params is None else urlparse.parse_qs(params)
        if ('..' in args) or ('.' in args):
          self.send_400()
          return
        if len(args) == 1 and args[0] == '':
          path = 'index.html'
        if len(args) == 1 and args[0] == 'animation.json':
          id = -1
          try:
            id = int(dparams['id'][0])
          except:
            pass
          animation = dparams['name'][0]
          params = None
          if animation == 'color':
            params = {
              'r':255,
              'g':255,
              'b':255
              }
            try:
              params = {
                'r':int(dparams['r'][0]),
                'g':int(dparams['g'][0]),
                'b':int(dparams['b'][0])
              }
            except:
              pass
          return self._get_animation(id, animation, params)
        elif len(args) == 1 and args[0] == 'intensity.json':
          return self._get_intensity(dparams['min'][0], dparams['max'][0])
        elif len(args) == 1 and args[0] == 'status.json':
          return self._get_status()
        else:
          return self._get_file(path)
      
class WebuiHTTPServer(ThreadingMixIn, HTTPServer, Thread):
  allow_reuse_address = True
  
  def __init__(self, server_address, app, RequestHandlerClass, bind_and_activate=True):
    HTTPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
    threading.Thread.__init__(self)
    self.app = app
    self.www_directory = "www/"
    self.stopped = False
    self.animation_index = 0
    
  def stop(self):
    self.stopped = True
    
  def run(self):
      while not self.stopped:
          self.handle_request()
