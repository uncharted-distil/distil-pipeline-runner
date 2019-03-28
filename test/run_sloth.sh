#!/bin/sh
python3 ../pipelinerunner/run_pipeline.py ./sloth.pln file://$D3MINPUTDIR/66_chlorineConcentration/TRAIN/dataset_TRAIN/datasetDoc.json -r $D3MSTATICDIR -v
