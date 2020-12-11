# paderborn.py

import os
import glob
import errno
import random
#import urllib
import urllib.request as ug
import numpy as np
from scipy.io import loadmat
import patoolib as pa

rarpath = "/usr/local/bin/unrar"

class PDB:
    def __init__(self, exp, rpm, rad_force, torque_mNm, length, skipSlice = False):
        #    def __init__(self):
        if exp not in ('K001', 'K002', 'K003', 'K004', 'K005', 'K006','KA01','KA02','KA03','KA04','KA05','KA06'
                       ,'KA07','KA08','KA09','KA15','KA16','KA22','KA30','KB23','KB24','KB27','KI01','KI03','KI04'
                       ,'KI05','KI07','KI08','KI14','KI16','KI17','KI18','KI21'):
            print("wrong experiment name: {}".format(exp))
            exit(1)
        if rpm not in ('1500', '900'):
            print("wrong rpm value: {}".format(rpm))
            exit(1)
        if rad_force not in ('1000', '400'):
            print("wrong load value: {}".format(rad_force))
            exit(1)
        if torque_mNm not in ('100', '700'):
            print("wrong torque value: {}".format(torque_mNm))
            exit(1)

        dict_rpm = {'1500': 'N15_', '900': 'N09_', '2900': 'N29_'}
        dict_torq = {'100': 'M01_', '700': 'M07_'}
        dict_load = {'400': 'F04_', '1000': 'F10_'}
        #Labels 1 = healthy bearing, 2 = outer ring damage , 3 = inner ring damage, 4 = combined damage
        dict_labels = {'K0': 1, 'KA': 2, 'KI': 3, 'KB': 4}

        #print(exp[0:2])
        self.y_label = dict_labels[exp[0:2]]
        print("Y is:")
        print(self.y_label)

        filestring = dict_rpm[rpm] + dict_torq[torque_mNm] + dict_load[rad_force]
        print('filestring')
        print(filestring)

        # create reciveing dir names from arguments
        rdir = os.path.join('.', 'data/PDB', exp)  # ,rpm,load)
        fmeta = os.path.join(os.path.dirname('.'), 'metadata.txt')
        all_lines = open(fmeta).readlines()

        lines = []
        for line in all_lines:
            l = line.split()
            # print(l)
            if (l[0] == exp): # and l[1] == rpm and l[2] == rad_force:  # and l[3] == torque_mNm:
                lines.append(l)

        print("l: ")
        print(lines)
        # prepare download
        self.length = length  # sequence length
        
        if(skipSlice == True):
            self._load_data(rdir, lines, filestring)
        else:
            self._load_and_slice_data(rdir, lines, filestring)

        # shuffle training and test arrays
        shuffle = 0
        if(shuffle):
            self._shuffle()

    def _mkdir(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                print("can't create directory '{}''".format(path))
                exit(1)

    def _download(self, fpath, link):
        print("Downloading to: '{}'".format(fpath))
        #urllib.request.urlretrieve(link, fpath)
        ug.urlretrieve(link, fpath)

    def _load_and_slice_data(self, rdir, infos, filestring):

        self.X_train = np.zeros((0, self.length))
        self.X_test = np.zeros((0, self.length))
        self.y_train = []
        self.y_test = []

        ## w
        for idx, info in enumerate(infos):

            # directory to put the raw rar file
            rawdir = os.path.join(rdir, 'raw')
            self._mkdir(rawdir)

            # path to find the file
            fpath = os.path.join(rawdir, info[0] + '.rar')

            # if file already exists, avoid duplicate downloads
            if not os.path.exists(fpath):
                print("no dir/file")
                self._download(fpath, info[3].rstrip('\n'))

            # compressed file to uncompress
            cmpfile = rawdir + '/' + info[0] + '.rar'

            print("file to exrtract is is::")
            print(cmpfile)

            # unpack file
            if not os.path.exists(rdir + '/' + info[0]):
                pa.extract_archive(cmpfile, outdir=rdir, program=rarpath)
            else:
                print("file already extracted, skipping unrar")

            # a list of all files in the extracted dir
            ddir = rdir + '/' + info[0]
            flist_all = os.listdir(ddir)

            # print("filelist:")
            # print(flist_all)

            # use the searchstring, build from the program arguments to find files of interest
            flistsorted = [i for i in flist_all if filestring in i]

            print("sorted filelist:")
            print(flistsorted)

            # now build the dataset from all files of interest
            # iterate through the filelist
            for f in flistsorted:
                # load matlab file
                mat_dict = loadmat(ddir + '/' + f)#,struct_as_record=False)

                # get the values key, tha name of thenactual dataset equal to filename
                #key = list(filter(lambda x: 'N15_M07_F04_' in x, mat_dict.keys()))
                key = list(filter(lambda x: filestring in x, mat_dict.keys()))
                # load data
                #time_series = mat_dict[key[0]][:, 0] #['Y']
                time_series = mat_dict[key[0]]['Y'][0, 0][0, 6][2][:][0]

                idx_last = -(time_series.shape[0] % self.length)
                clips = time_series[:idx_last].reshape(-1, self.length)

                n = clips.shape[0]

                split = 0
                if(split):
                    # 75% train 25%test
                    n_split = int(3 * n / 4)

                    self.X_train = np.vstack((self.X_train, clips[:n_split]))
                    self.X_test = np.vstack((self.X_test, clips[n_split:]))
                    # todo add meaning full label

                    self.y_train += [self.y_label] * n_split
                    self.y_test  += [self.y_label] * (clips.shape[0] - n_split)

                else:
                    self.X_train = np.vstack((self.X_train, clips[:n]))
                    #self.X_test = np.vstack((self.X_test, clips[n_split:]))
                    # todo add meaning full label

                    self.y_train += [self.y_label] * n#_split
                    #self.y_test  += [self.y_label] * (clips.shape[0] - n_split)
 
    def _load_data(self, rdir, infos, filestring):

        self.X = np.zeros((0,250000))
        ## w
        for idx, info in enumerate(infos):

            # directory to put the raw rar file
            rawdir = os.path.join(rdir, 'raw')
            self._mkdir(rawdir)

            # path to find the file
            fpath = os.path.join(rawdir, info[0] + '.rar')

            # if file already exists, avoid duplicate downloads
            if not os.path.exists(fpath):
                print("no dir/file")
                self._download(fpath, info[3].rstrip('\n'))

            # compressed file to uncompress
            cmpfile = rawdir + '/' + info[0] + '.rar'

            print("file to exrtract is is::")
            print(cmpfile)

            # unpack file
            if not os.path.exists(rdir + '/' + info[0]):
                pa.extract_archive(cmpfile, outdir=rdir, program=rarpath)
            else:
                print("file already extracted, skipping unrar")

            # a list of all files in the extracted dir
            ddir = rdir + '/' + info[0]
            flist_all = os.listdir(ddir)

            # print("filelist:")
            # print(flist_all)

            # use the searchstring, build from the program arguments to find files of interest
            flistsorted = [i for i in flist_all if filestring in i]

            print("sorted filelist:")
            print(flistsorted)

            # now build the dataset from all files of interest
            # iterate through the filelist
            for f in flistsorted:
                # load matlab file
                mat_dict = loadmat(ddir + '/' + f)#,struct_as_record=False)

                # get the values key, tha name of thenactual dataset equal to filename
                #key = list(filter(lambda x: 'N15_M07_F04_' in x, mat_dict.keys()))
                key = list(filter(lambda x: filestring in x, mat_dict.keys()))
                # load data
                #time_series = mat_dict[key[0]][:, 0] #['Y']
                time_series = mat_dict[key[0]]['Y'][0, 0][0, 6][2][:][0]

                self.X = np.vstack((self.X, time_series[0:250000]))
        
    def _shuffle(self):
        # shuffle training samples
        index = list(range(self.X_train.shape[0]))
        random.Random(0).shuffle(index)
        self.X_train = self.X_train[index]
        self.y_train = tuple(self.y_train[i] for i in index)

        # shuffle test samples
        index = list(range(self.X_test.shape[0]))
        random.Random(0).shuffle(index)
        self.X_test = self.X_test[index]
        self.y_test = tuple(self.y_test[i] for i in index)