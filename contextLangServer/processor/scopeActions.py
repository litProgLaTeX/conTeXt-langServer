
import copy
import importlib
import os
import pkgutil
import sys
import yaml

class ScopeActions :

  # Class variables and definitions

  actions = {} # Class variable

  def addMethod(scopeStr, aFunc, packed=True, kwargsDict={}) :
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
      'method' : aFunc,
      'packed' : packed,
      'kwargs' : copy.deepcopy(kwargsDict)
    }
    #print(yaml.dump(ScopeActions.actions))

  def method(scopeStr, packed=True, kwargsDict={}) :
    def decorator_scopeMethod(func) :
      ScopeActions.addMethod(
        scopeStr, func, packed=packed, kwargsDict=kwargsDict
      )
      return func
    return decorator_scopeMethod

  async def runTheAction(anAction) :
    if anAction and 'func' in anAction :
      kwargsDict = {}
      if 'kwargsDict' in anAction : kwargsDict = anAction['kwargsDict']
      if 'packed' in anAction :
        return await anAction['func'](kwargsDict)
      else :
        return await anAction['func'](**kwargsDict)

  def getAction(scopeStr) :
    scopeParts = scopeStr.split('.')
    curScope = ScopeActions.actions
    for aPart in scopeParts :
      if aPart in curScope : curScope = curScope[aPart]
      else                 : return None
    if '__action__' not in curScope : return None
    return curScope['__action__']

  def hasAction(scopeStr) :
    return ScopeActions.getAction(scopeStr) is not None

  async def run(scopeStr) :
    return await ScopeActions.runTheAction(ScopeActions.getAction(scopeStr))

  def getAllActions(scopeStr) :
    actionsFound = []
    scopeParts = scopeStr.split('.')
    curScope = ScopeActions.actions
    for aPart in scopeParts :
      if aPart in curScope :
        curScope = curScope[aPart]
      else :
        return actionsFound
      if '__action__' in curScope :
        actionsFound.insert(0, curScope['__action__'])
    return actionsFound

  def hasAnyAction(scopeStr) :
    return 0 < len(ScopeActions.getAction(scopeStr))

  async def runMostSpecific(scopeStr) :
    someActions = ScopeActions.getAllActions(scopeStr)
    if someActions :
      return await ScopeActions.runTheAction(someActions[0])

  """
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
  """

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

  def listActions() :
    actions = ScopeActions.actions
    print("--actions----------------------------------------------------")
    ScopeActions._listActions('', actions)
    print("-------------------------------------------------------------")

  def _listActions(baseScope, actions) :
    if '__action__' in actions :
      theAction = actions['__action__']
      print("{} : {}".format(
        theAction['scope'],
        'silly'
      ))
    for aPartKey in sorted(actions.keys()) :
      ScopeActions._listActions(
        baseScope+'.'+aPartKey,
        actions[aPartKey]
      )

  """
  # Instance varaibles and definitions

  def __init__(self, ctx=None, debugIO=None) :
    self.context = ctx
    self.debugIO = debugIO

  def getContext(self) :
    return self.context
  """
