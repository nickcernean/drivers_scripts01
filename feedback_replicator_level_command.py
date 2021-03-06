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

# set the Feedback answer/reply
# set the state for every replay

def reply_data_generator(state, count):
    if state == 0:
        e = "/PARAM/COBRANET/TXMUTE/IDX" + str(count + 1) + " 1"

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

#set the question for the replies, feedback question, feedback request/get command

def question_generator(count):
    e = "/PARAM/DSP/ANALOGIN_1/GAIN/IDX" + str(count+1) + " ?"
    # the following line will put the output in bytes
    e = bytes(e, 'utf-8')
    # this line transforms the command into HEX code
    e = binascii.hexlify(e)
    # it then is returned to string format
    e = e.decode('utf-8')
    # and then put in ALL UPPER CASE as following a normal sequence generated by the device editor
    e = e.upper()
    # e = "1B" + e
    # print(d)
    return e

# this function will give the proper name to the sequences

#  sequence_caption_generator gives the name for the Feedback answer/replay command

def sequence_caption_generator(count):
    b = "AI-1 Gain Input " + str(count+1) + " level reply"
    return b


def reply_generator(count):
    d = "                <Reply Caption=\"" + sequence_caption_generator(count) + "\" Guid=\""
    d += str(sequence_name_generator()) + "\">\n"
    d += "                  <Data>" + str(reply_data_generator(0,count)) + "</Data>\n"
    d += "                  <MappedToSeq Value=\"" + "\" />\n"
    d += "                </Reply>\n"
    return d

# set feedback name here!!! strating form Caption=\"

def feedback_sequence_generator(count):
    request = question_generator(count)
    result = "            <FeedbackSequence Name=\"" + str(sequence_name_generator())
    result += "\" Caption=\"AI-1 Gain Input " + str(count+1) + " level" + "\"" + " Mode=\"Pull\" " \
                                                                             "UseHeaderFooter=\"True\">\n"
    result += "              <RequestCommand>" + request + "</RequestCommand>\n"
    result += "              <RequestInterval Value=\"3000\" />\n"
    result += "              <ReplyDataType Value=\"NumberRange\" />\n"
# Change the minimum and maximum value
    result += "              <ReplyNumberRange Min=\"-80\" Max=\"20\" />\n"  # <--- this is the min-max range !!!!
    result += "              <ReplyByteOffset Value=\"0\" />\n"
# Change to RelplyValueType String or Binary
    result += "              <ReplyValueType Value=\"String\" />\n"
# If Value Type is String, change the ValueFormat to Decimal or Hexadecimal
    result += "              <ReplyValueFormat Value=\"Decimal\" />\n"
    result += "              <ReplyThousandSeperator Value=\"None\" />\n"
    result += "              <ReplyTimeFormat Value=\"\" />\n"
    result += "              <ReplyByteOrder Value=\"\" />\n"
    result += "              <ReplyMaxNumberOfBytesForValue Value=\"Unknown\" />\n"
    result += "              <Replies>\n"
    result += str(reply_generator(count))
    result += "              </Replies>\n"
    result += "            </FeedbackSequence>\n"
    print(result)

    return result

# stated_of_setting set the number of states must be generated

if __name__ == '__main__':
    states_of_setting = [0, 1, 2]# 3, 4, 5 ,6, 7, 8, 9, 10, 11, 12, 13, 14, 15 , 16 , 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
    result_final = ''

    # set the range of creating feedback commands

    for i in range(0, 8):
        result_final += feedback_sequence_generator(i)
    file2 = "C:/Users/Nicolae.Cernean/Desktop/Feedback.txt"
    with open(file2, 'w') as destination:
        destination.write(result_final)
        destination.close()
