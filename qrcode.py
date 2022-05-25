from pyzbar.pyzbar import decode
from PIL import Image
import scrapper


def scanner(path):
    d = decode(Image.open(path))
    if(d != []):
        return d[0].data.decode()
    else:
        return false
