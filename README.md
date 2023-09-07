# IBM AI Decision Coordination samples
AI Decision Coordination sample assets and notebooks.

[Introduction](#intro)<br>
[Collecting a dataset](#dataset)<br>
[Training a model](#model)<br>

[Running locally](docs/Local.md#local)<br>
Experiment with AIDC functionallity locally

[Integrations with Cloud Pak for Data/IBM AI Governance](docs/Integrations.md#integrations)<br>
Integrate with several of IBM products to create end-to-end solution to govern your models.

<a id="intro"></a>
## Introduction

AI Decision Coordination software analyses your data and calculates the success of tasks 
that are completed by automated AI, human resources, or augmentation that combines the two.

Our solution helps in obtaining the most optimal human-to-AI workload distribution and 
calculating the return on investment given specific business guidelines.

Examples:

![roi2](images/roi2.png)

![roi1](images/roi1.png)

Using the suggested distribution, we can calculate the predicted improvements which AI would bring:

![improvement](images/improvement.png)

<a id="dataset"></a>
## Collecting a dataset.

To utilize the solution we start with collecting the data. 
The dataset needs to include attributes involved in the decision process, 
the  target attribute (groundTruth) produced by experts, as well as decision made by human resource (hClass) in the current process.

![dataset](images/dataset.png)

Sample dataset is available in the data folder: [credit_with_human.csv](data/credit_with_human.csv)

On top of the above, we need to also collect the response of the Machine Learning model.

<a id="model"></a>
## Training a model

Given the dataset we can train a model to predict the target attribute (in our scenario Risk/No Risk of granting the loan).
This is needed to collect additional properties: `mlClass` (answer of the model) and `mlConfidence` (probability of the outcome).
If you already have a model, please move to the [Bring Your Own Model flow](docs/BYOM.md#byom), otherwise let's see how [IBM's AutoAI can assist us with this task](docs/AutoAI.md#autoai).