  #!/usr/bin/python      
import socket, sys, getopt           

## Variaveis Globais
#

deviceSerial = ''
checkType = ''
quiet = False
linkNumber = '0'
deviceChannel = ''


## Parametros TCP

kQueryTcpConn = socket.socket()     
hostname = 'localhost'          #socket.gethostname() # Get local machine name
port = 14130             


## Definicao de funcoes
#


def kQueryConnect(command, arg1,):
## Conecta via tcp, envia uma string e espera a resposta
#
# Retorna resposta da api
    kQueryTcpConn.connect((hostname,port))
    kQueryTcpConn.send(command + " " arg1 + '\n')
    return kQueryTcpConn.recv(1024)


def parseCliArg():
## Processa os argumentos da linha de comando
#Retorna lista com 
#@deviceSerial
#@checkType
#@quiet
#@linkNumber 
#@deviceChannel
    my_serial = ''
    my_type = ''
    my_quiet = False
    my_link = 0
    my_channel = ''

    ## Lista de argumetos
    #

    opts, args = getopt.getopt(sys.argv[1:],
                    'qhs:t:',
                    ['serial=',
                    'quiet',
                    'help',
                    'check-type=',
                    'channel=',
                    'link='
                    ])

    for opt, arg in opts:

        ## Seleciona parametros,
        #

        if opt in ('-h','--help'):
            print 'Usage: check-khomp.py --serial <SERIAL> --check-type <E1|GSM|DEVICE> --link=<Numero do link>\n\n'
            sys.exit()
        elif opt in  ('--serial','-s'):
            my_serial = arg
        elif opt in ('--check-type','-t'):
            my_type = arg
        elif opt in ('-q', '--quiet'):
            my_quiet = True
        elif opt in ('-l','--link'):
            my_link = arg
        elif opt in ('-c', '--channel'):
            my_channel = arg


    return my_serial, my_type, my_quiet, my_link, my_channel

def kE1StatusParser(response):
## Retorna o estado do E1 com base na reposta da api
#
#
    statusList =  {0: 'OK',
              1: 'Perda de Sinal',
              2: 'Central reportando falha em algum ponto',
              4: 'Quadro fora de sincronia',
              8: 'Falha de alinhamento de multiquadro',
              16: 'Falha reportada pela central',
              32: 'Taxa de erros excessiva',
              64: 'Alarme desconhecido',
              128: 'Controlador E1 danificado',
              255: 'Framer nao inicializado'
        }
    return statusList.get( int(response))


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
    return kQueryConnect("QUERY ", "k3l.Status.Link."+ serial +"."+ str(link) +".0.E1")


def checkDevice(serial):
    return 0


## Coletando argumentos.
deviceSerial, checkType, quiet, linkNumber, deviceChannel = parseCliArg()




if checkType in ('E1','e1'):

    response = checkE1( deviceSerial, 0)
    if !quiet:
        print "Estado do Link: " + kE1StatusParser(response)
    elif response == 0:
        print kE1StatusParser(response) + '- Link: ' + linkNumber + kE1StatusParser(response) +'| Estado do Link ' + linkNumber + ': ' + kE1StatusParser(response) 
        sys.exit(0)
    elif response == 32:
        print 'WARNING - ' + 'Link: ' + linkNumber + kE1StatusParser(response) +'| Estado do Link ' + linkNumber + ': ' + kE1StatusParser(response)
        sys.exit(1)
    elif response == 255:
        print 'UNKNOWN - ' + 'Link: ' + linkNumber + kE1StatusParser(response) +'| Estado do Link ' + linkNumber + ': ' + kE1StatusParser(response)
        sys.exit(3)
    else:
        print 'CRITICAL - ' + 'Link: ' + linkNumber + kE1StatusParser(response) +'| Estado do Link ' + linkNumber + ': ' + kE1StatusParser(response)
        sys.exit(2)