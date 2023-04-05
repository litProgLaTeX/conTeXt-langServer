
import asyncio
import pytest
import sys
import yaml

from contextLangServer.langserver.dispatcher import Dispatcher
from utils import MockJsonRpc

@Dispatcher.lsRequest('simpleStrParam', packed=False, kwargsDict={ 'test' : 'this is a test'})
async def simpleStrParam(disp, ctx, aMessage, **kwargs) :
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

@Dispatcher.lsRequest('simplePackedStrParam', kwargsDict={ 'test' : 'this is a test'})
async def simplePackedStrParam(disp, ctx, params, kwargs) :
  print("-----------------------------------------")
  print('simplePackedStrParam')
  print(params[0])
  print("-----------------------------------------")
  ctx.append({
    'method'   : 'simplePackedStrParam',
    'msg'      : params[0],
    'kwargs'   : kwargs,
    'dispType' : type(disp)
  })

@Dispatcher.lsRequest('simpleListParam', packed=False)
async def simpleListParam(disp, ctx, msg1, msg2, **kwargs) :
  print("-----------------------------------------")
  print('simpleListParam')
  print(msg1)
  print(msg2)
  print("-----------------------------------------")
  ctx.append({
    'method'   : 'simpleListParam',
    'msg1'     : msg1,
    'msg2'     : msg2,
    'kwargs'   : kwargs,
    'dispType' : type(disp)
  })

@Dispatcher.lsRequest('simplePackedListParam')
async def simplePackedListParam(disp, ctx, params, kwargs) :
  print("-----------------------------------------")
  print('simplePackedListParam')
  print(params[0])
  print(params[1])
  print("-----------------------------------------")
  ctx.append({
    'method'   : 'simplePackedListParam',
    'msg1'     : params[0],
    'msg2'     : params[1],
    'kwargs'   : kwargs,
    'dispType' : type(disp)
  })

@Dispatcher.lsRequest('simpleDictParam', packed=False)
async def simpleDictParam(disp, ctx, msg1="msg1", msg2="msg2", **kwargs) :
  print("-----------------------------------------")
  print('simpleDictParam')
  print(msg1)
  print(msg2)
  print("-----------------------------------------")
  ctx.append({
    'method'   : 'simpleDictParam',
    'msg1'     : msg1,
    'msg2'     : msg2,
    'kwargs'   : kwargs,
    'dispType' : type(disp)
  })

@Dispatcher.lsRequest('simplePackedDictParam')
async def simpleDictParam(disp, ctx, params, kwargs) :
  print("-----------------------------------------")
  print('simpleDictParam')
  print(kwargs['msg1'])
  print(kwargs['msg2'])
  print("-----------------------------------------")
  ctx.append({
    'method'   : 'simplePackedDictParam',
    'msg1'     : kwargs['msg1'],
    'msg2'     : kwargs['msg2'],
    'kwargs'   : kwargs,
    'dispType' : type(disp)
  })

@Dispatcher.lsRequest('simpleRaiseExcep')
async def simpleRaiseExcep(disp, ctx, *params, **kwargs) :
  raise Exception("simple exception raised")

@Dispatcher.lsRequest('simpleBrokenDef')
async def simpleBrokenDef() :
  pass

@Dispatcher.lsRequest('simpleNotAsync')
def simpleNotAsync(disp, ctx, *params, **kwargs) :
  pass

@Dispatcher.lsRequest('simpleStop')
async def simpleStop(disp, ctx, *params, **kwargs) :
  disp.stopDispatching()

def test_listMethods() :
  disp = Dispatcher(None)
  methods = disp.listMethods()
  assert isinstance(methods, list)

  # now that we are testing ls?_* we will have more methods
  #assert len(methods) == 10 
  
  assert 'simpleStrParam' in methods
  assert not Dispatcher.methods['simpleStrParam'][0]['packed'] 
  assert Dispatcher.methods['simpleStrParam'][0]['kwargs']['test'] == "this is a test"
  assert 'simplePackedStrParam' in methods
  assert Dispatcher.methods['simplePackedStrParam'][0]['packed']
  assert Dispatcher.methods['simplePackedStrParam'][0]['kwargs']['test'] == "this is a test"
  assert 'simpleListParam' in methods
  assert 'simplePackedListParam' in methods
  assert 'simpleDictParam' in methods
  assert 'simplePackedDictParam' in methods
  assert 'simpleRaiseExcep' in methods
  assert 'simpleBrokenDef' in methods
  assert 'simpleNotAsync' in methods
  assert 'simpleStop' in methods
  #print(yaml.dump(Dispatcher.methods))
  #assert False

@pytest.mark.asyncio
async def test_dispatch_strParam() :
  mockJsonRpc = MockJsonRpc(debugIO=sys.stdout)
  resultsCtx = []
  disp = Dispatcher(mockJsonRpc, resultsCtx)

  dispatcherTask = asyncio.create_task(disp.dispatchOnce())

  theMessage = 'this is a simple message'
  await mockJsonRpc.putNextMsg('simpleStrParam', theMessage)

  await dispatcherTask
  assert len(resultsCtx) == 1
  assert 'msg' in resultsCtx[0]
  assert resultsCtx[0]['msg'] == theMessage
  #print(yaml.dump(resultsCtx))
  #await mockJsonRpc.printMsgs()
  #assert False

