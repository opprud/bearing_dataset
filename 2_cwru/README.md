# CWRU data description
## 1 Overview
![](../doc/images/fig3.jpeg)

   The test was completed by Case Western Reserve University in the United States. It is the most widely used standard data set for bearing vibration signal processing and fault diagnosis. The fault characteristics are obvious, and there are many references available. It can be used as a basis for testing the dataset. There are also many projects on GitHub that use this dataset as examples, and it is worth learning from. Follow-up will gradually summarize the use of this data set. Welcome to provide materials.
Ranch


  Provided by Case Western Reserve University. The experiment was performed using a 2-horsepower Reliance Electric motor, and acceleration data was measured at positions near and far from the motor bearings. Each experiment carefully records the actual test conditions of the motor and the bearing failure status.
Use EDM to provide faults for motor bearings. In the inner raceway, the rolling elements (ie balls) and the outer raceway introduce faults with a diameter of 0.007 inches to 0.040 inches respectively. Reinstall the faulty bearing into the test motor and record the vibration data of the motor load from 0 to 3 horsepower (motor speed 1797 to 1720 RPM).


* Data download link (https://csegroups.case.edu/bearingdatacenter/pages/welcome-case-western-reserve-university-bearing-data-center-website)
The CWRU data set is the most widely used, and the literature is more. Not one by one. Among them, Wade A. Smith of the University of New South Wales conducted a comprehensive summary and comparison in 2015. A more objective review and analysis of the use of data for diagnostic and analytical research. The official website provides data in .mat format. It is more convenient to use MATLAB directly.
* Someone on Github shared how to automatically download and use in python. https://github.com/Litchiware/cwru
* Method used in R: https://github.com/coldfir3/bearing_fault_analysis


## 2.Test conditions
For the tests, faults ranging in diameter from 0.007 to 0.028 in. (0.18−0.71 mm) were seeded on the drive- and fan-end bearings (SKF deep-groove ball bearings: 6205-2RS JEM and 6203-2RS JEM, respectively ) of the motor using electro-discharge machining (EDM). The faults were seeded on the rolling elements and on the inner and outer races, and each faulty bearing was reinstalled (separately) on the test rig, which was then run at constant speed for motor loads of 0−3 horsepower (approximate motor speeds of 1797−1720 rpm). Table 2 shows the relevant bearing details and fault frequencies. During each test, acceleration was measured in the vertical direction on the housing of the drive-end bearing (DE), and in some tests acceleration was also measured in the vertical direction on the fan-end bearing housing (FE) and on the motor supporting base plate (BA). The sample rates used were 12 kHz for some tests and 48 kHz for others, as explained further in Section 3.2. Further details regar ding the test set-up can be found at the CWRU Bearing Data Center website.

### Table 2. Bearing details and fault frequencies.
Fault frequencies (multiple of shaft speed)
 
Position on rig | Model number | BPFI | BPFO | FTF | BSF 
--- | --- | --- | --- | --- | --- 
Drive end | SKF 6205-2RS JEM | 5.415 | 3.585 | 0.3983 | 2.357
Fan end | SKF 6203-2RS JEM | 4.947 | 3.053 | 0.3816 | 1.994

## 3. Data usage
Selected a few representative papers published in excellent journals. According to different perspectives from the beginning, there are three categories of research: benchmark review, signal processing and feature enhancement, and classification and pattern recognition. But many papers actually cross each other.
### Benchmarking
* Smith WA, Randall R B. Rolling element bearing diagnostics using the Case Western Reserve University data: A benchmark study [J]. Mechanical Systems and Signal Processing, 2015,64-65: 100-131. [Paper link] (https: //www.sciencedirect.com/science/article/pii/S0888327015002034)
* Boudiaf A, Moussaoui A, Dahane A, et al. A comparative study of various methods of bearing faults diagnosis using the case Western Reserve University data [J]. Journal of Failure Analysis and Prevention, 2016, 16 (2): 271- 284. [Paper Link] (https://link.springer.com/article/10.1007/s11668-016-0080-7)
### Signal Processing and Feature Engineering

 * Su W, Wang F, Zhu H, et al. Rolling element bearing faults diagnosis based on optimal Morlet wavelet filter and autocorrelation enhancement [J]. Mechanical systems and signal processing, 2010, 24 (5): 1458-1472. [Thesis Link) (https://www.sciencedirect.com/science/article/pii/S0888327009003835)
 Rolling bearing fault diagnosis method based on optimal wavelet filtering and autocorrelation enhancement
 
 * Saidi L, Ali JB, Fnaiech F. Bi-spectrum based-EMD applied to the non-stationary vibration signals for bearing faults diagnosis [J]. ISA transactions, 2014, 53 (5): 1650-1660. [Paper link] (https://www.sciencedirect.com/science/article/pii/S0019057814001220)
 Bispectrum-based emd for bearing fault diagnosis of non-stationary vibration signals
 
 * Zhu ​​K, Song X, Xue D. A roller bearing fault diagnosis method based on hierarchical entropy and support vector machine with particle swarm optimization algorithm [J]. Measurement, 2014, 47: 669-675. [Paper link] (https: //www.sciencedirect.com/science/article/pii/S0263224113004569)
 A fault diagnosis method for rolling bearings based on hierarchical entropy and support vector machines
 
 * Li Y, Wang X, Si S, et al. Entropy based fault classification using the Case Western Reserve University data: A benchmark study [J]. IEEE Transactions on Reliability, 2019. [Paper link] (https: // ieeexplore. ieee.org/abstract/document/8662701)
 Entropy-based fault classification using case data from Western Reserve University: a benchmark study
 
 * Kedadouche M, Liu Z, Vu V H. A new approach based on OMA-empirical wavelet transforms for bearing fault diagnosis [J]. Measurement, 2016, 90: 292-308. [Paper link] (https: // www. sciencedirect.com/science/article/pii/S0263224116301361)
 2. A bearing fault diagnosis method based on empirical wavelet transform was proposed.
 
 
### Classification and recognition

* Raj AS, Murali N. Early classification of bearing faults using morphological operators and fuzzy inference [J]. IEEE Transactions on Industrial Electronics, 2012, 60 (2): 567-574. [Paper link] (https: // ieeexplore. ieee.org/abstract/document/6153367)
Early classification of bearing faults using morphological operators and fuzzy reasoning

* Afrasiabi S, Afrasiabi M, Parang B, et al. Real-Time Bearing Fault Diagnosis of Induction Motors with Accelerated Deep Learning Approach [C] // 2019 10th International Power Electronics, Drive Systems and Technologies Conference (PEDSTC). IEEE, 2019 : 155-159. [Paper link] (https://ieeexplore.ieee.org/abstract/document/8697244)
Real-time diagnosis of asynchronous motor bearing faults using accelerated deep learning

* Zhang R, Tao H, Wu L, et al. Transfer learning with neural networks for bearing fault diagnosis in changing working conditions [J]. IEEE Access, 2017, 5: 14347-14357. [Paper link] (https: // ieeexplore.ieee.org/abstract/document/7961149)
Neural network-based bearing fault transfer learning method for bearing fault diagnosis under different operating conditions

## 3.Data Features
 Man-made faults have obvious features and are relatively easy to diagnose. Widely used and highly recognized. Can be used as the basic data set for algorithm verification.


[<< back to home directory](../README.md)
