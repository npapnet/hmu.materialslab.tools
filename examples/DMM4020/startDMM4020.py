from npp_materialslab_tools.dmm.TektronixDMM4020.SimpleScript import record_from_DMM4020


fname = "sample.txt"
n=10000
port= "COM1"
baudrate= 19200
record_from_DMM4020(fname=fname, n=n, fs=1,port=port , baudrate=baudrate)