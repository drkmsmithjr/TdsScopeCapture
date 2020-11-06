import sys
import pyvisa
import time
from tqdm import tqdm
import glob
#import datatime
#from progressBar import ProgressBar
#pbar = ProgressBar()

#use the utilility netfinder from prologix.biz to find the machines IP address
IPADDRESS = '192.168.1.68'

# the capture size of the data from the TDS scope for Tiff and BMP file formats
BMPSIZE = 308278
TIFFSIZE = 38878



if __name__ == "__main__":


   #print "hello world"

   if len(sys.argv) < 2:
      print("The format is assumed to be BMP.")
      print("Usage:  python3 TdsCapture [filetype]")
      print("   filetype = BMP  : Capture BMP format")
      print("   filetype = TIFF : Capture Tiff Format")
      SavedFileFormat = 'BMP'
      FileExten = '.bmp'
      SliceLen = -4
      FILESIZE = BMPSIZE
   elif len(sys.argv) == 2:
      SavedFileFormat = sys.argv[1]
      if SavedFileFormat != "BMP" and SavedFileFormat != "TIFF" :
         print("Incorrect File Format Defined.  It is either BMP or TIFF")
         exit()
      if SavedFileFormat == 'TIFF':
         FILESIZE = TIFFSIZE
         FileExten = '.tiff'
         SliceLen = -5
      elif SavedFileFormat == 'BMP':
         FILESIZE = BMPSIZE
         FileExten = '.bmp'
         SliceLen = -4
   elif len(sys.argv) >= 3:
      print("There was an incorrect number of arguments for program:  two maximum")
      exit()
   

   rm = pyvisa.ResourceManager('@py')
   rm.list_resources()
    #open the resource
   scope = rm.open_resource('TCPIP0::'+IPADDRESS+'::1234::SOCKET', timeout = 10000)
   scope.write_termination = '\n'
   scope.read_termination = '\n'
   # put the maximum prologix timeout for the GPIB-ETHER abdaptor of 3000ms
   scope.write('++read_tmo_ms 3000')
   scope.write('++eos 3')

   #capture # ID:
   print("Getting Hardcopy from the following Instrument at IPADDRESS = ",IPADDRESS)
   try:
      #scope.write('ID?')
      scope.write('ID?')
      scope.write('++read eoi')
      print(scope.read())
   except:
      print("Error with first ID?: often needed when first powering up")
      print("we will try again")
      scope.write('ID?')
      scope.write('++read eoi')
      print(scope.read())

   scope.write('HARDCopy:LAYout LANdscape')
   if SavedFileFormat =='BMP':
      scope.write('HARDCopy:FORMat BMPCOLOR')
   else:
      scope.write('HARDCopy:FORMat TIFf')

   #capture hardcopy
   scope.write('HARDCopy STARt')
   print("Please Wait")
   time.sleep(3)

   #output is type byte
   output = b''
   scope.write('++read')

   NOTDONE = True
   NumBytes = 0
   #we will save BMP the Tek scope does not give an indication of the end of the read.
   #FILESIZE = BMPSIZE
   pbar = tqdm(total=FILESIZE)
   while NOTDONE:
#    oneByte = scope.read_bytes(FILESIZE)
      oneByte = scope.read_bytes(1)
      NumBytes += 1
      output += oneByte
      #print(NumBytes)
      pbar.update(1)
      if NumBytes > FILESIZE-1:
         print("FILESIZE Size complete")
         NOTDONE = False
   pbar.close()
#    if oneByte == b'K':
#       print("Next Command found")
#       NOTDONE = False
#pbar.finish()

#print(output[:-1])
# should should get the rest of the ID command
#print(scope.read())
   print("finished with %s bytes", NumBytes)
#imageBytes = scope.read_bytes(1000)
#imageBytes[:-1]
# get list of the image files
# autoincrement to the largest integer
   SeedName = "capture"
   FileList = glob.glob(SeedName + "*" + FileExten)
   #print(FileList)
   max = 0
   for img in FileList:
      # remove .bmp
      sliceEnd = img[:SliceLen]
      # remove SeedName
      sliceFront = sliceEnd[len(SeedName):]
      #print(sliceFront)
      if sliceFront.isnumeric():
        if max < int(sliceFront):
            max = int(sliceFront)
   filename = SeedName + str(max+1) + FileExten

   print("Saving to filename:",filename)
   #f = open("image1.tiff","wb")
   f = open(filename,"wb")
   f.write(output)
