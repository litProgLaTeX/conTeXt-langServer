
from contextLangServer.langserver.dispatcher import Dispatcher

#############################################################################
# Document Synchronization
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_synchronization

#############################################################################
#    Did Open Text Document
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_didOpen
#
@Dispatcher.lsNotification('textDocument/didOpen', file=__file__) 
async def textDocument_didOpen(disp, ctx, params, kwargs) :
  pass

#############################################################################
#    Did Change Text Document
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_didChange
#
@Dispatcher.lsNotification('textDocument/didChange', file=__file__)
async def textDocument_didChange(disp, ctx, params, kwargs) :
  pass

#############################################################################
#    Will Save Text Document
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_willSave
#
@Dispatcher.lsNotification('textDocument/willSave', file=__file__)
async def textDocument_willSave(disp, ctx, params, kwargs) :
  pass

#############################################################################
#    Did Save Text Document
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_didSave
#
@Dispatcher.lsNotification('textDocument/didSave', file=__file__)
async def textDocument_didSave(disp, ctx, params, kwargs) :
  pass

#############################################################################
#    Did Close Text Document
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_didClose
#
@Dispatcher.lsNotification('textDocument/didClose', file=__file__)
async def textDocument_didClose(disp, ctx, params, kwargs) :
  pass

#############################################################################
# UNUSED: 

# Will Save Document Wait Until (unused)
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_willSaveWaitUntil
#
# This request allows the language server to send the client a list of edits
# that the langauge server feels are required. We do NOT change any documents
# from the langauge server, so this request is not implemented.

# Rename a Text Document
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_didRename
#
# This is not a request but the discussion of how a client should "rename" a
# document, by first closing the old document and opening the document under a
# new name.

#############################################################################
# Notbook interface is UNUSED: 
#    Overview - Notebook Document (unused)
#    Did Open Notebook Document (unused)
#    Did Change Notebook Document (unused)
#    Did Save Notebook Document (unused)
#    Did Close Notebook Document (unused)
