
from contextLangServer.langserver.dispatcher import Dispatcher

#############################################################################
# Workspace Features

#############################################################################
#    Workspace Symbols
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_symbol
@Dispatcher.lsRequest('workspace/symbol', file=__file__)
async def workspace_symbol(disp, ctx, params, kwargs) :
  pass

#    Workspace Symbol Resolve
#    Get Configuration

#############################################################################
#    Did Change Configuration
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeConfiguration
@Dispatcher.lsNotification('workspace/didChangeConfiguration', file=__file__)
async def workspace_didChangeConfiguration(disp, ctx, params, kwargs) :
  pass

#    Workspace Folders
#    Did Change Workspace Folders
#    Will Create Files
#    Did Create Files
#    Will Rename Files
#    Did Rename Files
#    Will Delete Files
#    Did Delete Files
#    Did Change Watched Files
#    Execute Command
#    Apply Edit



