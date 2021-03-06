#!/usr/bin/python
# -*- coding: utf-8 -*-

# DEV: Jordi Masip

from utiles import *
import tranf, imgio

def mirror_effect(img):
	"""
	Retorna la imatge girada 180º sobre l'eix Y
	>>> mirror_effect([[255,255,255, 0],[0,255,255, 255]])
	[[0, 255, 255, 255], [255, 255, 255, 0]]
	"""
	return [row[::-1] for row in img]

def transpose(img):
	"""
	Retorna una matriu amb les files com a columnes i les columnes com a files
	>>> transpose([[255,255,255, 255],[255,255,255, 255],[255,255,255, 255],[0,255,255, 255]])
	[[255,255,255,0],[255,255,255,255],[255,255,255,255],[255,255,255,255]]
	"""
	if len(img) == 0:
		return [[]]
	# Crea tantes files a "transposed_img" com columnes hi ha a "img":
	transposed_img = [[] for x in range(len(img[0]))]

	for row in img:
		i = 0
		for column in row:
			transposed_img[i] += [column]
			i += 1

	return transposed_img

def image_slice_vertical(image, f, to):
	"""
	Retorna la imatge entre la columna de la posició "f" fins la posició "to" (exclosa)
	>>> image_slice_vertical([[0,0,0], [0,0,0], [255,255,255]], 1,2)
	[[0], [0], [255]]
	"""
	if not isinstance(image[0], list):
		image = [image]
	return [row[f:to] for row in image]

def image_slice_horizontal(image, f, to):
	"""
	Retorna la imatge entre la fila de la posició "f" fins la posició "to" (exclosa)
	>>> image_slice_horizontal([[0,0,0], [0,0,0], [255,255,255]], 1,2)
	[[0], [0], [255]]
	"""
	#imgio.show(("1", image))
	a = transpose([row[f:to] for row in transpose(image)])
	#imgio.show(("1",a))
	return a

def getPositionOfFirstRowOfColor(color, img):
	"""
	Retorna la posició de la primera fila de la imatge que és tota del color "color"
	>>> getPositionOfFirstRowOfColor(0, [[255,255,255, 255],[255,255,255, 255],[255,255,255, 255],[0,255,255, 255]])
	-1
	>>> getPositionOfFirstRowOfColor(255, [[255,255,255, 255],[255,255,255, 255],[255,255,255, 255],[0,255,255, 255]])
	0
	>>> getPositionOfFirstRowOfColor(255, [[0,255,255, 255],[255,255,255, 255],[255,255,255, 255],[0,255,255, 255]])
	1
	"""
	position = 0
	for row in img:
		all_the_same = True
		for pixel in row:
			if pixel != color:
				all_the_same = False
				break
		if all_the_same:
			return position
		position += 1
	return -1

def getPositionOfFirstColumnOfColor(color, img):
	"""
	Retorna la posició de la primera columna de la imatge que és tota del color "color"
	>>> getPositionOfFirstColumnOfColor(0, [[255,255,255, 255],[255,255,255, 255],[255,255,255, 255],[0,255,255, 255]])
	-1
	>>> getPositionOfFirstColumnOfColor(0, [[255,0,255, 255],[255,0,255, 255],[0,0,0,0],[0,0,255, 255]])
	1
	"""
	return getPositionOfFirstRowOfColor(color, transpose(img))

def getPositionOfFirstRowOfColorDiff(color, img, exhaustive=False):
	"""
	Retorna la posició de la primera fila de la imatge on algun dels valors es diferent de "color"
	>>> getPositionOfFirstRowOfColorDiff(0, [[0,0,0,0], [255,255,255,255],[255,255,255,255],[0,255,255, 255],[0,0,0,0]])
	1
	>>> getPositionOfFirstRowOfColorDiff(0, [[0,0,0,0], [0,255,255,255],[255,255,255,255],[0,255,255, 255],[0,0,0,0]])
	2
	"""
	position = 0
	for row in img:
		all_the_same = True
		for pixel in row:
			if pixel != color:
				if exhaustive:
					all_the_same *= True
				else:
					all_the_same = False
					break
		if not all_the_same:
			return position
		position += 1
	return -1

