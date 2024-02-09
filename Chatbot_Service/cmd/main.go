package main

import (
	"fmt"
	"net/http"
	"time"
	"encoding/json"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"bytes"
	"io/ioutil"
)

type Message struct {
	Text string `json:"message"`
}

type QueryRequest struct {
	Query string `json:"query"`
}

type QueryResponse struct {
	Summary string `json:"summary"`
}

const pythonServiceURL = "http://localhost:5000/query"

func main() {
	r := gin.Default()

	// Use CORS middleware to allow all origins
	r.Use(cors.Default())

	r.POST("/api/echo", echoTest)

	r.POST("/query", handleQuery)

	// Start the server
	fmt.Println("Server listening on :8080")
	r.Run(":8080")
}


func handleQuery(c *gin.Context) {
	var request QueryRequest
	if err := c.BindJSON(&request); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request body"})
		return
	}

	// Prepare the request to Python service
	reqData, err := json.Marshal(request)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to prepare request"})
		return
	}

	resp, err := http.Post(pythonServiceURL, "application/json", bytes.NewBuffer(reqData))
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to send request to Python service"})
		return
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to read response from Python service"})
		return
	}

	var response QueryResponse
	if err := json.Unmarshal(body, &response); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to parse response from Python service"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"summary": response.Summary})
}



func echoTest(c *gin.Context) {
	var requestMessage Message
	if err := c.BindJSON(&requestMessage); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Failed to parse JSON request"})
		return
	}
	fmt.Println("Message received: ", requestMessage.Text)

	time.Sleep(2 * time.Second)

	// Echo the received message in the response
	c.JSON(http.StatusOK, requestMessage)
}