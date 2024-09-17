# Open the file in read mode
with open('URL.txt', 'r') as file:
    # Read lines from the file and store them in a list
    lines = file.readlines()

# Display the contents of the list
print("Contents of the list:")
for line in lines:
    print(line.strip())  # Strip any leading/trailing whitespace from each line
