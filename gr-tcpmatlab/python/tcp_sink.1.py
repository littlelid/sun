#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
import time
from gnuradio import gr
from socket import *
from queue import Queue
import threading
class tcp_sink(gr.sync_block):
    """
    docstring for block tcp_sink
    """
    def __init__(self, port ):
        gr.sync_block.__init__(self,
            name="tcp_sink",
            in_sig=None, 
            out_sig=[numpy.float32])
        print("init ", port) 
        self.host = ''
        self.port = port
        self.ADDR = (self.host, self.port)
        #self.tctime = socket(AF_INET, SOCK_STREAM)
        self.tctime = socket(AF_INET, SOCK_DGRAM)
        self.tctime.bind(self.ADDR)
        #self.tctime.listen(3)
        
        self.accept = False
        self.tctimeClient = None

        self.cnt = 0
        self.dataBuffer = Queue(maxsize=1e-6)
    
    def work(self, input_items, output_items):
        output_items[0] = numpy.zeros((1,))
        self.cnt += 1
        #if self.cnt % 1 == 0:
        #    print(self.cnt )
        #print("In work")
        #print(output_items[0].shape, output_items[0].dtype )
         
        #out = output_items[0]
        # <+signal processing here+>
        #out[:] = 3.14 
        #return len(out)

        #if not self.accept:
            #print('waiting for connect')
            #self.tctimeClient,addr = self.tctime.accept()
            #print('connect with', addr)
            #self.accept = True
        data, addr = self.tctime.recvfrom(2048)
        data = data.decode()
        #data = self.tctimeClient.recv(2048).decode()
        if not data:
            self.accept = False
            return 0
        print(data, len(data))
        out = output_items[0]
        # <+signal processing here+>
        out[:] = 3.14 
        return 1

class TCPServer(threading.Thread):
    def __init__(self, port, putter):
        self.putter = putter

        self.host = ''
        self.port = port
        self.ADDR = (self.host, self.port)
        self.tcpserver = socket(AF_INET, SOCK_STREAM)
        self.tcpserver.bind(self.ADDR)
        self.tcpserver.listen(3)

        self.accept = False
        self.sess = None
    
    def run(self):
        while True:
            

