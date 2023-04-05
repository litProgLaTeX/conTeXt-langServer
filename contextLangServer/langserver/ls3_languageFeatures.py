
from contextLangServer.langserver.dispatcher import Dispatcher

#############################################################################
# Language Features
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#languageFeatures

# Go to Declaration

#############################################################################
# Go to Definition
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_definition
@Dispatcher.lsRequest('textDocument/definition', file=__file__)
async def textDocument_definition(disp, ctx, params, kwargs) :
  pass

# Go to Type Definition
# Go to Implementation

#############################################################################
# Find References
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_references
@Dispatcher.lsRequest('textDocument/references', file=__file__)
async def textDocument_references(disp, ctx, params, kwargs) :
  pass

# Prepare Call Hierarchy
# Call Hierarchy Incoming Calls
# Call Hierarchy Outgoing Calls
# Prepare Type Hierarchy
# Type Hierarchy Super Types
# Type Hierarchy Sub Types
# Document Highlight
# Document Link
# Document Link Resolve

#############################################################################
# Hover
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_hover
@Dispatcher.lsRequest('textDocument/hover', file=__file__)
async def textDocument_hover(disp, ctx, params, kwargs) :
  pass

# Code Lens
# Code Lens Refresh
# Folding Range
# Selection Range

#############################################################################
# Document Symbols
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_documentSymbol
@Dispatcher.lsRequest('textDocument/documentSymbol', file=__file__)
async def textDocument_documentSymbol(disp, ctx, params, kwargs) :
  pass

# Semantic Tokens
# Inline Value
# Inline Value Refresh
# Inlay Hint
# Inlay Hint Resolve
# Inlay Hint Refresh
# Moniker

#############################################################################
# Completion Proposals
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_completion
@Dispatcher.lsRequest('textDocument/completion', file=__file__)
async def textDocument_completion(disp, ctx, params, kwargs) :
  pass

# Completion Item Resolve
# Publish Diagnostics
# Pull Diagnostics

#############################################################################
# Signature Help
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_signatureHelp
@Dispatcher.lsRequest('textDocument/signatureHelp', file=__file__)
async def textDocument_signatureHelp(disp, ctx, params, kwargs) :
  pass

# Code Action
# Code Action Resolve
# Document Color
# Color Presentation
# Formatting
# Range Formatting
# On type Formatting
# Rename
# Prepare Rename
# Linked Editing Range
