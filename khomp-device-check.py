#!/usr/bin/python
# -*- coding: utf-8 -*-

# title           :khomp-device-check.py
# description     :This script will check de state of khomp devices
# author              :Hebert L Silva
# date            :20170604
# version         :0.2
# usage               : ./khomp-device-check.py --serial <SERIAL> --check-type <E1|GSM|DEVICE> --link=<Numero do link>\n\n'
# python_version  :2.6
# ==============================================================================

import socket
import sys
import getopt

## Variaveis Globais
#

deviceSerial = ''
checkType = ''
quiet = False
linkNumber = '0'
deviceChannel = ''

## Parametros TCP

kQueryTcpConn = socket.socket()
hostname = 'localhost'  # socket.gethostname() # Get local machine name
port = 14130
kQueryTcpConn.connect((hostname, port))


## Definicao de funcoes
#

def kQueryConnect(command, arg1):

## Conecta via tcp, envia uma string e espera a resposta
#
# Retorna resposta da api

    kQueryTcpConn.send(command + arg1 + '\n')
    r = kQueryTcpConn.recv(1024)
    if r[:12] == 'Query failed':
        print 'ERRO - ' + r \
            + ' Durante a Requisicao | Erro ao executar o commando.'
        sys.exit(3)
    else:
        return r


def parseCliArg():

## Processa os argumentos da linha de comando
# Retorna lista com
# @deviceSerial
# @checkType
# @nagios
# @linkNumber
# @deviceChannel

    my_serial = ''
    my_type = ''
    my_nagios = False
    my_link = 0
    my_channel = ''

    # # Lista de argumetos
    #

    (opts, args) = getopt.getopt(sys.argv[1:], '-nhs:t:', [
        'serial=',
        'nagios',
        'help',
        'check-type=',
        'channel=',
        'link=',
        ])

    for (opt, arg) in opts:

        # # Seleciona parametros,
        #

        if opt in ('-h', '--help'):
            print '''Usage: ./khomp-device-check.py --serial <SERIAL> --check-type <E1|GSM|DEVICE> --link=<Numero do link>

'''
            sys.exit()
        elif opt in ('--serial', '-s'):
            my_serial = arg
        elif opt in ('--check-type', '-t'):
            my_type = arg
        elif opt in ('-q', '--quiet', '-n', '--nagios'):
            my_nagios = True
        elif opt in ('-l', '--link'):
            my_link = arg
        elif opt in ('-c', '--channel'):
            my_channel = arg

    return (my_serial, my_type, my_nagios, my_link, my_channel)


def kE1StatusParser(response):

## Retorna o estado do E1 com base na reposta da api
#
#

    statusList = {
        0: 'OK',
        1: 'Perda de Sinal',
        2: 'Central reportando falha em algum ponto',
        4: 'Quadro fora de sincronia',
        8: 'Falha de alinhamento de multiquadro',
        16: 'Falha reportada pela central',
        32: 'Taxa de erros excessiva',
        64: 'Alarme desconhecido',
        128: 'Controlador E1 danificado',
        255: 'Framer nao inicializado',
        }
    return statusList.get(int(response))


def checkEbsGsm(serial, channel):

## Retorna o estado do equipamento
# @deviceState # Canais habilitados "k3l.Config.Device."+ deviceSerial +".EnabledChannelCount"
# Canais em Falha "k3l.Status.Channel."+ deviceSerial +".TotalFail"
# Nivel de sinal do canal  k3l.Status.GSMChannel."+ deviceSerial +"."+ deviceChannel + ".SignalStrength.0"
# Operadora do canal  "k3l.Status.GSMChannel."+ deviceSerial +"."+ deviceChannel + ".OperName.0"
# Endereco ip do EBS  "k3l.Config.EBS."+ deviceSerial +".IP"

    return 0


def checkE1(serial, link):

# Retorna o estado do link E1 informado
# @kE1status
#  "k3l.Status.Link."+ serial +"."+ link +".0.E1"

    return kQueryConnect('QUERY ', 'k3l.Status.Link.' + serial + '.'
                         + str(link) + '.0.E1')


def checkDevice(serial):
    r = kQueryConnect('QUERY ', 'k3l.Status.Connected.' + str(serial))
    return bool(r)


## Coletando argumentos.

(deviceSerial, checkType, quiet, linkNumber, deviceChannel) = \
    parseCliArg()

## Verificando links E1

if checkType in ('E1', 'e1'):

    response = checkE1(deviceSerial, 0)
    if not nagios:
        print 'Estado do Link: ' + kE1StatusParser(response)
    elif response == 0:
        print kE1StatusParser(response) + '- Link: ' + linkNumber \
            + kE1StatusParser(response) + '| Estado do Link ' \
            + linkNumber + ': ' + kE1StatusParser(response)
        sys.exit(0)
    elif response == 32:
        print 'WARNING - ' + 'Link: ' + linkNumber \
            + kE1StatusParser(response) + '| Estado do Link ' \
            + linkNumber + ': ' + kE1StatusParser(response)
        sys.exit(1)
    elif response == 255:
        print 'UNKNOWN - ' + 'Link: ' + linkNumber \
            + kE1StatusParser(response) + '| Estado do Link ' \
            + linkNumber + ': ' + kE1StatusParser(response)
        sys.exit(3)
    else:
        print 'CRITICAL - ' + 'Link: ' + linkNumber \
            + kE1StatusParser(response) + '| Estado do Link ' \
            + linkNumber + ': ' + kE1StatusParser(response)
        sys.exit(2)
elif checkType in ('DEVICE', 'device') or checkType == '':

## Verificacao de estado para dispositivos.

    response = checkDevice(deviceSerial)
    if response:
        print 'OK - EBS Serial: ' + deviceSerial \
            + ' Estado: UP | Device: ' + deviceSerial + ' Estado: UP'
        sys.exit(0)
    else:
        print 'DOWN - EBS Serial: ' + deviceSerial \
            + ' Estado: DOWN | Device: ' + deviceSerial \
            + ' Estado: DOWN'
        sys.exit(2)
