## Image Data Registry with DVC

### Table of Contents

- [Image Data Registry with DVC](#image-data-registry-with-dvc)
  * [Introduction](#introduction)
  * [Data Versioning](#data-versioning)
  * [Prerequisites](#prerequisites)
  * [Installation & Configuration](#installation---configuration)
  * [Add a new raw data collection](#add-a-new-raw-data-collection)
  * [Create a new processed dataset from raw data](#create-a-new-processed-dataset-from-raw-data)
  * [Create a DVC pipeline](#create-a-dvc-pipeline)
  * [How to add more raw data](#how-to-add-more-raw-data)
  * [How to process the new raw data](#how-to-process-the-new-raw-data)
    

### Introduction

This project uses **DVC** to build an image data registry. The registry is divided into **raw** data and **processed** datasets.

- The [raw](raw) subdirectory contains the original files that come from the data collection, and they can be images or videos.
- The [processed](processed) subdirectory contains source code, pipelines and parameters used to convert the raw data into a dataset
  that can be use for training.
  
**DVC** works alongside **Git** and it helps to connect the data with the code. DVC uses Amazon S3, Microsoft Azure Blob
Storage, Google Cloud Storage or disc to store large files while keeping the metafiles in Git to describe and version control
the raw data, pipelines and processed datasets. Find more information about DVC in the following [link](https://dvc.org/).

The graph bellow shows the complete model life cycle. We will use a **NAS**, **DVC**, and **Git** to build a data version system.
Then we wil use **DVC**, **Git** and **MLflow** for model tracking. Finally we will use **MLflow** to build a model registry. 
- The first part **Data Versioning** is covered in the [current repository](https://github.com/marcopaspuel/image-data-registry-dvc).
- The second part **Model Training** is covered in [this repository](https://github.com/marcopaspuel/awesome-ml-model).
- The third section **Model Registry** is covered in [this repository]().

![pycharm0](assets/image-data-registry-dvc-flow-diagram.png)

### Data Versioning

### Prerequisites
- [Poetry](https://python-poetry.org/docs/#installation) 
- [Python >=3.8](https://www.python.org/doc/)

### Installation & Configuration

To initialize the project run the following command:
```bash
poetry install
```

To initialize DVC run the following command:
```bash
poetry run dvc init
```

Then we need to configure the remote storage, is this case we will use local storage. However, is recommended to use
SSH, S3, GCS, etc. as a data store. 

```bash
poetry run dvc remote add -d storage /Users/marco/Documents/image_data_registry_dvc_storage
```

### Add a new raw data collection

First you need to create a subdirectory in the [raw](raw) directory. Then run the following command:

```bash
poetry run dvc add raw/01_data_collection_16_oct_2021
```

Then add the dataset to git:

```bash
git add raw/01_data_collection_16_oct_2021.dvc raw/.gitignore
```

Finally, Push the new dataset to the remote storage:

```bash
poetry run dvc push
```

### Create a new processed dataset from raw data

Import the raw image data into the input folder:

```bash
poetry run dvc import https://github.com/marcopaspuel/image-data-registry-dvc \
                      raw/01_data_collection_16_oct_2021 \
                      -o processed/01_image_dataset/data/inputs
```

To track the changes with git, run the following command: 
```bash
git add processed/01_image_dataset/data/inputs/01_data_collection_16_oct_2021.dvc \
        processed/01_image_dataset/data/inputs/.gitignore
```

### Create a DVC pipeline

To create the first stage of the pipeline run the following command:

```bash
poetry run dvc run -n remove_corrupted_images \
                   -d src/remove_corrupted_images.py -d data/inputs/01_data_collection_16_oct_2021 \
                   -o data/intermediate/remove_corrupted_images \
                   poetry run python src/remove_corrupted_images.py data/inputs/01_data_collection_16_oct_2021/
```

To track pipeline with git run:

```bash
git add dvc.lock dvc.yaml
```

###  How to add more raw data

First create a new branch
```bash
git checkout -b add-new-raw-data-collection
```

Then create a new subdirectory in the [raw](raw) data folder and add the new raw data.

Add the new raw data collection to dvc:

```bash
poetry run dvc add raw/02_data_collection_20_oct_2021
```

Add the dataset to git and commit.

```bash
git add raw/02_data_collection_20_oct_2021.dvc raw/.gitignore
```

Push the new dataset to the remote storage
```bash
poetry run dvc push
```

Finally, open a PR and merge 

### How to process the new raw data

First create a new branch

```bash
git checkout -b add-new-raw-data-to-dataset
```

Then import the new raw image data into the input folder:

```bash
poetry run dvc import https://github.com/marcopaspuel/image-data-registry-dvc \
                      raw/02_data_collection_20_oct_2021 \
                      -o processed/01_image_dataset/data/inputs
```

To track the changes with git, run:

```bash
git add processed/01_image_dataset/data/inputs/.gitignore processed/01_image_dataset/data/inputs/02_data_collection_20_oct_2021.dvc
```
Add new dataset to the list of dependencies([deps](processed/01_image_dataset/dvc.yaml)) if necessary.

Rerun the pipeline with the following commands:

```bash
cd 01_image_dataset
poetry run dvc repro
```

Commit and push the results:
```bash
git push
poetry run dvc push
```

Finally, Open a PR and merge.