def getPositionOfFirstColumnOfColorDiff(color, img, exhaustive=False):
	"""
	Retorna la posició de la primera columna de la imatge on algun dels valors es diferent de "color"
	>>> getPositionOfFirstColumnOfColorDiff(0, [[0,0,255,0], [255,255,255,255],[255,255,255,255],[0,255,255, 255],[0,0,255,0]])
	2
	"""
	return getPositionOfFirstRowOfColorDiff(color, transpose(img), exhaustive)

def vtrim(img):
	"""
	Retalla tot el color blanc que hi ha a l'esquerra i a la dreta de la imatge abans de trobar-se un caràcter
	>>> vtrim([[255,255,0],[255,0,0]])
	[[255, 0], [0, 0]]
	>>> vtrim([[255,255,0,255],[255,255,0,255], [0, 255, 0,255]])
	[[255,255,0],[255,255,0], [0, 255, 0]]
	>>> vtrim([[255, 255, 0, 255]])
	[[0]]
	"""
	#imgio.show(("1", img))
	#debug("vtrim: " + str(img))
	position = getPositionOfFirstColumnOfColorDiff(255, img)
	#debug("Position 1: " + str(position))
	img = image_slice_vertical(img, position, len(img[0]))
	#print "first slice", img
	img = mirror_effect(img)
	#imgio.show(("1", img))
	#print "Mirroed", img
	position = getPositionOfFirstColumnOfColorDiff(255, img)
	#debug("Position 2: " + str(position))
	if position == -1:
		position = len(img[0])
	#debug("Slice " + "0:" + str(position))
	#print "slice_[[:", mirror_effect(img)
	img = image_slice_vertical(img, position, len(img[0]))
	#imgio.show(("1", img))
	img = mirror_effect(img)
	#imgio.show(("1", img))
	return img

def htrim(img):
	"""
	Retalla tot el color blanc que hi ha a dalt i abaix de la imatge abans de trobar-se un caràcter
	>>> htrim([[255,255,255],[255,0,0]])
	[[255, 0, 0]]
	>>> htrim([[255,255,255],[255,255,255],[255,255,255],[255,0,0], [255,255,255], [255,255,255]])
	[[255, 0, 0]]
	"""
	#imgio.show(("1", img))
	#debug("htrim: " + str(img))
	position = getPositionOfFirstRowOfColorDiff(255, img)
	#debug("Position 1: " + str(position))
	img = image_slice_horizontal(img, position, len(img))[::-1]
	#imgio.show(("1", img))
	position = getPositionOfFirstRowOfColorDiff(255, img)#, True)
	#debug("Position 2: " + str(position))
	if position == -1:
		position = len(img)
	#print "Mirror effect", img[::-1]
	#print "slice", 0, ":", position
	img = image_slice_horizontal(img, position, len(img))[::-1]
	#imgio.show(("1", img))
	#print "htim_rinal", img
	return img

def split_digit(img):
	"""
	Aquesta funció rebrà una imatge img en blanc i negre retallada verticalment i retorna una tupla (D,R) en la que D és una
	imatge amb el dígit de més a l’esquerra i R és la resta de la imatge. La imatge corresponent al dígit extret D es retorna
	convenientment retallada en la direcció horitzontal. La resta R esdevé una imatge nul.la quan s’han extret tots els dígits.
	>>> split_digit([[255,255,255,255], [255,255,0,255], [255,255,255,255], [255,255,0,255], [255,255,255,255]])
	([[0], [255], [0]], [])
	"""
	# S'escapça la imatge
	img = htrim(img)
	#print "htrim - ", img
	img = vtrim(img)

	# S'obté la posició de la primera columna on tot és blanc (aquesta serà la cordenada on acaba el primer caràcter)
	pos_end_first_char = getPositionOfFirstColumnOfColor(WHITE, img)
	#print "pos_end_first_char", pos_end_first_char

	if pos_end_first_char == -1: # Només hi ha un caràcter
		return (img, [])

	# Es fa un slice del primer caràcter, des de 0->pos_end_first_char
	img_char = image_slice_vertical(img, 0, pos_end_first_char)
	
	# Es fa un slice de la resta de caràcters des de pos_end_first_char->final
	img_restant = image_slice_vertical(img, pos_end_first_char, len(img[0]))
	
	# Es retorna una tupla (img_char, img_restant)
	return (img_char, img_restant) # vtrim(
