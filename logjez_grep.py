import argparse
import glob
import logging
import os
import pdb
import sys
from os import walk
from zipfile import ZipFile
import pandas as pd
import csv
import io
import py7zr

import asn1tools
    
def processaLogUrna(estado:str, logjez:str, fileName:str, logjezZip:ZipFile, searchFor:str):

    try:
        iofile = logjezZip.open(fileName,"r")

        logjez_file = py7zr.SevenZipFile(iofile, mode="r")
        logjez_file.extract("logd.dat")

        modelo = "Unknown"

        contents = open("./logd.dat/logd.dat", encoding="iso-8859-1")
        countLines = 0
        for line in contents.readlines():
            countLines += 1
            if line.find(searchFor) > 0:
                print(fileName+" "+countLines+": "+line)

        contents.close()
        os.unlink("./logd.dat/logd.dat")
    except:
        print(fileName+": ERRO ABRINDO ARQUIVO")

def main():
    folder = "C:\process_tse_logjez\logjez\*.zip"

    searchFor = sys.argv[1]

    if searchFor == "":
        print("Forneça o texto a ser buscado como parâmetro")
        exit(1)

    files = glob.glob(folder)
    for logjez in files:

        estado = logjez.split(".")[0][-2:] #deriva o estado a partir do nome do arquivo
        print("Processando estado " + estado +" logjez "+logjez)

        tempCount = 0

        with ZipFile(logjez) as logjezZip:
            for file in logjezZip.namelist():
                if (file.endswith(".logjez")):
                    processaLogUrna(estado, logjez, file, logjezZip, searchFor)
                # tempCount+=1
                # if tempCount > 100: break
            # if tempCount > 100: break

if __name__ == "__main__":
    main()
