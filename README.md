# IBM AI Decision Coordination samples
AI Decision Coordination sample assets and notebooks.

[Introduction](#intro)<br>
[Collecting a dataset](#dataset)<br>
[Training a model](#model)<br>
[IBM AutoAI flow](#autoai)<br>
[Bring Your Own Model flow](#byom)<br>
[Watson Machine Learning flow](#wml)<br>
[Watson OpenScale flow](#openscale)<br>
[IBM OpenPages flow](#openpages)

<a id="intro"></a>
## Introduction

AI Decision Coordination software analyses your data and calculates the success of tasks 
that are completed by automated AI, human resources, or augmentation that combines the two.

The below flow chart demonstrates how AIDC can be used to determine the benefits of using AI by involving IBM's AI Governance framework.

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
If you already have a model, please move to the [Bring Your Own Model flow](#byom), otherwise let's see how [IBM's AutoAI can assist us with this task](#autoai).

<a id="autoai"></a>
## AutoAI flow

We start with creating an IBM WatsonStudio project and uploading the necessary datasets:

Complete file with human results:
[credit_with_human.csv](data/credit_with_human.csv)

Training file with no human results:
[credit_no_human.csv](data/credit_no_human.csv)

[AIDC library](https://aidecisioncoordination.com/)

![new project](images/new_project.png)

By clicking the "New asset" button, we will now create an AutoAI experiment using the dataset without human output.
![new project](images/new_asset.png)

We are going to predict the groundTruth, and use Risk as the positive class.

![autoai](images/autoai.png)

Once the experiment completes, "Save code" of the experiment and navigate to the new notebook.

![autoai completed](images/autoai_completed.png)

Edit the notebook to start the environment.
![edit notebook](images/edit_notebook.png)

Run the entire notebook:
![run all](images/run_all.png)

You will see that Deployment creation fails due to a missing Space id:
![space fail](images/space_fail.png)

Let's create a new Deployment space and copy it's GUID

![deployment](images/deployment.png)
![guid](images/guid.png)

Coming back to the notebook, we can ignore the failed cell, and add a new cell at the end of the notebook
as we will now introduce AIDC logic to continue the model creation.

![new cell](images/insert_cell.png)

Please now copy the new cells from the [AutoAI flow](notebooks/AutoAI_flow.ipynb) notebook,
starting at "Finding the most optimal model with AIDC"


<a id="byom"></a>
## Bring Your Own Model flow

<a id="wml"></a>
## Watson Machine Learning flow

<a id="openscale"></a>
## Watson OpenScaleflow

<a id="openpages"></a>
## IBM OpenPages flow