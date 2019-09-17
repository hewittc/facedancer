# USBMicroLAN.py
#
# Contains class definitions to implement a USB to 1-Wire bridge.

from facedancer.USB import *
from facedancer.USBDevice import *
from facedancer.USBConfiguration import *
from facedancer.USBInterface import *
from facedancer.USBEndpoint import *
from facedancer.USBVendor import *

EP_CONTROL               = 0x0
EP_STATUS                = 0x1
EP_DATA_OUT              = 0x2
EP_DATA_IN               = 0x3

class USBMicroLANVendor(USBVendor):
    name = "USB MicroLAN vendor"

    CTRL_CMD             = 0x00
    COMM_CMD             = 0x01
    MODE_CMD             = 0x02

    CTL_RESET_DEVICE     = 0x0000
    CTL_START_EXE        = 0x0001
    CTL_RESUME_EXE       = 0x0002
    CTL_HALT_EXE_IDLE    = 0x0003
    CTL_HALT_EXE_DONE    = 0x0004
    CTL_FLUSH_COMM_CMDS  = 0x0007
    CTL_FLUSH_RCV_BUFFER = 0x0008
    CTL_FLUSH_XMT_BUFFER = 0x0009
    CTL_GET_COMM_CMDS    = 0x000A

    COMM_ERROR_ESCAPE    = 0x0601
    COMM_SET_DURATION    = 0x0012
    COMM_BIT_IO          = 0x0020
    COMM_PULSE           = 0x0030
    COMM_1_WIRE_RESET    = 0x0042
    COMM_BYTE_IO         = 0x0052
    COMM_MATCH_ACCESS    = 0x0064
    COMM_BLOCK_IO        = 0x0074
    COMM_READ_STRAIGHT   = 0x0080
    COMM_DO_RELEASE      = 0x6092
    COMM_SET_PATH        = 0x00A2
    COMM_WRITE_SRAM      = 0x00B2
    COMM_WRITE_EPROM     = 0x00C4
    COMM_READ_CRC_PROT   = 0x00D4
    COMM_READ_REDIRECT   = 0x21E4
    COMM_SEARCH_ACCESS   = 0x00F4

    MOD_PULSE_EN         = 0x0000
    MOD_SPEED_CHANGE_EN  = 0x0001
    MOD_1WIRE_SPEED      = 0x0002
    MOD_STRONG_PU_DUR    = 0x0003
    MOD_PD_SLEWRATE      = 0x0004
    MOD_PROG_PULSE_DUR   = 0x0005
    MOD_WRITE1_LOWTIME   = 0x0006
    MOD_DSOW0_TREC       = 0x0007

    PULSE_PROG           = 0x01
    PULSE_SPUE           = 0x02

    COMM_TYPE            = 0x0008
    COMM_SE              = 0x0008
    COMM_D               = 0x0008
    COMM_Z               = 0x0008
    COMM_CH              = 0x0008
    COMM_SM              = 0x0008
    COMM_R               = 0x0008
    COMM_IM              = 0x0001
   
    COMM_PS              = 0x4000
    COMM_PST             = 0x4000
    COMM_CIB             = 0x4000
    COMM_RTS             = 0x4000
    COMM_DT              = 0x2000
    COMM_SPU             = 0x1000
    COMM_F               = 0x0800
    COMM_NTF             = 0x0400
    COMM_ICP             = 0x0200
    COMM_RST             = 0x0100

    def setup_request_handlers(self):
        self.request_handlers = {
            self.CTRL_CMD : self.handle_control_request,
            self.COMM_CMD : self.handle_comm_request,
            self.MODE_CMD : self.handle_mode_request
        }

    def handle_control_request(self, req):
        if self.verbose > 0:
            print(self.name, "received control request", req)

        def print_control(name, control, req):
            if self.verbose > 0:
                print(name, "handling control request", control, "=", hex(req.index))

        if req.value == self.CTL_RESET_DEVICE:
            if self.verbose > 0:
                print_control(self.name, "CTL_RESET_DEVICE", req)

            self.device.status['spue'] = False
            self.device.status['spce'] = False
            self.device.status['speed'] = 0x00
            self.device.status['spud'] = 0x20
            self.device.status['pdsrc'] = 0x05
            self.device.status['lowt'] = 0x04
            self.device.status['rect'] = 0x04

            self.device.ready = True

        self.device.maxusb_app.send_on_endpoint(EP_CONTROL, b'')

    def handle_comm_request(self, req):
        if self.verbose > 0:
            print(self.name, "received command request", req)

        # COMM_SEARCH_ACCESS | COMM_IM | COMM_RST | COMM_SM | COMM_F | COMM_RTS

        def compare(value, command):
            return True if ((value & command) == command) else False

        def print_command(name, command):
            if self.verbose > 0:
                print(name, "handling command", command)

        if compare(req.value, self.COMM_SEARCH_ACCESS):
            print_command(self.name, "SEARCH_ACCESS")
            self.device.search = True
        elif compare(req.value, self.COMM_READ_REDIRECT):
            print_command(self.name, "READ_REDIRECT")
        elif compare(req.value, self.COMM_READ_CRC_PROT):
            print_command(self.name, "READ_CRC_PROT")
        elif compare(req.value, self.COMM_WRITE_EPROM):
            print_command(self.name, "WRITE_EPROM")
        elif compare(req.value, self.COMM_WRITE_SRAM):
            print_command(self.name, "WRITE_SRAM")
        elif compare(req.value, self.COMM_SET_PATH):
            print_command(self.name, "SET_PATH")
        elif compare(req.value, self.COMM_DO_RELEASE):
            print_command(self.name, "DO_RELEASE")
        elif compare(req.value, self.COMM_READ_STRAIGHT):
            print_command(self.name, "READ_STRAIGHT")
        elif compare(req.value, self.COMM_BLOCK_IO):
            print_command(self.name, "BLOCK_IO")
        elif compare(req.value, self.COMM_MATCH_ACCESS):
            print_command(self.name, "MATCH_ACCESS")
        elif compare(req.value, self.COMM_BYTE_IO):
            print_command(self.name, "BYTE_IO")
        elif compare(req.value, self.COMM_1_WIRE_RESET):
            print_command(self.name, "1_WIRE_RESET")
        elif compare(req.value, self.COMM_PULSE):
            print_command(self.name, "PULSE")
        elif compare(req.value, self.COMM_SET_DURATION):
            print_command(self.name, "SET_DURATION")
        elif compare(req.value, self.COMM_ERROR_ESCAPE):
            print_command(self.name, "ERROR_ESCAPE")

        self.device.maxusb_app.send_on_endpoint(EP_CONTROL, b'')

    def handle_mode_request(self, req):

        def print_mode(self, mode, req):
            print(self.name, "received mode request", mode, "=", hex(req.index))

        if req.value == self.MOD_PULSE_EN:
            print_mode(self, "MOD_PULSE_EN", req)
            self.device.status['spue'] = True if req.index == 0x02 else False
        elif req.value == self.MOD_SPEED_CHANGE_EN:
            print_mode(self, "MOD_SPEED_CHANGE_EN", req)
            self.device.status['spce'] = True if req.index == 0x01 else False
        elif req.value == self.MOD_1WIRE_SPEED:
            print_mode(self, "MOD_1WIRE_SPEED", req)
        elif req.value == self.MOD_STRONG_PU_DURATION:
            print_mode(self, "MOD_STRONG_PU_DURATION", req)
        elif req.value == self.MOD_PULLDOWN_SLEWRATE:
            print_mode(self, "MOD_PULLDOWN_SLEWRATE", req)
        elif req.value == self.MOD_PROG_PULSE_DURATION:
            print_mode(self, "MOD_PROG_PULSE_DURATION", req)
        elif req.value == self.MOD_WRITE1_LOWTIME:
            print_mode(self, "MOD_WRITE1_LOWTIME", req)
        elif req.value == self.MOD_DSOW0_TREC:
            print_mode(self, "MOD_DSOW0_TREC", req)

        self.device.maxusb_app.send_on_endpoint(EP_CONTROL, b'')


