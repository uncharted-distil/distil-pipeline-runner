"""
   Copyright © 2019 Uncharted Software Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import sys
import argparse
import pipeline_executor as pe
import json_to_proto as jp
import logging
import logging.config
import pprint

_logger = logging.getLogger(__name__)

if __name__ == "__main__":

    parser = argparse.ArgumentParser('runs d3m pipeline and writes output to stdout')
    parser.add_argument('pipeline_file', type=str, help='protobuf / json pipelne to execute')
    parser.add_argument('dataset_file', type=str,  nargs='+', help='datasetDoc.json file to run pipeline against')
    parser.add_argument('-r', '--resource', type=str, help='directory containing primitive static resources')
    parser.add_argument('-v', '--verbose', action='store_true', help='display detailed primitive execution')

    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s %(message)s')

    output = None
    if args.pipeline_file.endswith(".json"):
        # convert from json to proto if necessary
        pipeline = jp.convert_pipeline(args.pipeline_file)
        _logger.info('Executing pipeline: \n' + str(pipeline))
        output = pe.execute_pipeline(pipeline, args.dataset_file, args.resource)
    else:
        output = pe.execute_pipeline_file(args.pipeline_file, args.dataset_file, args.resource)

    print(output)
