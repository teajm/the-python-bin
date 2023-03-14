from PyQt5 import Qtwidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QInputDialog

import time

from processingThread import ProcessingThread
from include import *


class Ui(Qtwidges.QDialog):
    ddcEvent = pyqtSignal(int)
    
    def __init__(self,comm_port, comm_baud) -> None:
        super(Ui,self).__init__()
        uic.loadUi('ui/gui.ui',self)
        
        self.processingThread = ProcessingThread(comm_port, comm_baud)
        
        self.processingThread.consolePrint.connect(self.consolePrint)
        self.processingThread.canCommsUpdate.connect(self.updatecanCommsStatus)
        self.processingThread.start()
        
        #DDC buttons
        
        self.b_hv_relay_on.clicked.connect(lambda: self.handleDdcEvent(DDC_CH_HV_RELAY, DDC_CH_ON))
        self.b_hv_relay_off.clicked.connect(lambda: self.handleDdcEvent(DDC_CH_HV_RELAY, DDC_CH_OFF))
        self.b_water_pump_on.connect(lambda: self.handleDdcEvent(DDC_CH_WATER_PUMP, DDC_CH_ON))
        self.b_water_pump_off.connect(lambda: self.handleDdcEvent(DDC_CH_WATER_PUMP, DDC_CH_OFF))
        self.hvpe_fan_on.connect(lambda: self.handleDdcEvent(DDC_CH_HVPE_FAN, DDC_CH_ON))
        self.hvpe_fan_off.connect(lambda: self.handleDdcEvent(DDC_CH_HVPE_FAN, DDC_CH_OFF))
        self.pm150_pwr_on.connect(lambda: self.handleDdcEvent(DDC_CH_PM150_PWR, DDC_CH_ON))
        self.pm150_pwr_off.connect(lambda: self.handleDdcEvent(DDC_CH_PM150_PWR, DDC_CH_OFF))
        self.b_interlock_on.connect(lambda: self.handleDdcEvent(DDC_CH_INTERLOCK, DDC_CH_ON))
        self.b_interlock_off.connect(lambda: self.handleDdcEvent(DDC_CH_INTERLOCK, DDC_CH_OFF))
        self.b_pto_on.connect(lambda: self.handleDdcEvent(DDC_CH_PTO, DDC_CH_ON))
        self.b_pto_off.connect(lambda: self.handleDdcEvent(DDC_CH_PTO, DDC_CH_OFF))
        
        
        #pm150 buttons
        self.b_pm150_clr_faults.clicked.connect(self.pm150ClearFaults)
        self.b_pm150_enable_rect.clicked.conect(lambda:self.pm150RectCmd(PM150_RECT_ON))
        self.b_pm150_disable_rect.clicked.conect(lambda:self.pm150RectCmd(PM150_RECT_OFF))
        self.b_pm150_discharge.clicked.connect(self.pm150Discharge)
        
        #truck buttons
        
        self.b_truck_set_1000.clicked(lambda:self.handleTruckRpm(1000))
        self.b_truck_set_1500.clicked(lambda:self.handleTruckRpm(1500))
        self.b_truck_set_1800.clicked(lambda:self.handleTruckRpm(1800))
        self.b_truck_set_1900.clicked(lambda:self.handleTruckRpm(1900))
        self.b_truck_set_release.clicked(lambda:self.handleTruckRpm(0))
        
        #misc buttons
        self.b_water_fans_on.clicked.connect(lambda:self.handleWaterFans(WATER_FANS_ON))
        self.b_water_fans_off.clicked.connect(lambda:self.handleWaterFans(WATER_FANS_OFF))
        
        #CAN comms status
        
        self.1_pm150_status.setText("Inactive")
        self.1_pump_status.setText("Inactive")
        self.1_ddc_status.setText("Inactive")
        self.1_truck_status.setText("Inactive")
        
        
        self.consoleOut.setPlainText("")
        
        self.show()
        
        
    def handleDdcEvent(self,ch,onOroff):
        self.sendPkt([PACKET_CMD_PKT, PACKET_DDC_CMD, ch, onOroff])
        self.consolePrint("Turn DDC Channel %d %s" % (ch, "on" if onOrOff == 1 else "off"))
        
    def pm150ClearFaults(self);
        self.sendPkt([PACKET_CMD_PKT, PACKET_PM150_CLEAR_FAULTS_CMD])
        self.consolePrint("Clear PM150 Faults")
    
    def pm150RectCmd(self,onOroff):
        self.sendPkt([PACKET_CMD_PKT, PACKET_PM150_RECT_CMD, onOroff])
        self.consolePrint("PM150 Active Rectification: %s" % ("On" if onOroff == 1 else "off"))
        
    def pm150Discharge(self):
        self.sendPkt([PACKET_CMD_PKT, PACKET_PM150_DISCHARGE_CMD])
        self.consolePrint("PM150 Discharge Command")
        
    def handleTruckRPM(self,rpm):
        self.sendPkt([PACKET_CMD_PKT, PACKET_TRUCK_RPM_CMD, rpm & 0xff, (rpm >>8) & 0xff])
        self.consolePrint("Truck RPM: %d" & rpm)
        
    def handleWaterFans(self, onOrOff):
        self.sendPkt([PACKET_CMD_PKT, PACKET_WATER_FANS_CMD, onOrOff])
        self.consolePrint("Water fans: %s" % ("on" if onOrOff == 1 else "off"))

    def consolePrint(self,t):
        timeObj = time.localtime()
        curTime = time.strftime("[%H:%ML%S]". timeObj)
        self.consoleOut.append(curTime + t)
        verScrollBar = self.consoleOut.verticalScrollBar()
        
    def sendPkt(self,arr):
        cs = 0
        for i in arr:
            cs += 1
        cs &= 0xff
        
        arr += [cs]
        self.processingThread.sendPkt.emit(bytearray(arr))
        
        
    def updateCanCommsStatus(self, pm150Status, pumpStatus, ddcStatus, truckStatus):
        pm150Status_text = "Active" if pm150Status == 1 else "Inactive"
        pumpStatus_text = "Active" if pumpStatus == 1 else "Inactive"
        ddcStatus_text = "Active" if ddcStatus == 1 else "Inactive"
        truckStatus_text = "Active" if truckStatus == 1 else "Inactive"
        
        self.1_pm150_status,setText(pm150Status_text)
        self.1_pump_status.setText(pumpStatus_text)
        self.1_ddc_status.setText(ddcStatus_text)
        self.1_truck_status.setText(truckStatus_text)
        
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Window Close', 'are you sure you want to close this window?', 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            text, ok = QInputDialog.getText(self, 'Save Log', 'Save Log file to: ')
            if ok:
                t = self.consoleOut.toPlainText()
                f = open(text,'w')
                f.write(t)
                f.close()
                
            event.accept()
            print('Window Closed')
        else:
            event.ignore()