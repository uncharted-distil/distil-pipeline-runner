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

import ta3ta2_api.utils as ta3ta2
import argparse
import pipeline_pb2
import typing
from d3m.metadata import pipeline as pipeline_module


def convert_pipeline(input_file: str, output_file: str) -> pipeline_pb2.PipelineDescription:
    # load the protobuf
    infile = open(input_file, "rb")
    pipeline = pipeline_pb2.PipelineDescription()
    pipeline.ParseFromString(infile.read())
    infile.close()

    # convert to json and save
    return ta3ta2.decode_pipeline_description(pipeline, pipeline_module.Resolver())


if __name__ == "__main__":
    parser = argparse.ArgumentParser('converts a protobuf pipeline to a json pipeline')
    parser.add_argument('input_file', type=str, help='protobuf file to convert')
    parser.add_argument('output_file', type=str, help='name of converted file')
    args = parser.parse_args()

    d3m_pipeline = convert_pipeline(args.input_file, args.output_file)

    outfile = open(args.output_file, "w")
    outfile.write(d3m_pipeline.to_json(indent=4, sort_keys=True))
    outfile.close()
