#!/bin/sh
python3 ../pipelinerunner/run_pipeline.py ./target_ranking.pln file://$D3MINPUTDIR/185_baseball/TRAIN/dataset_TRAIN/datasetDoc.json -r $D3MSTATICDIR -v
