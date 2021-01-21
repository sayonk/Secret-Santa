# Secret Santa Chain Generator

import csv
import random
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# Extracts participants, emails, and exclusions from CSV file
with open('assets/SS-participants.csv', newline='') as f:
    reader = csv.reader(f)
    participant_data = list(reader)

# Extracts list of participants and emails from the data list
participants = [i[1] for i in participant_data[1:]]
names_drawn = []

# Initialize seed
random.seed(2019)

# Generates a chain until it is valid
isValid = False
while not isValid:

    # Creates duplicate list to modify
    temp_participants = list(participants)
    names_drawn = [i[:2] for i in participant_data[1:]]

    isValid = True

    # The first drawn name does not need to be checked for exclusions
    rand = temp_participants[random.randint(0, len(temp_participants)) - 1]
    first_drawn = rand
    temp_participants.remove(rand)

    for i in range(len(temp_participants)):

        last_index = participants.index(rand)

        # Create set of exclusions for the last drawn name
        exclusions = set(participant_data[last_index + 1][2:])

        # Create list of valid participants using the remaining names and the exclusion list
        valid_participants = [item for item in temp_participants if item not in exclusions]

        # The chain is invalid if there are no remaining valid participants
        if not len(valid_participants):
            isValid = False
            break

        else:

            # Generates a random name from the remaining valid names
            rand = valid_participants[random.randint(0, len(valid_participants)) - 1]

            # Add the new generated name to the names drawn list next to the last generated name
            names_drawn[last_index].append(rand)

        # Add the valid name to the chain
        temp_participants.remove(rand)

    # The chain is invalid if the first name is in the exclusions list of the last name
    last_index = participants.index(rand)
    if first_drawn in participant_data[last_index + 1][1:]:
        isValid = False
    else:
        names_drawn[last_index].append(first_drawn)

# Sends emails to all participants
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "testpython413@gmail.com"
password = input("Type your password and press enter: ")

for i in names_drawn:
    receiver_email = i[0]  # Enter receiver address

    message = MIMEMultipart("alternative")
    message["Subject"] = "Hi " + i[1] + ", you have drawn a name for Secret Santa!"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Creates HTML version of the message
    html = """\
    <html>
      <body>
        <div class="row">
            <img src="cid:image" alt="Secret Santa" height="200">
        </div>
        <div class="row">
            <h3>Hi """ + i[1] + """, <br> The draw for Secret Santa has taken place!<br></h3>
            <h2>Your drawn name is:<br></h2>
            <h1 style="color:red">""" + i[2] + """<br></h1>
            <h3>Have Fun!<br>
            Your Secret Santa Helpers</h3>
        </div>
      </body>
    </html>
    """

    # Assumes the image is in the current directory
    fp = open('assets/secretsanta.jpg', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image>')
    message.attach(msgImage)

    # Turns this into html MIMEText objects
    # Adds HTML-text parts to MIMEMultipart message
    message.attach(MIMEText(html, "html"))

    # Creates secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


