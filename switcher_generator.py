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
    b = "Screen " + str(output1 + 1) + " Recall preset " + str(input1 + 1) + " to Screen 2"  # <------------- POSSIBLE CHANGE HERE !!!
    return b


# this function will generate the command in ASCII characters and then transform it into bytes so that it can be
# transformed into the hex values, then the resulting string is decoded from bytes into a string and capitalized

# structure of changing source command: EVENT C[1].Z[1]!KeyRelease SelectSource 1<CR><LF>


def data_generator(input1, output1):
    d = str(output1 + 1-1) + "," + str(input1+1-1) + ",1,0,0,1GClrq" + "\n"  # <------------- POSSIBLE CHANGE HERE !!!
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
        feedback_sequence_generator(width, i, height)
    return result


# __________________________________________________________________________________________________________#
# __________________________________________________________________________________________________________#
# __________________________________________________________________________________________________________#
# Here begins the functions for the reply sequences generator for the matrix

# reply structure: S C[1].Z[1].currentSource="2"<CR><LF>

def reply_data_generator(input1):
    e = "Video Input " + str(input1+1)  # <------------- POSSIBLE CHANGE HERE !!!
    return e


# The next function dictates what is expected from the device

def reply_case_data_generator(output1):
    e = str(output1+1)  # <------------- POSSIBLE CHANGE HERE !!!
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


def reply_generator(mapped_seq, input1, output1):
    d = "                <Reply Caption=\"" + str(reply_data_generator(input1)) + "\" Guid=\""
    d += str(sequence_name_generator()) + "\">\n"
    d += "                  <Data>" + str(reply_case_data_generator(input1)) + "</Data>\n"
    d += "                  <MappedToSeq Value=\"" + mapped_seq + "\" />\n"
    d += "                </Reply>\n"
    return d


def question_generator(count):
    e = str(count) + "&"     # !!!!!!!!!!!!! -------------------------------- < possible change here
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


def feedback_sequence_generator(width, count, realcount):
    # this is the string to request the feedback from the machine: in this case the MCA-88Xi
    request = question_generator(count)
    result = "            <FeedbackSequence Name=\"" + str(sequence_name_generator())
    result += "\" Caption=\"" + "Preview Video Source\"" + " Mode=\"Pull\" UseHeaderFooter=\"True\">\n"
    result += "              <RequestCommand>" + request + "</RequestCommand>\n"
    result += "              <RequestInterval Value=\"3000\" />\n"
    result += "              <ReplyDataType Value=\"String\" />\n"
    result += "              <ReplyNumberRange Min=\"0\" Max=\"0\" />\n"
    result += "              <ReplyByteOffset Value=\"0\" />\n"
    result += "              <ReplyValueType Value=\"\" />\n"
    result += "              <ReplyValueFormat Value=\"\" />\n"
    result += "              <ReplyThousandSeperator Value=\"\" />\n"
    result += "              <ReplyTimeFormat Value=\"\" />\n"
    result += "              <ReplyByteOrder Value=\"\" />\n"
    result += "              <ReplyMaxNumberOfBytesForValue Value=\"\" />\n"
    result += "              <Replies>\n"
    p = count*width
    for y in range(0, width):
            print("count : " + str(count) + " | width " + str(width) + " | realcount : " + str(realcount) + " | p : "
                  + str(p) + " | y : " + str(y))
            print(sequence_names[p])
            result += str(reply_generator(sequence_names[p], p, count))
            p += 1
            print(p)
    result += "              </Replies>\n"
    result += "            </FeedbackSequence>\n"
    print(result)
    # -------------VERY IMPORTANT ------
    # ----------------THIS FUNCTION IS IN ITERATIVE MODE AND SO THE WRITING IS DONE IN APPEND MODE -------------------
    file2 = "C:/Users/fhu/Desktop/Feedback.txt"
    with open(file2, 'a') as destination:
        destination.write(result)

    return count + 1


# -------------VERY IMPORTANT ------
# --------------@PARAM1  is the number of outputs
#  -------------@PARAM2 is the number of inputs

if __name__ == '__main__':
    matrix_generator(2, 8)
    print(sequence_names.__str__())
