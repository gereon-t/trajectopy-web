# Trajectopy API

Trajectory evaluation API for the Trajectopy project. Currently work in progress, this API allows to upload trajectories to a session and evaluate them regarding the ATE and RPE metrics. The uploaded trajectories can be stored either in the local filesystem or an Azure Blob Storage. The metadata of the session and the trajectories are stored in a SQLite database using SQLAlchemy.

## Get Trajectories

<a id="opIdget_trajectories_trajectories__get"></a>

`GET /trajectories/`

<h3 id="get-trajectories-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|session_id|query|string|true|none|

> Example responses

> 200 Response

```json
[
  {
    "name": "string",
    "epsg": 0,
    "sorting": "string",
    "session_id": "string",
    "id": "string"
  }
]
```

<h3 id="get-trajectories-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="get-trajectories-responseschema">Response Schema</h3>

Status Code **200**

*Response Get Trajectories Trajectories  Get*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Response Get Trajectories Trajectories  Get|[[TrajectorySchema](#schematrajectoryschema)]|false|none|none|
|» TrajectorySchema|[TrajectorySchema](#schematrajectoryschema)|false|none|none|
|»» name|string|true|none|none|
|»» epsg|integer|true|none|none|
|»» sorting|string|true|none|none|
|»» session_id|string|true|none|none|
|»» id|string|true|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## Get Trajectory

<a id="opIdget_trajectory_trajectories__trajectory_id__get"></a>

`GET /trajectories/{trajectory_id}`

<h3 id="get-trajectory-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|trajectory_id|path|string|true|none|

> Example responses

> 200 Response

```json
{
  "name": "string",
  "epsg": 0,
  "sorting": "string",
  "session_id": "string",
  "id": "string"
}
```

<h3 id="get-trajectory-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[TrajectorySchema](#schematrajectoryschema)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## Delete Trajectory

<a id="opIddelete_trajectory_trajectories__trajectory_id__delete"></a>

`DELETE /trajectories/{trajectory_id}`

<h3 id="delete-trajectory-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|trajectory_id|path|string|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="delete-trajectory-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="delete-trajectory-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## Upload Trajectory

<a id="opIdupload_trajectory_trajectories_upload_post"></a>

`POST /trajectories/upload`

> Body parameter

```yaml
file: string

```

<h3 id="upload-trajectory-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|session_id|query|string|true|none|
|body|body|[Body_upload_trajectory_trajectories_upload_post](#schemabody_upload_trajectory_trajectories_upload_post)|true|none|

> Example responses

> 200 Response

```json
{
  "name": "string",
  "epsg": 0,
  "sorting": "string",
  "session_id": "string",
  "id": "string"
}
```

<h3 id="upload-trajectory-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[TrajectorySchema](#schematrajectoryschema)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## Download Trajectory

<a id="opIddownload_trajectory_trajectories_download__trajectory_id__get"></a>

`GET /trajectories/download/{trajectory_id}`

<h3 id="download-trajectory-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|trajectory_id|path|string|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="download-trajectory-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="download-trajectory-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## Compare Trajectories

<a id="opIdcompare_trajectories_trajectories_compare_post"></a>

`POST /trajectories/compare`

<h3 id="compare-trajectories-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|gt_id|query|string|true|none|
|est_id|query|string|true|none|
|rpe_enabled|query|boolean|false|none|

> Example responses

> 200 Response

```json
{
  "name": "string",
  "id": "string",
  "trajectory_id": "string",
  "session_id": "string"
}
```

<h3 id="compare-trajectories-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[ResultSchema](#schemaresultschema)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## Align Trajectories

<a id="opIdalign_trajectories_trajectories_align_post"></a>

`POST /trajectories/align`

<h3 id="align-trajectories-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|gt_id|query|string|true|none|
|est_id|query|string|true|none|

> Example responses

> 200 Response

```json
{
  "aligned_trajectory_id": "string",
  "trans_x": 0,
  "trans_y": 0,
  "trans_z": 0,
  "rot_x": 0,
  "rot_y": 0,
  "rot_z": 0,
  "scale": 0,
  "lever_x": 0,
  "lever_y": 0,
  "lever_z": 0,
  "sensor_rot_x": 0,
  "sensor_rot_y": 0,
  "sensor_rot_z": 0
}
```

<h3 id="align-trajectories-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[AlignmentResultSchema](#schemaalignmentresultschema)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## Match Trajectories

<a id="opIdmatch_trajectories_trajectories_match_post"></a>

`POST /trajectories/match`

<h3 id="match-trajectories-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|gt_id|query|string|true|none|
|est_id|query|string|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="match-trajectories-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="match-trajectories-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## Get Results

<a id="opIdget_results_results__get"></a>

`GET /results/`

<h3 id="get-results-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|trajectory_id|query|string|true|none|

> Example responses

> 200 Response

```json
[
  {
    "name": "string",
    "id": "string",
    "trajectory_id": "string",
    "session_id": "string"
  }
]
```

<h3 id="get-results-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="get-results-responseschema">Response Schema</h3>

Status Code **200**

*Response Get Results Results  Get*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Response Get Results Results  Get|[[ResultSchema](#schemaresultschema)]|false|none|none|
|» ResultSchema|[ResultSchema](#schemaresultschema)|false|none|none|
|»» name|string|true|none|none|
|»» id|string|true|none|none|
|»» trajectory_id|string|true|none|none|
|»» session_id|string|true|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## Delete Result

<a id="opIddelete_result_results__result_id__delete"></a>

`DELETE /results/{result_id}`

<h3 id="delete-result-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|result_id|path|string|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="delete-result-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="delete-result-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## Get Result

<a id="opIdget_result_results__result_id__get"></a>

`GET /results/{result_id}`

<h3 id="get-result-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|result_id|path|string|true|none|

> Example responses

> 200 Response

```json
{
  "name": "string",
  "id": "string",
  "trajectory_id": "string",
  "session_id": "string"
}
```

<h3 id="get-result-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[ResultSchema](#schemaresultschema)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## Render Result

<a id="opIdrender_result_results_render__result_id__get"></a>

`GET /results/render/{result_id}`

<h3 id="render-result-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|result_id|path|string|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="render-result-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="render-result-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## Create Sesssion

<a id="opIdcreate_sesssion_sessions_create_post"></a>

`POST /sessions/create`

<h3 id="create-sesssion-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|custom_id|query|any|false|none|

> Example responses

> 200 Response

```json
{
  "id": "string",
  "date": "string",
  "trajectories": []
}
```

<h3 id="create-sesssion-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[SessionSchema](#schemasessionschema)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## Delete Session

<a id="opIddelete_session_sessions_delete_delete"></a>

`DELETE /sessions/delete`

<h3 id="delete-session-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|session_id|query|string|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="delete-session-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="delete-session-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## Update Settings

<a id="opIdupdate_settings_settings_update_put"></a>

`PUT /settings/update`

> Body parameter

```json
{
  "alignment_min_speed": 0,
  "alignment_time_start": 0,
  "alignment_time_end": 0,
  "alignment_trans_x": true,
  "alignment_trans_y": true,
  "alignment_trans_z": true,
  "alignment_rot_x": true,
  "alignment_rot_y": true,
  "alignment_rot_z": true,
  "alignment_scale": false,
  "alignment_time_shift": false,
  "alignment_use_x_speed": true,
  "alignment_use_y_speed": true,
  "alignment_use_z_speed": true,
  "alignment_lever_x": false,
  "alignment_lever_y": false,
  "alignment_lever_z": false,
  "alignment_sensor_rotation": false,
  "alignment_auto_update": false,
  "alignment_std_xyz_from": 1,
  "alignment_std_xyz_to": 1,
  "alignment_std_z_from": 1,
  "alignment_std_z_to": 1,
  "alignment_std_roll_pitch": 0.017453292519943295,
  "alignment_std_yaw": 0.017453292519943295,
  "alignment_std_speed": 1,
  "alignment_error_probability": 0.05,
  "matching_method": "interpolation",
  "matching_max_time_diff": 0.01,
  "matching_max_dist_diff": 0,
  "matching_k_nearest": 10,
  "rpe_min_distance": 100,
  "rpe_max_distance": 800,
  "rpe_distance_step": 100,
  "rpe_distance_unit": "meter",
  "rpe_use_all_pairs": true,
  "report_downsample_size": 2000,
  "report_scatter_max_std": 4,
  "report_ate_unit": "millimeter",
  "report_directed_ate": true,
  "report_histogram_opacity": 0.6,
  "report_histogram_bargap": 0.1,
  "report_histogram_barmode": "overlay",
  "report_histogram_yaxis_title": "Count",
  "report_plot_mode": "lines+markers",
  "report_scatter_mode": "markers",
  "report_colorscale": "RdYlBu_r",
  "report_x_name": "x",
  "report_y_name": "y",
  "report_z_name": "z",
  "report_x_unit": "m",
  "report_y_unit": "m",
  "report_z_unit": "m",
  "report_rot_x_name": "roll",
  "report_rot_y_name": "pitch",
  "report_rot_z_name": "yaw",
  "report_rot_unit": "°",
  "report_single_height": 450,
  "report_double_height": 540,
  "report_triple_height": 750,
  "export_single_format": "png",
  "export_single_height": 500,
  "export_single_width": 800,
  "export_single_scale": 6,
  "export_double_format": "png",
  "export_double_height": 500,
  "export_double_width": 800,
  "export_double_scale": 6,
  "export_triple_format": "png",
  "export_triple_height": 500,
  "export_triple_width": 800,
  "export_triple_scale": 6
}
```

<h3 id="update-settings-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|trajectory_id|query|string|true|none|
|body|body|[SettingsSchema](#schemasettingsschema)|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="update-settings-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="update-settings-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## Update Single Settings

<a id="opIdupdate_single_settings_settings_update_single_put"></a>

`PUT /settings/update/single`

> Body parameter

```json
{}
```

<h3 id="update-single-settings-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|trajectory_id|query|string|true|none|
|body|body|object|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="update-single-settings-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="update-single-settings-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## Get Settings

<a id="opIdget_settings_settings__trajectory_id__get"></a>

`GET /settings/{trajectory_id}`

<h3 id="get-settings-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|trajectory_id|path|string|true|none|

> Example responses

> 200 Response

```json
{
  "alignment_min_speed": 0,
  "alignment_time_start": 0,
  "alignment_time_end": 0,
  "alignment_trans_x": true,
  "alignment_trans_y": true,
  "alignment_trans_z": true,
  "alignment_rot_x": true,
  "alignment_rot_y": true,
  "alignment_rot_z": true,
  "alignment_scale": false,
  "alignment_time_shift": false,
  "alignment_use_x_speed": true,
  "alignment_use_y_speed": true,
  "alignment_use_z_speed": true,
  "alignment_lever_x": false,
  "alignment_lever_y": false,
  "alignment_lever_z": false,
  "alignment_sensor_rotation": false,
  "alignment_auto_update": false,
  "alignment_std_xyz_from": 1,
  "alignment_std_xyz_to": 1,
  "alignment_std_z_from": 1,
  "alignment_std_z_to": 1,
  "alignment_std_roll_pitch": 0.017453292519943295,
  "alignment_std_yaw": 0.017453292519943295,
  "alignment_std_speed": 1,
  "alignment_error_probability": 0.05,
  "matching_method": "interpolation",
  "matching_max_time_diff": 0.01,
  "matching_max_dist_diff": 0,
  "matching_k_nearest": 10,
  "rpe_min_distance": 100,
  "rpe_max_distance": 800,
  "rpe_distance_step": 100,
  "rpe_distance_unit": "meter",
  "rpe_use_all_pairs": true,
  "report_downsample_size": 2000,
  "report_scatter_max_std": 4,
  "report_ate_unit": "millimeter",
  "report_directed_ate": true,
  "report_histogram_opacity": 0.6,
  "report_histogram_bargap": 0.1,
  "report_histogram_barmode": "overlay",
  "report_histogram_yaxis_title": "Count",
  "report_plot_mode": "lines+markers",
  "report_scatter_mode": "markers",
  "report_colorscale": "RdYlBu_r",
  "report_x_name": "x",
  "report_y_name": "y",
  "report_z_name": "z",
  "report_x_unit": "m",
  "report_y_unit": "m",
  "report_z_unit": "m",
  "report_rot_x_name": "roll",
  "report_rot_y_name": "pitch",
  "report_rot_z_name": "yaw",
  "report_rot_unit": "°",
  "report_single_height": 450,
  "report_double_height": 540,
  "report_triple_height": 750,
  "export_single_format": "png",
  "export_single_height": 500,
  "export_single_width": 800,
  "export_single_scale": 6,
  "export_double_format": "png",
  "export_double_height": 500,
  "export_double_width": 800,
  "export_double_scale": 6,
  "export_triple_format": "png",
  "export_triple_height": 500,
  "export_triple_width": 800,
  "export_triple_scale": 6
}
```

<h3 id="get-settings-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[SettingsSchema](#schemasettingsschema)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

<h2 id="tocS_AlignmentResultSchema">AlignmentResultSchema</h2>
<!-- backwards compatibility -->
<a id="schemaalignmentresultschema"></a>
<a id="schema_AlignmentResultSchema"></a>
<a id="tocSalignmentresultschema"></a>
<a id="tocsalignmentresultschema"></a>

```json
{
  "aligned_trajectory_id": "string",
  "trans_x": 0,
  "trans_y": 0,
  "trans_z": 0,
  "rot_x": 0,
  "rot_y": 0,
  "rot_z": 0,
  "scale": 0,
  "lever_x": 0,
  "lever_y": 0,
  "lever_z": 0,
  "sensor_rot_x": 0,
  "sensor_rot_y": 0,
  "sensor_rot_z": 0
}

```

AlignmentResultSchema

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|aligned_trajectory_id|string|true|none|none|
|trans_x|number|true|none|none|
|trans_y|number|true|none|none|
|trans_z|number|true|none|none|
|rot_x|number|true|none|none|
|rot_y|number|true|none|none|
|rot_z|number|true|none|none|
|scale|number|true|none|none|
|lever_x|number|true|none|none|
|lever_y|number|true|none|none|
|lever_z|number|true|none|none|
|sensor_rot_x|number|true|none|none|
|sensor_rot_y|number|true|none|none|
|sensor_rot_z|number|true|none|none|

<h2 id="tocS_Body_upload_trajectory_trajectories_upload_post">Body_upload_trajectory_trajectories_upload_post</h2>
<!-- backwards compatibility -->
<a id="schemabody_upload_trajectory_trajectories_upload_post"></a>
<a id="schema_Body_upload_trajectory_trajectories_upload_post"></a>
<a id="tocSbody_upload_trajectory_trajectories_upload_post"></a>
<a id="tocsbody_upload_trajectory_trajectories_upload_post"></a>

```json
{
  "file": "string"
}

```

Body_upload_trajectory_trajectories_upload_post

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|file|string(binary)|true|none|none|

<h2 id="tocS_ExportFormat">ExportFormat</h2>
<!-- backwards compatibility -->
<a id="schemaexportformat"></a>
<a id="schema_ExportFormat"></a>
<a id="tocSexportformat"></a>
<a id="tocsexportformat"></a>

```json
"png"

```

ExportFormat

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|ExportFormat|string|false|none|none|

#### Enumerated Values

|Property|Value|
|---|---|
|ExportFormat|png|
|ExportFormat|svg|
|ExportFormat|jpeg|
|ExportFormat|webp|

<h2 id="tocS_HTTPValidationError">HTTPValidationError</h2>
<!-- backwards compatibility -->
<a id="schemahttpvalidationerror"></a>
<a id="schema_HTTPValidationError"></a>
<a id="tocShttpvalidationerror"></a>
<a id="tocshttpvalidationerror"></a>

```json
{
  "detail": [
    {
      "loc": [
        "string"
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}

```

HTTPValidationError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|detail|[[ValidationError](#schemavalidationerror)]|false|none|none|

<h2 id="tocS_MatchingMethod">MatchingMethod</h2>
<!-- backwards compatibility -->
<a id="schemamatchingmethod"></a>
<a id="schema_MatchingMethod"></a>
<a id="tocSmatchingmethod"></a>
<a id="tocsmatchingmethod"></a>

```json
"nearest_spatial"

```

MatchingMethod

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|MatchingMethod|string|false|none|none|

#### Enumerated Values

|Property|Value|
|---|---|
|MatchingMethod|nearest_spatial|
|MatchingMethod|nearest_temporal|
|MatchingMethod|interpolation|
|MatchingMethod|nearest_spatial_interpolation|

<h2 id="tocS_ResultSchema">ResultSchema</h2>
<!-- backwards compatibility -->
<a id="schemaresultschema"></a>
<a id="schema_ResultSchema"></a>
<a id="tocSresultschema"></a>
<a id="tocsresultschema"></a>

```json
{
  "name": "string",
  "id": "string",
  "trajectory_id": "string",
  "session_id": "string"
}

```

ResultSchema

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|true|none|none|
|id|string|true|none|none|
|trajectory_id|string|true|none|none|
|session_id|string|true|none|none|

<h2 id="tocS_SessionSchema">SessionSchema</h2>
<!-- backwards compatibility -->
<a id="schemasessionschema"></a>
<a id="schema_SessionSchema"></a>
<a id="tocSsessionschema"></a>
<a id="tocssessionschema"></a>

```json
{
  "id": "string",
  "date": "string",
  "trajectories": []
}

```

SessionSchema

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|string|true|none|none|
|date|string|true|none|none|
|trajectories|[[TrajectorySchema](#schematrajectoryschema)]|false|none|none|

<h2 id="tocS_SettingsSchema">SettingsSchema</h2>
<!-- backwards compatibility -->
<a id="schemasettingsschema"></a>
<a id="schema_SettingsSchema"></a>
<a id="tocSsettingsschema"></a>
<a id="tocssettingsschema"></a>

```json
{
  "alignment_min_speed": 0,
  "alignment_time_start": 0,
  "alignment_time_end": 0,
  "alignment_trans_x": true,
  "alignment_trans_y": true,
  "alignment_trans_z": true,
  "alignment_rot_x": true,
  "alignment_rot_y": true,
  "alignment_rot_z": true,
  "alignment_scale": false,
  "alignment_time_shift": false,
  "alignment_use_x_speed": true,
  "alignment_use_y_speed": true,
  "alignment_use_z_speed": true,
  "alignment_lever_x": false,
  "alignment_lever_y": false,
  "alignment_lever_z": false,
  "alignment_sensor_rotation": false,
  "alignment_auto_update": false,
  "alignment_std_xyz_from": 1,
  "alignment_std_xyz_to": 1,
  "alignment_std_z_from": 1,
  "alignment_std_z_to": 1,
  "alignment_std_roll_pitch": 0.017453292519943295,
  "alignment_std_yaw": 0.017453292519943295,
  "alignment_std_speed": 1,
  "alignment_error_probability": 0.05,
  "matching_method": "interpolation",
  "matching_max_time_diff": 0.01,
  "matching_max_dist_diff": 0,
  "matching_k_nearest": 10,
  "rpe_min_distance": 100,
  "rpe_max_distance": 800,
  "rpe_distance_step": 100,
  "rpe_distance_unit": "meter",
  "rpe_use_all_pairs": true,
  "report_downsample_size": 2000,
  "report_scatter_max_std": 4,
  "report_ate_unit": "millimeter",
  "report_directed_ate": true,
  "report_histogram_opacity": 0.6,
  "report_histogram_bargap": 0.1,
  "report_histogram_barmode": "overlay",
  "report_histogram_yaxis_title": "Count",
  "report_plot_mode": "lines+markers",
  "report_scatter_mode": "markers",
  "report_colorscale": "RdYlBu_r",
  "report_x_name": "x",
  "report_y_name": "y",
  "report_z_name": "z",
  "report_x_unit": "m",
  "report_y_unit": "m",
  "report_z_unit": "m",
  "report_rot_x_name": "roll",
  "report_rot_y_name": "pitch",
  "report_rot_z_name": "yaw",
  "report_rot_unit": "°",
  "report_single_height": 450,
  "report_double_height": 540,
  "report_triple_height": 750,
  "export_single_format": "png",
  "export_single_height": 500,
  "export_single_width": 800,
  "export_single_scale": 6,
  "export_double_format": "png",
  "export_double_height": 500,
  "export_double_width": 800,
  "export_double_scale": 6,
  "export_triple_format": "png",
  "export_triple_height": 500,
  "export_triple_width": 800,
  "export_triple_scale": 6
}

```

SettingsSchema

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|alignment_min_speed|number|false|none|none|
|alignment_time_start|number|false|none|none|
|alignment_time_end|number|false|none|none|
|alignment_trans_x|boolean|false|none|none|
|alignment_trans_y|boolean|false|none|none|
|alignment_trans_z|boolean|false|none|none|
|alignment_rot_x|boolean|false|none|none|
|alignment_rot_y|boolean|false|none|none|
|alignment_rot_z|boolean|false|none|none|
|alignment_scale|boolean|false|none|none|
|alignment_time_shift|boolean|false|none|none|
|alignment_use_x_speed|boolean|false|none|none|
|alignment_use_y_speed|boolean|false|none|none|
|alignment_use_z_speed|boolean|false|none|none|
|alignment_lever_x|boolean|false|none|none|
|alignment_lever_y|boolean|false|none|none|
|alignment_lever_z|boolean|false|none|none|
|alignment_sensor_rotation|boolean|false|none|none|
|alignment_auto_update|boolean|false|none|none|
|alignment_std_xyz_from|number|false|none|none|
|alignment_std_xyz_to|number|false|none|none|
|alignment_std_z_from|number|false|none|none|
|alignment_std_z_to|number|false|none|none|
|alignment_std_roll_pitch|number|false|none|none|
|alignment_std_yaw|number|false|none|none|
|alignment_std_speed|number|false|none|none|
|alignment_error_probability|number|false|none|none|
|matching_method|[MatchingMethod](#schemamatchingmethod)|false|none|none|
|matching_max_time_diff|number|false|none|none|
|matching_max_dist_diff|number|false|none|none|
|matching_k_nearest|integer|false|none|none|
|rpe_min_distance|number|false|none|none|
|rpe_max_distance|number|false|none|none|
|rpe_distance_step|number|false|none|none|
|rpe_distance_unit|[Unit](#schemaunit)|false|none|none|
|rpe_use_all_pairs|boolean|false|none|none|
|report_downsample_size|integer|false|none|none|
|report_scatter_max_std|number|false|none|none|
|report_ate_unit|[Unit](#schemaunit)|false|none|none|
|report_directed_ate|boolean|false|none|none|
|report_histogram_opacity|number|false|none|none|
|report_histogram_bargap|number|false|none|none|
|report_histogram_barmode|string|false|none|none|
|report_histogram_yaxis_title|string|false|none|none|
|report_plot_mode|string|false|none|none|
|report_scatter_mode|string|false|none|none|
|report_colorscale|string|false|none|none|
|report_x_name|string|false|none|none|
|report_y_name|string|false|none|none|
|report_z_name|string|false|none|none|
|report_x_unit|string|false|none|none|
|report_y_unit|string|false|none|none|
|report_z_unit|string|false|none|none|
|report_rot_x_name|string|false|none|none|
|report_rot_y_name|string|false|none|none|
|report_rot_z_name|string|false|none|none|
|report_rot_unit|string|false|none|none|
|report_single_height|integer|false|none|none|
|report_double_height|integer|false|none|none|
|report_triple_height|integer|false|none|none|
|export_single_format|[ExportFormat](#schemaexportformat)|false|none|none|
|export_single_height|integer|false|none|none|
|export_single_width|integer|false|none|none|
|export_single_scale|number|false|none|none|
|export_double_format|[ExportFormat](#schemaexportformat)|false|none|none|
|export_double_height|integer|false|none|none|
|export_double_width|integer|false|none|none|
|export_double_scale|number|false|none|none|
|export_triple_format|[ExportFormat](#schemaexportformat)|false|none|none|
|export_triple_height|integer|false|none|none|
|export_triple_width|integer|false|none|none|
|export_triple_scale|number|false|none|none|

<h2 id="tocS_TrajectorySchema">TrajectorySchema</h2>
<!-- backwards compatibility -->
<a id="schematrajectoryschema"></a>
<a id="schema_TrajectorySchema"></a>
<a id="tocStrajectoryschema"></a>
<a id="tocstrajectoryschema"></a>

```json
{
  "name": "string",
  "epsg": 0,
  "sorting": "string",
  "session_id": "string",
  "id": "string"
}

```

TrajectorySchema

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|true|none|none|
|epsg|integer|true|none|none|
|sorting|string|true|none|none|
|session_id|string|true|none|none|
|id|string|true|none|none|

<h2 id="tocS_Unit">Unit</h2>
<!-- backwards compatibility -->
<a id="schemaunit"></a>
<a id="schema_Unit"></a>
<a id="tocSunit"></a>
<a id="tocsunit"></a>

```json
"meter"

```

Unit

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Unit|string|false|none|none|

#### Enumerated Values

|Property|Value|
|---|---|
|Unit|meter|
|Unit|millimeter|
|Unit|second|

<h2 id="tocS_ValidationError">ValidationError</h2>
<!-- backwards compatibility -->
<a id="schemavalidationerror"></a>
<a id="schema_ValidationError"></a>
<a id="tocSvalidationerror"></a>
<a id="tocsvalidationerror"></a>

```json
{
  "loc": [
    "string"
  ],
  "msg": "string",
  "type": "string"
}

```

ValidationError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|loc|[anyOf]|true|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|integer|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|msg|string|true|none|none|
|type|string|true|none|none|

