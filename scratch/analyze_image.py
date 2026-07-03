from PIL import Image
try:
    img = Image.open(r"c:\Users\Admin\sim_magang_portofolio\theme\static\images\logo_diskominfo-kab-bekasi.png")
    print("Format:", img.format)
    print("Size:", img.size)
    print("Mode:", img.mode)
except Exception as e:
    print("Error:", e)
