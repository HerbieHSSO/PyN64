from io import BytesIO



def analysis(value):
    value = hex(value)

    val = str(value).replace('0x','')
    if len(val) == 1:
        value = f'0x0{val}'
    return str(value).replace('0x', '')




class ROM:

    def __init__(self, data, ram):
        self._data = data

        self._ram = ram

    
    def getImageName(self):
        data = self._data
        return f'{chr(data[0x0020])}{chr(data[0x0021])}{chr(data[0x0022])}{chr(data[0x0023])}{chr(data[0x0024])}{chr(data[0x0025])}{chr(data[0x0026])}{chr(data[0x0027])}{chr(data[0x0028])}{chr(data[0x0029])}{chr(data[0x002a])}{chr(data[0x002b])}{chr(data[0x002c])}{chr(data[0x002d])}{chr(data[0x002e])}{chr(data[0x002f])}{chr(data[0x0030])}{chr(data[0x0031])}{chr(data[0x0033])}{chr(data[0x0032])}'
    def getCountry(self):
        data = self._data
        country_code = chr(data[0x003E])

        if country_code == 'D':
            country = 'Germany'
        if country_code == 'E':
            country = 'USA'
        if country_code == 'J':
            country = 'Japan'
        if country_code == 'P':
            country = 'Europe'
        if country_code == 'U':
            country = 'Australia'
        return country

    def getEntryPoint(self):
        return int(f'0x{analysis(self._data[0x08])}{analysis(self._data[0x09])}{analysis(self._data[0xA])}{analysis(self._data[0xB])}', 16)
    
    def read(self, address):

 
        value = self._data[address]
        
        return value
 
    def write(self, address, value):
        data = self._data
        data[address] = value
        return data[address]



















