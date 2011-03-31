import django_tables as tables
from django.template.loader import render_to_string
from django.conf import settings
import inspect
class SarpamTable(tables.MemoryTable):
    def abstract(self):
        caller = inspect.getouterframes(inspect.currentframe())[1][3]
        raise NotImplementedError(caller + ' must be implemented in subclass')
    
    NO_DATA = "--"
    
    def round_to_set_decimal_places(self, row, column):
        value = row[column]
                    
        if value is None:
            value = self.NO_DATA
        else:
            value = round(float(value), settings.SARPAM_NUMBER_ROUNDING)
         
        row[column] = value

    def as_html(self):
        extra_context = {
            'sarpam_number_format':settings.SARPAM_NUMBER_FORMAT,
            'sarpam_number_rounding':settings.SARPAM_NUMBER_ROUNDING,
            'sarpam_currency_code':settings.SARPAM_CURRENCY_CODE,
            'table':self
        }
        return render_to_string('table.html', extra_context)

    def get_rows_template(self):
        self.abstract()
