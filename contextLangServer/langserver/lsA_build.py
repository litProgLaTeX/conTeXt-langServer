
from enum import Enum

from contextLangServer.langserver.dispatcher import Dispatcher

##############################################################################
# Extended Language Server Protocol Messages
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification

##############################################################################
# Build context document
#
class BuildStatus(Enum) :
   # The build process terminated without any errors.
  Success = 0

  # The build process terminated with errors.
  Error = 1

  # The build process failed to start or crashed.
  Failure = 2

  # The build process was cancelled.
  Cancelled = 3

#class BuildResult :
#  # The status of the build process.
#  status: BuildStatus

@Dispatcher.lsRequest('textDocument/build', file=__file__)
async def buildContextDoc(disp, ctx, params, kwargs) :
  if disp.debugIO : 
    disp.debugIO.write("lsRequest: textDocument/build\n")

  return {
    'status' : BuildStatus.Failure.value
  }
