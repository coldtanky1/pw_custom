BASE_DIR := $(shell pwd)
SERVER := $(BASE_DIR)/admin_panel/backend/main.go

run:
	go run $(SERVER) &
	python main.py