#!/bin/sh
python3 ../pipelinerunner/run_pipeline.py ./denorm.pln file://$D3MINPUTDIR/32_wikiqa/TRAIN/dataset_TRAIN/datasetDoc.json -r $D3MSTATICDIR -v
