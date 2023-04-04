import numpy as np
from PIL import Image

def encode(img_path, data_path, out_path):
	img = Image.open(img_path).convert("RGB")
	data = open(data_path, "rb").read()
	data_len = len(data)
	data_nbits = 8*data_len

	height, width = img.size
	max_bits = 3 * height * width - 32

	if data_nbits > max_bits:	
		print("can only encode max", max_bits, "bits")
		print("data contains", data_nbits, "bits")
		return 0

	data_len_bytes = data_len.to_bytes(4, byteorder="little", signed=False)
	
	data_bytes = data_len_bytes + data

	data_bits = [int(i) for i in "".join([f'{a:b}'.zfill(8) for a in data_bytes])]

	for i in range(3-len(data_bits)%3):
		data_bits.append(0)

	k = 0
	
	def bitencode(even, value):
		if even:
			if value % 2 == 0: return value
			else:              return value+1
		else:
			if value % 2 == 0: return value+1
			else:              return value
	
	for w in range(width):
		for h in range(height):
			b0, b1, b2 = tuple(data_bits[k:k+3])
			r, g, b = img.getpixel((h, w))

			r = bitencode(b0, r)
			g = bitencode(b1, g)
			b = bitencode(b2, b)
			
			img.putpixel((h, w), (r, g, b))
			
			if k < len(data_bits)-3:
				k += 3
			else:
				break
		
		if k >= len(data_bits)-3: break

	img.save(out_path)

def decode(img_path, out_path):
	img = Image.open(img_path).convert("RGB")
	height, width = img.size
	
	def bits2bytes(bits):
		return bytes([int("".join(map(str, bits[i:i+8])), 2) for i in range(0, len(bits), 8)])

	def bitdecode(value):
		if value % 2 == 0: return 1
		else:              return 0
	
	def readnbits(n):	
		bits = []
		k = 0
		for w in range(width):
			for h in range(height):
				r, g, b = img.getpixel((h, w))	
				bits.append(bitdecode(r))
				bits.append(bitdecode(g))
				bits.append(bitdecode(b))
				if k > n-3: break
				else: k += 3
			if k > n-3: break
		return bits
	
	bits = readnbits(32)
	data_nbytes = int.from_bytes(bits2bytes(bits[0:31]), "little", signed=False)
	data_nbits = 32+8*data_nbytes
	bits = readnbits(data_nbits)[32:32+8*data_nbytes]
	data = bits2bytes(bits)
	open(out_path, "wb").write(data)
	
	
encode("test.jpg", "data.txt", "out.bmp")
decode("out.bmp", "decoded.txt")
