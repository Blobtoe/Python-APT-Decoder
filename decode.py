from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import statistics

def isOppositeSign(num1, num2):
    if (num1 < 0 and num2 > 0) or (num2 < 0 and num1 > 0):
        return True
    else:
        return False

def decode(samples):

    #temporary array storing each "wave" to find its peak
    wave = [0]

    #the array containing the total image
    image = []

    #temporary array to store each line as they are decoded
    line = []

    #buffer to find the sync lines
    buffer = []

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

            if len(line) > 39:
                buffer = line[-39:]
                for i in range(0, 4):
                    #print(i)
                    if buffer[0] <= 100 and buffer[5] <= 100:
                        buffer = buffer[10:]
                    if i >= 3:
                        line[len(line)-39] = 255
                        line[len(line)-1] = 255
            
            #append the line to the image when it is complete
            if len(line) == 2400:
                image.append(line)
                line = []
            line.append(value)
            
        wave.insert(0, sample)
        
    return np.array(image)



rate, data = wavfile.read('audio-short.wav')

targetRate = 20800

if rate != targetRate:
    print("Please resample your audio file to {}".format(targetRate))

data = decode(data)
im = Image.fromarray(data)
im.show()
#im.convert("RGB").save("first3.png", "PNG")