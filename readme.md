ure, here's the entire content you can copy and paste directly into your README.md file:

markdown

# Ruedex AI Service

This repository contains the code and configuration for the Ruedex AI Service, a Flask application running as a systemd service on an Ubuntu server.

## Service Configuration

The service is configured with the following settings:

```ini
[Unit]
Description=Ruedex AI Service
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/education_ai
ExecStart=/bin/python3 /home/ubuntu/education_ai/main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
Setup Instructions
Follow these steps to set up and manage the Flask application service.

1. Create the Service File
Create a new service file for the Flask application:



sudo nano /etc/systemd/system/education_ai.service
Copy and paste the service configuration into the file. Save and exit (CTRL + X, then Y, then Enter).

2. Reload the systemd Daemon
Reload the systemd manager configuration to recognize the new service:



sudo systemctl daemon-reload
3. Start the Service
Start the Flask service:



sudo systemctl start education_ai.service
4. Enable the Service at Boot
Enable the service to start on boot:



sudo systemctl enable education_ai.service
5. Check Service Status
Check the status of the Flask service:



sudo systemctl status education_ai.service
6. View Logs
To view the logs for the Flask service, use journalctl:



sudo journalctl -u education_ai.service
Managing the Service
Here are some common commands to manage the Flask service:

Restart the service:



sudo systemctl restart education_ai.service
Stop the service:



sudo systemctl stop education_ai.service
Disable the service from starting on boot:



sudo systemctl disable education_ai.service
Troubleooting
If you encounter issues, check the logs using journalctl to diagnose any problems. Ensure that the Python interpreter and application paths are correct in the service file.



sudo journalctl -u education_ai.service