#!/bin/sh
python3 ../pipelinerunner/run_pipeline.py ./croc.pln file://$D3MINPUTDIR/22_handgeometry/TRAIN/dataset_TRAIN/datasetDoc.json -r $D3MSTATICDIR -v
