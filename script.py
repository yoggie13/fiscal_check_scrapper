from cv2 import scaleAdd
import qrcode
import scrapper

arr = ["IMG_O152.JPEG"]

for a in arr:
    result = qrcode.scanner(a)
    if(result != false):
        fiscal = scrapper.scrape_web_page(result)
        if(fiscal != false):
            print(fiscal)
        else:
            print("Scrape error")
    else:
        print("QR Code error")
