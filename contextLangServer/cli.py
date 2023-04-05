
import asyncio
import os
import yaml

import contextLangServer.langserver.ls1_lifeCycle
import contextLangServer.langserver.lsA_build

from contextLangServer.langserver.simpleJsonRpc import (
  asyncWrapStdinStdout, AsyncJsonRpc
)
from contextLangServer.langserver.dispatcher import Dispatcher

async def asyncMain() :
  reader, writer = await asyncWrapStdinStdout()
  debugIO = open(f"/tmp/context-langserver-{os.getpid()}.log", 'w')
  debugIO.write("Started context language server\n")
  ajr = AsyncJsonRpc(reader, writer)
  lsDispatcher = Dispatcher(ajr, debugIO=debugIO)
  lsDispatcher.reportMethods()
  
  await lsDispatcher.run()

def cli() :
  asyncio.run(asyncMain())