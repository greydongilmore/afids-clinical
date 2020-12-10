# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import subprocess
import numpy as np
import pandas as pd
import argparse
import os.path

###############################################################################
# functions
###############################################################################
def convertSlicerRASFCSVtoAntsLPSCSV( input_fcsv, output_csv ):
    # convert Slicer RAS oriented FCSV (default) to Ants LPS oriented format (expected orientation)
    # use with CAUTION: orientation flips here

    df = pd.read_csv( input_fcsv, skiprows=2, usecols=['x','y','z'] ) # first 2 rows of fcsv not necessary for header
    df['x'] = -1 * df['x'] # flip orientation in x
    df['y'] = -1 * df['y'] # flip orientation in y
    df.to_csv( output_csv, index=False )

def convertAntsLPSCSVtoSlicerRASFCSV( input_csv, output_fcsv, ref_fcsv ):
    # convert Ants LPS oriented format (ants expected orientation) to Slicer RAS oriented FCSV (for viewing in Slicer)
    # use with CAUTION: orientation flips here

    # extract Slicer header
    f = open( ref_fcsv, 'r' )
    lines = f.readlines()
    f.close()

    # orienting the image image back to RAS from LPS
    input_df = pd.read_csv( input_csv, usecols=['x','y','z'] ) # use reference fcsv as template
    df = pd.read_csv( ref_fcsv, skiprows=2 ) # use reference fcsv as template
    df['x'] = -1 * input_df['x'] # flip orientation in x
    df['y'] = -1 * input_df['y'] # flip orientation in y
    df['z'] = input_df['z'] # normal orientation in z
    df.to_csv( output_fcsv, index=False )

    # add in extracted Slicer header
    with open( output_fcsv, 'r+' ) as f:
        old = f.read() # read all the old csv file info
        f.seek(0) # rewind, start at the top
        f.write( lines[0] + lines[1] + old ) # add expected Slicer header

def run_command(cmdLineArguments):
    process = subprocess.Popen(cmdLineArguments, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
    stdout = process.communicate()[0]
    p_status = process.wait()

###############################################################################
# command-line arguments with flags
###############################################################################
parser = argparse.ArgumentParser(description="Apply ants transform to Slicer FCSV format file.")
# TODO: handling of concatenated transforms (multi-level)
parser.add_argument("-i", "--input-fcsv", dest="inputfcsv", help="Input Slicer FCSV File (RAS-oriented)")
parser.add_argument("-o", "--output-fcsv", dest="outputfcsv", help="Output Slicer FCSV File (RAS-oriented)")
parser.add_argument("-a", "--affine", dest="affine", help="Affine Transform: Source-to-Reference (Ants .mat format)")
parser.add_argument("-d", "--displace", dest="displace", help="Affine Transform: Source-to-Reference (Ants .mat format)")

args = parser.parse_args()

# for debugging input
# print( "InputFCSV {} OutputFCSV {} Affine {} ".format(
#         args.inputfcsv,
#         args.outputfcsv,
#         args.affine,
#         ))

###############################################################################
# initialize variables
###############################################################################
# input variables
input_landmarks_fcsv = args.inputfcsv
input_GenericAffine = args.affine

# output variables
output_fcsv = args.outputfcsv

# temporary variables
working_path = os.path.dirname(output_fcsv) + "/" # put temp files where output is
tmp_slicer_to_ants_csv = working_path + "tmp_slicer_to_ants.csv"
tmp_slicer_to_ants_transformed_csv = working_path + "tmp_slicer_to_ants_transformed.csv"

###############################################################################
# main
###############################################################################
def main():
    # 1. convert fcsv to antsApplyTransformsToPoints compatible csv and from RAS to LPS csv
    convertSlicerRASFCSVtoAntsLPSCSV( input_landmarks_fcsv, tmp_slicer_to_ants_csv )

    # 2. run antsApplyTransformsToPoints on output from #2
        # TODO: handle exceptions

    cmd = ' '.join(['/opt/ANTs/bin/antsApplyTransformsToPoints',
                            '-d', str(3),
                            '-i', '"'+tmp_slicer_to_ants_csv+'"',
                            '-o', '"'+tmp_slicer_to_ants_transformed_csv+'"',
                            '-t', ''.join(['"[', '"', input_GenericAffine, '"', ",", str(1), ']"']),
                            '-t', args.displace])

    run_command(cmd)

    # 3. convert from LPS back to RAS; and csv back to fcsv
    convertAntsLPSCSVtoSlicerRASFCSV( tmp_slicer_to_ants_transformed_csv, output_fcsv, input_landmarks_fcsv )

###############################################################################
if __name__ == "__main__":
    main()
