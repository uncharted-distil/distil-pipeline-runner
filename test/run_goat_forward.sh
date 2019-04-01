#!/bin/sh
python3 ../pipelinerunner/run_pipeline.py ./create_goat_forward.pln file://$D3MINPUTDIR/LL0_acled/TRAIN/dataset_TRAIN/datasetDoc.json -r $D3MSTATICDIR -v