class USBMicroLANInterface(USBInterface):
    name = "USB MicroLAN interface"

    def __init__(self, verbose=0, alternate=0):
        descriptors = { }

        endpoints = [
            [
                # alternate 0 (10 ms polling, 16 byte bulk max packet size)
                USBEndpoint(
                    EP_STATUS,           # endpoint number
                    USBEndpoint.direction_in,
                    USBEndpoint.transfer_type_interrupt,
                    USBEndpoint.sync_type_none,
                    USBEndpoint.usage_type_data,
                    32,                  # max packet size
                    10,                  # polling interval
                    self.handle_status   # handler function
                ),
                USBEndpoint(
                    EP_DATA_OUT,         # endpoint number
                    USBEndpoint.direction_out,
                    USBEndpoint.transfer_type_bulk,
                    USBEndpoint.sync_type_none,
                    USBEndpoint.usage_type_data,
                    16,                  # max packet size
                    0,                   # polling interval
                    self.handle_data_out # handler function
                ),
                USBEndpoint(
                    EP_DATA_IN,          # endpoint number
                    USBEndpoint.direction_in,
                    USBEndpoint.transfer_type_bulk,
                    USBEndpoint.sync_type_none,
                    USBEndpoint.usage_type_data,
                    16,                  # max packet size
                    0,                   # polling interval
                    self.handle_data_in  # handler function
                )
            ], [
                # alternate 1 (10 ms polling, 64 byte bulk max packet size)
                USBEndpoint(
                    EP_STATUS,           # endpoint number
                    USBEndpoint.direction_in,
                    USBEndpoint.transfer_type_interrupt,
                    USBEndpoint.sync_type_none,
                    USBEndpoint.usage_type_data,
                    32,                  # max packet size
                    10,                  # polling interval
                    self.handle_status   # handler function
                ),
                USBEndpoint(
                    EP_DATA_OUT,         # endpoint number
                    USBEndpoint.direction_out,
                    USBEndpoint.transfer_type_bulk,
                    USBEndpoint.sync_type_none,
                    USBEndpoint.usage_type_data,
                    64,                  # max packet size
                    0,                   # polling interval
                    self.handle_data_out # handler function
                ),
                USBEndpoint(
                    EP_DATA_IN,          # endpoint number
                    USBEndpoint.direction_in,
                    USBEndpoint.transfer_type_bulk,
                    USBEndpoint.sync_type_none,
                    USBEndpoint.usage_type_data,
                    64,                  # max packet size
                    0,                   # polling interval
                    self.handle_data_in  # handler function
                )
            ], [
                # alternate 2 (1 ms polling, 16 byte bulk max packet size)
                USBEndpoint(
                    EP_STATUS,           # endpoint number
                    USBEndpoint.direction_in,
                    USBEndpoint.transfer_type_interrupt,
                    USBEndpoint.sync_type_none,
                    USBEndpoint.usage_type_data,
                    32,                  # max packet size
                    1,                   # polling interval
                    self.handle_status   # handler function
                ),
                USBEndpoint(
                    EP_DATA_OUT,         # endpoint number
                    USBEndpoint.direction_out,
                    USBEndpoint.transfer_type_bulk,
                    USBEndpoint.sync_type_none,
                    USBEndpoint.usage_type_data,
                    16,                  # max packet size
                    0,                   # polling interval
                    self.handle_data_out # handler function
                ),
                USBEndpoint(
                    EP_DATA_IN,          # endpoint number
                    USBEndpoint.direction_in,
                    USBEndpoint.transfer_type_bulk,
                    USBEndpoint.sync_type_none,
                    USBEndpoint.usage_type_data,
                    16,                  # max packet size
                    0,                   # polling interval
                    self.handle_data_in  # handler function
                )
            ], [
                # alternate 3 (1 ms polling, 16 byte bulk max packet size)
                USBEndpoint(
                    EP_STATUS,           # endpoint number
                    USBEndpoint.direction_in,
                    USBEndpoint.transfer_type_interrupt,
                    USBEndpoint.sync_type_none,
                    USBEndpoint.usage_type_data,
                    32,                  # max packet size
                    1,                   # polling interval
                    self.handle_status   # handler function
                ),
                USBEndpoint(
                    EP_DATA_OUT,         # endpoint number
                    USBEndpoint.direction_out,
                    USBEndpoint.transfer_type_bulk,
                    USBEndpoint.sync_type_none,
                    USBEndpoint.usage_type_data,
                    64,                  # max packet size
                    0,                   # polling interval
                    self.handle_data_out # handler function
                ),
                USBEndpoint(
                    EP_DATA_IN,          # endpoint number
                    USBEndpoint.direction_in,
                    USBEndpoint.transfer_type_bulk,
                    USBEndpoint.sync_type_none,
                    USBEndpoint.usage_type_data,
                    64,                  # max packet size
                    0,                   # polling interval
                    self.handle_data_in  # handler function
                )
            ]
        ]

        USBInterface.__init__(
                self,
                0,          # interface number
                alternate,  # alternate setting
                0xff,       # interface class: vendor-specific
                0xff,       # subclass: vendor-specific
                0xff,       # protocol: vendor-specific
                0,          # string index
                verbose,
                endpoints[alternate],
                descriptors
        )

    def handle_set_interface_request(self, req):
        if req.index == 0 and req.value in range(0, 4):
            self.configuration.device.maxusb_app.ack_status_stage()
        else:
            self.configuration.device.maxusb_app.stall_ep0()

    def handle_status(self):
        print("EP1: STATUS")

        if self.configuration.device.ready:
            if self.configuration.device.search:
                self.configuration.device.maxusb_app.send_on_endpoint(EP_STATUS,
                    self.configuration.device.state_bytes + b'\x20\x00\x00\x00\x00\x08\x00\x00\xa5')

    def handle_data_out(self, req):
        print("EP2: DATA OUT =", req)

    def handle_data_in(self):
        print("EP3: DATA_IN")

        if self.configuration.device.search:
            self.configuration.device.maxusb_app.send_on_endpoint(EP_DATA_IN,
                b'\x00\x01\x02\x03\x04\x05\x06\x07')
            self.configuration.device.search = False


