from textwrap import wrap
from PIL import Image, ImageDraw
from math import sqrt, ceil
import binascii


def code(st: str):
	letter_list = [format(ord(x), 'b').rjust(7, '0') for x in st]
	line = "".join(letter_list)
	return line


def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
	n = int(bits, 2)
	return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def decode(line: str):
	line = wrap(line, 7)
	res = ''
	for letter in line:
		if '1' in letter:
			res += text_from_bits(letter)
	return res


def create_img(line):
	size = ceil(sqrt(len(line)))
	img = Image.new(mode='1', size=(size, size), color=(1,))
	linegen = (letter for letter in line)
	
	for i in range(size):
		for j in range(size):
			try:
				if next(linegen) == '1':
					img.putpixel((j, i), (0,))
			except StopIteration:
				img.putpixel((j, i), (1,))
	
	img = apply_mask(img, size)
	return img


def apply_mask(img: Image, size: int):
	flag = True
	for i in range(size):
		for j in range(size):
			if flag:
				img.putpixel((j, i), (1 - img.getpixel((j, i))))
				flag = False
			else:
				flag = True
	return img


def remove_mask(line):
	newline = ''
	flag = True
	for letter in line:
		if flag:
			newline += f'{1 - int(letter)}'
			flag = False
		else:
			newline += letter
			flag = True
	return newline


def read_img(path: str):
	img = Image.open('qr.png', mode='r')
	size = img.size[0]
	line = ''
	for i in range(size):
		for j in range(size):
			px = img.getpixel((j, i))
			
			if px == 255:
				line += '0'
			else:
				line += '1'
	line = remove_mask(line)
	return line


if __name__ == '__main__':
	line = input('Введите текст >>> ')
	line = code(line)
	img = create_img(line)
	img.save('qr.png')
	print('QR-код создан')
	line = read_img('qr.png')
	result = decode(line)
	print(result)
