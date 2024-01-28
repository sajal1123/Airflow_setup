package main

import (
	"fmt"

	"github.com/go-gomail/gomail"
)

func sendEmail(subscriberInfo subscriber, emailBody string) error {
	// Create a new message

	name, email := subscriberInfo.Name, subscriberInfo.Email
	fmt.Println("Sending Email to ", name, email)
	m := gomail.NewMessage()
	m.SetHeader("From", constants.Email_id)
	m.SetHeader("To", email)
	m.SetHeader("Subject", fmt.Sprintf("Hi %s, Here is some curated News for you!", name))
	m.SetBody("text/plain", emailBody)

	// Create a new dialer to connect to the Gmail SMTP server
	d := gomail.NewDialer("smtp.gmail.com", 587, constants.Email_id, constants.Email_password)

	// Send the email
	if err := d.DialAndSend(m); err != nil {
		fmt.Println("Error sending email:", err)
		return err
	} else {
		fmt.Println("Email sent successfully!")
		return nil
	}
}

func SendDailyEmail() error {
	subscriberList, err := GetSubscribers()
	if err != nil {
		// fmt.Println("failed to get subscriber list ", err)
		return err
	}
	for _, subscriber := range subscriberList {
		err := sendEmail(subscriber, "another test email lol")
		if err != nil {
			fmt.Println("Failed to send email->", err)
		}
	}
	fmt.Println("All emails sent Successfully!")
	return nil
}
