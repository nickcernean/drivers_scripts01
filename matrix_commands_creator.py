import string
import random
import binascii

r = 'abcdef'
sequence_names = []


# this function generates a string for the sequence name in the device, it uses the hex values for the sequence

def letters(n):
    if (n < 10):
        return str(n)
    elif (n == 10):
        return "A"
    elif (n == 11):
        return "B"
    elif (n == 12):
        return "C"
    elif (n == 13):
        return "D"
    elif (n == 14):
        return "E"
    elif (n == 15):
        return "F"
    else:
        return letters(n // 16) + letters(n % 16)


def zero(n):
    if (n > 15):
        return letters(n)
    else:
        return "0" + letters(n)


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
# it is good to set the input to input variables and output to output variables

def sequence_caption_generator(input1, output1):
    b = "ZONE" + str(input1 + 1) + "-" + str(output1 + 1) + "<CR>"
    return b


# this function will generate the command in ASCII characters and then transform it into bytes so that it can be
# transformed into the hex values, then the resulting string is decoded from bytes into a string and capitalized
# generate commands

# !!! Carriage return is "\r", and the Line feed is "\n"

def data_generator(input1, output1):
    d = "Output " + str(input1 + 1) + " " + str(output1 + 1) + "\r "

    # if input1 >= 9 and output1 >= 9:
    # d = "OUTPUT" + str(output1 + 1) + " " + str(input1 + 1)
    # elif input1 <= 8 and output1 <= 8:
    # d = "OUTPUT0" + str(output1 + 1) + " 0" + str(input1 + 1)
    # elif input1 <= 8 and output1 >= 9:
    # d = "OUTPUT" + str(output1 + 1) + " 0" + str(input1 + 1)
    # elif input1 >= 9 and output1 <= 8:
    #  d = "OUTPUT0" + str(output1 + 1) + " " + str(input1 + 1)

    # if input1 > 8 and output1 <= 8:
    #  d = "OUT " + str(output1 + 1) + " FR 0" + str(input1 + 1) + "" #FOR 16x16 MATRICES!!!
    # elif input1 <= 8 and output1 > 8:                                      #FOR 16x16 MATRICES!!!
    # d = "OUT 0" + str(output1 + 1) + " FR " + str(input1 + 1) + "" #FOR 16x16 MATRICES!!!
    # elif input1 > 8 and output1 > 8:                                      #FOR 16x16 MATRICES!!!
    # d = "OUT " + str(output1 + 1) + " FR " + str(input1 + 1) + ""  #FOR 16x16 MATRICES!!!

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


# In SequenceType change to Source or Control?

def sequence_generator(input1, output1):
    a = str(sequence_name_generator())
    sequence_names.append(a)
    c = "            <Sequence Name=\"" + a + "\""
    c += " Caption=\"" + str(sequence_caption_generator(input1, output1)) + "\""
    c += " DeviceMenu=\"True\" ProjectMenu=\"True\" Selectable=\"True\" SequenceType=\"Control\" Deletable=\"True\" " \
         "HasData=\"False\" UseHeaderFooter=\"True\">\n              "
    b = str(sequence_name_generator())
    c += "<Reply Name=\"" + b + "\" Caption=\"Reply\" DeviceMenu=\"True\" " \
                                "ProjectMenu=\"True\" Selectable=\"True\" SequenceType=\"Reply\" " \
                                "UseHeaderFooter=\"True\">\n "
    c += "                <Image />\n"
    c += "                <Command>\n"
    c += "                  <Data1 />\n"
    c += "                  <SeekOffset Value=\"0\" />\n"
    c += "                </Command>\n"
    c += "              </Reply>\n"
    c += "              <Description />\n"
    c += "              <Image />\n"
    c += "              <Command>\n"
    c += "                <Data1>" + str(data_generator(input1, output1)) + "</Data1>\n"
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
    file = "C:/Users/Nicolae.Cernean/OneDrive - Biamp Systems/Desktop/Result.txt"
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

# set the Feedback answer/reply
# set the state for every replay

def reply_data_generator(input1, output1):
    e = "SET SELECT ZONE " + str(output1+1) + " " + str(input1+1)
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


# feedback reply name

def reply_sequence_caption_generator(input1, output1):
    b = "ZONE " + str(output1+1) + "-" + str(input1+1)
    return b


def reply_generator(mapped_seq, input1, output1):
    d = "                <Reply Caption=\"" + str(reply_sequence_caption_generator(input1, output1)) + "\" Guid=\""
    d += str(sequence_name_generator()) + "\">\n"
    d += "                  <Data>" + reply_data_generator(input1, output1) + "</Data>\n"
    #    d += "                  <Data>" + "OUT"+ str(output1+1) + " VS IN" + str(input1+1) + "</Data>\n"
    d += "                  <MappedToSeq Value=\"" + mapped_seq + "\" />\n"
    d += "                </Reply>\n"
    return d


# set the question for the replies, feedback question, feedback request/get command

def question_generator(count):
    e = "GET SELECT ZONE " + str(count+1) + str("0D")  # <-------------- POSSIBLE CHANGE HERE

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
    result += "\" Caption=\" Get Select Zone "+str(count+1) + "\"" + " Mode=\"Pull\" UseHeaderFooter=\"True\">\n"
    result += "              <RequestCommand>" + request + "</RequestCommand>\n"
    result += "              <RequestInterval Value=\"3000\" />\n"
    result += "              <ReplyDataType Value=\"String\" />\n"
    # Change the minimum and maximum value
    result += "              <ReplyNumberRange Min=\"0\" Max=\"0\" />\n"
    result += "              <ReplyByteOffset Value=\"" + str(0) + "\" />\n"
    result += "              <ReplyValueType Value=\"\" />\n"
    result += "              <ReplyValueFormat Value=\"\" />\n"
    result += "              <ReplyThousandSeperator Value=\"\" />\n"
    result += "              <ReplyTimeFormat Value=\"\" />\n"
    result += "              <ReplyByteOrder Value=\"\" />\n"
    result += "              <ReplyMaxNumberOfBytesForValue Value=\"\" />\n"
    result += "              <Replies>\n"
    p = width*count
    for y in range(0, width):

        result += str(reply_generator(sequence_names[p], count, y))
        p += 1
    result += "              </Replies>\n"
    result += "            </FeedbackSequence>\n"
    print(result)
    # -------------VERY IMPORTANT ------
    # ----------------THIS FUNCTION IS IN ITERATIVE MODE AND SO THE WRITING IS DONE IN APPEND MODE -------------------
    file_2 = "C:/Users/Nicolae.Cernean/OneDrive - Biamp Systems/Desktop/Result.txt"
    with open(file_2, 'a') as destination_2:
        destination_2.write(result)

    return count + 1


if __name__ == '__main__':
    file2 = "C:/Users/Nicolae.Cernean/OneDrive - Biamp Systems/Desktop/Result.txt"
    with open(file2, 'w') as destination:
        destination.write('')
        destination.close()

    # !!!! matrix_generator(output, input)
    matrix_generator(10, 8)