class OneWireDevice:
    """
        Base class for bus-connected 1-wire devices
    """

    lookup = bytes([
        0x00, 0x5e, 0xbc, 0xe2, 0x61, 0x3f, 0xdd, 0x83, 0xc2, 0x9c, 0x7e,
        0x20, 0xa3, 0xfd, 0x1f, 0x41, 0x9d, 0xc3, 0x21, 0x7f, 0xfc, 0xa2,
        0x40, 0x1e, 0x5f, 0x01, 0xe3, 0xbd, 0x3e, 0x60, 0x82, 0xdc, 0x23,
        0x7d, 0x9f, 0xc1, 0x42, 0x1c, 0xfe, 0xa0, 0xe1, 0xbf, 0x5d, 0x03,
        0x80, 0xde, 0x3c, 0x62, 0xbe, 0xe0, 0x02, 0x5c, 0xdf, 0x81, 0x63,
        0x3d, 0x7c, 0x22, 0xc0, 0x9e, 0x1d, 0x43, 0xa1, 0xff, 0x46, 0x18,
        0xfa, 0xa4, 0x27, 0x79, 0x9b, 0xc5, 0x84, 0xda, 0x38, 0x66, 0xe5,
        0xbb, 0x59, 0x07, 0xdb, 0x85, 0x67, 0x39, 0xba, 0xe4, 0x06, 0x58,
        0x19, 0x47, 0xa5, 0xfb, 0x78, 0x26, 0xc4, 0x9a, 0x65, 0x3b, 0xd9,
        0x87, 0x04, 0x5a, 0xb8, 0xe6, 0xa7, 0xf9, 0x1b, 0x45, 0xc6, 0x98,
        0x7a, 0x24, 0xf8, 0xa6, 0x44, 0x1a, 0x99, 0xc7, 0x25, 0x7b, 0x3a,
        0x64, 0x86, 0xd8, 0x5b, 0x05, 0xe7, 0xb9, 0x8c, 0xd2, 0x30, 0x6e,
        0xed, 0xb3, 0x51, 0x0f, 0x4e, 0x10, 0xf2, 0xac, 0x2f, 0x71, 0x93,
        0xcd, 0x11, 0x4f, 0xad, 0xf3, 0x70, 0x2e, 0xcc, 0x92, 0xd3, 0x8d,
        0x6f, 0x31, 0xb2, 0xec, 0x0e, 0x50, 0xaf, 0xf1, 0x13, 0x4d, 0xce,
        0x90, 0x72, 0x2c, 0x6d, 0x33, 0xd1, 0x8f, 0x0c, 0x52, 0xb0, 0xee,
        0x32, 0x6c, 0x8e, 0xd0, 0x53, 0x0d, 0xef, 0xb1, 0xf0, 0xae, 0x4c,
        0x12, 0x91, 0xcf, 0x2d, 0x73, 0xca, 0x94, 0x76, 0x28, 0xab, 0xf5,
        0x17, 0x49, 0x08, 0x56, 0xb4, 0xea, 0x69, 0x37, 0xd5, 0x8b, 0x57,
        0x09, 0xeb, 0xb5, 0x36, 0x68, 0x8a, 0xd4, 0x95, 0xcb, 0x29, 0x77,
        0xf4, 0xaa, 0x48, 0x16, 0xe9, 0xb7, 0x55, 0x0b, 0x88, 0xd6, 0x34,
        0x6a, 0x2b, 0x75, 0x97, 0xc9, 0x4a, 0x14, 0xf6, 0xa8, 0x74, 0x2a,
        0xc8, 0x96, 0x15, 0x4b, 0xa9, 0xf7, 0xb6, 0xe8, 0x0a, 0x54, 0xd7,
        0x89, 0x6b, 0x35
    ])

    def __init__(self, family, serial, verbose=0):
        self.family = family
        self.serial = serial

    @classmethod
    def crc(self, data):
        c = 0

        for i in range(0, len(data)):
            c = self.lookup[c ^ data[i]]

        return bytes([c])

    @property
    def rom(self):
        return OneWireDevice.crc(self.family + self.serial) + self.serial + self.family


