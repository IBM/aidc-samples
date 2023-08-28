<a id="openpages"></a>
## IBM OpenPages flow

To configure the tracking of the deployed model using the custom monitor, we need to start by
configuring [OpenPages for Model Risk Governance](https://www.ibm.com/docs/en/cloud-paks/cp-data/4.7.x?topic=openpages-integrating)
and [connecting Watson OpenScale](https://www.ibm.com/docs/en/cloud-paks/cp-data/4.7.x?topic=governance-end-end-model-tutorial#mrm-risk-config-dsx-work-step3).

Next, let's introduce a new Model Use Case:
![new_model_use_case](../images/new_model_use_case.png)

![model_use_case](../images/model_use_case.png)

and start tracking the deployed model using the new Model Use Case:
![track](../images/track.png)

Using the custom filters functionality of OpenPages, we can define a filter for the `roi` metric:

![object_types](../images/object_types.png)

![roi_filter](../images/roi_filter.png)

Going back to the OpenPages dashboard, we can define a new panel
![panel](../images/panel.png) 

and add it to the dashboard:

![roi_panel](../images/roi_panel.png)

We can monitor the trends of the metric:

![trend](../images/trend.png)

![tracking](../images/tracking.png)