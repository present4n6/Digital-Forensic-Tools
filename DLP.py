from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)
        text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return text

extracted_text = convert_pdf_to_txt('D:\privacy.pdf')

pat = re.compile("([0-9]{6}[\s~-]+[1-8][0-9]{6})")
pat2 = re.compile("01[016789][-~\s][0-9]{3,4}[-~\s][0-9]{4}")
RRN=pat.findall(extracted_text) #Resident Registration Number
PN=pat2.findall(extracted_text) #Phone Number
print("주민등록 번호 목록\n")
for i in range(0,len(RRN)):
    print(RRN[i])
print("\n전화번호 목록\n")
for i in range(0,len(PN)):
    print(PN[i])