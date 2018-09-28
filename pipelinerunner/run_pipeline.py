#!/bin/bash
import sys
import pipeline_executor as pe

if __name__ == "__main__":
   # path to pipeline file
    pipeline_filename = sys.argv[1]

    # path to dataset
    dataset_filename = sys.argv[2]

    # optional resource path
    static_resource_path = None
    if len(sys.argv) >= 4:
        static_resource_path = sys.argv[3]

    # execute the pipeline against the data
    output = pe.execute_pipeline_file(pipeline_filename, dataset_filename, static_resource_path)
    print(output)
