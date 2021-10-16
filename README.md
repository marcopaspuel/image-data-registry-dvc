# image-data-registry-dvc
This project contains an example of how to build a data registry for image datasets using DVC. 

Initialize the project with:
```bash
poetry install
```

First we need to initialize DVC with the following command:
```bash
poetry run dvc init
```

Then we need to configure the remote storage, is this case we will use local storage. However, is recommended to use
SSH, S3, GCS, etc. as a data store. 

```bash
poetry run dvc remote add -d storage /Users/marco/Documents/image_data_registry_dvc_storage
```

## Add a new raw dataset

```bash
poetry run dvc add raw/01_data_collection_16_oct_2021
```

Add the dataset to git 

```bash
git add raw/01_data_collection_16_oct_2021.dvc raw/.gitignore
```

Push the new dataset to the remote storage
```bash
poetry run dvc push
```
