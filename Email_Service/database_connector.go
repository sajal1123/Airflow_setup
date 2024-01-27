package main

import (
	"database/sql"
	"fmt"

	_ "github.com/lib/pq"
)

type subscriber struct {
	Name string
	Email string
}

var constants, _ = GetConstants("../config.json")

func connect() (*sql.DB, error) {
 	connStr := fmt.Sprintf("user=%s password=%s dbname=%s host=%s port=%s sslmode=%s",
							constants.Postgres_id, constants.Postgres_password,
							constants.Postgres_db_name, constants.Postgres_host, 
							constants.Postgres_port, constants.Ssl_mode)
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		return nil, err
	}
	return db, nil
}

func fetchData(db *sql.DB) ([]subscriber, error) {
	rows, err := db.Query("SELECT email, name FROM subscribers")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var subscribers []subscriber

	for rows.Next() {
		var email, name string
		if err := rows.Scan(&email, &name); err != nil {
			return nil, err
		}
		currentSubscriber := subscriber{
			Name: name,
			Email: email,
		}
		subscribers = append(subscribers, currentSubscriber)
	}

	if err := rows.Err(); err != nil {
		return nil, err
	}

	return subscribers, nil
}

func GetSubscribers() ([]subscriber, error) {
	db, err := connect()
	if err != nil {
		fmt.Println("Error connecting to the database:", err)
		return nil, err
	}
	defer db.Close()

	subscribers, err := fetchData(db)
	if err != nil {
		return nil, err
	}
	return subscribers, nil
}

// GET NEWS SUMMARY FROM DBEAVER
