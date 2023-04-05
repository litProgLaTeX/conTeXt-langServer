

import asyncio
import pytest
import sys
import yaml

from contextLangServer.processor.scopeActions import ScopeActions

@ScopeActions.method('simple.Str.Param')
def simpleStrParam(disp, ctx, aMessage, **kwargs) :
  print("-----------------------------------------")
  print('simpleStrParam')
  print(aMessage)
  print("-----------------------------------------")
  ctx.append({
    'method'   : 'simpleStrParam',
    'msg'      : aMessage,
    'kwargs'   : kwargs,
    'dispType' : type(disp)
  })

  
def test_simpleStrParam() :
  actions = ScopeActions.actions
  #print("----------------------------------------------------------------")
  #print(yaml.dump(actions))
  #print("----------------------------------------------------------------")
  assert isinstance(actions, dict)
  assert 'simple' in actions
  assert 'Str' in actions['simple']
  assert 'Param' in actions['simple']['Str']
  assert '__action__' in actions['simple']['Str']['Param']
  action = actions['simple']['Str']['Param']['__action__']
  #print("----------------------------------------------------------------")
  #print(yaml.dump(action))
  #print("----------------------------------------------------------------")
  assert isinstance(action['kwargs'], dict)
  assert not action['kwargs']
  assert action['packed']
  assert action['scope'] == 'simple.Str.Param'
  #print(type(simpleStrParam))
  assert isinstance(action['method'], type(simpleStrParam))
  assert action['method'] == simpleStrParam
  assert ScopeActions.hasAction('simple.Str.Param')
  assert ScopeActions.hasAction('simple.Str')
  assert ScopeActions.hasAction('simple')
  assert not ScopeActions.hasAction('does.not.exist')
  #assert False

def test_loadedStrParam() :
  if 'loaded' not in ScopeActions.actions :
    ScopeActions.loadActionsFromDir('tests/actions')
  actions = ScopeActions.actions
  print("----------------------------------------------------------------")
  print(yaml.dump(actions))
  print("----------------------------------------------------------------")
  assert isinstance(actions, dict)
  assert 'loaded' in actions
  assert 'Str' in actions['loaded']
  assert 'Param' in actions['loaded']['Str']
  assert '__action__' in actions['loaded']['Str']['Param']
  action = actions['loaded']['Str']['Param']['__action__']
  print("----------------------------------------------------------------")
  print(yaml.dump(action))
  print("----------------------------------------------------------------")
  assert isinstance(action['kwargs'], dict)
  assert not action['kwargs']
  assert action['packed']
  assert action['scope'] == 'loaded.Str.Param'
  #print(type(simpleStrParam))
  assert isinstance(action['method'], type(simpleStrParam))
#  assert action['method'] == simpleStrParam
  assert ScopeActions.hasAction('loaded.Str.Param')
  assert ScopeActions.hasAction('loaded.Str')
  assert ScopeActions.hasAction('loaded')
  assert not ScopeActions.hasAction('does.not.exist')
  #assert False

