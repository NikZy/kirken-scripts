from PIL import Image, ImageDraw, ImageFont
img = Image.open("MAL.jpg")
fontzise = 40

font = ImageFont.truetype("Lato-Reg.ttf", fontzise)


draw = Image.Draw(image)

draw.text((10, 0 ), txt, (0,0,0), font=font)

img_resized = image.resize((188, 40), Image.ANTIALIAS)

del draw

# write to stdout
img.save("D:\Sindre\Dokumenter\Programmering\Python\Image bot\stdout.png", "PNG")
