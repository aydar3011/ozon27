# encoding=utf8
import sys
from rtfw import *
reload(sys)
sys.setdefaultencoding('utf8')

def createTable():
    table = Table(TabPropertySet.DEFAULT_WIDTH * 4,
                  TabPropertySet.DEFAULT_WIDTH * 2,
                  TabPropertySet.DEFAULT_WIDTH * 5,
                  TabPropertySet.DEFAULT_WIDTH * 2)

    c1 = Cell(Paragraph(u"Наименование"))
    c2 = Cell(Paragraph(u"Артикул"))
    c3 = Cell(Paragraph(u"Изображение"))
    c4 = Cell(Paragraph(u"Цена в руб."))
    table.append(c1, c2, c3, c4)
    return table

def write1(data):
    doc = Document()
    ss = doc.StyleSheet
    section = Section()
    doc.Sections.append(section)

    p = Paragraph(ss.ParagraphStyles.Heading2)
    p.append(u"Отчет о продукции интернет-магазина Озон по выборке «"+data[0]['mainCategory']+"»")
    section.append(p)

    p = Paragraph(ss.ParagraphStyles.Normal)
    p.append(u"В категории {0} на стр. {1} по запросу: {2}".format(data[0]['mainCategory'], data[0]['page'], data[0]['request']))
    section.append(p)

    products = data[len(data) - 1]
    counter = 1

    table = createTable()

    for product in products:
        c1 = Cell(Paragraph(product['name']))
        c2 = Cell(Paragraph(product['id']))
        image = Image(product['img'])
        c3 = Cell(Paragraph(image))
        c4 = Cell(Paragraph(product['price']))
        if(counter < 6):
            table.append(c1, c2, c3, c4)
            counter += 1
        else:
            table.append(c1, c2, c3, c4)
            section.append(table)
            p = Paragraph(ss.ParagraphStyles.Normal)
            p.append(u"Товаров на странице {0}. Страница ".format(counter), PAGE_NUMBER)
           # section.append(p)
            section.Footer.append(p)
            section = Section()
            doc.Sections.append(section)
            p = Paragraph(ParagraphPropertySet().SetPageBreakBefore(True))
            p.append('')
            section.append(p)
            counter = 1
            table = createTable()

    if counter != 1:
        section.append(table)
        p = Paragraph(ss.ParagraphStyles.Normal)
        p.append(u"Товаров на странице {0}. Страница ".format(counter-1), PAGE_NUMBER)
        section.Footer.append(p)
        section = Section()
        doc.Sections.append(section)
        p = Paragraph(ParagraphPropertySet().SetPageBreakBefore(True))
        p.append('')
        section.append(p)

    with open(u"{0}.rtf".format(data[0]['mainCategory']), "w") as f:
        DR = Renderer()
        DR.Write(doc, f)

