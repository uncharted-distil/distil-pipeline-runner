import ta3ta2_api.utils as ta3ta2
import argparse
import typing
from d3m.metadata import pipeline as pipeline_module


def convert_pipeline(input_file: str) -> pipeline_module.Pipeline:
    # load the json pipeline
    infile = open(input_file, "r")
    pipeline = pipeline_module.Pipeline.from_json(infile)
    infile.close()

    # convert to proto
    return ta3ta2.encode_pipeline_description(pipeline, [ta3ta2.ValueType.RAW], '/tmp')


if __name__ == "__main__":
    parser = argparse.ArgumentParser('converts a protobuf pipeline to a json pipeline')
    parser.add_argument('input_file', type=str, help='json file to convert')
    parser.add_argument('output_file', type=str, help='name of converted file')
    args = parser.parse_args()

    proto_pipeline = convert_pipeline(args.input_file)

    outfile = open(args.output_file, "wb")
    outfile.write(proto_pipeline.SerializeToString())
    outfile.close()