@pytest.mark.asyncio
async def test_dispatch_packedStrParam() :
  mockJsonRpc = MockJsonRpc(debugIO=sys.stdout)
  resultsCtx = []
  disp = Dispatcher(mockJsonRpc, resultsCtx)

  dispatcherTask = asyncio.create_task(disp.dispatchOnce())

  theMessage = 'this is a simple message'
  await mockJsonRpc.putNextMsg('simplePackedStrParam', theMessage)

  await dispatcherTask
  assert len(resultsCtx) == 1
  assert 'msg' in resultsCtx[0]
  assert resultsCtx[0]['msg'] == theMessage
  #print(yaml.dump(resultsCtx))
  #await mockJsonRpc.printMsgs()
  #assert False

@pytest.mark.asyncio
async def test_dispatch_listParam() :
  mockJsonRpc = MockJsonRpc(debugIO=sys.stdout)
  resultsCtx = []
  disp = Dispatcher(mockJsonRpc, resultsCtx)

  dispatcherTask = asyncio.create_task(disp.dispatchOnce())

  theMsg1 = 'this is the first message'
  theMsg2 = 'this is the second message'
  await mockJsonRpc.putNextMsg('simpleListParam', [ theMsg1, theMsg2 ], anId=1)

  await dispatcherTask
  assert len(resultsCtx) == 1
  assert 'msg1' in resultsCtx[0]
  assert resultsCtx[0]['msg1'] == theMsg1
  assert 'msg2' in resultsCtx[0]
  assert resultsCtx[0]['msg2'] == theMsg2
  #print(yaml.dump(resultsCtx))
  #await mockJsonRpc.printMsgs()
  #assert False

@pytest.mark.asyncio
async def test_dispatch_packedListParam() :
  mockJsonRpc = MockJsonRpc(debugIO=sys.stdout)
  resultsCtx = []
  disp = Dispatcher(mockJsonRpc, resultsCtx)

  dispatcherTask = asyncio.create_task(disp.dispatchOnce())

  theMsg1 = 'this is the first message'
  theMsg2 = 'this is the second message'
  await mockJsonRpc.putNextMsg('simplePackedListParam', [ theMsg1, theMsg2 ], anId=1)

  await dispatcherTask
  assert len(resultsCtx) == 1
  assert 'msg1' in resultsCtx[0]
  assert resultsCtx[0]['msg1'] == theMsg1
  assert 'msg2' in resultsCtx[0]
  assert resultsCtx[0]['msg2'] == theMsg2
  #print(yaml.dump(resultsCtx))
  #await mockJsonRpc.printMsgs()
  #assert False

@pytest.mark.asyncio
async def test_dispatch_dictParam() :
  mockJsonRpc = MockJsonRpc(debugIO=sys.stdout)
  resultsCtx = []
  disp = Dispatcher(mockJsonRpc, resultsCtx)

  dispatcherTask = asyncio.create_task(disp.dispatchOnce())

  theMsg1 = 'this is the first message'
  theMsg2 = 'this is the second message'
  await mockJsonRpc.putNextMsg('simpleDictParam', {
    'msg1' : theMsg1,
    'msg2' : theMsg2
  })

  await dispatcherTask
  assert len(resultsCtx) == 1
  assert 'msg1' in resultsCtx[0]
  assert resultsCtx[0]['msg1'] == theMsg1
  assert 'msg2' in resultsCtx[0]
  assert resultsCtx[0]['msg2'] == theMsg2
  #print(yaml.dump(resultsCtx))
  #await mockJsonRpc.printMsgs()
  #assert False

@pytest.mark.asyncio
async def test_dispatch_packedDictParam() :
  mockJsonRpc = MockJsonRpc(debugIO=sys.stdout)
  resultsCtx = []
  disp = Dispatcher(mockJsonRpc, resultsCtx)

  dispatcherTask = asyncio.create_task(disp.dispatchOnce())

  theMsg1 = 'this is the first message'
  theMsg2 = 'this is the second message'
  await mockJsonRpc.putNextMsg('simplePackedDictParam', {
    'msg1' : theMsg1,
    'msg2' : theMsg2
  })

  await dispatcherTask
  assert len(resultsCtx) == 1
  assert 'msg1' in resultsCtx[0]
  assert resultsCtx[0]['msg1'] == theMsg1
  assert 'msg2' in resultsCtx[0]
  assert resultsCtx[0]['msg2'] == theMsg2
  #print(yaml.dump(resultsCtx))
  #await mockJsonRpc.printMsgs()
  #assert False

