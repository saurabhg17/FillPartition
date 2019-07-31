"""Fill free space in a partition with files containing zero bytes.

The purpose of this script is to allow the user to fill the entire 
free space in the specified partition with files containing zero bytes
as a safety measure before discarding a hard drive.

The script has one mandatory argument (the path of the partition) and
one optional argument (--outputDir, -od) the directory where files 
should be written. If the optional argument is not specified, it is
set to the partition path.

Examples:
python FillPartition.py -od C:\\Users\\USER_NAME\\ C:
python FillPartition.py -od /home/USER_NAME /

Note that the output directory should have write permission for the 
current user, otherwise the script will fail. 
"""

import argparse, os, random, shutil
from timeit import default_timer as __timer


__author__    = "Saurabh Garg"
__copyright__ = "Copyright 2019, Saurabh Garg"
__license__   = "MIT"
__version__   = "1.0"
__email__     = "saurabhgarg@mysoc.net"


__NUM_ITERS   = 1024
__BUFFER_SIZE = 1024 * 1024
__DATA        = None

def fillPartition():
	parser = argparse.ArgumentParser(description="Fill free space in a partition with files containing zero bytes.")
	parser.add_argument("partition"         , type=str, help="The partition to be filled, for example C:\\, /dev/hda1")
	parser.add_argument("--outputDir", "-od", type=str, help="Save generated files in this folder.", default="")
	args = parser.parse_args()
	
	if args.outputDir is "":
		args.outputDir = args.partition
	else:
		args.outputDir = os.path.normpath(args.outputDir)
	
	# Print partition statistics.
	usage = shutil.disk_usage(args.partition)
	total = usage[0] / (1024 * 1024 * 1024)
	used  = usage[1] / (1024 * 1024 * 1024)
	free  = usage[2] / (1024 * 1024 * 1024)
	
	print("")	
	print("Partition statistics:")
	print("Total size of the partition      : {:7.2f} GB".format(total))
	print("Used size of the partition       : {:7.2f} GB".format(used))
	print("Free space available in partition: {:7.2f} GB".format(free))
	print("")
	
	if usage[2] == 0:
		print("Available free space is already 0.")
		return
	
	# Initialize DATA of size 1GB with all zeros.
	global __DATA
	if free > 1:
		__DATA = bytearray(__BUFFER_SIZE)
	end = __timer()
	
	# Fill partition with 1GB files until free space is less than 1GB.
	num1GBFiles = int(free)
	if num1GBFiles > 0:
		print("Writing {} 1GB files".format(num1GBFiles))
		for i in range(num1GBFiles):
			__write1GBFile(args.outputDir)
		print("Finihsed writing 1GB files.")
		print("")
	
	# Fill remaining free space in the partition with a single file.
	usage = shutil.disk_usage(args.partition)
	free  = usage[2]
	if free > 0:
		print("Free space left {} bytes.".format(free))
		print("Writing last {} bytes file.".format(free))
		__writeFile(args.outputDir, free)
	
	print("")
	print("Free disk space is now 0 bytes.")


def __generateFileName(outputDir):
	return os.path.join(outputDir, "{:.0f}".format(random.uniform(1000000, 9999999)))


def __write1GBFile(outputDir):
	start = __timer()
	
	fileName = __generateFileName(outputDir)
	print("Writing {}...".format(fileName), end="")
	
	with open(fileName, 'w+b') as file:
		for i in range(0, __NUM_ITERS):
			file.write(__DATA)
	
	end = __timer()
	print("  took {:.3f} seconds.".format(end - start))
	

def __writeFile(outputDir, fileLength):
	start = __timer()
	
	fileName = __generateFileName(outputDir)
	print("Writing {}...".format(fileName), end="")
	
	try:
		with open(fileName, 'w+b') as file:
			numIters = int(fileLength/__BUFFER_SIZE)
			for i in range(0, numIters):
				file.write(__DATA)
			file.write(bytearray(fileLength - numIters*__BUFFER_SIZE))
	except Exception as e:
		doNothing = 0
	
	end = __timer()
	print("  took {:.3f} seconds.".format(end - start))
	

if __name__ == '__main__':
    fillPartition()
