import numpy as np
from scipy.fftpack import fft
from scipy.signal import hilbert
from scipy.signal import butter, lfilter
from scipy.signal import freqz

def doHilbertFFT(y):
    N=np.size(y)
    hill = abs(hilbert(y)) 
    Y = abs(np.fft.ifft(hill))##*np.hanning(N)))
    return Y
"""
def doHpFilter(high_pas_f, width, y, N, x):
    y[0] = 0
    y[N-1] = 0
    x_max = x[N-1]
    high_w1 = 1- 1/(np.exp((x-high_pas_f)/width)+1)
    high_w2 = 1- 1/(np.exp((x_max-x-high_pas_f)/width)+1)
    f = y*high_w1*high_w2
    return f
"""
'''
y0 is a frequency array
'''
def doHpFilter(high_pas_f,y0, Fs):
    N =np.size(y0)
    n0 = int(N*high_pas_f/Fs)
    y = np.zeros(N) 
    y[n0:(N-n0)] = y0[n0:(N-n0)]
    return y
"""
def doBandFilter(low_f,high_f, width, y, N, x):
    y[0] = 0
    y[N-1] = 0
    x_max = x[N-1]
    high_w1 = 1- 1/(np.exp((x-low_f)/width)+1)
    high_w2 = 1- 1/(np.exp((high_f-x)/width)+1)
    f = y*high_w1*high_w2
    return f    
"""
def doBandFilter(low_f,high_f,y0, Fs):
    N =np.size(y0)
    n1 = int(N*low_f/Fs)
    n2 = int(N*high_f/Fs)
    y = np.zeros(N) * 0.0j
    y[n1:n2] = y0[n1:n2]
    y[(N-n2-1):(N-n1-1)] = y0[(N-n2-1):(N-n1-1)]
    return y  

# function to calculate peak area, noise floor substracted. The highest peak in the window bw around center -
# frequency f is detected. Returns the frequency of the highest peak in this band and the area under the peak. 
def calcBinsArea(freq,data,f,bw,Fs):
    from scipy.interpolate import interp1d
    #substract the window around the frequency of interest
    N = np.size(data)
    fre0 = freq[int((((f-bw)/Fs)*N)):int((((f+bw)/Fs)*N)+1)]
    
    N2 = np.size(fre0)
#    data0 = data[int(np.round(((f-bw)/Fs)*N)):int(np.round(((f+bw)/Fs)*N)+1)] 
    data0 = abs(data[int((((f-bw)/Fs)*N)):int((((f+bw)/Fs)*N)+1)])
    # interpolate the datapoints to get more precise results
    f_data = interp1d(fre0,data0)
    interpol_factor = 10 # the number of datapoints in the selected window is multiplied by this number
    n2 = N2*interpol_factor
    fre = np.linspace(fre0[0],fre0[N2-1],n2)
    data11 = f_data(fre)
    medi = np.median(data11) # the median is found. The median is selected because it is less sensitive to peaks than average
    data1 = data11-medi # noisefloor is substracted
   
    index_max = np.argmax(data1) # max peak detected
#     print data1[(index_max-5):(index_max+5)]
    maxA = data1[index_max]
    # the data is "folded" around the peak too make further analysis easy.
    if index_max < (n2-1-index_max):
        maxN = index_max
    else:
        maxN = n2-index_max-1    
    data2 = np.zeros(maxN+1)
    data2[0] = maxA
    for ii in range(maxN):
        data2[ii] = (data1[ii+index_max]+data1[index_max-ii])/2
    # Simple algorith for finding least square to linear regression fitting the peak. 
    #The shape of the curve is unknown but a triangle seems to work in most cases. 
    #Because the data is folded around the peak,
    # the peak can be fittet by drawing a line from (0,maxA) to (ii,0) 
    #by changing ii the least square is found 
    # and thereby the width of the peak 
    ii = 1
    dif_s = np.zeros(maxN+1)
    dif_s[0] = maxA
    amp_window = 1
