#!/bin/sh
python3 ../pipelinerunner/run_pipeline.py \
    ./join.pln \
    file://$D3MINPUTDIR/185_baseball/TRAIN/dataset_TRAIN/datasetDoc.json \
    file://$D3MINPUTDIR/196_autoMpg/TRAIN/dataset_TRAIN/datasetDoc.json \
    -r $D3MSTATICDIR -v
