
import copy
import glob
import importlib.resources
import json
import os
#import pprint
import yaml

from contextLangServer.processor.scopeActions import ScopeActions

# see:
#  https://code.visualstudio.com/api/language-extensions/syntax-highlight-guide
#  https://macromates.com/manual/en/language_grammars

class Grammar :

  # Class variables and definitions

  repository = {}
  scopes2patterns = {}
  baseScopes = {}

  def addPatternsToRepository(aName, aScope, patterns) :
    if aName in Grammar.repository :
      print("WARNING: Duplicate pattern name {aPatternName} in repository.")
      print("  last pattern wins! (This may not be what you want)")
      print("")
    Grammar.repository[aName] = patterns
    if aScope :
      Grammar.scopes2patterns[aScope] = aName

  def loadFromDict(gDict) :

    # deal with the grammar's repository
    if 'repository' in gDict :
      for aPatternName, aPattern in gDict['repository'].items() :
        aPatternScope = None
        if 'name' in aPattern: aPatterScope = aPattern['name']
        Grammar.addPatternsToRepository(aPatternName, aPatternScope, aPattern)
  
    # deal with the grammar's base scope/pattern
    scopeName = None
    if 'scopeName' in gDict :
      scopeName = gDict['scopeName']
    if 'patterns' in gDict :
      if not scopeName :
        print("WARNING: loading a grammer with no scope! ")
        print("  this means that this grammar can not be directly used!")
        print("")
      Grammar.addPatternsToRepository(
        scopeName, scopeName, {
          'patterns' : gDict['patterns']
        }
      )
  
    # deal with the grammar's info
    info = {}
    if 'fileTypes' in gDict :
      info['fileTypes'] = gDict['fileTypes']
    if 'foldingStartMarker' in gDict :
      info['foldingStartMarker'] = gDict['foldingStartMarker']
    if 'foldingStopMarker' in gDict :
      info['foldingStopMarker'] = gDict['foldingStopMarker']
    if 'firstLineMatch' in gDict :
      info['firstLineMatch'] = gDict['firstLineMatch']
    info['scopeName'] = scopeName
    Grammar.baseScopes[scopeName] = info
  

  def loadFromFile(aGrammarPath) :
    with open(aGrammarPath) as grammarFile :
      grammarDict = json.loads(grammarFile.read())
      Grammar.loadFromDict(grammarDict)

  def loadFromResourceDir(aGrammarPackage) :
    syntaxDir = importlib.resources.files(aGrammarPackage)
    for aSyntaxFile in syntaxDir.iterdir() :
      if not aSyntaxFile.name.endswith('tmGrammar.json') : continue
      with importlib.resources.as_file(aSyntaxFile) as syntaxFile :
        syntaxStr = syntaxFile.read_text()
        syntaxDict = json.loads(syntaxStr)
        Grammar.loadFromDict(syntaxDict)

  def loadFromVSCodeDir(
    anExtensionDir=None,
    anAuthor='lpic-tools',
    anExtension='context-lpic-tools',
    grammarExt='tmGrammar.json'
  ) :
    if anExtensionDir is None :
      homeDir = os.path.expanduser("~")
      anExtensionDir = os.path.join(homeDir, '.vscode', 'extensions')
      if not os.path.exists(anExtensionDir) :
        anExtensionDir = os.path.join(homeDir, '.vscode-oss', 'extensions')
    if not os.path.exists(anExtensionDir) :
      print("Can not load grammars from VSCode directory")
      print("  no code directory found")
      return
    extensionGlob = f"{anAuthor}.{anExtension}*/*/*{grammarExt}"
    print(extensionGlob)
    for anExtensionPath in glob.iglob(extensionGlob, root_dir=anExtensionDir) :
      #print(anExtensionPath)
      Grammar.loadFromFile(os.path.join(anExtensionDir, anExtensionPath))

  def collectPatternReferences(aScope) :
    repo = Grammar.repository
    patRefs = {}
    if aScope : patRefs[aScope] = True
    for aName, aPattern in repo.items() :
      #print(aName)
      if 'patterns' in aPattern :
        for aSubPattern in aPattern['patterns'] :
          if 'include' in aSubPattern :
            aPatRef = aSubPattern['include']
            if aPatRef == '$self' : continue
            #print(f"  {aPatRef}")
            patRefs[aPatRef] = True
    return list(patRefs.keys())
  
  def collectScopePaths(withAction=False) :
    # base case
    aStruct = Grammar.repository
    spDict = {}
    spKeys = []
    changed = True
    while changed :
      changed = Grammar._collectScopePaths(
        aStruct, spDict, spKeys, withAction=withAction
      )
      spKeys = list(spDict.keys())
    return spDict

  def _collectScopePaths(aStruct, spDict, spKeys, withAction=False) :
    # collectScopePaths recursion 
    changed = False
    if isinstance(aStruct, dict) :
      for aKey, aValue in aStruct.items() :
        if aKey in [ 'name', 'include' ] : 
          strippedValue = aValue.lstrip('#')
          if ScopeActions.hasAction(strippedValue) :
            action = ScopeActions.getAction(strippedValue)
            if '__action__' in action and 'method' in action['__action__'] :
              theMethod = action['__action__']['method']
              if 'action' not in spDict : changed = True
              spDict['action'] = theMethod.__module__+'.'+theMethod.__name__
              if aKey not in spDict : changed = True
              spDict[aKey] = aValue
          elif strippedValue in spKeys :
            if aKey not in spDict : changed = True
            spDict[aKey] = aValue
          elif not withAction :
            if aKey not in spDict : changed = True
            spDict[aKey] = aValue
        else :
          spLevelDict = {}
          if aKey in spDict : spLevelDict = spDict[aKey]
          newChanged = Grammar._collectScopePaths(
            aStruct=aValue, spDict=spLevelDict,
            spKeys=spKeys, withAction=withAction
          )
          if aKey not in spDict and spLevelDict : 
            changed = True
            spDict[aKey] = spLevelDict
          changed = changed or newChanged
    elif isinstance(aStruct, list) :
      for anIndex, aValue in enumerate(aStruct) :
        spLevelDict = {}
        if anIndex in spDict : spLevelDict = spDict[anIndex]
        newChanged = Grammar._collectScopePaths(
          aStruct=aValue, spDict=spLevelDict, 
          spKeys=spKeys, withAction=withAction
        )
        if anIndex not in spDict and spLevelDict :
          changed = True
          spDict[anIndex] = spLevelDict
        changed = changed or newChanged
    return changed

  def removePatternsWithoutActions() :
    # base case
    scopePaths = Grammar.collectScopePaths(withAction=True)
    repo = Grammar.repository
    names2delete = []
    for aName, aPattern in repo.items() :
      if aName not in scopePaths : 
        names2delete.append(aName)
      else :
        Grammar._removePatternsWithoutActions(aPattern, scopePaths[aName])
    for aName in names2delete :
      del repo[aName]

  def _removePatternsWithoutActions(aStruct, spLevelDict) :
    # removePatternsWithoutActions recursion...
    if isinstance(aStruct, dict) :
      for aKey, aValue in aStruct.items() :
        if aKey == 'patterns' :
          indices2delete = []
          for anIndex, aPattern in enumerate(aValue) :
            if anIndex not in spLevelDict['patterns'] : 
              indices2delete.append(anIndex)
            elif anIndex in spLevelDict['patterns'] :
              Grammar._removePatternsWithoutActions(
                aPattern, spLevelDict['patterns'][anIndex]
              )
          indices2delete.reverse()
          for anIndex in indices2delete :
            del aValue[anIndex]
        elif aKey in spLevelDict :
          Grammar._removePatternsWithoutActions(aValue, spLevelDict[aKey])

    elif isinstance(aStruct, list) :
      indices2delete = []
      for anIndex, aPattern in enumerate(aStruct) :
        if anIndex not in spLevelDict :
          indices2delete.append(anIndex)
          continue
        Grammar._removePatternsWithoutActions(aPattern, spLevelDict[anIndex])
      indices2delete.reverse()
      for anIndex in indices2delete :
        del aValue[anIndex]
      
  def pruneRepository(aScope) :
    patRefs     = Grammar.collectPatternReferences(aScope)
    repo        = Grammar.repository
    keys2delete = []
    for aName in repo :
      if aName not in patRefs and f"#{aName}" not in patRefs :
        keys2delete.append(aName)
    for aName in keys2delete :
      del repo[aName]
    return keys2delete

  def checkRepository(aScope) :
    patRefs = Grammar.collectPatternReferences(aScope)
    repo    = Grammar.repository
    missingPats = []
    extraPats   = []
    for aName in patRefs :
      aName = aName.lstrip('#')
      if aName not in repo :
        missingPats.append(aName)
    for aName in repo :
      if aName not in patRefs and f"#{aName}" not in patRefs :
        extraPats.append(aName)
    return missingPats, extraPats, patRefs

  def saveToDict(aScope) :
    if aScope not in Grammar.baseScopes :
      return None
    gDict = Grammar.baseScopes[aScope]
    gDict['patterns'] = [
      { 'include' : aScope }
    ]
    gDict['repository'] = copy.deepcopy(Grammar.repository)
    return gDict

  def savedToFile(aScope, aGrammarPath) :
    grammarDict = Grammar.saveToDict(aScope)
    if grammarDict :
      grammarStr = json.dumps(grammarDict, indent=2) 
      with open(aGrammarPath, 'w') as grammarFile :
        grammarFile.write(grammarStr)
        grammarFile.write("\n")
      return True
    return False

  def dumpGrammar() :
    print("------------------------------------------------")
    print(yaml.dump(Grammar.repository))
    print("------------------------------------------------")
    print(yaml.dump(Grammar.scopes2patterns))
    print("------------------------------------------------")
    print(yaml.dump(Grammar.baseScopes))
    print("------------------------------------------------")

