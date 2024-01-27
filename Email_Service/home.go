package main

import (
	"fmt"

	_ "github.com/lib/pq"
)

func main() {

	// var constants, err = getConstants(("../config.json"))
	// if err != nil {
	// 	fmt.Println("error loading constants from main() : ", err)
	// }

	fmt.Println("Calling SendDailyEmail...\n\n")

	err := SendDailyEmail()
	if err != nil {
		fmt.Println("Failed to send emails -> ", err)
	}
	fmt.Println("Service ran successfully.")
}
