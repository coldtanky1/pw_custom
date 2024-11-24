BASE_DIR := $(shell pwd)
SERVER := $(BASE_DIR)/admin_panel/backend/main.go
OS := $(shell uname)


run:
	go run $(SERVER) &
	python main.py


setup:
	go mod download
	pip install discord.py
	pip install python-dotenv


	# Check the OS and create .env for Linux
ifeq ($(OS), Linux)
	echo "DISCORD_TOKEN=''" > .env
endif

	# Check the OS and create .env for macOS (Darwin)
ifeq ($(OS), Darwin)
	echo "DISCORD_TOKEN=''" > .env
endif

	# Check the OS and create .env for Windows (Cygwin, MINGW, MSYS)
ifeq ($(OS), CYGWIN)
	echo "DISCORD_TOKEN=''" > .env
endif
ifeq ($(OS), MINGW)
	echo "DISCORD_TOKEN=''" > .env
endif
ifeq ($(OS), MSYS)
	echo "DISCORD_TOKEN=''" > .env
endif
