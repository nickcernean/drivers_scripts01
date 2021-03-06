import string
import random
import binascii

r = 'abcdef'
sequence_names = []

# this function generates a string for the sequence name in the device, it uses the hex values for the sequence


def sequence_name_generator():
    a = ""
    for i in range(0, 36):
        if i == 8 or i == 13 or i == 18 or i == 23:
            a += "-"
        else:
            b = random.choice(r + string.digits)
            a += b.lower()
    # print(a)
    return a


# this function will give the proper name to the sequences


def sequence_caption_generator(input1, output1):
    b = "Output " + str(input1 + 1) + " Input " + str(output1 + 1)
    return b


# this function will generate the command in ASCII characters and then transform it into bytes so that it can be
# transformed into the hex values, then the resulting string is decoded from bytes into a string and capitalized

def cks_hex_calc(a,b):
    sum_hex_before = int("80",16) # checksum value before input and output
    return hex(sum_hex_before + int(str(a), 16) + int(str(b), 16))[2:]

def temp_cal_hex(input1,output1):
    o = hex(int(str(output1+1),16))[2:]
    i = hex(int(str(input1+1),16))[2:]
    if input1+1 < 10 and output1+1 > 9:
        d = "<T000070100" + i + o + "00" + cks_hex_calc(output1+1,input1+1) + ">" + "\r"
        return d
    elif input1+1 > 9 and output1+1 < 10:
        d = "<T00007010" + i + "0" + o + "00" + cks_hex_calc(output1 + 1, input1 + 1) + ">" + "\r"
        return d
    elif input1+1 > 9 and output1+1 > 9:
        d = "<T00007010" + i + o + "00" + cks_hex_calc(output1 + 1, input1 + 1) + ">" + "\r"
        return d
    elif input1+1 < 10 and output1+1 < 10:
        d = "<T000070100" + i + "0" + o + "00" + cks_hex_calc(output1 + 1, input1 + 1) + ">" + "\r"
        return d



def data_generator(input1, output1):

    o = hex(int(str(output1+1),16))[2:]
    i = hex(int(str(input1+1),16))[2:]
    d = str(temp_cal_hex(input1, output1))
    # d = "<T000070100" + i + o + "00" + cks_hex_calc(output1+1,input1+1) + ">" + "\r"
    # the following line will put the output in bytes
    d = bytes(d, 'utf-8')
    # this line transforms the command into HEX code
    d = binascii.hexlify(d)
    # it then is returned to string format
    d = d.decode('utf-8')
    # and then put in ALL UPPER CASE as following a normal sequence generated by the device editor
    d = d.upper()
    # print(d)
    return d


def sequence_generator(input1, output1):
    a = str(sequence_name_generator())
    sequence_names.append(a)
    c = "            <Sequence Name=\"" + a + "\""
    c += " Caption=\"" + str(sequence_caption_generator(input1, output1)) + "\""
    c += " DeviceMenu=\"True\" ProjectMenu=\"True\" Selectable=\"True\" SequenceType=\"Source\" Deletable=\"True\" " \
        "HasData=\"False\" UseHeaderFooter=\"True\">\n              "
    b = str(sequence_name_generator())
    c += "<Reply Name=\"" + b + "\" Caption=\"Reply\" DeviceMenu=\"True\" " \
         "ProjectMenu=\"True\" Selectable=\"True\" SequenceType=\"Reply\" UseHeaderFooter=\"True\">\n"
    c += "                <Image />\n"
    c += "                <Command>\n"
    c += "                  <Data1 />\n"
    c += "                  <SeekOffset Value=\"0\" />\n"
    c += "                </Command>\n"
    c += "              </Reply>\n"
    c += "              <Description />\n"
    c += "              <Image />\n"
    c += "              <Command>\n"
    c += "                <Data1>" + data_generator(input1, output1) + "</Data1>\n"
    c += "                <Data2 />\n"
    c += "                <Lock1 Value=\"0\" />\n"
    c += "                <Lock2 Value=\"0\" />\n"
    c += "              </Command>\n"
    c += "            </Sequence>\n"
    # print(c)
    return c


def matrix_generator(height, width):
    result = ""
    for i in range(0, width):
        for j in range(0, height):
            result += sequence_generator(i, j)
    file = "C:/Users/fhu/Desktop/Result.txt"
    with open(file, 'w') as destination:
        destination.write(result)
    print(result)
    counter = 0
    for i in range(0, height):
        counter = feedback_sequence_generator(width, counter)
    return result


# __________________________________________________________________________________________________________#
# __________________________________________________________________________________________________________#
# __________________________________________________________________________________________________________#
# Here begins the functions for the reply sequences generator for the matrix

# checksum for query
def cks_Feed_hex_calc(a):
    sum_hex_before = int("81",16) # checksum value before input and output
    return hex(sum_hex_before + int(str(a), 16))[2:]

