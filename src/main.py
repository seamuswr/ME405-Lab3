import utime
import encoder_reader
import MotorDriver
import closed_loop
import pyb

enc = encoder_reader.Encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7, pyb.Timer(8, prescaler=0, period=65535))
moe = MotorDriver.MotorDriver(pyb.Pin.board.PC1, pyb.Pin.board.PA0, pyb.Pin.board.PA1, pyb.Timer(5, freq=20000))

while(True):
    try:
        Kp = float(input("Kp: "))
    except (ValueError, IndexError):
        print("Invalid Kp")
    else:
        enc.zero()
        close = closed_loop.closed_loop(0, Kp)
        output = close.run(1024, enc.read())

        while(output != "End"):
            output = close.run(1024, enc.read())
            moe.set_duty_cycle(output)
            utime.sleep_ms(10)

        close.print_values()
                
