'''
The configuration header has follwing contents
Bearing type [string]
Bearing manufacturer [string]
BPFFO - outer ring constant   = 3.6070	
BPFFI - inner ring constant= 5.3929	
BSFF - roller element constant= 2.4205	
RPM - axle rpm
isFixedRpm - 1 if RPM is constant
'''
class bearingConfig:
    bearingType = '0'
    bearingManufacturer = 'CS'
    BPFFO = 0
    BPFFI = 0
    BSFF = 0
    FTF = 0
    RPS = 0
    isFixedRpm = 0