#     print data2[0:10], "\n"
    while ii < maxN:
        for jj in range(1,ii+1):
            dif_s[ii] = dif_s[ii] + np.power(data2[jj]-(maxA-maxA/ii*(jj)),2)
        dif_s[ii] = np.sqrt(dif_s[ii]/ii)
        if  dif_s[ii] >  dif_s[ii-1]:
            amp_window = ii-1
            break 
        ii =ii+1    
#     print "amp_window", amp_window
    #return fre[index_max], np.sum(data2[0:amp_window])/interpol_factor
    return np.sum(data2[0:amp_window])/interpol_factor


'''
calculate RMS power as an RMS on the frequency bins covering f+/-bw
ft is the FFT array
f is the center frequency of interest
bw is the bandwidth, from the center
N is the number of samples in the FFT array
Fs is the sample frequency
'''
def calcBinsPower(ft,f, bw, N, Fs):
    #extract freq bins for RMS
    bins = ft[int(np.round(((f-bw)/Fs)*N)):int(np.round(((f+bw)/Fs)*N)+1)]
    #calc RMS
    return  np.sqrt(np.mean(abs(bins)**2))
 

'''
Extract FFT samples from object
'''
def getFftBearing(obj):
    #describe features
    Fs = obj.sampleRate
    N = obj.nSamples

    #extract samples
    y = np.array(obj.values)
    ft = fft(y*np.hanning(N))/N ##normalizes...
    return ft
 
# calculate RMS energy in a frequency window
def doRMSfreq(low_n,high_n,y):
    return np.sqrt(np.mean(np.power(abs(y[low_n:high_n]),2)))
# calculate RMS energy on a time signal
def doRMStime(y):
    return np.sqrt(np.mean(np.power(y,2))) 
''' take a fft return a number '''
def doRMS2_1000(yfft,Fs):
    # ft = np.fft.fft(y)
    # N = np.size(yfft)
    Nff = np.size(yfft)
    n1 = int (np.round(2.0*Nff/Fs))
    n2 = int (np.round(1000.0*Nff/Fs))
    #CA = np.sqrt(2)*Fs/Nff
    return doRMSfreq(n1,n2,yfft)

def doRMS1k_5k(y,Fs):
    ft = np.fft.fft(y)
    #N = np.size(y)
    Nff = np.size(y)
    n1 = int (np.round(1000.0*Nff/Fs))
    n2 = int (np.round(5000.0*Nff/Fs))
    return doRMSfreq(n1,n2,y)

def doRMS5k_10k(y,Fs):
    #ft = np.fft.fft(y)
    #N = np.size(y)
    Nff = np.size(y)
    n1 = int (np.round(5000.0*Nff/Fs))
    n2 = int (np.round(10000.0*Nff/Fs))
    return doRMSfreq(n1,n2,y)

def doRMS10k_15k(y,Fs):
    #ft = np.fft.fft(y)
    #N = np.size(y)
    Nff = np.size(y)
    n1 = int (np.round(10000.0*Nff/Fs))
    n2 = int (np.round(15000.0*Nff/Fs))
    return doRMSfreq(n1,n2,y)


def doCrestCalc(y):
    meanValue = np.mean(y)
    ptp = np.ptp(y)
    rmsv = np.mean(abs(y))
    cpv = (abs(ptp)/(rmsv))-1.0
    #print cpv, rmsv
    return cpv, rmsv

def rmsAmplitude(values):
    returnValue = 0
    for x in values:
        returnValue += x**2
    returnValue = returnValue/len(values)
    returnValue = np.sqrt(returnValue)
    return returnValue

def crest(sig):
    meanValue = np.mean(sig)
    rms = rmsAmplitude(sig)
    ptp = np.ptp(sig)
    crestFactorValue=(abs(ptp)/(rms))
    
    return crestFactorValue

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y
