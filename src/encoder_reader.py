import pyb
import time


class Encoder:
    """
    Class to interface with an encoder.
    """
    
    def __init__(self, enc1_pin, enc2_pin, timer):
        """
        Initializes the Encoder instance.

        :param enc1_pin: Pin for encoder channel 1.
        :type enc1_pin: pyb.Pin
        :param enc2_pin: Pin for encoder channel 2.
        :type enc2_pin: pyb.Pin
        :param timer: Timer object for the encoder.
        :type timer: pyb.Timer
        """
        self.tim = timer
        self.enc1 = self.tim.channel(1, mode=pyb.Timer.ENC_AB, pin=enc1_pin)
        self.enc2 = self.tim.channel(2, mode=pyb.Timer.ENC_AB, pin=enc2_pin)
        self.position = 0
        self.last = self.position   

    def read(self):
        """
        Reads the encoder position and prints it.

        :return: None
        """
        temp = self.tim.counter() - self.last
        if temp > 32767:
            temp -= 65535
        elif temp < -32767:
            temp += 65535
        self.last = self.tim.counter()     
        self.position += temp
        #print(self.position)
        return self.position//16
        #time.sleep(.2)
    
    def zero(self):
        """
        Resets the encoder position to zero.

        :return: None
        """
        self.position = 0
        
        
if __name__ == '__main__':
    
    enc = Encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7, pyb.Timer(8, prescaler=0, period=65535))

    while(True):
        
        enc.read()        
        

    