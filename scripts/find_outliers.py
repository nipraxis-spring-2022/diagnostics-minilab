""" Python script to find outliers

Run as:

    python3 scripts/find_outliers.py data
"""

import os.path as op
import sys

from argparse import ArgumentParser, RawDescriptionHelpFormatter

# Put the findoutlie directory on the Python path.
PACKAGE_DIR = op.join(op.dirname(__file__), '..')
sys.path.append(PACKAGE_DIR)

from findoutlie import outfind


def print_outliers(data_directory, **kwargs):
    outlier_dict = outfind.find_outliers(data_directory, **kwargs)
    for fname, outliers in outlier_dict.items():
        if len(outliers) == 0:
            continue
        outlier_strs = []
        for out_ind in outliers:
            outlier_strs.append(str(out_ind))
        print(', '.join([fname] + outlier_strs))


def get_parser():
    parser = ArgumentParser(description=__doc__,  # Usage from docstring
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('data_directory',
                        help='Directory containing data')
    parser.add_argument('-m', '--metric', nargs='?', default='vol_means',
        help="""The metric to summarize timecourse data across volumes with 
        before outlier detection is applied""")
    parser.add_argument('-d', '--detector', nargs='?', default='std',
        help="""The outlier detection method to be used.""")
    parser.add_argument('-s', '--n-stds', default=2,
        help="""The standard deviation threshold used with the 'std' 
        detector method.""")
    parser.add_argument('-q', '--iqr-prop', default=1.5,
        help="""The interquartile proportion threshold to use with the
        'iqr' method.""")
    parser.add_argument('-j', '--mask-join', default='or',
        help="""The method used to join outlier masks obtained when multiple
        metrics or detection methods are used.""")
    return parser


def main():
    # This function (main) called when this file run as a script.
    #
    # Get the data directory from the command line arguments
    parser = get_parser()
    args = parser.parse_args()
    # Call function to find outliers.
    print(f"\nPrinting outliers obtained using\n  metric: ({args.metric})\n  detector: ({args.detector})\n...\n...\n")
    print_outliers(args.data_directory,
                metric=args.metric,
                detector=args.detector,
                n_stds=args.n_stds,
                iqr_proportion=args.iqr_prop,
                mask_join=args.mask_join)


if __name__ == '__main__':
    # Python is running this file as a script, not importing it.
    main()
