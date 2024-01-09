import credentials
from intersight.api import workflow_api
from intersight.rest import ApiException
from intersight.model.workflow_workflow_info import WorkflowWorkflowInfo
from intersight.model.mo_base_mo_relationship import MoBaseMoRelationship
from intersight.model.workflow_workflow_definition_relationship import WorkflowWorkflowDefinitionRelationship

# Variables. Change accordingly
workflow_name = 'Create NTP Policy'
org_moid = '636d24fc6972652d3071677c'

workflow_inputs = {
    "name": "Boris-ntp-test-delete"
}

# Authenticate
api_client = credentials.config_credentials()


# Get Workflow Moid based on workflow name

def get_workflow_definitions(api_client):
    """ Gets the list of workflows """
    api_instance = workflow_api.WorkflowApi(api_client)

    try:
        query_filter = "Label eq '{0}'".format(workflow_name)
        api_response = api_instance.get_workflow_workflow_definition_list(filter=query_filter,top=0,_check_return_type=False)
        return api_response.results[0]['Moid']
    except ApiException as e:
        print("Exception when calling WorkflowApi->get_workflow_workflow_definition_list: %s\n" % e)

workflow_moid = get_workflow_definitions(api_client)

#### Workflow Payload ###

ass_obj = MoBaseMoRelationship(
   moid=org_moid,
   object_type="organization.Organization",
   class_id="mo.MoRef"
)

workflow_def = WorkflowWorkflowDefinitionRelationship(
   moid = workflow_moid,
   object_type = "workflow.WorkflowDefinition",
   class_id="mo.MoRef"
)

# Workflow Definition

workflow = WorkflowWorkflowInfo(
   name="Create an NTP Policy",
   associated_object=ass_obj,
   action="Start",
   input = workflow_inputs,
   workflow_definition=workflow_def
) 


def execute_workflow(workflow, api_client):
    """ Execute a Workflow """
    api_instance = workflow_api.WorkflowApi(api_client)

    try:
        api_response = api_instance.create_workflow_workflow_info(workflow,_check_return_type=False)
        return api_response
    
    except ApiException as e:
        print("Exception when calling WorkflowApi->create_workflow_workflow_info: %s\n" % e)

# Execute the Workflow
exec = execute_workflow(workflow,api_client)

print(exec)
print()
print('Execution Moid: {}'.format(exec['moid']))
print('Executed by: {}'.format(exec['email']))
