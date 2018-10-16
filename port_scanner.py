import optparse
import nmap
from socket import *
from threading import *
def NmapScan(tgtHost,tgtPort):
	nmScan=nmap.PortScanner()
	nmScan.scan(tgtHost,tgtPort)
	state=nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
	print("[*]"+tgtHost+" tcp/"+tgtPort+" "+state)
def main():
	parser=optparse.OptionParser('usage %prog -H'+'<target host> -p <target port>')
	parser.add_option('-H',dest='tgtHost',type='string',help='specify target host')
	parser.add_option('-p',dest='tgtPort',type='string',help='specify target port')
	(options,args)=parser.parse_args()
	tgtHost=options.tgtHost
	tgtPort=options.tgtPort
	if tgtHost is None or tgtPort is None:
		print(parser.usage)
		exit(0)
	tgtPorts=tgtPort.split(",")
	for tgtPort in tgtPorts:
		NmapScan(tgtHost,tgtPort)
if __name__ == '__main__':
	main()