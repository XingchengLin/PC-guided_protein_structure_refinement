######################################################################################
# This script will help delete the last frame in each file being concatenated into the
# whole trajectory file. This last frame is recorded in the checkpoint file and usually
# not useful, and will be annoying in comparing them with energy file;
#
# Written by Xingcheng Lin, 05/12/3014;
#######################################################################################

################################################
def my_range(start, end, step):
    while start <= end:
        yield start
        start += step
###########################################

infile = open("rmsd-anstrom.xvg", 'r');
outfile = open("rmsd-anstrom-good.xvg", 'w');

# Read in lines from the qvalue file;

lines = [line.strip() for line in infile];
infile.close();

length = len(lines);

# We needn't check the first line, so start from 1 instead of 0;
# And we need to output the first line into the file firstly;
outfile.write(lines[0] + "\n");

line = lines[0].split();
# Variable recording the time step value of the previous frame;
last = float(line[0]);

# The interval of recording in the targeted file
interval = 100.0;

for i in my_range(1, length-1, 1):

	line = lines[i].split();

	# If the time recorded at this frame is not "interval" pico-second after that of the 
	# previous frame, we will not output this line into the good file;
	timeStep = float(line[0]);
	if timeStep == last + interval:
		outfile.write(lines[i] + "\n");
		# Update the variable;
		last = timeStep;

outfile.close();

