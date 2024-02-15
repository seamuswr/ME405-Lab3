import cqueue
import utime

class closed_loop():
    
    def __init__(self, setpoint, Kp):
        self.setpoint = setpoint
        self.Kp = Kp
        self.measured_output = 0
        self.time_queue = cqueue.IntQueue(200)
        self.pos_queue = cqueue.IntQueue(200)
        self.start_time = utime.ticks_ms()
        
    def run(self, setpoint, measured_output):
        self.setpoint = setpoint
        self.measured_output = measured_output
        error = self.setpoint - self.measured_output
        actuation_value = self.Kp * error
        if not self.time_queue.full():
            self.time_queue.put(utime.ticks_ms()-self.start_time)
            self.pos_queue.put(self.measured_output)
        else:
            return "End"
        return actuation_value
        
    def set_setpoint(self, setpoint):
        this.setpoint = setpoint
        
    def set_Kp(self, Kp):
        this.Kp = Kp
    
    def print_values(self):
        for idx in range(200):
            print(f'{self.time_queue.get()}, {self.pos_queue.get()}')
        print('END')
        
        
if __name__ == '__main__':
    
    enc = encoder_reader.Encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7, pyb.Timer(8, prescaler=0, period=65535))
    moe = MotorDriver.MotorDriver(pyb.Pin.board.PC1, pyb.Pin.board.PA0, pyb.Pin.board.PA1, pyb.Timer(5, freq=20000))
    close = closed_loop(0, .1)
        
        
    while(True):
        output = close.run(1000, enc.read())
        moe.set_duty_cycle(output)
            
        
