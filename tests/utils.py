
import asyncio
import io
import yaml

from contextLangServer.langserver.simpleJsonRpc import AsyncJsonRpc

##############################################################################
# A subclass of various IO classes to simulate stdin/stdout pipes
#
class AsyncTestReader(io.StringIO) :
  def __aiter__(self) :
    return self

  async def __anext__(self) :
    val = self.readline()
    if val == '' :
      raise StopAsyncIteration
    return val.encode()

  async def read(self, n=-1) :
    return super().read(n).encode()

class AsyncTestWriter(io.BytesIO) :
  async def drain(self) :
    pass

class ClientServerIO :
  def __init__(self, initialReaderStr=None) :
    self.reader = AsyncTestReader(initialReaderStr)
    self.writer = AsyncTestWriter()

  def reverse(self) :
    self.reader = AsyncTestReader(self.writer.getvalue().decode())
    self.writer = AsyncTestWriter()

##############################################################################
# A subclass of the AsyncJsonRpc class to simulate the server end of a
# client/server setup.
#
class MockJsonRpc(AsyncJsonRpc) :
  def __init__(self, debugIO = None) :
    self.debugIO = debugIO
    self.receiveQueue = asyncio.Queue()
    self.sendQueue   = asyncio.Queue()

  # Simulate the recipt of a new JSON-RPC message from the client
  #
  async def _receive(self) :
    msgDict = await self.receiveQueue.get() 
    self.receiveQueue.task_done()
    return msgDict

  # Simulate sending a new JSON-RPC message to the client
  #
  async def _sendDict(self, msgDict, anId=None) :
    await self.sendQueue.put((msgDict, anId))

  # Put the next JSON-RPC message into the server's receive queue
  #
  async def putNextMsg(self, method, params, anId=None) :
    jsonMsg = {
      'jsonrpc' : '2.0',
      'method' : method,
      'params' : params
    }
    if anId : jsonMsg['id'] = anId
    await self.receiveQueue.put(jsonMsg)

  # Get the last JSON-RPC message from the server's send queue
  #
  def getNumMsgs(self) :
    return self.sendQueue.qsize()

  async def getLastMsg(self) :
    msgDict, anId = await self.sendQueue.get()
    self.sendQueue.task_done()
    return msgDict, anId

  async def printMsgs(self) :
    if self.sendQueue.qsize() < 1 :
      print("------NO-Send-msgs-----------------------------------")
      return
    while 0 < self.sendQueue.qsize() :
      msgDict, anId = await self.getLastMsg()
      print("---send-msg---------------------------------------------")
      print(f"id: {anId}")
      print(yaml.dump(msgDict))