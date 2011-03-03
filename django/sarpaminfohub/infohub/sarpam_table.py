import django_tables as tables
class SarpamTable(tables.MemoryTable):
    NO_DATA = "--"
    
    def round_to_three_decimal_places(self, row, column):
        value = row[column]
                    
        if value is None:
            value = self.NO_DATA
        else:
            value = round(float(value), 3)
         
        row[column] = value
