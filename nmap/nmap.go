package main

import (
	"fmt"

	"github.com/JustinTimperio/gomap"
)

func main() {
	fmt.Println("TCP:")
	scan, err := gomap.ScanRange("tcp", true, false)
	if err != nil {
		// handle error
	}
	fmt.Printf(scan.String())

	fmt.Println("\nUDP:")
	scan, err = gomap.ScanRange("udp", true, false)
	if err != nil {
		// handle error
	}
	fmt.Printf(scan.String())

	fmt.Println("\nICMP:")
	scan, err = gomap.ScanRange("icmp", true, false)
	if err != nil {
		// handle error
	}
	fmt.Printf(scan.String())
}
