import StringIO
class PricePopup(object):
    def __init__(self, price_fields):
        self.price_fields = price_fields
        
    def as_html(self):
        fields = {'issue_unit' : "Issue Unit",
                  'incoterm' : "Incoterm",
                  'supplier' : "Supplier",
                  'supplier_country' : "Supplier Country",
                  'manufacture_country' : "Country of Manufacture",
                  'volume' : "Volume"}
                
        output = StringIO.StringIO()
        output.write("<dl>")
        
        for field_name in fields:
            field_title = fields[field_name]
            field_value = self.price_fields[field_name] or "N/A"
            output.write("<dt>%s</dt><dd>%s</dd>" % (field_title, field_value))
        
        output.write("</dl>")
        
        html = output.getvalue()
        output.close()

        return html

