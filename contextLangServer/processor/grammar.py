
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
  scopes2rules = {}
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
      Grammar.addPatternsToRepository(
        scopeName, scopeName, {
          'patterns' : gDict['patterns']
        }
      )
      if scopeName :
        Grammar.repository[scopeName]['name'] = scopeName
      else :
        print("WARNING: loading a grammer with no scope! ")
        print("  this means that this grammar can not be directly used!")
        print("")
  
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

  def collectPatternReferences(someScopes=None) :
    repo = Grammar.repository
    patRefs = {}
    if someScopes is None :
      for aScope in Grammar.baseScopes.keys() :
        patRefs[aScope] = True
    elif isinstance(someScopes, str) :
      patRefs[someScopes] = True
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
  

  def addScopeRules(aScope, aRule, patternName=None) :
    if 'name' in aRule :
      if aRule['name'] != aScope :
        ruleName = aRule['name']
        newRule = {
          'name' : ruleName
        }
        if ScopeActions.hasAction(ruleName) :
          action = ScopeActions.getAction(ruleName)
          if '__action__' in action and 'method' in action['__action__'] :
            theMethod = action['__action__']['method']
            newRule['action'] = theMethod.__module__+'.'+theMethod.__name__

        if patternName : newRule['pattern'] = patternName
        if 'begin' in aRule :
          newRule['begin'] = aRule['begin']
          if 'beginCaptures' in aRule :
            newRule['beginCaptures'] = aRule['beginCaptures']
        if 'match' in aRule :
          newRule['match'] = aRule['match']
          if 'captures' in aRule : 
            newRule['captures'] = aRule['captures']
        Grammar.scopes2rules[aScope]['rules'].append(newRule)
        return
    if 'end' in aRule : 
      anEndRule = {
        'match' : aRule['end']
      }
      if 'endCaptures' in aRule :
        anEndRule['captures'] = aRule['endCaptures']
      Grammar.scopes2rules[aScope]['endRules'].append(anEndRule)
    if 'patterns' in aRule :
      for aPattern in aRule['patterns'] :
        Grammar.addScopeRules(aScope, aPattern)
    if 'include' in aRule :
      includeKey = aRule['include'].lstrip('#')
      if includeKey in Grammar.repository :
        Grammar.addScopeRules(
          aScope, Grammar.repository[includeKey], includeKey
        )

  def addScope(aScope, howFound, aRule=None) :
    s2r = Grammar.scopes2rules
    if aScope not in s2r : s2r[aScope] = {
      'found'    : howFound,
      'endRules' : [],
      'rules'    : []
    }
    if aRule : Grammar.addScopeRules(aScope, aRule)

  def collectRules() :
    # base case
    for aKey, aRule in Grammar.repository.items() :
      Grammar._collectRules(aRule)
    return Grammar.scopes2rules

  def _collectRules(aRule) :
    if 'name' in aRule :
      Grammar.addScope(aRule['name'], 'rule.name', aRule)
      #return
    if 'include' in aRule and aRule['include'][0] not in '#$' :
      Grammar.addScope(aRule['include'], 'include.name')
    for aCapKey in ['captures', 'beginCaptures', 'endCaptures'] :
      if aCapKey in aRule : 
        for aKey, aCapture in aRule[aCapKey].items() :
          if 'name' in aCapture :
            Grammar.addScope(aCapture['name'], f'{aCapKey}.name')
    if 'patterns' in aRule :
      for aPattern in aRule['patterns'] :
        Grammar._collectRules(aPattern)

  def collectScopePaths(withAction=False) :
    return sorted(Grammar.collectRules().keys())

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
      
  def pruneRepository(someScopes=None) :
    keys2keep   = {}
    keys2delete = []
    repo        = Grammar.repository
    patRefs     = Grammar.collectPatternReferences(someScopes)
    for aName in repo :
      if aName in patRefs or f"#{aName}" in patRefs :
        keys2keep[aName] = True
    for aKey in list(repo.keys()):
      if aKey not in repo :
        keys2delete.append(aKey)
        del repo[aKey]
    return sorted(keys2delete)

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
    print("--repository -----------------------------------")
    print(yaml.dump(Grammar.repository))
    print("--scopes 2 patterns_----------------------------")
    print(yaml.dump(Grammar.scopes2patterns))
    print("--base scopes-----------------------------------")
    print(yaml.dump(Grammar.baseScopes))
    print("------------------------------------------------")

  def matchUsing(aLine, aScope) :
    if aScope not in Grammar.scopes2patterns : return None
    aPattern = Grammar.scopes2patterns[aScope]
    if aPattern not in Grammar.repository : return None
    aRule = Gramamr.repository[aPattern]