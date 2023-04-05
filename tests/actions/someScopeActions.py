
from contextLangServer.processor.scopeActions import ScopeActions

# for the scope actions tests
#
@ScopeActions.method('loaded.Str.Param')
def loadedStrParam(disp, ctx, aMessage, **kwargs) :
  print("-----------------------------------------")
  print('loadedStrParam')
  print(aMessage)
  print("-----------------------------------------")
  ctx.append({
    'method'   : 'loadedStrParam',
    'msg'      : aMessage,
    'kwargs'   : kwargs,
    'dispType' : type(disp)
  })

# for the grammar tests
#
@ScopeActions.method('source.lua')
def sourceLua(disp, ctx, aMessage, **kwargs) :
  print("-----------------------------------------")
  print('sourceLua')
  print(aMessage)
  print("-----------------------------------------")
  ctx.append({
    'method'   : 'sourceLua',
    'msg'      : aMessage,
    'kwargs'   : kwargs,
    'dispType' : type(disp)
  })

