# LSP Implementation Notes

## LSP Messages *recieved*

### LSP `c->s` notification listeners

All of the notifications below potentially alter our cache of ConTeXt
docuemnt-files. Either by rebasing the document-file's path, or by notifying the
cache that the document-file has changed (either in the editor or in the
file-system). In all cases, the document-file cache needs to be updated, and
potentially the ConTeXt document needs to be re-parsed.

  - [textDocument/didOpen](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_didOpen) 
    - a `c->s` notification, which contains the text of the newly opened document
      as a single string
    - We **implement** a listener for this notification so that we can begin
      providing document structure.
  - [textDocument/didChange](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_didChange)
    - a `c->s` notification, which contains either the full text for the changed
      document, *or* the changed text contained in a simple region
    - We **implement** a listener for this notification so that we can track
      changes in the document structure.
  - [textDocument/didClose](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_didClose)
    - a `c->s` notification, which does *not* contain the text of the document
    - We **implement** a listener for this notification so that we can
      (potentially) stop monitoring changes in the document.
  - [workspace/didChangeWorkspaceFolders](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWorkspaceFolders)
    - a `c->s` notification which contains lists of added and removed workspace
      folders.
    - We **implement** a listener for this notification so that we can track
      changes to the base directory of each workspace (and essentially the base
      directory of the ConTeXt document)
  - [workspace/didChangeWatchedFiles](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWatchedFiles)
    - a `c->s` notification which provides a "central" file-system change
      service for all lanaguage servers registered with a given editor.
    - While, for editor managed files, we get this directly via the existing
      `textDocument/didChange` notifications, we *do not* get this information
      for files which might have been altered *outside* of the editor.
    - We **implement** a listener for this notification so we can identify when
    we need to re-parse the ConTeXt document's structure.

### LSP `c->s` request handlers

The `documentSymbols` request provides the client-editor with the currently
known document structure via a hierarchical tree of symbol localions.

  - [textDocument/documentSymbols](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_documentSymbol) 
    - a `c->s` request which provides the document structure (including
      cross-references) as a tree
    - We **implement** a handler for this request

The `workspace/symbols` request provides the client-editor with the currently
known locations of symbols matching a given query string.

  - [workspace/symbols](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_symbol)
    - a `c->s` request which expects a list of symbol references (across the whole
      workspace) corresponding to the given query string (hence this request
      implements a form of global search)
    - We (eventually) **implement** a handler for this request

## LSP Messages *sent*

### LSP `s->c` notifications sent

The `pushDiagnostics` notification gets sent whenever problems are dected while
parsing the ConTeXt document.

  - [textDocument/publishDiagnostics](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_publishDiagnostics)
    - a `s->c` notification which provides a list of the currently known
      problems with the document.
    - We **implement** 

### LSP `s->c` requests sent

We send the `workspaceFolders` request just after we have initialized with the
client-editor. This request provides the document-file cache with the base URL /
file-system-path for any ConTeXt documents in a given workspace.

  - [workspace/workspaceFolders](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_workspaceFolders) 
    - a `s->c` request which responds with a list of the workspace folders and
      their URIs 
    - We **implement** this request so that we can obtain the base directory of
      each workspace (and essentially the base directory of the ConTeXt document)
    - We send this message just after initialization.
