#! .venv/bin/python

import asyncio
import os
import yaml

from experiments.simpleJsonRpc import asyncWrapStdinStdout, AsyncJsonRpc
from experiments.dispatcher import Dispatcher

async def stopDispatcher(dispatcher=None, **someKWargs) :
  if dispatcher : dispatcher.stopDispatching()
  return None

async def doNothing(**someKWargs) :
  return None

async def echoMessage(dispatcher=None, **someParams) :
  return {
    'method' : 'echo',
    'someParams' : someParams
  }

async def asyncMain() :
  reader, writer = await asyncWrapStdinStdout()
  debugIO = open(f"/tmp/experiments-server-{os.getpid()}", 'w')
  ajr = AsyncJsonRpc(reader, writer, debugIO=debugIO)
  sDispatcher = Dispatcher(ajr)
  sDispatcher.addMethod('stop', stopDispatcher)
  sDispatcher.addMethod('unknown', doNothing)
  sDispatcher.addMethod('echo', echoMessage)
  debugIO.write(yaml.dump(sDispatcher.listMethods()))
  await sDispatcher.run()

def main() :
  asyncio.run(asyncMain())

if __name__ == '__main__' :
  main()