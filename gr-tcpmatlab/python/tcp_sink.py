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

        self.dataBuffer = Queue(maxsize=1e-6)
        self.tcp = TCPServer(port, self.dataBuffer)
        self.tcp.start()

        self.cnt = 0
    
    def work(self, input_items, output_items):
        if self.cnt % 100 == 0:
            print(self.cnt )
        self.cnt += 1

        #output_items[0] = numpy.zeros((1,), numpy.float32)
        output_items[0] = output_items[0][:1]
        #output_items[0][:] = 3.14 
        #print(output_items[0].dtype, output_items[0].size)
        #time.sleep(0.005)
        #return len(output_items[0])

        #print("???")
        data = self.dataBuffer.get()
        if(data):
            try:
                out = output_items[0]
                #print(len(data),data)
                data = float(data)
                out[:] = data
                #print(output_items)
                return 1
            except Exception as e:
                print(e)
                return 0
        return 0

class TCPServer(threading.Thread):
    def __init__(self, port, putter, split='%'):
        threading.Thread.__init__(self)
        self.putter = putter
        self.split = split


        self.ADDR = ('', port)  #local host
        self.tcpserver = socket(AF_INET, SOCK_STREAM)
        self.tcpserver.bind(self.ADDR)
        self.tcpserver.listen(3)

        self.accept = False
        self.sess = None

    def run(self):
        while True:
            if not self.accept:
                print('waiting for connect')
                self.sess, addr = self.tcpserver.accept()
                print('connected with', addr)
                self.accept = True
            data = self.sess.recv(2048).decode()
            #print(len(data), data)
            if not data:
                self.accept = False
                self.sess = None
                continue
            data = data.split(self.split)
            for d in data:
                self.putter.put(d)
                #print(self.putter.qsize())