import pyvisa
import time
rm = pyvisa.ResourceManager('@py')
rm.list_resources()
#open the resource
scope = rm.open_resource('TCPIP0::192.168.1.67::1234::SOCKET', timeout = 10000)

scope.write_termination = '\n'
scope.read_termination = '\n'
scope.write('++read_tmo_ms 3000')
#scope.timeout = 10000
#scope.write('*WAI')

output = ''
scope.write('++read')
print("waiting to clear buffer")
NOTDONE = True
while NOTDONE:
    oneByte = scope.read_bytes(1)
    output = output + str(oneByte)
    print(oneByte)
    if oneByte == b'I':
       print("end of buffer found")
       NOTDONE = False
#print(output)
print(scope.read())
print("finished")


#imageBytes = scope.read_bytes(1000)
#imageBytes[:-1]
#f = openfile("image1.tiff","w")
#f.write(imageBytes)
