from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
from summarize import get_tokens
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def tokenize_content(content):
    stop_words = set(stopwords.words('english') + list(punctuation))
    words = word_tokenize(content.lower())

    return [
        sent_tokenize(content),
        [word for word in words if word not in stop_words]
    ]


def sanitize_input(data):
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


text = convert('files/input/MotorSecure-Add-on-Covers-PolicyWordings.pdf').decode('utf-8')
# text = open('files/input/input.txt').read().decode('utf-8')           # for text file testing
text = sanitize_input(text)
sentence_tokens, word_tokens = tokenize_content(text)
output_file = open('files/output/output.txt', 'w')
output_file.write(get_tokens(sentence_tokens, word_tokens).encode('utf-8'))
