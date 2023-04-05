
import copy
import importlib
import os
import pkgutil
import sys
import yaml

class ScopeActions :

  # Class variables and definitions

  actions = {} # Class variable

  def method(scopeStr, packed=True, kwargsDict={}) :
    def decorator_scopeMethod(func) :
      scopeParts = scopeStr.split('.')
      #print(yaml.dump(scopeParts))
      curScope = ScopeActions.actions
      for aScopePart in scopeParts :
        #print(aScopePart)
        if aScopePart not in curScope :
          curScope[aScopePart] = {}
        curScope = curScope[aScopePart]
      curScope['__action__'] = {
        'scope'  : scopeStr,
        'method' : func,
        'packed' : packed,
        'kwargs' : copy.deepcopy(kwargsDict)
      }
      #print(yaml.dump(ScopeActions.actions))
      return func
    return decorator_scopeMethod

  def hasAction(scopeStr) :
    scopeParts = scopeStr.split('.')
    curScope = ScopeActions.actions
    for aPart in scopeParts :
      if aPart in curScope :
        curScope = curScope[aPart]
      else :
        return False
    return True

  def getAction(scopeStr) :
    scopeParts = scopeStr.split('.')
    curScope = ScopeActions.actions
    for aPart in scopeParts :
      if aPart in curScope :
        curScope = curScope[aPart]
      else :
        return {}
    return curScope

  async def run(scopeStr) :
    scopeParts = scopeStr.split('.')

  def pattern(scopeStr, aPattern) :
    scopeParts = scopeStr.split('.')
    #print(yaml.dump(scopeParts))
    curScope = ScopeActions.actions
    for aScopePart in scopeParts :
      #print(aScopePart)
      if aScopePart not in curScope :
        curScope[aScopePart] = {}
      curScope = curScope[aScopePart]
    curScope['__pattern__'] = {
      'scope'   : scopeStr,
      'pattern' : aPattern,
    }
    #print(yaml.dump(ScopeActions.actions))

  def loadActionsFromDir(aDir) :
    #Load/import all scope actions found in the aDir directory.

    if aDir.startswith('~') :
      aDir = os.path.expanduser(aDir)
    aPkgPath = os.path.basename(aDir)
    aSysPath = os.path.dirname(aDir)
    if aSysPath not in sys.path :
      sys.path.insert(0, aSysPath)

    for (_, module_name, _) in pkgutil.iter_modules([aDir]) :
      theModule = importlib.import_module(aPkgPath+'.'+module_name)

  # Instance varaibles and definitions

  def __init__(self, ctx=None, debugIO=None) :
    self.context = ctx
    self.debugIO = debugIO

  def getContext(self) :
    return self.context

