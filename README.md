# IBM AI Decision Coordination samples
AI Decision Coordination sample assets and notebooks.

[Introduction](#intro)<br>
[Collecting a dataset](#dataset)<br>
[Training a model](#model)<br>

[IBM AutoAI flow](docs/AutoAI.md#autoai)<br>
Build an optimized model based on a dataset

[Bring Your Own Model flow](docs/BYOM.md#byom)<br>
Evaluate an existing Machine Learning model

[Watson Machine Learning flow](docs/WML.md#wml)<br>
Manage decisions made by a model

[Watson OpenScale flow](docs/OpenScale.md#openscale)<br>
Define monitoring for your model

[IBM OpenPages flow](docs/OpenPages.md#openpages)<br>
Govern your model and build custom workflows

<a id="intro"></a>
## Introduction

AI Decision Coordination software analyses your data and calculates the success of tasks 
that are completed by automated AI, human resources, or augmentation that combines the two.

Our solution helps in obtaining the most optimal human-to-AI workload distribution and 
calculating the return on investment given specific business guidelines.

![roi](images/roi.png)

The below flow chart demonstrates how AIDC can be used to determine 
the benefits of using AI by involving IBM's AI Governance framework.

The described actions will be in the context of Cloud Pak for Data interface.

![AIDC flows](images/aidc.png)

<a id="dataset"></a>
## Collecting a dataset.

To utilize the solution we start with collecting the data. The dataset needs to include attributes involved in the decision process, 
the  target attribute (groundTruth) produced by experts, as well as decision made by human resource (hClass) in the current process.

![dataset](images/dataset.png)

Sample dataset is available in the data folder: [credit_with_human.csv](data/credit_with_human.csv)

<a id="model"></a>
## Training a model

Given the dataset we can train a model to predict the target attribute (in our scenario Risk/No Risk of granting the loan).
If you already have a model, please move to the [Bring Your Own Model flow](docs/BYOM.md#byom), otherwise let's see how [IBM's AutoAI can assist us with this task](docs/AutoAI.md#autoai).

