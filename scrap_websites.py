import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Function to scrape xyz website and extract opening form details
def scrape_xyz_website():
    url = "https://xyz.io/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract opening form details
    opening_form = soup.find("form", {"id": "opening-form"})
    if opening_form:
        details = opening_form.text.strip()
        return details
    else:
        return None

# Function to save captured result in a text file
def save_to_text_file(details):
    with open("captured_result.txt", "w") as file:
        file.write(details)

# Function to send email with captured result as attachment
def send_email(details):
    sender_email = "shashank@gmail.com"
    receiver_email = "shashank@gmail.com"
    subject = "Captured Result from xyz Website"
    body = "Please find the captured result from the xyz website attached."
    
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    
    # Add captured result as attachment
    attachment = MIMEBase("application", "octet-stream")
    attachment.set_payload(details)
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename="captured_result.txt")
    message.attach(attachment)
    
    # Send email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, "your_password")
        server.sendmail(sender_email, receiver_email, message.as_string())

# Main function
def main():
    # Scrape XYZ website
    details = scrape_xyz_website()
    
    if details:
        # Save captured result in a text file
        save_to_text_file(details)
        
        # Send email with captured result as attachment
        send_email(details)
        print("Captured result saved in 'captured_result.txt' and email sent successfully.")
    else:
        print("Failed to scrape xyz website or no opening form found.")

if __name__ == "__main__":
    main()