#!/usr/bin/python
# -*- coding: utf-8 -*-

# DEV: Jordi Masip

import imgio, img, tranf
from utiles import *

def compare_image(img, pttrn):
	"""
	Retorna un real entre 0-1 amb el nivell de coincidència de la imatge amb el patró
	"""	
	total_pixels, coincidence = 0, 0

	for i in range(len(img)):
		for j in range(len(img[i])):
			if img[i][j] == pttrn[i][j]:
				coincidence += 1
	return coincidence / total_pixels

def image_slice_with(image, f, to):
	"""
	Retorna la imatge
	"""
	sliced_image = []
	for row in image:
		sliced_image += row[f:to+1]
	return sliced_image

def load_patterns(prefix):
	"""
	Retorna una llista de tuples on el primer element és el valor que representa el patró i el segon valor és el patró
	"""
	return [(num, imgio.read_bn(str(prefix) + "_" + str(num) + ".jpeg")) for num in [4]] # range(10)

def match(img, patlst):
	"""
	Retorna un número enter entre el 0-9 per indicar la matrícula o -1 si cap dels patros concorda més de 0.5 amb la matrícula
	"""
	# Mida de la imatge
	img_size = (get_w(img), get_h(img))

	# ((int) valor de la imatge, (float) coincidence)
	best_match = (-1, 0.0)

	# Es compara cada pattern:
	for i, pattern in enumerate(patlst):
		# S'escala el patró a la mida del caràcter
		pattern = scale(pattern, img_size[1])

		# Es desa la nova mida
		patter_size = (get_w(pattern), get_h(pattern))

		for position in range(img_size[0] - patter_size[0] + 1):
			coincidence = compare_image(image_slice_with(img, position, img_size[0]), pattern)
			if coincidence >= best_match[1]:
				best_match = (i, coincidence)
	debug("El best_match es " + str(best_match))
	return best_match[0] if best_match[1] >= 0.5 else -1
