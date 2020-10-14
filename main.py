# Secret Santa Chain Generator

import csv
import random
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# Extracts participants, emails, and exclusions from CSV file
with open('SS-participants.csv', newline='') as f:
    reader = csv.reader(f)
    participant_data = list(reader)

# Extracts list of participants and emails from the data list
participants = [i[1] for i in participant_data[1:]]
names_drawn = []

# Initialize seed
SEED = 2019

# Creates a string of integers using the seed that will determine the order of future random integers
random.seed(SEED)
s = str(random.random())
s_index = 2

# Generates a chain until it is valid
isValid = False
while not isValid:

    # Creates duplicate list to modify
    temp_participants = list(participants)
    names_drawn = [i[:2] for i in participant_data[1:]]

    isValid = True
    drawn = ""
    first_drawn = ""

    for i in range(len(participants)):

        # Breaks loop when the chain becomes invalid
        if not isValid:
            break

        # Check for exclusions only after the first name has been generated
        if len(temp_participants) < len(participants):
            rand = drawn
            last_index = participants.index(rand)

            # The chain is invalid if all of the remaining names are in the exclusions list of the generated name
            if all(i in participant_data[last_index + 1][1:] for i in temp_participants):
                isValid = False

            else:
                # Generate a name until there is one that is not in the exclusions list
                while rand in participant_data[last_index + 1][1:]:

                    # Generates a random integer using the next integer in the SEED string as the seed
                    random.seed(int(s[s_index]))
                    s_index += 1
                    rand = temp_participants[random.randint(0, len(temp_participants)) - 1]

                    # Increase SEED by 1 to use a new string of integers when the previous one runs out
                    if s_index == len(s):
                        SEED += 1
                        random.seed(SEED)
                        s = str(random.random())
                        s_index = 2

                # Add the new generated name to the names drawn list next to the last generated name
                names_drawn[last_index].append(rand)
        else:
            random.seed(int(s[s_index]))
            s_index += 1
            rand = temp_participants[random.randint(0, len(temp_participants)) - 1]
            first_drawn = rand

        # Add the valid name to the chain
        if isValid:
            drawn = rand
            temp_participants.remove(rand)

        if s_index == len(s):
            SEED += 1
            random.seed(SEED)
            s = str(random.random())
            s_index = 2

    # The chain is invalid if the first name is in the exclusions list of the last name
    last_index = participants.index(drawn)
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
    fp = open('secretsanta.jpg', 'rb')
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


