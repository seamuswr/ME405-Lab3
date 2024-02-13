import utime
import encoder_reader
import MotorDriver
import closed_loop
import pyb

enc = encoder_reader.Encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7, pyb.Timer(8, prescaler=0, period=65535))
moe = MotorDriver.MotorDriver(pyb.Pin.board.PC1, pyb.Pin.board.PA0, pyb.Pin.board.PA1, pyb.Timer(5, freq=20000))
close = closed_loop.closed_loop(0, .4)
output = close.run(1024, enc.read())

while(output > 0):
    output = close.run(1024, enc.read())
    moe.set_duty_cycle(output)
    utime.sleep_ms(10)

close.print_values()
            
