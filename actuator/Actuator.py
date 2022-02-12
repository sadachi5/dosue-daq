# Built-in python modules
import time
import serial
import argparse

class Actuator:
    """
    The Actuator object is for writing commands and reading stats of the actuator via serial communication.

    NOTE: The user must have permission to control the devfile (e.g. /dev/ttyUSB0).
          If the group of devfile is "dialout", you should add your user account to group "dialout".
    """

    def __init__(self, devfile='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AB0KPFJJ-if00-port0', sleep=0.10, verbose=0):
        self.devfile = devfile
        self.sleep   = sleep
        self.verbose = verbose

        self.maxwaitloop = 10
        self.maxwaitloop_for_read = 1000

        self.Fmax =2000
        self.Fmin =   0

        self.Xmin = 0.
        self.Xmax = 700.
        self.Ymin = 0.
        self.Ymax = 1000.

        # Open serial communication
        self.ser = None
        self.ser = serial.Serial(
            self.devfile,
            baudrate=115200,
        )
        if self.ser is None :
            print('Actuator:__init__() : ERROR! Could not open the serial communication to the actuator.')
        else :
            print('Actuator:__init__() : serial = {}'.format(self.ser))
            pass
        self.ser.write(b'\r\n\r\n')
        self.ser.flushInput()
        time.sleep(2)
        res = self.__readAll() # this is necessary to work correctly.
        self.__print('Actuator:__init__() : output of blackbox in the initialization = {}'.format(res), -1)
        # Set blackbox parameters
        self.__setActuatorParameters()
        pass

    def __del__(self) :
        if not self.ser is None :
            self.ser.close()
            del self.ser
            pass
        return True

    ##################
    # Main functions #
    ##################

    # move
    # move to (x,y) position
    def move(self, x=None, y=None, speedrate=0.1) :
        if speedrate<0. or speedrate>1. :
            print("Actuator:move() : WARNING! Speedrate should be between 0 and 1.")
            print("Actuator:move() : WARNING! Speedrate is sed to 0.1.")
            speedrate = 0.1
            pass
        if (x is not None) and (self.Xmin>x or self.Xmax<x) :
            print("Actuator:move() : ERROR! X position (={}) is not valid range ({}--{}).".format(x, self.Xmin, self.Xmax))
            print("Actuator:move() : ERROR! --> Do NOT move!")
            msg = 'Actuator:move : Failed to move due to being out of range in X position'
            return False, msg
        if (y is not None) and (self.Ymin>y or self.Ymax<y) :
            print("Actuator:move() : ERROR! Y position (={}) is not valid range ({}--{}).".format(y, self.Ymin, self.Ymax))
            print("Actuator:move() : ERROR! --> Do NOT move!")
            msg = 'Actuator:move() : Failed to move due to being out of range in Y position'
            return False, msg
        speed = int(speedrate * (self.Fmax-self.Fmin) + self.Fmin)
        # G90: Position move / G91: Diff. move
        moveAxis = []
        if x is not None and y is None:
            cmd  = '$J=G90 F{:d} X{}'.format(speed, x) 
            moveAxis = [0]
        elif y is not None and x is None:
            cmd  = '$J=G90 F{:d} Y{}'.format(speed, y) 
            moveAxis = [1, 2]
        elif x is not None and y is not None:
            cmd  = '$J=G90 F{:d} X{} Y{}'.format(speed, x, y) 
            moveAxis = [0, 1, 2]
        else:
            msg = 'Actuator:move() : Warning! There is no target X or Y position.\n'\
                  'Actuator:move() : Warning! --> Do NOT move!'
            return False, msg
        # Get current position
        tmp, tmp2 = self.getPosition()
        if len(tmp2) == 3 :
            x_now, y_now, z_now = tmp2
        else:
            msg = "Actuator:move() : ERROR! Failed to get the current position!"
            print(msg)
            return False, msg
        # Get current status
        ret, status, limitswitch = self.getStatus()
        initial_limitswitch = False
        for axis in moveAxis:
            if limitswitch[axis] :
                initial_limitswitch = True
                break
            pass
        self.__print(f'Actuator:move() : initial limitswitch = {initial_limitswitch}')
        if initial_limitswitch and (x <= x_now or y <= y_now):
            msg = f'Actuator:move() : WARMING! Initial limitswitch is ON.'\
                  f'--> Do NOT move!\n'\
                  f'Actuator:move() : current (x, y) = ({x_now}, {y_now})\n'\
                  f'Actuator:move() : target  (x, y) = ({x}, {y})\n'\
                  f'Actuator:move() : limitswitch (x, y1, y2) = '\
                  f'({limitswitch[0]}, {limitswitch[1]}, {limitswitch[2]})'
            print(msg)
            return False, msg
        # Move
        self.__print(f'Actuator:move() : Move to ({x},{y})')
        ret = self.__sendCommand(cmd)
        if not ret :
            msg = 'Actuator:move() : ERROR in __sendCommand(command = {})'.format(cmd)
            return False, msg
        self.__print(f'Actuator:move() : Send command = "{cmd}"')
        if initial_limitswitch:
            time.sleep(2)
            pass
        ret, msg = self.waitIdle(moveAxis=moveAxis)
        if not ret:
            msg = 'Actuator:move() : WARNING! in waitIdle() --> hold()'
            print(msg)
            self.hold()
            return False, msg
        msg = self.__print('Actuator:move() : Successfully finished!')
        return True, msg

    # moveDiff
    # move by (dx,dy)
    def moveDiff(self, dx=0., dy=0., speedrate=0.1, nolimit=False) :
        if speedrate < 0. or speedrate > 1. :
            print("Actuator:moveDiff() : WARNING! Speedrate should be between 0 and 1.")
            print("Actuator:moveDiff() : WARNING! Speedrate is sed to 0.1.")
            speedrate = 0.1
            pass
        tmp, tmp2 = self.getPosition()
        if len(tmp2) == 3 :
            x_now, y_now, z_now = tmp2
        else:
            msg = "Actuator:moveDiff() : ERROR! Failed to get the current position!"
            print(msg)
            return False, msg
        x_next = x_now + dx
        y_next = y_now + dy
        if not nolimit:
            if (self.Xmin > x_next) or (self.Xmax < x_next) :
                print("Actuator:moveDiff() : ERROR! Next X position (={}) is not valid range ({}--{}). (dx = {})".format(x_next, self.Xmin, self.Xmax, dx))
                print("Actuator:moveDiff() : ERROR! --> Do NOT move!")
                msg = 'Actuator:moveDiff() : Failed to move due to being out of range in X position'
                return False, msg
            if (self.Ymin > y_next) or (self.Ymax < y_next) :
                print("Actuator:moveDiff() : ERROR! Next Y position (={}) is not valid range ({}--{}). (dy = {})".format(y_next, self.Ymin, self.Ymax, dy))
                print("Actuator:moveDiff() : ERROR! --> Do NOT move!")
                msg = 'Actuator:moveDiff() : Failed to move due to being out of range in Y position'
                return False, msg
            pass
        speed = int(speedrate * (self.Fmax-self.Fmin) + self.Fmin)
        moveAxis = []
        if dx != 0.:
            moveAxis.append(0)
            pass
        if dy != 0.:
            moveAxis.append(1)
            moveAxis.append(2)
            pass
        # Get current status
        ret, status, limitswitch = self.getStatus()
        initial_limitswitch = False
        for axis in moveAxis:
            if limitswitch[axis] :
                initial_limitswitch = True
                break
            pass
        self.__print(f'Actuator:moveDiff() : initial limitswitch = {initial_limitswitch}')
        if initial_limitswitch and (dx < 0. or dy < 0.):
            msg = f'Actuator:moveDiff() : WARNING! Initial limitswitch is ON.'\
                  f'--> Do NOT move!\n'\
                  f'Actuator:moveDiff() : (dx, dy) = ({dx}, {dy})\n'\
                  f'Actuator:moveDiff() : limitswitch (x, y1, y2) = '\
                  f'({limitswitch[0]}, {limitswitch[1]}, {limitswitch[2]})'
            print(msg)
            return False, msg
        # Move
        # G90: Position move / G91: Diff. move
        cmd  = '$J=G91 F{:d} X{} Y{}'.format(speed, dx, dy)
        self.__print(f'Actuator:moveDiff() : Move by ({dx},{dy})')
        ret = self.__sendCommand(cmd)
        if not ret :
            msg = 'Actuator:moveDiff() : ERROR! in __sendCommand(command = {})'.format(cmd)
            print(msg)
            return False, msg
        self.__print(f'Actuator:moveDiff() : Send command = "{cmd}"')
        if initial_limitswitch:
            time.sleep(2)
            pass
        ret, msg = self.waitIdle(moveAxis=moveAxis)
        if not ret:
            msg = 'Actuator:moveDiff() : WARNING! in waitIdle() --> hold()'
            print(msg)
            self.hold()
            return False, msg
        msg = self.__print('Actuator:moveDiff() : Successfully finished!')
        return True, msg

    # get status: return Jog/Idle/Run..
    def getStatus(self, doSleep=True) :
        res = self.__getresponse('?', doSleep).replace('\r','').replace('\n','/').strip()
        self.__print('Actuator:getStatus() : response to \"?\" = \"{}\"'.format(res), 1)
        status = (res.split('<')[-1].split('>')[0]).split('|')[0].split(':')[0]
        limitswitch = [False, False, False] # X, Y, Z
        if "Pn" in res:
            ls_status = (res.split('<')[-1].split('>')[0]).split('|')[3].split(':')[1]
            if 'X' in ls_status:
                limitswitch[0] = True
                pass
            if 'Y' in ls_status:
                limitswitch[1] = True
                pass
            if 'Z' in ls_status:
                limitswitch[2] = True
                pass
            pass
        self.__print('Actuator:getStatus() : status = "{}"'.format(status), 1)
        self.__print(f'Actuator:moveDiff() : limitswitch (x, y1, y2) = '
                     f'({limitswitch[0]}, {limitswitch[1]}, {limitswitch[2]})', 1)
        if len(status)==0 :
            print('Actuator:getStatus() : ERROR! Could not get status!')
            print('Actuator:getStatus() : --> Stop the actuator!')
            self.hold()
            print('Actuator:getStatus() : --> Reconnect to the actuator')
            self.__reconnect()
            res    = self.__getresponse('?', doSleep).replace('\r','').replace('\n','/').strip()
            status = (res.split('<')[-1].split('>')[0]).split('|')[0].split(':')[0]
            if len(status)==0 :
                msg = 'Actuator:getStatus() : ERROR! Could not get status again!'
                print(msg)
                return False, msg, limitswitch
            return True, status, limitswitch
        return True, status, limitswitch

    # get position: return (x,y,z)
    def getPosition(self, doSleep=True) :
        res = self.__getresponse('?', doSleep).replace('\r','').replace('\n','/').strip()
        self.__print('Actuator:getPosition() : response to \"?\" = \"{}\"'.format(res))
        xyz = (res.split('<')[-1].split('>')[0]).split('|')[1].split(':')[1]
        try:
            x,y,z = [ float(pos) for pos in xyz.split(',') ]
        except Exception:
            msg = 'Actuator:getPosition() : ERROR! Could not get position! \n'\
                  'Actuator:getPosition() : response = "{}"'.format(res)
            print(msg)
            return False, msg
        self.__print('Actuator:getPosition() : postion = ({},{},{})'.format(x,y,z))
        return True, (x,y,z)

    # get position & status
    def getPositionStatus(self, doSleep=True, doPrint=True):
        ret, xyz = act.getPosition()
        ret2, status, limitswitch = act.getStatus()
        self.__print(f'Current Position (x,y,z) = ({xyz[0]},{xyz[1]},{xyz[2]})', -1 if doPrint else 0)
        self.__print(f'Current Status = {status}')
        self.__print(f'Current Limit Switch (x,y1,y2) = '
                     f'({limitswitch[0]}, {limitswitch[1]}, {limitswitch[2]})', -1 if doPrint else 0)
        return ret and ret2, xyz, status, limitswitch 

    # status==Idle
    # moveAxis: 0:X-axis, 1:Y1-axis, 2:Y2-axis
    def isIdle(self, doSleep=True, moveAxis=[]):
        ret, status, limitswitch = self.getStatus(doSleep)
        ls_stop = False
        for axis in moveAxis:
            if limitswitch[axis]:
                ls_stop = True
                break
            pass
        if not ret :
            msg = 'Actuator:isIdle() : ERROR! Could not get status!'
            print(msg)
            return None, ls_stop, msg
        if  status == 'Idle':
            msg = self.__print('Actuator:isIdle() : True', 1)
            return True, ls_stop, msg 
        else:
            msg = self.__print('Actuator:isIdle() : False', 1)
            return False, ls_stop, msg
    
    # status==Jog or Run
    # moveAxis: 0:X-axis, 1:Y1-axis, 2:Y2-axis
    def isRun(self, doSleep=True, moveAxis=[]):
        ret, status, limitswitch = self.getStatus(doSleep)
        ls_stop = False
        for axis in moveAxis:
            if limitswitch[axis]:
                ls_stop = True
                break
            pass
        if not ret :
            return None, ls_stop, 'Actuator:isRun() : ERROR! Could not get status!'
        if status in ['Jog', 'Run'] :
            return True, ls_stop, 'Actuator:isRun() :'
        else: 
            return False, ls_stop, 'Actuator:isRun() :'

    # Wait for end of moving (until Idle status)
    # max_loop_time : maximum waiting time [sec]
    # moveAxis: 0:X-axis, 1:Y1-axis, 2:Y2-axis
    def waitIdle(self, max_loop_time = 180, moveAxis=[]):
        max_loop = int(max_loop_time/self.sleep) # # of loop for  max_loop_time [sec]
        for i in range(max_loop):
            isIdle, ls_stop, msg = self.isIdle(moveAxis=moveAxis)
            if isIdle:
                msg = self.__print('Actuator:waitIdle() : Successfully finished!')
                return True, msg
            if ls_stop:
                msg = self.__print('Actuator:waitIdle() : WARNING! Actuator touches the limitswitch!')
                print(msg)
                return False, msg
            pass
        msg = 'Actuator:waitIdle() : ERROR! Exceed max number of loop ({} times)'.format(i)
        print(msg)
        return False, msg

    # Check the connection
    def check_connect(self):
        try:
            self.ser.inWaiting()
        except Exception as e:
            msg = 'Actuator:check_connect() : ERROR! Could not connect to the actuator serial! | ERROR: "{}"'.format(e)
            return False, msg
        return True, 'Actuator:check_connect() : Successfully connect to the actuator serial!'

    # Hold
    def hold(self) :
        self.__print('Actuator:hold() : Hold the actuator')
        for i in range(self.maxwaitloop) :
            self.__sendCommand('!')
            ret, status, limitswitch = self.getStatus(doSleep=True)
            if not ret          : return False, 'Actuator:hold() : Failed to get status!'
            if status == 'Hold' : return True , 'Actuator:hold() : Successfully hold the actuator!'
            print('Actuator:hold() : WARNING! Could not hold the actuator! --> Retry')
            pass
        msg = 'Actuator:hold() : ERROR! Exceed the max number of retry ({} times).'.format(i)
        print(msg)
        return False, msg

    # Release(unhold) the hold state
    def release(self) :
        self.__print('Actuator:release() : Release the actuator from hold state')
        self.__sendCommand('~') # cycle start
        self.__sendCommand('$X') # kill alarm lock
        return True, 'Actuator:release() :'

    # Homing
    def homing(self) :
        self.release()
        self.__print('Actuator:homing() : Move to (-x, -y) direction until limit switches turn ON')
        speedrate_fast = 0.2
        speedrate_slow = 0.005

        # X-axis homing
        # Fast homing
        self.__print('Actuator:homing() : Move to -x')
        res, msg = self.moveDiff(dx=-1.*self.Xmax, speedrate=speedrate_fast, nolimit=True)
        if res:
            print('Actuator:homing() : ERROR! Did NOT touch x limit switch in fast homing')
            return False, 'Actuator:homing() : Failed to touch the x limit switch in fast homing!'
        self.__print('Actuator:homing() : Touched x limit switch')
        self.release()
        # Back a small distance
        self.__print('Actuator:homing() : Move back a small distance in x')
        res, msg = self.moveDiff(dx=5., speedrate=1., nolimit=True)
        # Slow homing
        self.__print('Actuator:homing() : Move to x limit switch slowly')
        res, msg = self.moveDiff(dx=-10., speedrate=speedrate_slow, nolimit=True)
        if res:
            print('Actuator:homing() : ERROR! Did NOT touch x limit switch in slow homing')
            return False, 'Actuator:homing() : Failed to touch the x limit switch in slow homing!'
        self.release()
        res, position, xyz, limitswitch = self.getPositionStatus()
        if limitswitch[0]:
            self.__print('Actuator:homing() : Successfully finish homing in x-axis (X-axis limitswitch is ON.)')
        else:
            msg = 'Actuator:homing() : Failed to do homing in x-axis (X-axis limitswitch is OFF.)'
            print(msg)
            return False, msg

        # Y-axis homing
        # Fast homing
        self.__print('Actuator:homing() : Move to -y')
        res, msg = self.moveDiff(dy=-1.*self.Ymax, speedrate=speedrate_fast, nolimit=True)
        if res:
            print('Actuator:homing() : ERROR! Did NOT touch y limit switch in fast homing')
            return False, 'Actuator:homing() : Failed to touch the y limit switch in fast homing!'
        self.__print('Actuator:homing() : Touched y limit switch')
        self.release()
        # Back a small distance
        self.__print('Actuator:homing() : Move back a small distance in y')
        res, msg = self.moveDiff(dy=5., speedrate=1., nolimit=True)
        # Slow homing
        self.__print('Actuator:homing() : Move to y limit switch slowly')
        res, msg = self.moveDiff(dy=-10., speedrate=speedrate_slow, nolimit=True)
        if res:
            print('Actuator:homing() : ERROR! Did NOT touch y limit switch in slow homing')
            return False, 'Actuator:homing() : Failed to touch the y limit switch in slow homing!'
        self.release()
        res, position, xyz, limitswitch = self.getPositionStatus()
        if limitswitch[1] or limitswitch[2]:
            self.__print('Actuator:homing() : Successfully finish homing in y-axis (Y-axis limitswitch is ON.)')
        else:
            msg = 'Actuator:homing() : Failed to do homing in y-axis (Y-axis limitswitch is OFF.)'
            print(msg)
            return False, msg
        # Print initial position & status after homing
        res, position, xyz, limitswitch = self.getPositionStatus(doPrint=True)

        # Reconnect to the BlackBox to initialize the position to (0, 0)
        self.__reconnect()
        res, position, xyz, limitswitch = self.getPositionStatus()

        msg = 'Actuator:homing() : Successfully homing!'
        self.__print(msg)
        return True, msg

    ######################
    # Internal functions #
    ######################

    # Print message
    def __print(self, msg, threshold_verbose=0):
        if self.verbose > threshold_verbose:
            print(msg)
            pass
        return msg

    # Read all strings until the buffer is empty.
    def __readAll(self) :
        lines = ''
        for i in range(self.maxwaitloop_for_read) :
            if self.ser.in_waiting==0 : break  # if buffer is empty, reading is finished.
            else :
                try:
                    line = self.ser.readline().decode()
                except Exception as e:
                    print('Actuator:__readAll() : Failed to readline from actuator! | ERROR = "%s"' % e)
                    continue
                lines += line
                pass
            pass
        if i==self.maxwaitloop-1 : 
            print('Actuator:__readAll() : WARNING! Exceed the max number of loop. ({} times)'.format(i))
            print('Actuator:__readAll() : (size={}) "{}"'.format(len(lines),lines.replace('\n','\\n')))
        else :
            self.__print('Actuator:__readAll() : (size={}) "{}"'.format(len(lines),lines.replace('\n','\\n')), 1)
            pass
        return lines
    
    # Simple write function
    def __sendCommand(self, command, doSleep=True) :
        self.__print('Actuator:__sendCommand() : command = {}\\n'.format(command), 1)
        # wait until out buffer becomes empty
        success_waiting = False
        for i in range(self.maxwaitloop) :
            try : 
                if self.ser is None : break
                out_waiting = self.ser.out_waiting
                if out_waiting == 0 :
                    success_waiting = True
                    break
            except OSError as e:
                msg = 'Actuator:__sendCommand() : ERROR! OSError ({}) in serial.out_waiting'.format(e)
                print(msg)
                time.sleep(self.sleep)
                continue
            pass
        if not success_waiting :
            print('Actuator:__sendCommand() : ERROR! The out_waiting is not 0. (# of loop is over maxloop.) [command:{}] --> Reconnect'.format(command))
            ret, msg = self.__reconnect()
            if not ret :
                print('Actuator:__sendCommand() : ERROR! Failed to reconnect! --> Skip [command:{}]'.format(command))
                return False
            time.sleep(1)
            pass
            
        self.ser.write((command+'\n').encode())
        if doSleep: time.sleep(self.sleep)
        return True
    
    # Send command & get response
    def __getresponse(self, command, doSleep=True) :
        self.__print('Actuator:__getresponse() : command = {}'.format(command), 1)
        ret = self.__sendCommand(command, doSleep=doSleep)
        if not ret :
            print('Actuator:__getresponse() : ERROR in __sendCommand(command = {})'.format(command))
            return ''
        res = ''
        res = self.__readAll()
        self.__print('Actuator:__getresponse()  : response = {}'.format(res.replace('\n','\\n')), 1)
        return res

    def __connect(self):
        # Open serial communication
        self.ser = None
        self.ser = serial.Serial(
            self.devfile,
            baudrate=115200,
        )
        if self.ser is None :
            msg = 'Actuator:__connect() : ERROR! Could not open the serial communication to the actuator.'
            print(msg)
            return False, msg
        else :
            print('Actuator:__connect() : serial = {}'.format(self.ser))
            pass
        self.ser.write(b'\r\n\r\n')
        self.ser.flushInput()
        #time.sleep(2)
        res = self.__readAll() # this is necessary to work correctly.
        self.__print('Actuator:__connect() : output of blackbox in the initialization = {}'.format(res))
        # Set blackbox parameters
        self.__setActuatorParameters()
        msg = 'Actuator:__connect() : Finished make a connection.'
        return True, msg
 
    def __reconnect(self):
        print('Actuator:__reconnect() : *** Trying to reconnect... ***')

        for i in range(self.maxwaitloop) :
            time.sleep(1)
            # reconnect
            print('Actuator:__reconnect() : * {}th try to reconnection'.format(i))
            try :
                if self.ser : 
                   self.ser.close()
                   del self.ser
                ret, msg = self.__connect()
                if not ret:
                    msg = 'Actuator:__reconnect() : WARNING! Failed to reconnect to the actuator!'
                    print(msg)
                    if self.ser : del self.ser
                    self.ser = None
                    continue
            except Exception as e:
                msg = 'Actuator:__reconnect() : WARNING! Failed to initialize Actuator! | ERROR: %s' % e
                print(msg)
                self.ser = None
                continue
            # reinitialize cmd
            ret, msg = self.check_connect()
            if ret :
                msg = 'Actuator:__reconnect() : Successfully reconnected to the actuator!'
                print(msg)
                return True, msg
            else :
                print(msg)
                msg = 'Actuator:__reconnect() : WARNING! Failed to reconnect to the actuator!'
                print(msg)
                if self.ser : del self.ser
                self.ser = None
                continue
            pass
        msg = 'Actuator:__reconnect() : ERROR! Exceed the max number of trying to reconnect to the actuator.'
        print(msg)
        return False, msg

    def __setActuatorParameters(self) :
        self.__sendCommand('$10=0') # Show 0: Work Position (WPos) / 1: Machine Position (MPos)
        self.__sendCommand('$21=0'); # hard limit switch OFF
        self.__sendCommand('$22=0'); # homing disable
        #self.__sendCommand('$22=1'); # homing enable
        #self.__sendCommand('$23=7'); # homing direction (-x,-y,-z)
        #self.__sendCommand('$24=100'); # slow speed for homing
        #self.__sendCommand('$25=1000'); # fast speed for homing
        #self.__sendCommand('$26=250'); # msec stop time for homing
        #self.__sendCommand('$27=10'); # back distance for homing
        self.__sendCommand('$100=16.665') # step/mm X-axis (MISUMI GPA32GT3060-B-P6.35)
        self.__sendCommand('$101=26.667') # step/mm Y-axis (openbuilds 3GT Timing Pulley 20 Tooth)
        self.__sendCommand('$102=26.667') # step/mm Z-axis (not used) (blackbox original)
        self.__sendCommand('$110={}'.format(self.Fmax)) # speed [mm/min] X-axis 
        self.__sendCommand('$111={}'.format(self.Fmax)) # speed [mm/min] Y-axis
        self.__sendCommand('$112={}'.format(self.Fmax)) # speed [mm/min] Z-axis (not used)
        self.__sendCommand('$120=10') # accel. [mm/sec^2] X-axis
        self.__sendCommand('$121=10') # accel. [mm/sec^2] Y-axis
        self.__sendCommand('$122=10') # accel. [mm/sec^2] Z-axis (not used)
        self.__sendCommand('$130=1500') # max travel [mm] X-axis
        self.__sendCommand('$131=1500') # max travel [mm] Y-axis
        self.__sendCommand('$132=1500') # max travel [mm] Z-axis (not used)
        msg = 'Actuator:__setActuatorParameters : Finished to set actuator controller parameters!'
        self.__print(msg, -1)
        return True, msg
  
 
