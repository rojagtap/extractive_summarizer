from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
from summarize import get_tokens
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import re


def tokenize_content(content):
    stop_words = set(stopwords.words('english') + list(punctuation))
    words = word_tokenize(content.lower())

    return [
        sent_tokenize(content),
        [word for word in words if word not in stop_words]
    ]


def sanitize_input(data):
    # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    data.replace('\f', ' ')
    data.replace('\t', ' ')
    data.replace('\r', '')

    return data


# converts pdf, returns its text content as a string
# noinspection PyShadowingNames
def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    return text


def section(text,temp,temp3):
    sections = list()
    cap = '[A-Z]'
    caps = '[A-Z\s]+$'
    digit = '[0-9]+'
    content = '[A-Za-z]+'
    roman = '^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})'
    hyphen = '.'
    space = '[\s]+'
    newline = '[\n]'
    heading1 = r"%s%c%s%s" % (roman, hyphen, space, caps)
    heading2 = r"%s%c%s%s" % (cap, hyphen, space, caps)
    heading3 = r"%s%c%s%s" % (digit, hyphen, space, caps)
    con = r"%s" % (content)
    # heading2 = (heading|heading1)
    # inputtext = "I. SFFFG Phjbjk"
    # inputtext = open('files/input/trial.docx','r')
    # with open('files/input/trial.txt') as f:

    def format1():
        i = 0
        secsummary=""
        for line in temp.readlines():
            # print(line)
            # print("bbbbbbbbbbbbbbbbbbbbbb")

            if re.search(heading1, line) :
                print(line)
                if i == 0:

                    i = 1
                else:
                    secsummary = sanitize_input(secsummary)
                    print(secsummary)
                    sections.append(secsummary)
                    # con_file = open('files/input/content.txt','a')
                    # print(text.encode('utf-8'))
                    sentence_tokens, word_tokens = tokenize_content(secsummary)
                    output_file.write(get_tokens(sentence_tokens, word_tokens))
                    output_file.write("\n\n\n".encode('utf-8'))

                    # sentence_tokens, word_tokens = tokenize_content(secsummary)

                    # output_file = open('files/output/output.txt', 'a')
                    # output_file.write(get_tokens(sentence_tokens, word_tokens))
                    secsummary = ""
                    i = 0
                    # print(line)

            else:

                secsummary = secsummary + line
                i = 1

    def format2():
        secsummary = ""
        i = 0
        for line in temp.readlines():
            # print(line)
            # print("bbbbbbbbbbbbbbbbbbbbbb")

            if re.search(heading2, line):
                print(line)
                if i == 0:

                    i = 1
                else:
                    secsummary = sanitize_input(secsummary)
                    print(secsummary)
                    sections.append(secsummary)
                    # con_file = open('files/input/content.txt','a')
                    # print(text.encode('utf-8'))
                    sentence_tokens, word_tokens = tokenize_content(secsummary)
                    output_file.write(get_tokens(sentence_tokens, word_tokens))
                    output_file.write("\n\n\n".encode('utf-8'))

                    # sentence_tokens, word_tokens = tokenize_content(secsummary)

                    # output_file = open('files/output/output.txt', 'a')
                    # output_file.write(get_tokens(sentence_tokens, word_tokens))
                    secsummary = ""
                    i = 0
                    # print(line)

            else:

                secsummary = secsummary + line
                i = 1

    def format3():
        secsummary = ""
        i = 0
        for line in temp3.readlines():
            # print(line)
            # print("bbbbbbbbbbbbbbbbbbbbbb")

            if re.search(heading3, line):
                print(line)
                if i == 0:

                    i = 1
                else:
                    secsummary = sanitize_input(secsummary)
                    print(secsummary)
                    sections.append(secsummary)
                    # con_file = open('files/input/content.txt','a')
                    # print(text.encode('utf-8'))
                    sentence_tokens, word_tokens = tokenize_content(secsummary)
                    output_file.write(get_tokens(sentence_tokens, word_tokens))
                    output_file.write("\n\n\n".encode('utf-8'))

                    # sentence_tokens, word_tokens = tokenize_content(secsummary)

                    # output_file = open('files/output/output.txt', 'a')
                    # output_file.write(get_tokens(sentence_tokens, word_tokens))
                    secsummary = ""
                    i = 0
                    # print(line)

            else:

                secsummary = secsummary + line
                i = 1


    def switch(format):
        switcher = {
            1:format1(),
            2:format2(),
            3:format3()

        }
        return switcher.get(format, "Invalid pattern")


    for line in text.readlines():
        if re.search(heading1, line):
            switch(1)
            break
        elif re.search(heading2, line):
            switch(2)
            break
        elif re.search(heading3, line):
            switch(3)
            break



# text = convert('files/input/MotorSecure-Add-on-Covers-PolicyWordings.pdf').decode('utf-8')
# text = open('files/input/input.txt').read().decode('utf-8')           # for text file testing

# with open('files/input/trial.txt' , 'r') as text:
#    section(text)

text = open('files/input/input.txt', 'r')
temp = open('files/input/input.txt', 'r')
temp3 = open('files/input/input.txt', 'r')
output_file = open('files/output/output.txt', 'a+')
section(text,temp,temp3)
