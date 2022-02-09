#!/usr/bin/env python3
# #####################################################################################################################
#  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.                                                 #
#                                                                                                                     #
#  Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance     #
#  with the License. A copy of the License is located at                                                              #
#                                                                                                                     #
#  http://www.apache.org/licenses/LICENSE-2.0                                                                         #
#                                                                                                                     #
#  or in the 'license' file accompanying this file. This file is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES  #
#  OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions     #
#  and limitations under the License.                                                                                 #
# #####################################################################################################################
from aws_cdk import core
from lib.mlops_orchestrator_stack import MLOpsStack
from lib.blueprints.byom.model_monitor import ModelMonitorStack
from lib.blueprints.byom.realtime_inference_pipeline import BYOMRealtimePipelineStack
from lib.blueprints.byom.byom_batch_pipeline import BYOMBatchStack
from lib.blueprints.byom.single_account_codepipeline import SingleAccountCodePipelineStack
from lib.blueprints.byom.multi_account_codepipeline import MultiAccountCodePipelineStack
from lib.blueprints.byom.byom_custom_algorithm_image_builder import BYOMCustomAlgorithmImageBuilderStack
from lib.aws_sdk_config_aspect import AwsSDKConfigAspect
from lib.blueprints.byom.pipeline_definitions.cdk_context_value import get_cdk_context_value

app = core.App()
solution_id = get_cdk_context_value(app, "SolutionId")
version = get_cdk_context_value(app, "Version")

mlops_stack_single = MLOpsStack(
    app,
    "mlops-workload-orchestrator-single-account",
    description=f"({solution_id}-sa) - MLOps Workload Orchestrator (Single Account Option). Version {version}",
)

# add AWS_SDK_USER_AGENT env variable to Lambda functions
core.Aspects.of(mlops_stack_single).add(AwsSDKConfigAspect(app, "SDKUserAgentSingle", solution_id, version))

mlops_stack_multi = MLOpsStack(
    app,
    "mlops-workload-orchestrator-multi-account",
    multi_account=True,
    description=f"({solution_id}-ma) - MLOps Workload Orchestrator (Multi Account Option). Version {version}",
)

core.Aspects.of(mlops_stack_multi).add(AwsSDKConfigAspect(app, "SDKUserAgentMulti", solution_id, version))

BYOMCustomAlgorithmImageBuilderStack(
    app,
    "BYOMCustomAlgorithmImageBuilderStack",
    description=(
        f"({solution_id}byom-caib) - Bring Your Own Model pipeline to build custom algorithm docker images"
        f"in MLOps Workload Orchestrator. Version {version}"
    ),
)

batch_stack = BYOMBatchStack(
    app,
    "BYOMBatchStack",
    description=(f"({solution_id}byom-bt) - BYOM Batch Transform pipeline in AWS MLOps Framework. Version {version}"),
)

core.Aspects.of(batch_stack).add(AwsSDKConfigAspect(app, "SDKUserAgentBatch", solution_id, version))

data_quality_monitor_stack = ModelMonitorStack(
    app,
    "DataQualityModelMonitorStack",
    monitoring_type="DataQuality",
    description=(f"({solution_id}byom-dqmm) - DataQuality Model Monitor pipeline. Version {version}"),
)

core.Aspects.of(data_quality_monitor_stack).add(
    AwsSDKConfigAspect(app, "SDKUserAgentDataMonitor", solution_id, version)
)

model_quality_monitor_stack = ModelMonitorStack(
    app,
    "ModelQualityModelMonitorStack",
    monitoring_type="ModelQuality",
    description=(f"({solution_id}byom-mqmm) - ModelQuality Model Monitor pipeline. Version {version}"),
)

core.Aspects.of(model_quality_monitor_stack).add(
    AwsSDKConfigAspect(app, "SDKUserAgentModelQuality", solution_id, version)
)

model_bias_monitor_stack = ModelMonitorStack(
    app,
    "ModelBiasModelMonitorStack",
    monitoring_type="ModelBias",
    description=(f"({solution_id}byom-mqmb) - ModelBias Model Monitor pipeline. Version {version}"),
)

core.Aspects.of(model_bias_monitor_stack).add(AwsSDKConfigAspect(app, "SDKUserAgentModelBias", solution_id, version))


model_explainability_monitor_stack = ModelMonitorStack(
    app,
    "ModelExplainabilityModelMonitorStack",
    monitoring_type="ModelExplainability",
    description=(f"({solution_id}byom-mqme) - ModelExplainability Model Monitor pipeline. Version {version}"),
)

core.Aspects.of(model_explainability_monitor_stack).add(
    AwsSDKConfigAspect(app, "SDKUserAgentModelExplainability", solution_id, version)
)


realtime_stack = BYOMRealtimePipelineStack(
    app,
    "BYOMRealtimePipelineStack",
    description=(f"({solution_id}byom-rip) - BYOM Realtime Inference Pipeline. Version {version}"),
)

core.Aspects.of(realtime_stack).add(AwsSDKConfigAspect(app, "SDKUserAgentRealtime", solution_id, version))

SingleAccountCodePipelineStack(
    app,
    "SingleAccountCodePipelineStack",
    description=(f"({solution_id}byom-sac) - Single-account codepipeline. Version {version}"),
)

MultiAccountCodePipelineStack(
    app,
    "MultiAccountCodePipelineStack",
    description=(f"({solution_id}byom-mac) - Multi-account codepipeline. Version {version}"),
)


app.synth()
