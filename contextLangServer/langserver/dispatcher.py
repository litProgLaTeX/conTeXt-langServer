
import asyncio
import copy
import functools
import yaml

class Dispatcher :
  # Class variables and definitions

  methods = {} # Class variable

  def lsRequest(route, packed=True, kwargsDict={}, file=__file__) :
    def decorator_routeMethod(asyncMethodFunc) :
      if route not in Dispatcher.methods :
        Dispatcher.methods[route] = []
      Dispatcher.methods[route].insert(0, {
        'route'  : route,
        'method' : asyncMethodFunc,
        'packed' : packed,
        'kwargs' : copy.deepcopy(kwargsDict),
        'file'   : file
      })
      return asyncMethodFunc
    return decorator_routeMethod

  lsNotification = lsRequest  # alias

  # Instance varaibles and definitions

  def __init__(self, jsonRpc, ctx=None, debugIO=None) :
    self.jsonRpc = jsonRpc
    self.context = ctx
    self.debugIO = debugIO
    self.continueDispatching = True

  def getMethodsFor(self, aRoute) :
    if aRoute not in self.methods : return []
    return self.methods[aRoute]

  def getContext(self) :
    return self.context

  def stopDispatching(self) :
    self.continueDispatching = False

  def reportMethods(self) :
    if not self.debugIO : return
    routes = sorted(self.methods.keys())
    for aRoute in routes :
      someMethods = self.methods[aRoute]
      for anIndex, aMethod in enumerate(someMethods) :
        self.debugIO.write(f"{aMethod['route']}[{anIndex}] <{aMethod['file']}>\n")

  def listMethods(self) :
    return list(self.methods.keys())

  async def dispatchOnce(self) :
    aMethod, someParams, anId = await self.jsonRpc.receive()
    if aMethod not in self.methods or not self.methods[aMethod] :
      await self.jsonRpc.sendError(f"No method found for [{aMethod}]")
      return
    aMethodConfig = self.methods[aMethod][0]
    if not aMethodConfig : 
      await self.jsonRpc.sendError(f"No method defined for [{aMethod}]")
      return
    if 'method' not in aMethodConfig :
      await self.jsonRpc.sendError(f"No method provided for [{aMethod}]")
      return
    aMethodFunc = aMethodConfig['method']
    if not asyncio.iscoroutinefunction(aMethodFunc) : 
      await self.jsonRpc.sendError(f"No coroutine defined for [{aMethod}]")
      return
    kwargs = {} 
    if 'kwargs' in aMethodConfig :
      kwargs = copy.deepcopy(aMethodConfig['kwargs'])
    kwargs['context'] = self.context
    kwargs['id'] = anId
    if isinstance(someParams, list)   : pass
    elif isinstance(someParams, dict) : 
      for aKey, aValue in someParams.items() :
        kwargs[aKey] = aValue
      someParams = []
    else                              : someParams = [ someParams ]
    if self.debugIO :
        self.debugIO.write("\n-dispatcher-----------------------------\n")
        self.debugIO.write(f"method: {aMethod}\n")
        self.debugIO.write(f"id: {anId}\n")
        self.debugIO.write("params:\n")
        self.debugIO.write(yaml.dump(someParams))
        self.debugIO.write("kwargs:\n")
        self.debugIO.write(yaml.dump(kwargs))
        self.debugIO.flush()
    try :
      if aMethodConfig['packed'] :
        theResult = await aMethodFunc(self, self.context, someParams, kwargs)
      else :
        theResult = await aMethodFunc(self, self.context, *someParams, **kwargs)
      if theResult :
        await self.jsonRpc.sendResult(theResult, anId)
    except Exception as err :
      await self.jsonRpc.sendError(repr(err))

  async def run(self) :
    while self.continueDispatching :
      await self.dispatchOnce()
