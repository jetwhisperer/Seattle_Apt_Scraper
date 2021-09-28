import datetime


# TODO: This will add the data to a database, but for now, it just prints it out
def add_to_db(complex: str, apt_num: str, bed: int, bath: int, sqft: int, rent: int, floor: int, available,
              urban=False, apt_model='', on_sale=False, sale_expire='', reg_price=None, on_special=False,
              special_details=''):
    message = f'Added to {complex}: Apt {apt_num}. Floor {floor},'
    message += f' urban' if urban else ''
    message += f' {bed}Br/{bath}ba, {sqft} sqft, ${rent}, available {available}'
    message += f', apt model: {apt_model}' if apt_model else ''
    message += f'. On Sale!' if on_sale else ''
    message += f' Regular price: ${reg_price}' if reg_price else ''
    message += f' Special deal: {special_details}. Special expires {sale_expire}' if on_special else ''
    message += f'. Date added: {datetime.date.today()}'
    print(message)
