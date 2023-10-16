# Secret Santa Chain Generator

import csv
from itertools import permutations
import smtplib, ssl
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

def getOptionsList(p, roll, groups):

    exclusions = []
    for i in p[2:roll+2]:
        exclusions.append(i)
    for group in groups:
        if p[0] in group:
            for i in group:
                if i != p[0]:
                    exclusions.append(i)
    return exclusions
def getPairs(groups, roll, previous):

    exclusions = dict()
    for p in previous:
        exclusions[p[0]] = getOptionsList(p, roll, groups)

    participants = []
    emails = dict()
    for p in previous:
        participants.append(p[0])
        emails[p[0]] = p[1]

    chain = []
    p = 0
    while len(participants):
        if len(chain) == 0:
            chain.append(participants[p])
            del participants[p]
        else:
            if set(participants).issubset(set(exclusions[chain[-1]])): # WRITE CODE FOR THIS
                print("FIX")

            if participants[p] in exclusions[chain[-1]]:
                p += 1
            else:
                chain.append(participants[p])
                del participants[p]
        if p == len(participants):
            p = 0

    pairs = []
    for i in range(len(chain[:-1])):
        pairs.append([emails[chain[i]], chain[i], chain[i+1]])
    pairs.append([emails[chain[-1]], chain[-1], chain[0]])

    return pairs

# Extracts rolling list and participant groups, emails, and exclusions from CSV file
with open('assets/SS-groups.csv', newline='') as f:  # Change file when testing
    reader = csv.reader(f)
    participant_groups = list(reader)
with open('assets/SS-previous-real.csv', newline='') as f:
    reader = csv.reader(f)
    previous_draws = list(reader)

# Number of years after which a participant can draw a previously drawn participant
ROLLING_LIST = int(previous_draws[0][0])

# Option for adding participants
print("Is there a participant to add? (Y/N)")
while input().upper() == 'Y':
    print('Enter the name of the new participant:')
    name = input()
    print('Enter the email address of the new participant:')
    email = input()
    print('Choose the group that the new participant is being added to (#):')
    x = 0
    for i in participant_groups:
        print(i[0] + ' (' + str(x) + ')')
        x += 1
    group = int(input())

    # Add participant data to appropriate files ###FIX THIS### (WRITE TO FILE)
    participant_groups[group].append(name)
    previous_draws.append([name,email])

    print("Is there another participant to add? (Y/N)")

# Run algorithm to draw names
names_drawn = getPairs(participant_groups, ROLLING_LIST, previous_draws[1:])

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
                                <h2 style="color:green;display:inline">""" + str(datetime.date.today().year) + """</h2>
                            </td>
                        </tr>
                    </table>
                </div>
                <h3>Hi """ + i[1] + """, <br> The draw for Secret Santa has taken place again!<br></h3>
                <h2>Your drawn name is:<br></h2>
                <h1 style="color:red">""" + i[2] + """<br></h1>
                <h3>The budget is $30. Please update your wishlist
                <a href="https://l.messenger.com/l.php?u=https%3A%2F%2Fdocs.google.com%2Fspreadsheets%2Fd%2F1OZx5OpkVIADD90ZxYlb_pxXQo5Q8Yx-USD3Ui2xncUA%2Fedit%3Fusp%3Dsharing&h=AT0jzZsfINmqe7uS4M73YaMzep9HomErvFJqYLeMjaqxgjnaU7rb5e4fqrxWKyEafQY6mtI4d8SnBJMCD3v0y0Yx9HSZLOh3KTy6y2_V1ys1_LYBJFsF16RCHhHMZjdN09c6iy-wEASk_FMzDQmFAw" target="_blank">here</a>.<br>
                Please have your gifts bought by December 24th, """ + str(datetime.date.today().year) + """.<br>
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