# command with checksum calculator (query)
def temp_Feed_cal_hex(input1,output1):
    o = hex(int(str(output1+1),16))[2:]
    i = hex(int(str(input1+1),16))[2:]
    if output1+1 > 9 and input1+1 < 10:
        d = "<F000070110" + i + o + "00" + cks_Feed_1_hex_calc(output1+1,input1+1) + ">" + "\r"
        return d
    elif output1+1 < 10 and input1+1 > 9:
        d = "<F00007011" + i + "0" + o + "00" + cks_Feed_1_hex_calc(output1 + 1, input1 + 1) + ">" + "\r"
        return d
    elif output1+1 > 9 and input1+1 > 9:
        d = "<F00007011" + i + o + "00" + cks_Feed_1_hex_calc(output1 + 1, input1 + 1) + ">" + "\r"
        return d
    elif output1+1 < 10 and input1+1 < 10:
        d = "F000070110" + i + "0" + o + "00" + cks_Feed_1_hex_calc(output1 + 1, input1 + 1) + ">" + "\r"
        return d

# checksum for replies of query
def cks_Feed_1_hex_calc(a,b):
    sum_hex_before = int("81",16) # checksum value before input and output
    return hex(sum_hex_before + int(str(a), 16) + int(str(b), 16))[2:]

# command with checksum calculator (query replies)
def temp_Feed_1_cal_hex(count):
   # i =
    c = 81
#    sum_before = int(str(c), 16)
    if count+1 > 9:
        d = "<T00007011" + str(count+1) + "0000" + hex(int(str(c), 16) + int(str(count+1), 16))[2:] + ">" + "\r"
        return d
    else:
        d = "<T000070110" + str(count+1) + "0000" + hex(int(str(c), 16) + int(str(count+1), 16))[2:] + ">" + "\r"
        return d


def reply_data_generator(input1, output1):
    e = str(temp_Feed_cal_hex(input1, output1))
    # the following line will put the output in bytes
    e = bytes(e, 'utf-8')
    # this line transforms the command into HEX code
    e = binascii.hexlify(e)
    # it then is returned to string format
    e = e.decode('utf-8')
    # and then put in ALL UPPER CASE as following a normal sequence generated by the device editor
    e = e.upper()
    # print(d)
    return e


def reply_sequence_caption_generator(input1, output1):
    # feedback replay name / petite description like on off
    b = " Out " + str(input1+1) + " In " + str(output1+1)
    return b


def reply_generator(mapped_seq, input1, output1):
    d = "                <Reply Caption=\"" + str(reply_sequence_caption_generator(input1, output1)) + "\" Guid=\""
    d += str(sequence_name_generator()) + "\">\n"
    # le truc a changer la valeur pr le ON/OFF par exemple
    d += "                  <Data>" + str(reply_data_generator(input1, output1)) + "</Data>\n"
    #    d += "                  <Data>" + "OUT"+ str(output1+1) + " VS IN" + str(input1+1) + "</Data>\n"
    d += "                  <MappedToSeq Value=\"" + mapped_seq + "\" />\n"
    d += "                </Reply>\n"
    return d



def question_generator(count):
    # General command request for
    e = temp_Feed_1_cal_hex(count)   # <-------------- POSSIBLE CHANGE HERE
    # the following line will put the output in bytes
    e = bytes(e, 'utf-8')
    # this line transforms the command into HEX code
    e = binascii.hexlify(e)
    # it then is returned to string format
    e = e.decode('utf-8')
    # and then put in ALL UPPER CASE as following a normal sequence generated by the device editor
    e = e.upper()
    # print(d)
    return e


def feedback_sequence_generator(width, count):
    # Big Description nom de base
    # this is the request "STA" for the FSA DV-HMSW4K-88 Matrix
    request = question_generator(count)
    result = "            <FeedbackSequence Name=\"" + str(sequence_name_generator())
    result += "\" Caption=\"Output source " + str(count+1) + " status" + "\"" + " Mode=\"Pull\" UseHeaderFooter=\"True\">\n"
    result += "              <RequestCommand>" + request + "</RequestCommand>\n"
    result += "              <RequestInterval Value=\"3000\" />\n"
    result += "              <ReplyDataType Value=\"String\" />\n"
    result += "              <ReplyNumberRange Min=\"0\" Max=\"0\" />\n"
    result += "              <ReplyByteOffset Value=\"" + str(0) + "\" />\n"
    result += "              <ReplyValueType Value=\"\" />\n"
    result += "              <ReplyValueFormat Value=\"\" />\n"
    result += "              <ReplyThousandSeperator Value=\"\" />\n"
    result += "              <ReplyTimeFormat Value=\"\" />\n"
    result += "              <ReplyByteOrder Value=\"\" />\n"
    result += "              <ReplyMaxNumberOfBytesForValue Value=\"\" />\n"
    result += "              <Replies>\n"
    p = count * width
    for y in range(0, width):
            result += str(reply_generator(sequence_names[p], count, y))
            p += 1
    result += "              </Replies>\n"
    result += "            </FeedbackSequence>\n"
    print(result)
    # -------------VERY IMPORTANT ------
    # ----------------THIS FUNCTION IS IN ITERATIVE MODE AND SO THE WRITING IS DONE IN APPEND MODE -------------------
    file_2 = "C:/Users/fhu/Desktop/Feedback.txt"
    with open(file_2, 'a') as destination_2:
        destination_2.write(result)

    return count + 1


if __name__ == '__main__':
    file2 = "C:/Users/Nicolae.Cernean/Desktop/Feedback.txt"
    with open(file2, 'w') as destination:
        destination.write('')
        destination.close()

    matrix_generator(16, 16)