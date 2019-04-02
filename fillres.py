from modeller import *
from modeller.automodel import *    # Load the automodel class
import sys
import time

alnfileName = sys.argv[1]
knownsName = sys.argv[2]
sequenceName = sys.argv[3]


log.verbose()
env = environ()

# directories for input atom files
env.io.atom_files_directory = ['.', '../atom_files']

a = automodel(env, alnfile=alnfileName,
              knowns=knownsName, sequence=sequenceName)
a.starting_model = 1
a.ending_model = 1

#a.loop.starting_model = 1
#a.loop.ending_model   = 2
#a.loop.md_level       = refine.fast

a.make()
