import qrcode

url = "https://pedidos-qr-flask.onrender.com"  # URL público de tu app
img = qrcode.make(url)
img.save("static/qr_menu.png")  # guarda el QR

print("QR generado")

