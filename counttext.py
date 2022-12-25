from numpy import char

def countStrings(text):
    num = 0
    res = char.str_len(text)
    for ele in res:
        num = num + ele

    return num

listText = ["yes", "noo"]

print(countStrings(listText))