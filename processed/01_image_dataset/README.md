## 01 Image Dataset

### Description

This dataset contains drone data classified to day, nigh, foggy and sharp images.
The process data can be found in the [outputs](data/outputs) directory.

### How to import the dataset

To import the processed dataset run the following command:

```bash
poetry run dvc import https://github.com/marcopaspuel/image-data-registry-dvc \
                      processed/01_image_dataset/data/outputs/day_images \
                      -o data/training
```

### Data Pipeline

To initialize the project run the following command:
```bash
+------------------------------------------------+                           +------------------------------------------------+  
| data/inputs/01_data_collection_16_oct_2021.dvc |                           | data/inputs/02_data_collection_20_oct_2021.dvc |  
+------------------------------------------------+                           +------------------------------------------------+  
                                         *******                                *******                                          
                                                ******                    ******                                                 
                                                      ****            ****                                                       
                                                  +-------------------------+                                                    
                                                  | remove_corrupted_images |                                                    
                                                  +-------------------------+                                                    
                                                                *                                                                
                                                                *                                                                
                                                                *                                                                
                                               +-------------------------------+                                                 
                                               | remove_dark_and_bright_images |                                                 
                                               +-------------------------------+                                                 
                                                                *                                                                
                                                                *                                                                
                                                                *                                                                
                                            +-------------------------------------+                                              
                                            | classify_day_night_and_foggy_images |                                              
                                            +-------------------------------------+                                              

```

### Tags

`#Drone` `#Day` `#Night` `Foggy` `#Sharp`
