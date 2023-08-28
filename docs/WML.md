<a id="wml"></a>
## Watson Machine Learning flow

In this process, we start by defining a [custom image](https://www.ibm.com/docs/en/cloud-paks/cp-data/4.7.x?topic=environments-building-custom-images)
using the provided [Dockerfile](../cp4d_assets/Dockerfile).

We also need the JSON representation of AIDC model from [AutoAI](../docs/AutoAI.md#autoai) or processing your [own model](../docs/BYOM.md#byom).

Following the [WML_flow.ipynb notebook](../notebooks/WML_flow.ipynb) we will load the model, 
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