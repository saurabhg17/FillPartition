# Fill Partition
Fill free space in a partition with files containing zero bytes.

The purpose of this script is to allow the user to fill the entire 
free space in the specified partition with files containing zero bytes
as a safety measure before discarding a hard drive.

The script has one mandatory argument (the path of the partition) and
one optional argument (--outputDir, -od) the directory where files 
should be written. If the optional argument is not specified, it is
set to the partition path.

Examples:

python FillPartition.py -od C:\Users\USER_NAME\ C:

python FillPartition.py -od /home/USER_NAME /

Note that the output directory should have write permission for the 
current user, otherwise the script will fail.
