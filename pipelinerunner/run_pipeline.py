import sys
import argparse
import pipeline_executor as pe
import json_to_proto as jp

if __name__ == "__main__":

    parser = argparse.ArgumentParser('runs d3m pipeline and writes output to stdout')
    parser.add_argument('pipeline_file', type=str, help='protobuf / json pipelne to execute')
    parser.add_argument('dataset_file', type=str, help='datasetDoc.json file to run pipeline against')
    parser.add_argument('-r', '--resource', type=str, help='directory containing primitive static resources')
    parser.add_argument('-v', '--verbose', action='store_true', help='display detailed primitive execution')

    args = parser.parse_args()

    output = None
    if args.pipeline_file.endswith(".json"):
        # convert from json to proto if necessary
        pipeline = jp.convert_pipeline(args.pipeline_file)
        output = pe.execute_pipeline(pipeline, args.dataset_file, args.resource, args.verbose)
    else:
        output = pe.execute_pipeline_file(args.pipeline_file, args.dataset_file, args.resource, args.verbose)

    print(output)
