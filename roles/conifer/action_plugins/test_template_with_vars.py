from __future__ import absolute_import
from copy import deepcopy
from ansible.plugins.action import ActionBase
from ansible.plugins.action.template import ActionModule as TemplateActionModule
from ansible.errors import AnsibleError
from ansible.module_utils.common._collections_compat import Mapping
import json
import re

class ActionModule(TemplateActionModule, ActionBase):
  TRANSFERS_FILES = False

  def run(self, tmp=None, task_vars=None):
    custom_vars = self._task.args.get('vars', None)

    # remove parameters not allowed, nor needed, by parent ActionModule    
    if 'vars' in self._task.args:
      self._task.args.pop('vars')

    if custom_vars is None:
      return super(ActionModule, self).run(tmp, task_vars)

    if not isinstance(custom_vars, dict):
      raise AnsibleError(
        "The {0} vars parameter must be a dictionary, got a {1}.".
          format(self._task.action, type(custom_vars).__name__)
      )

    #custom_vars['hostvars'] = deepcopy(custom_vars)
    #custom_vars['vars'] = deepcopy(custom_vars)
    custom_vars['ansible_facts'] = task_vars['ansible_facts']

    #print(json.dumps(custom_vars, indent=4))
    #print("\n\n\n\n\n\n\n")
    return super(ActionModule, self).run(tmp, custom_vars)

#  def run(self, tmp=None, task_vars=None):
#    custom_vars = {
#    "project" : "Plasmo",
#    "fancy_project": '{{ project }}'
#    }
#    custom_vars['ansible_facts'] = task_vars['ansible_facts']

    #self.re_filter = re.compile('({0})'.format('=c='))

    #custom_vars['ansible_facts'] = task_vars['ansible_facts']
    #print("\nBEFORE: " + str(task_vars))
    #task_vars = self.scrub(task_vars, 1)
    #print("\nAFTER:" + str(task_vars))

#    return super(ActionModule, self).run(tmp, task_vars)

  def scrub(self, d, level):
    if isinstance(d, dict) or isinstance(d, Mapping):
      print("Scrubbing dictionary, Level " + str(level))
      d2 = dict(d)
      for k in d2.keys():
        if k == 'hostvars':
          print("Skipping hostvars key")
        elif isinstance(d[k], dict) or isinstance(d[k], Mapping):
          print("Found nested structure under " + k)
          d[k] = self.scrub(d[k], level + 1)
          if len(d[k]) == 0:
            del d[k]
        elif d[k] is None or (isinstance(d[k], str) and self.re_filter.match(d[k])):
          del d[k]
    else:
      print("Not a dictionary!")
    return d