class USBMicroLANDevice(USBDevice, OneWireDevice):
    name = "USB MicroLAN device"

    ST_SPUA   = 0x01 # strong pull-up active
    ST_PMOD   = 0x08 # DS2490 powered from USB and external sources
    ST_HALT   = 0x10 # DS2490 currently halted
    ST_IDLE   = 0x20 # DS2490 currently idle
    ST_EP0F   = 0x80 # EP0 FIFO status

    RR_DETECT = 0xA5 # new device detected
    RR_NRS    = 0x01 # no presence pulse
    RR_SH     = 0x02 # short on bus
    RR_APP    = 0x04 # alarming presence pulse
    RR_CMP    = 0x10 # compare error
    RR_CRC    = 0x20 # CRC error
    RR_RDP    = 0x40 # redirected page
    RR_EOS    = 0x80 # end of search error

    REGULAR   = 0x00 # 65 us time slot (15.4 kbps)
    FLEXIBLE  = 0x01 # 65 to 72 us time slot (13.9 kbps to 15.4 kbps)
    OVERDRIVE = 0x02 # 10 us time slot (100 kbps)

    def __init__(self, maxusb_app, bus, verbose=0):
        interfaces = [
            USBMicroLANInterface(verbose=verbose, alternate=0),
            USBMicroLANInterface(verbose=verbose, alternate=1),
            USBMicroLANInterface(verbose=verbose, alternate=2),
            USBMicroLANInterface(verbose=verbose, alternate=3)
        ]

        config = USBConfiguration(
                1,                 # configuration index
                0,                 # string desc index
                interfaces,        # interfaces
                0xe0,              # attributes (self-powered, remote-wakeup)
                50                 # 100 mA max
        )

        USBDevice.__init__(
                self,
                maxusb_app,
                0xff,              # device class
                255,               # device subclass
                255,               # protocol release number
                64,                # max packet size for endpoint 0
                0x04fa,            # vendor id: Dallas Semiconductor
                0x2490,            # product id: DS1490F 2-in-1 Fob, 1-Wire adapter
                0x0200,            # device revision
                0,                 # manufacturer string index
                0,                 # product string index
                0,                 # serial number string index
                [ config ],        # configurations
                verbose=verbose
        )

        self.device_vendor = USBMicroLANVendor(verbose)
        self.device_vendor.set_device(self)

        self.status = {
            'spue': False,
            'spce': False,
            'speed': 0x00,
            'spud': 0x20,
            'pdsrc': 0x05,
            'lowt': 0x04,
            'rect': 0x04
        }

        OneWireDevice.__init__(self, b'\x1f', b'\x50\x6f\x43\x20\x7c\x7c')

        for device in bus:
            pass

        self.ready = False
        self.search = False

    @property
    def state_bytes(self):
        state = \
            bytes([(self.status['spce'] << 2) + self.status['spue']]) + \
            bytes([self.status['speed']]) + \
            bytes([self.status['spud']]) + \
            bytes([0x00]) + \
            bytes([self.status['pdsrc']]) + \
            bytes([self.status['lowt']]) + \
            bytes([self.status['rect']]) + \
            bytes([0x00])

        return state

    def handle_get_string_descriptor_request(self, num):
        try:
            return super().handle_get_string_descriptor_request(num)
        except IndexError:
            pass

