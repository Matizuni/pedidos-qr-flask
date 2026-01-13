import qrcode

url = "http://127.0.0.1:5000"
img = qrcode.make(url)
img.save("qr_menu.png")

print("QR generado")

