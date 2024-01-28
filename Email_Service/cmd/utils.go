package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type Constants struct {
	Email_id          string `json:"Email_id"`
	Email_password    string `json:"Email_password"`
	Postgres_id       string `json:"Postgres_user"`
	Postgres_password string `json:"Postgres_password"`
	Postgres_db_name  string `json:"Postgres_db_name"`
	Postgres_host     string `json:"Postgres_host"`
	Postgres_port     string `json:"Postgres_port"`
	Ssl_mode          string `json:"ssl_mode"`
}

func GetConstants(filepath string) (Constants, error) {
	file, err := os.Open(filepath)
	if err != nil {
		return Constants{}, err
	}
	defer file.Close()

	var constants Constants
	decoder := json.NewDecoder(file)
	err = decoder.Decode(&constants)
	if err != nil {
		fmt.Println("Error decoding config file -> ", err)
		return Constants{}, err
	}
	return constants, nil
}
