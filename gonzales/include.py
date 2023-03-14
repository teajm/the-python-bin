#DDC Channel Constant
DDC_CH_HV_RELAY = 0
DDC_CH_WATER_PUMP = 1
DDC_CH_HVPE_FAN = 2
DDC_CH_PM150_PWR = 3
DDC_CH_INTERLOCK = 4
DDC_CH_PTO = 6

DDC_CH_ON = 1
DDC_CH_OFF = 0

#PM150
PM150_RECT_ON = 1
PM150_RECT_OFF = 0

#Water fans constants
WATER_FANS_ON = 1
WATER_FANS_OFF = 0

#serial packets
PACKET_STS_PKT = 0x00
PACKET_CMD_PKT = 0x01
PACKET_RSP_PKT = 0x02
PACKET_CONSOLE_PKT = 0x03

#command function codes

PACKET_DDC_CMD = 0x00
PACKET_TRUCK_RPM_CMD = 0x01
PACKET_WATER_FANS_CMD = 0x02
PACKET_PM150_READ_EEPROM_CMD = 0x03
PACKET_PM150_CLEAR_FAULTS_CMD = 0x04
PACKET_PM150_RECT_CMD = 0x05
PACKET_PM150_DISCHARGE_CMD = 0x06

#status function codes
PACKET_CONSOLE_STS = 0x00
PACKET_CAN_COMMS_STS = 0x05