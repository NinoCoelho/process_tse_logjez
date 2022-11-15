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

asn1_paths = 'bu.asn1'

urnasFields = [
    "UF",
    "municipio",
    "zona",
    "secao",
    "qtdEleitoresAptos",
    "qtdComparecimento",
    "dataHoraAbertura",
    "dataHoraEncerramento",
    "idPleito",
    "qtdEleitoresLibCodigo",
    "qtdEleitoresCompBiometrico",
    "modelo"]

votosFields = [
    "UF",
    "municipio",
    "zona",
    "secao",
    "cargo",
    "quantidadeVotos",
    "partido",
    "candidato"]
    
def processaLogUrna(estado:str, logjez:str, fileName:str, logjezZip:ZipFile):

    logFileName = fileName[:-2]+"logjez"
    iofile = logjezZip.open(logFileName,"r")

    logjez_file = py7zr.SevenZipFile(iofile, mode="r")
    logjez_file.extract("logd.dat")

    modelo = "Unknown"

    contents = open("./logd.dat/logd.dat", encoding="iso-8859-1")
    for line in contents.readlines():
        if line.find("Modelo de Urna") > 0:
            modelo = line.split()[10]
            break

    contents.close()
    os.unlink("./logd.dat/logd.dat")
    return modelo
    
    
def processBU(estado:str, logjez:str, fileName:str, logjezZip:ZipFile):
    urnas = []
    votos = []

    modeloUrna = processaLogUrna(estado, logjez, fileName, logjezZip)

    conv = asn1tools.compile_files(asn1_paths, codec="ber")
    f = logjezZip.open(fileName)
    envelope_encoded = bytearray(f.read())
    envelope_decoded = conv.decode(
        "EntidadeEnvelopeGenerico", envelope_encoded)
    bu_encoded = envelope_decoded["conteudo"]
    bu_decoded = conv.decode("EntidadeBoletimUrna", bu_encoded)
    del envelope_decoded["conteudo"]

    municipio = envelope_decoded['identificacao'][1]['municipioZona']['municipio']
    zona = envelope_decoded['identificacao'][1]['municipioZona']['zona']
    secao = envelope_decoded['identificacao'][1]['secao']
    qtdEleitoresAptos = bu_decoded['resultadosVotacaoPorEleicao'][0]['qtdEleitoresAptos']
    qtdComparecimento = bu_decoded['resultadosVotacaoPorEleicao'][0]['resultadosVotacao'][0]['qtdComparecimento']
    dataHoraAbertura = bu_decoded['dadosSecaoSA'][1]['dataHoraAbertura']
    dataHoraEncerramento = bu_decoded['dadosSecaoSA'][1]['dataHoraEncerramento']
    try:
        qtdEleitoresLibCodigo = bu_decoded["qtdEleitoresLibCodigo"]
    except:
        qtdEleitoresLibCodigo = 0
        pass
    try:
        qtdEleitoresCompBiometrico = bu_decoded["qtdEleitoresCompBiometrico"]
    except:
        qtdEleitoresCompBiometrico = 0
        pass
    urnas.append([
        estado,
        municipio,
        zona,
        secao,
        qtdEleitoresAptos,
        qtdComparecimento,
        dataHoraAbertura,
        dataHoraEncerramento,
        bu_decoded["cabecalho"]["idEleitoral"][1],
        qtdEleitoresLibCodigo,
        qtdEleitoresCompBiometrico,
        modeloUrna
    ])

    for totaisVotosCargo in bu_decoded['resultadosVotacaoPorEleicao'][0]['resultadosVotacao'][0]['totaisVotosCargo']:
        codigoCargo = totaisVotosCargo['codigoCargo'][1]
        for votosVotaveis in totaisVotosCargo['votosVotaveis']:
            votos.append([
                estado,
                municipio,
                zona,
                secao,
                codigoCargo,
                votosVotaveis['quantidadeVotos'],
                votosVotaveis['identificacaoVotavel']['partido'] if votosVotaveis["tipoVoto"] == "nominal" else votosVotaveis["tipoVoto"],
                votosVotaveis['identificacaoVotavel']['codigo'] if votosVotaveis["tipoVoto"] == "nominal" else votosVotaveis["tipoVoto"]
            ])

    return urnas, votos

def main():
    folder = "c:\PythonEleicoesBrasil\logjez_process\logjez\*.zip"

    files = glob.glob(folder)
    for logjez in files:

        estado = logjez.split(".")[0][-2:] #deriva o estado a partir do nome do arquivo
        print("Processando estado " + estado +" logjez "+logjez)

        urnasFile = open(estado+".urnas.csv", 'w', newline='')
        votosFile = open(estado+".votos.csv", 'w', newline='')

        urnasCSV = csv.writer(urnasFile)
        votosCSV = csv.writer(votosFile)

        urnasCSV.writerow(urnasFields)
        votosCSV.writerow(votosFields)

        tempCount = 0

        with ZipFile(logjez) as logjezZip:
            for file in logjezZip.namelist():
                if (file.endswith(".bu")):
                    print("Processando arquivo "+file)
                    urnas, votos = processBU(estado, logjez, file, logjezZip)
                    urnasCSV.writerows(urnas)
                    votosCSV.writerows(votos)
                tempCount+=1
            #     if tempCount > 100: break
            # if tempCount > 100: break
        urnasFile.close()
        votosFile.close()

if __name__ == "__main__":
    main()
