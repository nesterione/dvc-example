## DVC Example 

Hi, this repository contains demo example from meetup. The goal is to show how to improve Machine Learning workflow with [DVC](https://dvc.org/) 

You can find slides [here](https://docs.google.com/presentation/d/1zKxr4IYhCcxsatVdqEKLTAt6Gbw-JCk0FnsruRKUTGc/edit?usp=sharing)

In this example, a very simple code that solves the problem of sentiment analysis on dasaset from [IMDB](https://www.kaggle.com/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews). The purpose of this example is to show how DVC can be used. `Do not use it as an example of organizing a machine learning project.`


There are implemented following DAG: 

![alt text](images/dag.png "DAG")

The code won't work without configuration the bucket for storing artefacts, you can use it as example. 

1. Init dvc project and configure storage 

```
git init
dvc init
git commit -m "Initialize DVC project"

# Configure any storage type (I used minio)
dvc remote add -d s3remote s3://dvc-meetup/nlp-imdb-demo

dvc remote modify s3remote endpointurl <YOUR URL TO BUCKET>
```

2. Add data, put in in the foder `data/raw`

```
dvc add data/raw
git add .
git commit -m "Added raw data to project"
dvc push
```

3. Add data preparation stage 

```
dvc run -f preprop.dvc \
        -d src/preproc.py -d data/raw -o data/prepared \
        python src/preproc.py "data/raw/IMDB Dataset.csv"

git add .
git commit -m "Added preprocessing stage"
```

4. Add vectorization stage 

```
dvc run -f vectorize.dvc \                                                  
        -d src/vectorize.py -d data/prepared \
        -o data/vectorized -o models/vectorizer.pkl \
        python src/vectorize.py data/prepared  data/vectorized models/vectorizer.pkl

git add .
git commit -m "Added vectorization stage"
```

5. Add trainig stage 

```
dvc run -f train.dvc 
        -d src/train.py -d data/vectorized 
        -o models/model.pkl python src/train.py data/vectorized models/model.pkl

git add .
git commit -m "Added training stage"
```

6. Add evaluation stage 

```
dvc run -f evaluate.dvc 
    -d src/evaluate.py -d models/model.pkl -d data/vectorized 
    -M classification.json 
    python src/evaluate.py models/model.pkl data/vectorized classification.json
    
git commit -m "Added evaluation stage"
```

7. Make release 

```
git tag -a baseline -m "model baseline"
git push
git push --tags
dvc push
```

Then you can show metrics:

```
dvc metrics show
```

And visualize DAG:

```
dvc pipeline show --ascii train.dvc
```

```
            +--------------+
            | data\raw.dvc |
            +--------------+
                    *
                    *
                    *
             +-------------+
             | preprop.dvc |
             +-------------+
                    *
                    *
                    *
            +---------------+
            | vectorize.dvc |
            +---------------+
             **            **
           **                **
         **                    **
+-----------+                    **
| train.dvc |                  **
+-----------+                **
             **            **
               **        **
                 **    **
            +--------------+
            | evaluate.dvc |
            +--------------+

```

## Scenarios 

### Scenario 1: Update code

* Let’s update vectorizer `src/vectorize.py` 
* Run `dvc repro evaluate.dvc`
* Compare` metrics dvc metrics show -T`
* Commit `git commit -a -m "Added new vectorizer"`
* Release `git tag -a v2.0 -m "New model"`
* Push `git push && dvc push`

### Scenario 2: Add more data

* Put new data in `data/raw`
* Add `dvc add data/raw`
* Run `dvc repro evaluate.dvc`
* Compare metrics `dvc metrics show -T`
* Commit `git commit -a -m "Added new data"`
* Release `git tag -a v3.0 -m "Added data"`
* Push `git push && dvc push`

### Scenario 3: Re-run old model with new data

Let's assume you got new data (it is added in v3.0 model) and you want to re-run baseline with new data

* Go to old model `git checkout baseline && dvc checkout`
* Update data `git checkout v3.0 data/raw.dvc` 
* Pull `dvc checkout data/raw.dvc && dvc pull`
* Run `dvc repro evaluate.dvc`
* Compare `metrics dvc metrics show -T`
* Commit `git commit -m "Baseline with new data"`
* Release `git tag -a baseline-v2 -m "Added data"`
* Push `git push && dvc push`

