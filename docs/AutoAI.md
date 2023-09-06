<a id="autoai"></a>
## AutoAI flow

We start with creating an IBM WatsonStudio project and uploading the necessary datasets:

Complete file with human results:
[credit_with_human.csv](../data/credit_with_human.csv)

Training file with no human results:
[credit_no_human.csv](../data/credit_no_human.csv)

[AIDC library](https://aidecisioncoordination.com/)

![new project](../images/new_project.png)

By clicking the "New asset" button, we will now create an AutoAI experiment using the dataset without human output.
![new project](../images/new_asset.png)

We are going to predict the groundTruth, and use Risk as the positive class.

![autoai](../images/autoai.png)

Once the experiment completes, "Save code" of the experiment and navigate to the new notebook.

![autoai completed](../images/autoai_completed.png)

Edit the notebook to start the environment.
![edit notebook](../images/edit_notebook.png)

Run the entire notebook:
![run all](../images/run_all.png)

You will see that Deployment creation fails due to a missing Space id:
![space fail](../images/space_fail.png)

Let's create a new Deployment space and copy it's GUID

![deployment](../images/deployment.png)
![guid](../images/guid.png)

Coming back to the notebook, we can ignore the failed cell, and add a new cell at the end of the notebook
as we will now introduce AIDC logic to continue the model creation.

![new cell](../images/insert_cell.png)

Please now copy the new cells from the [AutoAI flow](../notebooks/AutoAI_flow.ipynb) notebook,
starting at "Finding the most optimal model with AIDC"

![finding](../images/finding.png)
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

![confidence](../images/confidence.png)

As expected when the Machine Learning model is not sure about the decision, we can utilize the human resources.

What's interesting is how different models will compliment humans.
Our tool allows you to calculate the most optimial distribution and provide the statistical information to justify it.

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

![comparison](../images/comparison.png)

In the `Calculate ROI` we can see the improvement introduced by implementing the AIDC solution.

ROI is measured as the sum of improvements over each decision between the current process (done by human) and the augmented
human+AI process:

![roi](../images/roi.png)

The total improvement based on the dataset is calculated:

![improvement](../images/improvement.png)

We will later see in the [OpenScale](OpenScale.md#openscale) section how we can monitor the return on investment introduced by AIDC.

Finally we move to deploying the model and saving the JSON representation of our `dispatch rules`.

This way we can use it in [Watson Machine Learning](WML.md).
