from django.shortcuts import render
from django.http import FileResponse

# Create your views here.
def new_invoice_form(req):
    return render(req,'new_invoice.html')

def pdf_invoice(req):
    from fpdf import FPDF
    DATE = req.POST.get("InvoiceDate")
    BILLNO = "20020921001"#req.POST.get("InvoiceView")
    CUSTNAME = req.POST.get("CustName")
    COMPANY = "ABC Infotech"
    CADDRESS = req.POST.get("SiteAddress")
    PH = "98834XXXXY"
    EM = "invalid@abc.com"
    # print(float(req.POST.get("h")), float(req.POST.get("w")), \
    #     float(req.POST.get("qty")) , float(req.POST.get("rate")), 555555555555555555)
    tot = float(req.POST.get("h")) * float(req.POST.get("w")) * \
        float(req.POST.get("qty")) * float(req.POST.get("rate"))
    ITEMS = [ ['1', req.POST.get('wt'), req.POST.get("wd"), req.POST.get("w"),\
            req.POST.get("h"), req.POST.get("qty"), req.POST.get("area"),\
            req.POST.get("rate"), tot  ], ]
    # ITEMS = [['1', 'Glass', 'Classic', 70, 90, 2, 70*90, 15, 70*90*15*2 ],\
    #         ['2', 'Wooden', 'Classic', 30, 40, 3, 30*40, 13, 30*40*13*3 ],\
    #         ['3', 'Glass', 'Classic', 50, 70, 1, 50*70, 15, 50*70*15 ],\
    #         ['4', 'Glass', 'Classic', 60, 70, 1, 60*70, 15, 60*70*15 ],\
    #     ]
    spacing = [16, 12, 37, 35, 15, 15, 10, 17, 15]
    print(tot)
    TOTAL = str(sum([i[-1] for i in ITEMS]))
    print(TOTAL, 777777777777777)
    TC = req.POST.get("tc")
    TAX = str((18*(float(TOTAL)+int(TC)))/100)
    DIS = "100"
    DTOTAL = str(float(TOTAL)+float(TC)+float(TAX)-float(DIS))
    ROUND = "0" if "." not in DTOTAL else DTOTAL.split('.')[-1]
    class Document(FPDF):
        border_width = 10
        width = 210
        height = 297
        def lines(self):
            self.set_line_width(0.0)
            self.line(Document.border_width, Document.border_width, Document.width - Document.border_width,\
                Document.border_width)#top
            self.line(Document.border_width, Document.height - Document.border_width, Document.width - Document.border_width,\
                Document.height - Document.border_width)#bottom
            self.line(Document.border_width, Document.border_width, Document.border_width, \
                Document.height - Document.border_width )#left
            self.line(Document.width - Document.border_width,Document.border_width, \
                Document.width - Document.border_width, Document.height - Document.border_width)

    doc = Document(orientation='P', unit='mm', format='A4')
    doc.add_page()
    doc.lines()
    doc.image(r'C:\Users\vicky\Desktop\logo.png', 15, 20, w=180, h=20)
    doc.image(r'C:\Users\vicky\Desktop\address_dt_billno.png', 15, 40, w=180, h=25)
    doc.set_xy(157, 47)
    doc.set_font('Arial', 'B', 12)
    doc.cell(w=5,h=5,txt=DATE)
    doc.set_xy(157, 53.5)
    doc.cell(w=5,h=5,txt=BILLNO)
    doc.line(Document.border_width, 65, Document.width - Document.border_width, 65)
    doc.image(r'C:\Users\vicky\Desktop\cli_details.png', 15, 68, w=180, h=25)
    doc.image(r'C:\Users\vicky\Desktop\list.png', 11, 100, w=188, h=180)
    y = 115
    for item in ITEMS:
        x = 0
        for i in range(len(item)):
            x += spacing[i]
            doc.set_xy(x, y)
            doc.cell(w=5,h=5,txt=str(item[i]))
        y+=7
    doc.set_xy(172, 223)
    doc.cell(w=5,h=5,txt=TOTAL)
    doc.set_xy(172, 228)
    doc.cell(w=5,h=5,txt=TC)
    doc.set_xy(172, 233)
    doc.cell(w=5,h=5,txt=TAX)
    doc.set_xy(172, 238)
    doc.cell(w=5,h=5,txt=DIS)
    doc.set_xy(172, 243)
    doc.cell(w=5,h=5,txt=ROUND)
    doc.set_xy(172, 249)
    doc.cell(w=5,h=5,txt=DTOTAL)

    doc.set_xy(50, 72)
    doc.set_font('Arial', 'B', 9)
    doc.cell(w=5,h=5,txt=CUSTNAME)
    doc.set_xy(50, 75)
    doc.cell(w=5,h=5,txt=COMPANY)
    doc.set_xy(50, 78)
    doc.cell(w=5,h=5,txt=CADDRESS)
    doc.set_xy(50, 81)
    doc.cell(w=5,h=5,txt=PH)
    doc.set_xy(50, 84)
    doc.cell(w=5,h=5,txt=EM)
    '''
    doc.set_xy(40,45)
    doc.set_font('Arial', 'B', 15)
    #doc.set_text_color(220, 50, 50)
    doc.cell(w=5,h=5,align="C",txt="Bright UPVC Windows",border=0)
    '''
    doc.output(r'test.pdf','F')
    doc.close()
    return FileResponse(open('test.pdf', 'rb'))
    #render(req, "message.html", {"msg": CUSTNAME})
