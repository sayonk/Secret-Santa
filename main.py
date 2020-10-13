# Secret Santa Chain Generator

import csv
import random

# Extracts participants and exclusions from CSV file
with open('SS-exclusions.txt', newline='') as f:
    reader = csv.reader(f)
    exclusions = list(reader)

# Extracts list of participants from the exclusions list
participants = [i[0] for i in exclusions[1:]]
chain = []

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
    chain = []

    isValid = True

    for i in range(len(participants)):

        # Breaks loop when the chain becomes invalid
        if not isValid:
            break

        # Check for exclusions only after the first name has been generated
        if len(chain):
            rand = chain[-1]
            last_index = participants.index(rand)

            # The chain is invalid if all of the remaining names are in the exclusions list of the generated name
            if all(i in exclusions[last_index + 1] for i in temp_participants):
                isValid = False

            else:
                # Generate a name until there is one that is not in the exclusions list
                while rand in exclusions[last_index + 1]:

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

        else:
            random.seed(int(s[s_index]))
            s_index += 1
            rand = temp_participants[random.randint(0, len(temp_participants)) - 1]

        if s_index == len(s):
            SEED += 1
            random.seed(SEED)
            s = str(random.random())
            s_index = 2

        # Add the valid name to the chain
        if isValid:
            chain.append(rand)
            temp_participants.remove(rand)

    # The chain is invalid if the first name is in the exclusions list of the last name
    if chain[-1] in exclusions[participants.index(chain[0]) + 1]:
        isValid = False

# Convert the chain list into a list of pairs
pairs = []
for i in range(len(chain)):
    pairs.append([chain[i], chain[(i + 1) % len(chain)]])

print(pairs)
