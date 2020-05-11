from scipy.io import wavfile
from scipy import signal
import numpy as np
from PIL import Image

def isOppositeSign(num1, num2):
    if (num1 < 0 and num2 > 0) or (num2 < 0 and num1 > 0):
        return True
    else:
        return False

def decode(samples):

    print("Started decoding process")

    #temporary array storing each "wave" to find its peak
    wave = [0]

    #the array containing the total image
    image = []

    #temporary array to store each line as they are decoded
    line = []

    i = 0
    for sample in samples:

        #once the entire wave is stored
        if isOppositeSign(wave[0], sample) == True:

            #Get the value that is farthest from 0 (the "peak" of the wave)
            value = 0
            if sample < 0:
                value = max(wave)
            else:
                value = min(wave) * -1
            wave = [0]

            
            #remap that value to 0-255
            value = (int(value)/20000)*255
            
            #append the line to the image when it is complete
            if len(line) == 2400:
                image.append(line)
                line = []
                i += 1
                print("Decoded line {}".format(i))
            line.append(value)
            
        wave.insert(0, sample)
        
    print("Done decoding")
    return np.array(image)



targetRate = 20800

rate, data = wavfile.read('D:\Radio\Audio\SDRTouch_20200508_064104_137100kHz.wav')
print("Loaded audio file")

data = signal.resample(data, len(data)//rate*targetRate+(targetRate//2))
print("Audio resampled to {}".format(targetRate))


data = decode(data)
im = Image.fromarray(data)
print("Showing image...")
im.show()
#im.convert("RGB").save("first3.png", "PNG")