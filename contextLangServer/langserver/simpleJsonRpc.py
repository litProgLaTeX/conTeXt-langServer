# A simple JSON-RPC library based on asyncio and inspired by
#   [digestif's](https://github.com/astoff/digestif.git)
# simple implementation in Lua.

import asyncio
import json
import re
import sys
import yaml

# The following has been taken from alex_noname's excellent answer to: 
# https://stackoverflow.com/questions/64303607/python-asyncio-how-to-read-stdin-and-write-to-stdout
#
async def asyncWrapStdinStdout():
  return await asyncWrapReaderWriter(sys.stdin, sys.stdout)

async def asyncWrapReaderWriter(aFileReader, aFileWriter):
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, aFileReader)
    w_transport, w_protocol = await loop.connect_write_pipe(
      asyncio.streams.FlowControlMixin, aFileWriter
    )
    writer = asyncio.StreamWriter(w_transport, w_protocol, reader, loop)
    return reader, writer

class AsyncJsonRpc :
  def __init__(self, reader, writer, debugIO = None) :
    self.reader  = reader
    self.writer  = writer
    self.debugIO = debugIO

  headerRegexp = re.compile(r"([a-zA-Z\-]+): (.*)")

  async def _receive(self) :

    # Get the JSON-RPC payload (wrapped as an HTTP message)
    if self.debugIO :
      self.debugIO.write("\n-----------------------\nReceived:\n")
      self.debugIO.flush()
    msgDict = {}
    headers = {}
    async for aLine in self.reader :
      aLine = aLine.strip()
      if self.debugIO :
        self.debugIO.write(f"aLine: ({len(aLine)})[{aLine}] <{type(aLine)}>\n")
        self.debugIO.flush()
      if len(aLine) < 1 : break
      parsedHeader = self.headerRegexp.match(aLine.decode())
      if parsedHeader :
        headerKey = parsedHeader.group(1)
        if headerKey :
          headers[headerKey] = parsedHeader.group(2).strip()
    if self.debugIO : 
      self.debugIO.write("headers:\n")
      self.debugIO.write(yaml.dump(headers))
      self.debugIO.write("\n")
      self.debugIO.flush()
    contentLen = 0
    if 'Content-Length' in headers : 
      contentLen = int(headers['Content-Length'])
      if self.debugIO :
        self.debugIO.write(f"contentLen = {contentLen}\n")
        self.debugIO.flush()
    if contentLen : 
      jsonData = await self.reader.read(n=contentLen)
      if self.debugIO : 
        self.debugIO.write(f"jsonData: [{jsonData}]\n")
        self.debugIO.flush()
      try :
        if jsonData : msgDict = json.loads(jsonData)
      except Exception as err :
        msgDict = {
          'method'  : 'error',
          'params'  : repr(err),
          'jsonrpc' : "2.0"
        }
      if self.debugIO :
        self.debugIO.write("\n-simple-json-rpc-----------------------------\n")
        self.debugIO.write("json dict:\n")
        self.debugIO.write(yaml.dump(msgDict))
        self.debugIO.write("\n------------------------------\n\n")
        self.debugIO.flush()
    return msgDict

  async def receive(self) :

    msgDict = await self._receive()

    # Check JSON-RPC structure
    if 'jsonrpc' not in msgDict or msgDict['jsonrpc'] != '2.0' :
      await self.sendError('Not a JSON-RPC 2.0 message')
      msgDict['jsonrpc'] = "2.0"
    if 'params' not in msgDict :
      await self.sendError('No prameters found in JSON message')
      msgDict['params'] = {}  # we assume all parameters will be kwargs
    if 'method' not in msgDict :
      await self.sendError('No method specified in JSON message')
      msgDict['method'] = 'unknown'
    if 'id' not in msgDict :
      msgDict['id'] = None

    # return JSON-RPC payload
    if self.debugIO : 
      self.debugIO.write("\n-simple-json-rpc-----------------------------\n")
      self.debugIO.write(f"method: {msgDict['method']}\n")
      self.debugIO.write(f"id: {msgDict['id']}\n")
      self.debugIO.write("params:\n")
      self.debugIO.write(yaml.dump(msgDict['params']))
    return (msgDict['method'], msgDict['params'], msgDict['id'])

  crlf = "\r\n"
  async def _sendDict(self, aDict, id=None) :
    aDict['jsonrpc'] = "2.0"
    if id : aDict['id'] = id
    if self.debugIO :
      self.debugIO.write("\n-----------------------\nSend:\n")
      self.debugIO.write(yaml.dump(aDict))
      self.debugIO.write("\n")
      self.debugIO.flush()
    jsonStr = json.dumps(aDict)
    if self.debugIO :
      self.debugIO.write(f"data: [{jsonStr}]\n")
      self.debugIO.flush()
    dataStr = f"Content-Length: {len(jsonStr)}{self.crlf}{self.crlf}{jsonStr}"
    self.writer.write(dataStr.encode())
    await self.writer.drain()

  async def sendResult(self, aResult, id=None) :
    await self._sendDict({'result' : aResult}, id)

  async def sendError(self, errMsg, id=None) :
    await self._sendDict({'error': errMsg}, id)
