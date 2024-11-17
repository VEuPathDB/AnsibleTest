from __future__ import absolute_import
from copy import deepcopy
from ansible.plugins.action import ActionBase
from ansible.plugins.action.template import ActionModule as TemplateActionModule
from ansible.errors import AnsibleError
import json

class ActionModule(TemplateActionModule, ActionBase):
  TRANSFERS_FILES = False

  def run(self, tmp=None, task_vars=None):
    custom_vars = {
    "project" : "Plasmo",
    "fancy_project": '{{ project }}'
    }
    custom_vars['ansible_facts'] = task_vars['ansible_facts']

    return super(ActionModule, self).run(tmp, task_vars)

