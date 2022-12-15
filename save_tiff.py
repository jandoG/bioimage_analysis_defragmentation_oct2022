# ============================================= README ======================================================
#
# Author: Gayathri Nadar, Cellular Imaging Facility, FMP Berlin, nadar@fmp-berlin.de
#	
#	This script converts images in a folder into TIFF files and saves them. The channels are split and saved separately. 
#    
# Usage:
#	Arrange your data into a folder.
# 	Open this script with FIJI and click run.
# 	A window will pop-up, enter the necessary values and click ok to run the script.
#
# Results:
# 	tiff files are stored in a folder called "TIFF_Files" inside the image folder specified.
#
# ====================================================================================================================


#@ File (label= "Specify the folder containing images", style= "directory") processpath
#@ String (label= "File extension", choices = {".czi", ".tiff", ".TIF", ".tif"}, default= ".czi") file_extension

from ij import IJ
from ij import Prefs
from ij.io import FileSaver
from ij.io import Opener
from ij import ImagePlus
from ij import ImageStack
from ij.plugin import Duplicator, ChannelSplitter
from loci.plugins import BF
from loci.formats import ImageReader, FilePattern
from loci.formats import MetadataTools
from loci.plugins.prefs import OptionsList
from loci.plugins.in import ImporterOptions
import os, math, re, sys
import fnmatch as fnm
from os.path import isfile, join
from os import listdir 
import glob

def main():
	# get folder containing images 
	process_dir = processpath.getPath()
	
	# create folder to save output 
	results_path = join(process_dir, 'TIFF_Files')
	if not os.path.exists(results_path):
		os.makedirs(results_path)
		
	files = getFilesFromDir(process_dir, extension=file_extension)
	
	for i, f in enumerate(files):
	
		print "Processing file " + str(i + 1) + "/" + str(len(files))
		
		# open image and get name
		imp = openImageWithBF(f, virtual= True, groupfiles = False, seriesdata = False, openseries = 1)
		fname = os.path.splitext(os.path.basename(f))[0]
		
		# make pretty 
		makePretty(imp)
		
		print "Processing file =", fname 
		
		# split channels and save 
		imps = ChannelSplitter().split(imp)
		no_channels = len(imps)
		
		for c in range(no_channels):
			impname = "C" + str(c+1) + "_" + fname + ".tif"
			
			image_to_save = imps[c]
			
			print "Saving file.."
			
			FileSaver(image_to_save).saveAsTiff(join(results_path, impname))
		














#======================================================= helper ===============================================



def getFilesFromDir(path, extension=None):
	"""
	Function to get list of files in a directory.
	params:
	path: str data dir path
	extension: str file extension for e.g. '.tif', '.lsm'
	
	Returns: 
	filelist: list of files with entire path 
	"""
	if extension is None:
		filelist = [join(path,f) for f in sorted(listdir(path)) if isfile(join(path, f))]
	else:
		filelist = [join(path,f) for f in sorted(listdir(path)) if isfile(join(path, f)) and f.endswith(extension)]

	return filelist


def makePretty(imp):
	"""
	Improve display of imp. 
	"""
	ch = imp.getNChannels();
	slices = imp.getNSlices();
	
	if slices//2 == 0:
		z = int(slices/2)
	else:
		z = int(slices/2) + 1
	
	for c in range(1, ch + 1):
		imp.setPosition(c, z, 1);
		IJ.run(imp, "Enhance Contrast", "saturated=0.35");
		
	imp.setC(1)


def openImageWithBF(path, virtual= True, groupfiles = False, seriesdata = True, openseries = 1):
	"""
	set options to open image using bio-formats- use virtual for quick loading
	params:
	path to file 
	virtual: bool set True to load image as virtual stack (for big data)
	groupfiles: bool set True to load images from folder having similar name pattern (stored in the metadata of first image)
	seriesdata: bool set True if image contains series 
	openseries: int series ID no to be opened 
	returns: 
	imp: ImagePlus 
	"""
	options = ImporterOptions()
	options.setColorMode(ImporterOptions.COLOR_MODE_DEFAULT)
	options.setAutoscale(True)
	options.setStackFormat("Hyperstack")
	options.setVirtual(virtual)
	options.setGroupFiles(groupfiles) 
	
	if seriesdata: 
		reader = ImageReader()
		reader.setId(path)
		seriesCount = reader.getSeriesCount()
		reader.close()
		print "Found series data. Image series count =", seriesCount
		print "Reading series ID ", openseries, "\n"
		options.setOpenAllSeries(True)

	options.setId(path)
	allimps = BF.openImagePlus(options)

	if seriesdata:
		imp = allimps[openseries - 1]

	else:
		imp = allimps[0]
	
	return imp
	
def cleanstart():
	"""
	Clean start to set options for black background and clear log, close all open images.
	"""
	IJ.run("Options...", "iterations=1 count=1 black pad");
	Prefs.setBlackBackground=True
	Prefs.padEdges=True
	IJ.setBackgroundColor(0,0,0) 
	IJ.run("Close All", ""); 
	
	
main()
print "Done"