@pytest.mark.asyncio
async def test_dispatch_raiseException() :
  mockJsonRpc = MockJsonRpc(debugIO=sys.stdout)
  resultsCtx = []
  disp = Dispatcher(mockJsonRpc, resultsCtx)

  dispatcherTask = asyncio.create_task(disp.dispatchOnce())

  theMsg1 = 'this is the first message'
  theMsg2 = 'this is the second message'
  await mockJsonRpc.putNextMsg('simpleRaiseExcep', {
    'msg1' : theMsg1,
    'msg2' : theMsg2
  })

  await dispatcherTask
  assert len(resultsCtx) == 0
  assert mockJsonRpc.getNumMsgs() == 1
  aMsgDict, anId = await mockJsonRpc.getLastMsg()
  assert 'error' in aMsgDict
  assert -1 < aMsgDict['error'].find('simple exception raised')
  #print(yaml.dump(aMsgDict))
  #print(yaml.dump(resultsCtx))
  #await mockJsonRpc.printMsgs()
  #assert False

@pytest.mark.asyncio
async def test_dispatch_brokenDef() :
  mockJsonRpc = MockJsonRpc(debugIO=sys.stdout)
  resultsCtx = []
  disp = Dispatcher(mockJsonRpc, resultsCtx)

  dispatcherTask = asyncio.create_task(disp.dispatchOnce())

  theMsg1 = 'this is the first message'
  theMsg2 = 'this is the second message'
  await mockJsonRpc.putNextMsg('simpleBrokenDef', {
    'msg1' : theMsg1,
    'msg2' : theMsg2
  })

  await dispatcherTask
  assert len(resultsCtx) == 0
  assert mockJsonRpc.getNumMsgs() == 1
  aMsgDict, anId = await mockJsonRpc.getLastMsg()
  assert 'error' in aMsgDict
  assert -1 < aMsgDict['error'].find('TypeError')
  #print(yaml.dump(aMsgDict))
  #print(yaml.dump(resultsCtx))
  #await mockJsonRpc.printMsgs()
  #assert False

@pytest.mark.asyncio
async def test_dispatch_notAsync() :
  mockJsonRpc = MockJsonRpc(debugIO=sys.stdout)
  resultsCtx = []
  disp = Dispatcher(mockJsonRpc, resultsCtx)

  dispatcherTask = asyncio.create_task(disp.dispatchOnce())

  theMsg1 = 'this is the first message'
  theMsg2 = 'this is the second message'
  await mockJsonRpc.putNextMsg('simpleNotAsync', {
    'msg1' : theMsg1,
    'msg2' : theMsg2
  })

  await dispatcherTask
  assert len(resultsCtx) == 0
  assert mockJsonRpc.getNumMsgs() == 1
  aMsgDict, anId = await mockJsonRpc.getLastMsg()
  assert 'error' in aMsgDict
  assert -1 < aMsgDict['error'].find('No coroutine')
  #print(yaml.dump(aMsgDict))
  #print(yaml.dump(resultsCtx))
  #await mockJsonRpc.printMsgs()
  #assert False

@pytest.mark.asyncio
async def test_dispatch_run() :
  mockJsonRpc = MockJsonRpc(debugIO=sys.stdout)
  resultsCtx = []
  disp = Dispatcher(mockJsonRpc, resultsCtx, debugIO=sys.stdout)

  dispatcherTask = asyncio.create_task(disp.run())

  theMsg  = "this is a message"
  theMsg1 = 'this is the first message'
  theMsg2 = 'this is the second message'
  theMsgs = { 'msg1' : theMsg1, 'msg2' : theMsg2 }

  await mockJsonRpc.putNextMsg('simpleStrParam', theMsg, anId=1)
  await mockJsonRpc.putNextMsg('simpleRaiseExcep', theMsgs, anId=2)
  await mockJsonRpc.putNextMsg('simpleListParam', [ theMsg1, theMsg2 ], anId=3)
  await mockJsonRpc.putNextMsg('simpleBrokenDef', theMsgs, anId=4)
  await mockJsonRpc.putNextMsg('simpleDictParam', theMsgs, anId=5)
  await mockJsonRpc.putNextMsg('simpleNotAsync', theMsgs, anId=6)
  await mockJsonRpc.putNextMsg('simpleStop', theMsgs, anId=7)
  
  await dispatcherTask
  assert len(resultsCtx) == 3
  aResult = resultsCtx[0]
  assert aResult['method'] == 'simpleStrParam'
  assert aResult['kwargs']['id'] == 1

  aResult = resultsCtx[1]
  assert aResult['method'] == 'simpleListParam'
  assert aResult['kwargs']['id'] == 3

  aResult = resultsCtx[2]
  assert aResult['method'] == 'simpleDictParam'
  assert aResult['kwargs']['id'] == 5

  assert mockJsonRpc.getNumMsgs() == 3
  aMsgDict, anId = await mockJsonRpc.getLastMsg()
  assert -1 < aMsgDict['error'].find('simple exception raised')
  aMsgDict, anId = await mockJsonRpc.getLastMsg()
  assert -1 < aMsgDict['error'].find('TypeError')
  aMsgDict, anId = await mockJsonRpc.getLastMsg()
  assert -1 < aMsgDict['error'].find('No coroutine')

  #print(yaml.dump(resultsCtx))
  #await mockJsonRpc.printMsgs()
  #assert False