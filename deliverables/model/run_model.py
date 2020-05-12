#!/usr/bin/env python3
"""Reproduce your result by your saved model.

This is a script that helps reproduce your prediction results using your saved
model. This script is unfinished and you need to fill in to make this script
work. If you are using R, please use the R script template instead.

The script needs to work by typing the following commandline (file names can be
different):

python3 run_model.py -i unlabelled_sample.txt -m model.pkl -o output.txt

"""

# author: Chao (Cico) Zhang
# date: 31 Mar 2017

import argparse
import sys
# Start your coding
import pickle
import pandas as pd
# End your coding


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Reproduce the prediction')
    parser.add_argument('-i', '--input', required=True, dest='input_file',
                        metavar='unlabelled_sample.txt', type=str,
                        help='Path of the input file')
    parser.add_argument('-m', '--model', required=True, dest='model_file',
                        metavar='model.pkl', type=str,
                        help='Path of the model file')
    parser.add_argument('-o', '--output', required=True,
                        dest='output_file', metavar='output.txt', type=str,
                        help='Path of the output file')
    # Parse options
    args = parser.parse_args()

    if args.input_file is None:
        sys.exit('Input is missing!')

    if args.model_file is None:
        sys.exit('Model file is missing!')

    if args.output_file is None:
        sys.exit('Output is not designated!')

    # Start your coding

    # suggested steps
    # Step 1: load the model from the model file
    # Step 2: apply the model to the input file to do the prediction
    # Step 3: write the prediction into the desinated output file

    model = args.model_file
    input = args.input_file
    output = args.output_file

    with open(model, 'rb') as file:
        pickle_model = pickle.load(file)

    """ The gene regions selected by our feature selection method,
    how these were selected can be found in code/Pipeline_Final.ipynb
    or in our draft/final report"""
    important_genes = [65, 111, 157, 192, 249, 360, 361, 479, 576, 583, 625,
    664, 668, 669, 670, 671, 672, 673, 674, 675, 676, 679, 688, 691, 692, 693,
    694, 695, 696, 697, 772, 814, 818, 819, 831, 832, 834, 835, 837, 838, 839,
    840, 841, 842, 843, 844, 845, 846, 847, 848, 849, 850, 851, 852, 853, 854,
    855, 856, 857, 858, 859, 860, 861, 862, 863, 864, 876, 877, 878, 937, 966,
    991, 992, 993, 999, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1008, 1015,
    1016, 1018, 1022, 1024, 1025, 1026, 1027, 1032, 1034, 1035, 1050, 1055,
    1057, 1061, 1062, 1090, 1091, 1092, 1136, 1137, 1207, 1234, 1296, 1310,
    1370, 1371, 1387, 1407, 1513, 1563, 1567, 1569, 1575, 1583, 1589, 1611,
    1645, 1656, 1657, 1672, 1674, 1697, 1725, 1734, 1735, 1865, 1904, 1911,
    1965, 2015, 2016, 2017, 2021, 2023, 2024, 2026, 2027, 2039, 2040, 2041,
    2048, 2049, 2051, 2054, 2055, 2056, 2057, 2058, 2059, 2063, 2064, 2065,
    2068, 2070, 2071, 2074, 2075, 2076, 2078, 2079, 2081, 2126, 2135, 2136,
    2160, 2161, 2184, 2200, 2201, 2205, 2206, 2207, 2208, 2209, 2210, 2211,
    2212, 2213, 2214, 2215, 2218, 2219, 2220, 2221, 2223, 2224, 2306, 2446,
    2681, 2682, 2683, 2684, 2685, 2723, 2732, 2744, 2750, 2751, 2794, 2822]

    temp_list = []

    with open(input, 'r') as temp:
        for line in temp:
            temp_list.append(line.split())

    columns_temp = temp_list[0]
    columns_temp = [x.replace("\"", "") for x in columns_temp]

    df_test = pd.DataFrame(temp_list[1:], columns=columns_temp)
    test_set = df_test.drop(['Chromosome', 'Start','End', 'Nclone'], axis=1)
    test_set = test_set.transpose()

    for i in range(len(test_set.columns)):
        if i not in important_genes:
            test_set = test_set.drop([i], axis=1)

    patient_ids = test_set.index.values

    predictions = pickle_model.predict(test_set)

    output_preds = []

    for i, pred in enumerate(predictions):
        if pred == 1:
            output_preds.append([patient_ids[i],"HER2+"])
        if pred == 2:
            output_preds.append([patient_ids[i],"HR+"])
        if pred == 3:
            output_preds.append([patient_ids[i],"Triple Neg"])

    file1 = open(output,"w")

    file1.write("\"Sample\"\t\"Subgroup\"\n")
    for i, prediction in enumerate(predictions):
        if i == len(predictions):
            file1.write("\"{0}\" \t \"{1}\"".format(output_preds[i][0], output_preds[i][1]))
        else:
            file1.write("\"{0}\" \t \"{1}\"\n".format(output_preds[i][0], output_preds[i][1]))

    file1.close()
    # End your coding


if __name__ == '__main__':
    main()
