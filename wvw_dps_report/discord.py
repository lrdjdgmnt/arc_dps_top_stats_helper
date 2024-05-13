import requests
import subprocess
import configparser
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def send_to_discord(webhook_url, message):
    """
    Send a message to a Discord channel via webhook.
    """
    data = {
        "content": message,
        "username": "F.R.E.D."
    }
    response = requests.post(webhook_url, json=data)
    response.raise_for_status()  # This will raise an exception for HTTP errors.
    print("Message sent to Discord")

def generate_url(base_url):
    """
    Generate a URL that includes the current date in YYYYMMDD format.
    """
    current_date = datetime.now().strftime("%Y%m%d")
    return f"{base_url}/#{current_date}-WvW-Log-Review"

def confirm_upload(webhook_url, config):
    """
    Create a pop-up to confirm whether the logs have been uploaded.
    """
    answer = messagebox.askyesno("Confirm Upload", "Are we uploading the logs for this WvW Session?")
    if answer:
        subprocess.run(["python", "upload.py"], shell=False)
        message = f"Check out the latest WvW Log Review here: {generate_url(config['URLs']['WikiURL'])}"
        send_to_discord(webhook_url, message)
        messagebox.showinfo("Done", "The message has been posted to Discord.")
    else:
        messagebox.showinfo("No Upload", "No Log upload tonight! I hope you had fun!")

    root.destroy()

def main():
    # Load configuration settings
    config = configparser.ConfigParser()
    config.read('settings.ini')

    # Get webhook URL from config
    webhook_url = config['Discord']['WebhookURL']
    confirm_upload(webhook_url, config)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    main()
