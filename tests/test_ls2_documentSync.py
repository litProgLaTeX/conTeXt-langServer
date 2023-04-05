
import asyncio
import pytest
import sys
import yaml

from contextLangServer.langserver.dispatcher import Dispatcher
from utils import MockJsonRpc

import contextLangServer.langserver.ls1_lifeCycle
import contextLangServer.langserver.ls2_documentSync

@pytest.mark.skip
@pytest.mark.asyncio
async def test_simple_lifeCycle() :
  mockJsonRpc = MockJsonRpc(debugIO=sys.stdout)
  resultsCtx = []
  disp = Dispatcher(mockJsonRpc, resultsCtx, debugIO=sys.stdout)

  dispatcherTask = asyncio.create_task(disp.run())

  await mockJsonRpc.putNextMsg('initialize', {}, anId=1)
  await mockJsonRpc.putNextMsg('initialized', {}) # notification
  await mockJsonRpc.putNextMsg('textDocument/didOpen', {}) # notification
  await mockJsonRpc.putNextMsg('textDocument/didChange', {}) # notification
  await mockJsonRpc.putNextMsg('textDocument/willSave', {}) # notification
  await mockJsonRpc.putNextMsg('textDocument/didSave', {}) # notification
  await mockJsonRpc.putNextMsg('textDocument/didClose', {}) # notification
  await mockJsonRpc.putNextMsg('shutdown', {}, anId=2)
  await mockJsonRpc.putNextMsg('exit', {}) # notification
  
  await dispatcherTask
  """
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
  """

  print("-------------------------------------------------")
  print(yaml.dump(resultsCtx))
  await mockJsonRpc.printMsgs()
  assert False
