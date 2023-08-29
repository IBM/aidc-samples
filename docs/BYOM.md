<a id="byom"></a>
## Bring Your Own Model flow

In this scenario, we will use the pre-existing model to produce 
required dataset based on our [dataset without human output](data/credit_no_human.csv).

Using the model, we obtain additional columns, namely<br>
`mlClass` (the decision made by the model) and<br>
`mlConfidence` (the probability that the transaction is a Risk) and combine it with the human results.

Please see: [credit with human and ml](../data/credit_human_ml.csv) for an example.

We will run the [BYOM_flow](../notebooks/BYOM_flow.ipynb) notebook.

Similarly to the [AutoAI flow](#performance), we will start with default performance model <br>
then define different values in the performance model, calculate the ROI and finally save the rules as JSON.

Follow the [OpenScale](OpenScale#openscale) section to see how we can monitor the return on investment introduced by AIDC.
