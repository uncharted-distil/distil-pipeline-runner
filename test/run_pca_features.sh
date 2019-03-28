#!/bin/sh
python3 ../pipelinerunner/run_pipeline.py ./pca_features.pln file://$D3MINPUTDIR/185_baseball/TRAIN/dataset_TRAIN/datasetDoc.json -r $D3MSTATICDIR -v
