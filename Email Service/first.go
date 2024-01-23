package main

import (
	"fmt"
	"github.com/go-gomail/gomail"
)

func main() {
	// Replace with your Gmail account configuration
	sender := "daily.messenger.service@gmail.com"
	password := "fkruypoasaccxqdo" // Use the app password generated in the steps above
	receiver := "deepaliagarwal39@gmail.com"

	// Create a new message
	m := gomail.NewMessage()
	m.SetHeader("From", sender)
	m.SetHeader("To", receiver)
	m.SetHeader("Subject", "IMPORTANT INFORMATION")
	m.SetBody("text/plain", "You are the cutest CUTIE ever")

	// Create a new dialer to connect to the Gmail SMTP server
	d := gomail.NewDialer("smtp.gmail.com", 587, sender, password)

	// Send the email
	if err := d.DialAndSend(m); err != nil {
		fmt.Println("Error sending email:", err)
	} else {
		fmt.Println("Email sent successfully!")
	}
}
