#!/bin/bash
import sys
import argparse
import pipeline_executor as pe

if __name__ == "__main__":

    parser = argparse.ArgumentParser('runs d3m pipeline and writes output to stdout')
    parser.add_argument('pipeline_file', type=str, help='serialized protobuf pipeline to execute')
    parser.add_argument('dataset_file', type=str, help='datasetDoc.json file to run pipeline against')
    parser.add_argument('-r', '--resource', type=str, help='directory containing primitive static resources')
    parser.add_argument('-v', '--verbose', action='store_true', help='display detailed primitive execution')

    args = parser.parse_args()

    # execute the pipeline against the data
    output = pe.execute_pipeline_file(args.pipeline_file, args.dataset_file, args.resource, args.verbose)
    print(output)
