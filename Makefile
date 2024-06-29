.PHONY: all setup build run clean logs

all: setup build run

setup:
	# Create directories for input, output, logs, and config if they don't exist
	mkdir -p /mnt/input /mnt/output /mnt/logs /mnt/config

	# Ensure input directory is read-only and output directory is read-write
	chmod -R 555 /mnt/input
	chmod -R 755 /mnt/output

	# Install dependencies
	sudo apt-get update
	sudo apt-get install -y docker.io make

build:
	# Build the Docker image
	docker build -t video-processor .

run:
	# Run the Docker container
	docker run -d --name video_processor \
		-v /mnt/input:/app/input:ro \
		-v /mnt/output:/app/output:rw \
		-v /mnt/logs:/app/logs:rw \
		-v /mnt/config:/app/config:rw \
		video-processor

logs:
	# Tail the logs
	docker logs -f video_processor

clean:
	# Stop and remove the Docker container
	docker stop video_processor || true
	docker rm video_processor || true

	# Remove the Docker image
	docker rmi video-processor || true

	# Clean up directories
	rm -rf /mnt/input/* /mnt/output/* /mnt/logs/* /mnt/config/*

# Command to check system status
status:
	# Display Docker status
	systemctl status docker

	# Display Proxmox VM status
	qm list
