from PyQt5 import Qtwidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal

import sys
import time
from include import *

class ProcessingThread(QThread):
    comm_port = ""
    comm_baud = 0
    
    consolePrint = (pyqtSignal(str))
    sendPkt = pyqtSignal(bytearray)
    canCommsUpdate = pyqtSignal(bool,bool,bool,bool)
    
    def __init__(self,comm_port,comm_baud):
        super(ProcessingThread,self).__init__()
        self.comm_baud = comm_baud
        self.comm_port = comm_port
        
        self.sendPkt.connect(self.uartSend)
        
    def run(self):
        self.initSerial(self.comm_port,self.comm_baud)
        self.handleCommsSerial()
    
    def initSerial(self, comm_port, comm_baud):
        self.ser = serial.Serial()
        self.ser.baudrate = comm_baud
        self.ser.port = comm_port
        self.ser.timeout = 0.05
        self.ser.open()
        
    def handleCommsSerial(self):
        while True:
            if self.ser.in_waiting > 0:
                pkt = self.ser.read(1024)
                self.parsePkt(pkt)
                time.sleep(1)
                
    def uartSend(self,pkt):
        self.ser.write(pkt)
        
    def parsePkt(self,packet):
        nextByte = 0
        pkt = packet
        
        while True:
            if nextByte >= len(pkt):
                break
            pkt = pkt[nextByte:]
            
            if pkt[0] == PACKET_STS_PKT:
                nextByte = self.parseStatusMsg(pkt[1:]) + 1
            elif pkt[0] == PACKET_CMD_PKT:
                self.consolePrint.emit("ERROR: Received command packet from the PMC")
                break
            elif pkt[0] == PACKET_RSP_PKT: #TODO
                break
            elif pkt[0] == PACKET_CONSOLE_PKT:
                endofstring = (pkt[1:].index(0x00) + 1) if 0 in pkt[1:] else len(pkt[1:]+ 1)
                s = bytearray(pkt[1:endofstring]).decode('UTF-8')
                self.consolePrint.emit("PMC Console: %s" % s)
                nextByte = endofstring
            else:
                self.consolePrint.emit("ERROR: Received packet from the PMC with unknown type")
                nextByte = len(pkt) 
                
        def parseStatusMsg(self,pkt):
            nextByte = len(pkt)
            if nextByte <= 0:
                return nextByte
            if pkt[0] == PACKET_CONSOLE_STS:
                if len(pkt)> 2:
                    msg = bytearray(pkt[2:]).decode('UTF-8')
                    self.consolePrint.emit("PMC Console: " + msg)
                    if 0 in pkt[2:]:
                        nextByte = pkt[2:].index(0) + 2
                    else:
                        nextByte = len(pkt)
            elif pkt[0] == PACKET_CAN_COMMS_STS:
                if len(pkt) > 1:
                    pm150Status = (pkt[1] & 0x01) !=0
                    pumpStatus = (pkt[1] & 0x02) !=0
                    ddcStatus = (pkt[1] & 0x04) !=0
                    truckStatus = (pkt[1] & 0x08) !=0
                    self.canCommsUpdate.emit(pm150Status, pumpStatus, ddcStatus, truckStatus)
                    nextByte = 3
                else:
                    self.consolePrint.emit("ERROR: Packet corrupted")
                    nextByte = 1
                    
            return nextByte