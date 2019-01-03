#!/bin/sh
python3 ../pipelinerunner/run_pipeline.py \
    ./join.pln \
    file://$D3MINPUTDIR/185_baseball/TRAIN/dataset_TRAIN/datasetDoc.json \
    file://$D3MINPUTDIR/185_baseball/TRAIN/dataset_TRAIN/datasetDoc.json \
    -r $STATIC_RESOURCE_PATH -v