if __name__ == '__main__':
    #devfile = '/dev/ttyUSB0'
    devfile = '/dev/ttyUSB-BlackBox'
    sleep = 0.10
    verbose = 0
    speedrate = 0.5

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--devfile', dest='devfile', type=str, default=devfile, help=f'device file path (default: {devfile})')
    parser.add_argument('--sleep', dest='sleep', type=float, default=sleep, help=f'sleep time for each commands (default: {sleep})')
    parser.add_argument('-s', '--speedrate', dest='speedrate', type=float, default=speedrate, help=f'speed rate between 0. and 1. (default: {speedrate})')
    parser.add_argument('-v', '--verbose', dest='verbose', type=int, default=verbose, help=f'verbosity level (default: {verbose})')
    parser.add_argument('-x', '--xpos', dest='x', type=float, default=None, help=f'Target x position (default: None)')
    parser.add_argument('-y', '--ypos', dest='y', type=float, default=None, help=f'Target y position (default: None)')
    parser.add_argument('--xdiff', dest='dx', type=float, default=0., help=f'Distance travelled in x-axis (default: 0.)')
    parser.add_argument('--ydiff', dest='dy', type=float, default=0., help=f'Distance travelled in y-axis (default: 0.)')
    parser.add_argument('--nohoming', dest='nohoming', default=False, action='store_true', help=f'Will not do homing before movement (default: False)')
    parser.add_argument('--release', dest='release', default=False, action='store_true', help=f'Will release the actuator before movement (default: False)')
    args = parser.parse_args()

    act = Actuator(args.devfile, args.sleep, args.verbose)

    # Release
    if args.release:
        act.release()
        pass

    # Homing (NOTE: This is required to know the correct position.)
    if not args.nohoming:
        act.homing()
        pass

    # Move to (x,y)
    if args.x is not None or args.y is not None:
        act.move(args.x, args.y, speedrate=args.speedrate)
        pass

    # Move by (dx,dy)
    if args.dx != 0. or args.dy != 0.:
        act.moveDiff(args.dx, args.dy, speedrate=args.speedrate)
        pass

    # Print current status
    if args.verbose > 0:
        act.getPositionStatus(doPrint=True)
        pass

    del act
    pass
