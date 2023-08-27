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

![finding](images/finding.png)
<a id="performance"></a>
Starting with library imports, we will analyze the AutoAI provided models using our unique algorithms.

Initially we will determine how to best distribute the workload between human and AI,
based on the `confidence` (defined as a number between 0 and 1 that represents the likelihood that the output of a Machine Learning model is correct).

We apply a default cost matrix (also called `performance model`), like so:
```
#We gain 1 point for correctly determining a Risk scenario
TruePositiveCost = "1"      

#We lose 1 point  for incorrectly marking a scenario as Risk
FalsePositiveCost = "-1"

#We lose 1 point  for incorrectly marking a scenario as No Risk
FalseNegativeCost = "-1"

#We gain 1 point for correctly determining a No Risk scenario
TrueNegativeCost = "1"

#For now lets assume the decision taking does not have a cost
ModelDecisionCost = "0"
HumanDecisionCost = "0"
```

You will notice that the distribution (called `dispatch rule`) 
will differ across the models, for example:

![confidence](images/confidence.png)

As expected when the Machine Learning model is not sure about the decision, we can utilize the human resources.

What's interesting is how different models will compliment humans.
Our tool allows you to calculate the most optimial distribution and provide the statistical information to justify it.

We can also see the improvement introduced by implementing the AIDC solution:

![roi](images/roi.png)

We will see in the [OpenScale](#openscale) section how we can monitor the return on investment introduced by AIDC.

We sort the models by the best performance (average number of points per decision).
Suprisingly, it may not be the most accurate models which perform best - this is due the fact that human can fill the uncertainty of the models.

In the next steps we will compare the models, and apply more complex `performance model`.
We can use the attributes of the model, to calculate the impact of each outcome, for example:
```
# If Risk, we dont gain anything
TruePositiveCost = "0"

# We missed a No Risk application
FalsePositiveCost = "-LoanAmount*0.3"

# The loan was actually Risky
FalseNegativeCost = "-LoanAmount*0.5"

# Correctly identified as No Risk
TrueNegativeCost = "LoanAmount*0.3"

#Costs of each decision
ModelDecisionCost = "-0.02"
HumanDecisionCost = "-0.05"
```

Once we run the cells, we will realize that the most optimal solution 
based on the defined `performance matrix` depends on human in almost quarter of the decisions.

`if confidence <35.42%: use ml else if confidence <59.462%: use human else use ml`

For some of the more accurate models, the distribution is close to 50/50:

`f confidence <28.39%: use ml else if confidence <81.765%: use human else use ml`

![comparison](images/comparison.png)

We then move to deploying the model and saving the JSON representation of our `dispatch rules`.

<a id="byom"></a>
## Bring Your Own Model flow

In this scenario, we will use the pre-existing model to produce 
required dataset based on our [dataset without human output](data/credit_no_human.csv).

Using the model, we obtain additional columns, namely<br>
`mlClass` (the decision made by the model) and<br>
`mlConfidence` (the probability that the transaction is a Risk) and combine it with the human results.

Please see: [credit with human and ml](data/credit_human_ml.csv) for an example.

We will run the [BYOM_flow](notebooks/BYOM_flow.ipynb) notebook.

Similarly to the [AutoAI flow](#performance), we will start with default performance model <br>
then define different values in the performance model and finally save the rules as JSON.

<a id="wml"></a>
## Watson Machine Learning flow

In this process, we start by defining a [custom image](https://www.ibm.com/docs/en/cloud-paks/cp-data/4.7.x?topic=environments-building-custom-images)
using the provided [Dockerfile](cp4d_assets/Dockerfile).

We also need the JSON representation of AIDC model from [AutoAI](#autoai) or processing your [own model](#byom).

Following the [WML_flow.ipynb notebook](notebooks/WML_flow.ipynb) we will load the model, 
make sure it applies the decision table we have selected, and then deploy it.

This will allow all the future requests to the model be handled by our `dispatch` function.

To deploy the function we follow the mechanism of deployable Python functions:

https://www.ibm.com/docs/en/cloud-paks/cp-data/4.7.x?topic=functions-writing-deployable-python

with private libraries:

https://www.ibm.com/docs/en/cloud-paks/cp-data/4.7.x?topic=runtimes-customizing-third-party-private-python-libraries

As inputs, it takes the request data (attributes and the values) as well as the URL of the model.

It produces the output suggesting whether the machine learning model decision should be followed, or the human operator should be involved.
For example:

```
test_values_for_human = [["CheckingStatus", "LoanDuration", "CreditHistory", "LoanPurpose", "LoanAmount", "ExistingSavings", "EmploymentDuration", "InstallmentPercent", "Sex", "OthersOnLoan", "CurrentResidenceDuration", "OwnsProperty", "Age", "InstallmentPlans", "Housing", "ExistingCreditsCount", "Job", "Dependents", "Telephone", "ForeignWorker"], 
["no_checking", 20, "prior_payments_delayed", "repairs", 3094, "500_to_1000", "greater_7", 39, "male", "none", 3, "savings_insurance", 29, "none", "own", 1, "skilled", 1, "yes", "yes"],
model_serving_url]

job_payload = {
client.deployments.ScoringMetaNames.INPUT_DATA: [{
    "fields": [ "message" ],
    "values": [[test_values_for_human]]
    }]
 }

function_result = client.deployments.score(deployment_uid, job_payload)
print( function_result )
```
would produce:
```
{'predictions': [{'fields': ['AIDC Decision'], 'values': [[{'toolToUse': 'human', 'type': 'h'}]]}]}
```

If we modify the data accordingly, the result may be:
```
{'predictions': [{'fields': ['AIDC Decision'], 'values': [[{'toolToUse': 'ml', 'type': 'ml', 'confidence': 0.8580362993842072, 'outcome': 'No Risk'}]]}]}
```

<a id="openscale"></a>
## Watson OpenScale flow

After the [model](#model) and the [dispatch function](#wml) have been deployed, 
we can use the Watson OpenScale capabilities to monitor & alert if the AIDC rules change.

We are able to calculate the human-to-ml distribution, the average cost of decision, 
average performance and impact costs, as well as the ROI metric.

ROI is measured as the sum of improvements over each decision between the current process (done by human) and the augmented
human+AI process.

![roi](images/roi.png)

Start with adding the deployed model to Watson OpenScale dashboard:

![add_model](images/add_model.png)
![add_deployment](images/add_deployment.png)

next collect the Subscription ID from the model information:

![model_info](images/model_info.png)
![subscription](images/subscription.png)

use this information in the [OpenScale notebook](notebooks/OpenScale_flow.ipynb).

Running th notebook for the first time, will result in 0s as the metrics' values.
![first_run](images/first_run.png)

To correct this, we need to upload the Feedback data to the model using the Evaluate function of Watson OpenScale.
You can upload the [dataset with human and machine learning outputs](data/credit_human_ml.csv).

![evaluate](images/evaluate.png)

![feedback](images/feedback.png)

Running the 2 last steps of the notebook, should return:

![second_run](images/second_run.png)

<a id="openpages"></a>
## IBM OpenPages flow