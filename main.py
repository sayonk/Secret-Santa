# Secret Santa Chain Generator

import csv
import random
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

YEAR = 2022

# Extracts participants, emails, and exclusions from CSV file
with open('assets/SS-participants.csv', newline='') as f:
    reader = csv.reader(f)
    participant_data = list(reader)

# Extracts list of participants and emails from the data list
participants = [i[1] for i in participant_data[1:]]
names_drawn = []

# Verify if exclusions are valid names
valid = True
for i in participant_data[1:]:
    for j in i[2:]:
        if j not in participants:
            valid = False
            print("Invalid names in the exclusion list")
            break

if valid:
    # Initialize seed
    random.seed(YEAR)

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
    sender_email = "bfgkSS@gmail.com"
    password = input("Type your password and press enter: ")

    for i in names_drawn:
        # if i[0] == "sayon.mk@gmail.com":
            receiver_email = i[0]  # Enter receiver address

            message = MIMEMultipart("alternative")
            message["Subject"] = "Hi " + i[1] + ", you have DRAWN a name for Secret Santa!"
            message["From"] = "BFGK Secret Santa"
            message["To"] = receiver_email

            # Creates HTML version of the message
            html = """\
            <html>
                <body>
                    <div style="display:inline-block;vertical-align:top;">
                        <img src="cid:image" alt="Secret Santa" height="200">
                    </div>
                    <div style="display:inline-block;">
                        <table>
                            <tr><br><br><br></tr>
                            <tr>
                                <td>&emsp;</td>
                                <td>
                                    <h2 style="color:green;display:inline">BFGK </h2>
                                    <h2 style="color:red;display:inline">SECRET<br></h2>
                                </td>
                            </tr>
                            <tr>
                                <td>&emsp;</td>
                                <td>
                                    <h2 style="color:red;display:inline">SANTA </h2>
                                    <h2 style="color:green;display:inline">""" + str(YEAR) + """</h2>
                                </td>
                            </tr>
                        </table>
                    </div>
                    <h3>Hi """ + i[1] + """, <br> The draw for Secret Santa has taken place again!<br></h3>
                    <h2>Your drawn name is:<br></h2>
                    <h1 style="color:red">""" + i[2] + """<br></h1>
                    <h3>The budget is $30. Please update your wishlist
                    <a href="https://l.messenger.com/l.php?u=https%3A%2F%2Fdocs.google.com%2Fspreadsheets%2Fd%2F1OZx5OpkVIADD90ZxYlb_pxXQo5Q8Yx-USD3Ui2xncUA%2Fedit%3Fusp%3Dsharing&h=AT0jzZsfINmqe7uS4M73YaMzep9HomErvFJqYLeMjaqxgjnaU7rb5e4fqrxWKyEafQY6mtI4d8SnBJMCD3v0y0Yx9HSZLOh3KTy6y2_V1ys1_LYBJFsF16RCHhHMZjdN09c6iy-wEASk_FMzDQmFAw" target="_blank">here</a>.<br>
                    Please have your gifts bought by December 24th, """ + str(YEAR) + """.<br>
                    Logistics of the exchange are TBA.<br></h3>
                    <h4>If you have any questions, please drop it in the main group chat.<br>
                    If there are any complaints, please address them
                    <a href="https://tinyurl.com/ycttvdwt" target="_blank">here</a>.</h4>
                    <h3>Have Fun!<br>
                    Your BFGK Executives</h3>
                </body>
            </html>
            """

            # Assumes the image is in the current directory
            fp = open('assets/tamilsanta.png', 'rb')
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


