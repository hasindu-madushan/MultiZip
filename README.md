# MultiZip

## Introduction
MultiZip is a module to extract zip files with multiple parts in a python code. It uses zlib library. However, Multizip does not support encrypted zip files yet but I am working on it too. 

## Requirements 
* python 3 or later
* zlib 
* ZipFile

## Usage
Usage of Multizip is very easy
* step 1: Import MultiZip
	import multizip

* step 2: create Multizip object. Give the path to your zip files as the argument.
	mz = multizip.Multizip("my zip file.zip")

* step 3: extract 
	mz.etract("a file inside the zip.txt")

