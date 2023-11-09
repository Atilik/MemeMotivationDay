import requests
import smtplib
import datetime as dt
import random
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

MEME_SIZE = int(input("How many memes do you want to send? "))

# Make a request to get meme data
meme_response = requests.get(url=f"https://meme-api.com/gimme/musicmemes/{MEME_SIZE}")
meme_response.raise_for_status()
meme = meme_response.json()
print(meme)

# Check if there are memes in the response
if 'memes' in meme and len(meme['memes']) > 0:
    # Get the last 5 memes in the list (or any other number you want)
    last_memes = meme['memes'][-MEME_SIZE:]

    # Create a folder to save the meme images
    folder_path = 'meme_images'
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    # Download and save valid meme images
    for i, meme_data in enumerate(last_memes):
        meme_image_url = meme_data['url']
        try:
            response = requests.get(meme_image_url)
            response.raise_for_status()
            file_path = os.path.join(folder_path, f'meme_image_{i+1}.png')  # Adjust the file format if needed
            with open(file_path, 'wb') as file:
                file.write(response.content)
        except requests.exceptions.HTTPError as e:
            print(f"Error downloading meme image {i+1}: {e}")
            continue

    print(f"Downloaded and saved {len(os.listdir(folder_path))} meme images in the '{folder_path}' folder.")
else:
    print("No memes found in the response.")

now = dt.datetime.now()
day_of_week = now.weekday()
with open("quotes.txt") as quotes_file:
    quotes_list = quotes_file.readlines()
    todays_quote = random.choice(quotes_list)

    my_email = "atilaylaylandin@gmail.com"  # Replace with your email
    password = "ihwmjqccmvsghspm"  # Replace with your email password or use a secure method to handle it

    # List of recipient email addresses
    recipient_emails = ["atilaykucukoglu@gmail.com"]  # Add more recipients as needed

    # Create a connection to the SMTP server
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)

        # Send separate emails for each meme to all recipients
        for recipient_email in recipient_emails:
            for i in range(MEME_SIZE):
                file_path = os.path.join(folder_path, f'meme_image_{i + 1}.png')
                # Create a new MIME multipart message for each email
                msg = MIMEMultipart()
                msg['From'] = my_email
                msg['To'] = recipient_email
                msg['Subject'] = f"Meme Motivation {i + 1}"
                msg.attach(MIMEText(todays_quote, 'plain'))
                with open(file_path, 'rb') as image_file:
                    image = MIMEImage(image_file.read(), name=os.path.basename(file_path))
                    msg.attach(image)

                # Send the email
                connection.sendmail(from_addr=my_email,
                                    to_addrs=recipient_email,
                                    msg=msg.as_string())

print("All meme emails sent.")

# my_email = "atilaylaylandin@gmail.com"
# password = "ihwmjqccmvsghspm"
# recipient mails = "timu08@hotmail.com", "emretenker@gmail.com", "www.dbicakci@hotmail.com"
