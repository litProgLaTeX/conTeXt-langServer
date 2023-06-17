# A review of the Language Server Protocol

We review the
[request](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#requestMessage),
[response](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#responseMessage)
and
[notification](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#notificationMessage)
messages of the [Language Server
Protocol](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/)
which are important for *this* ConTeXt Language Server (and its associated
[Literate Programming in ConTeXt Language
Server](https://github.com/litProgConTeXt/lpic-langServer)).

## Goals

Our goal is to provide a reasonably useful but light weight editing environment
for (Literate Programming in) ConTeXt documents in VSCode editors.

To do this we plan to leaverage VSCode's [Syntax
Highlighting](https://code.visualstudio.com/api/language-extensions/syntax-highlight-guide)
(using a [TextMate Grammar](https://macromates.com/manual/en/language_grammars))
as well as VSCode's
[Snippets](https://code.visualstudio.com/api/language-extensions/snippet-guide).

We will use *this* language server to provide fuctions which can not be done
using the Syntax Highlighting or Snippets, namely:
- an overview of a ConTeXt's document structure (eventually across all files in
  the document), 
- (eventually) diagnostic messages (about missing document-files, unstopped
  starts...)
- (eventually) links to all references (both where they are defined and where
  they are used), 

## Implementation

The ConTeXt document overview will be provided by implementing:
  - [textDocument/documentSymbols](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_documentSymbol) 
    - a `c->s` request which provides the document structure (including
      cross-references) as a tree
    - We **implement** a handler for this request
  - [workspace/symbols](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_symbol)
    - a `c->s` request which expects a list of symbol references (across the whole
      workspace) corresponding to the given query string (hence this request
      implements a form of global search)
    - We (eventually) **implement** a handler for this request

The ConTeXt document diagnostics will be provided by implementing:
  - [textDocument/publishDiagnostics](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_publishDiagnostics)
    - a `s->c` notification which provides a list of the currently known
      problems with the document.
    - We **implement** sending this notification whenever problems are dected
      while parsing the ConTeXt document.
  - (we could but won't implement the associated
    [textDocument/pullDiagnostics](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_pullDiagnostics)
    `c->s` request)

The cross references will be provided by implementing:
  - [textDocument/documentSymbols](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_documentSymbol) 
    - a `c->s` request which provides the document structure (including
      cross-references) as a tree
    - We **implement** a handler for this request
  - [workspace/symbols](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_symbol)
    - a `c->s` request which expects a list of symbol references (across the
      whole workspace) corresponding to the given query string (hence this
      request implements a form of global search)
    - We (eventually) **implement** a handler for this request
  - [textDocument/references](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_references)
    - a `c->s` request asking for all known references for the symbol at the
      given location.
  - [textDocument/gotoDeclaration](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_declaration)
    - a `c->s` request asking for the location of the *declaration* of the
      symbol at the given location.
  - [textDocument/gotoDefinition](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_definition)
    - a `c->s` request asking for the location of the *definition* of the
      symbol at the given location.
  - [textDocument/gotoImplementation](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_implementation)
    - a `c->s` request asking for the location of the *implementation* of the
      symbol at the given location.
  - [textDocument/gotoTypeDefinition](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_typeDefinition)
    - a `c->s` request asking for the location of the *type definition* of the
      symbol at the given location.

## Review of change synchronization messages

In order to enable our *primary* goals, we will need to monitor on-going changes
to the documents, notebooks and workspaces containing these documents.

### [Document synchronization](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_synchronization)

Since our primary aim is to provide *global* document structure for a ConTeXt
document (which typically contains multiple files), we *need* to monitor which
documents we can safely read from the file system and which we must "get" from
the editor. The document lifecycle notifications listed below, delineate those
document-files we MUST NOT obtain from the file system (since these files are
currently being changed by the editor). These lifecycle messages also provide us
with the current state of the managed files.

The following document-file lifecycle messages are only sent when a document is
actually being managed (for editing) in the editor:

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
- [textDocument/willSave](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_willSave)
  - a `c->s` notification, which contains the reason for this save, but does not
  contain the full text of the document
- [textDocument/willSaveWaitUntil](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_willSaveWaitUntil)
  - a `c->s` request, which allows the *server* to request changes before the
    actual save
- [textDocument/didSave](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_didSave)
  - a `c->s` notification, which can contain, if requested by the server during
  initialization, the full text of the document as saved
- [textDocument/didClose](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_didClose)
  - a `c->s` notification, which does *not* contain the text of the document
  - We **implement** a listener for this notification so that we can
    (potentially) stop monitoring changes in the document.

[Renaming of
documents](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_didRename)
is captured by listening for the corresponding `didClose` / `didOpen`
notifications.

### [(Jupyter) Notebook synchronization](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#notebookDocument_synchronization)

There are currently no (TeX, LaTeX, or) ConTeXt [Jupyter
kernels](https://github.com/jupyter/jupyter/wiki/Jupyter-kernels). So there is
really no reason to monitor the editor's managment of notebooks.

The following are only sent when a jupyter notebook is actually being managed
(for editing / use) in the editor:

- [notebookDocument/didOpen](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#notebookDocument_didOpen)
  - a `c->s` notification
- [notebookDocument/didChange](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#notebookDocument_didChange)
  - a `c->s` notification
- [notebookDocument/didSave](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#notebookDocument_didSave)
  - a `c->s` notification
- [notebookDocument/didClose](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#notebookDocument_didClose)
  - a `c->s` notification

### [Workspace synchronization](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspaceFeatures)

The workspace folders provide an interface to logically important collections of
docuemnt-files from the file-system. In particular a workspace folder contains
the base URL / directory-path for each of these collections, and hence the base
of a ConTeXt document.

The Langauge Server Protocol provides the follow workspace related change
messages:

- [workspace/workspaceFolders](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_workspaceFolders) 
  - a `s->c` request which responds with a list of the workspace folders and
    thier URIs 
  - We **implement** this request so that we can obtain the base directory of
    each workspace (and essentially the base directory of the ConTeXt document)
- [workspace/didChangeWorkspaceFolders](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWorkspaceFolders)
  - a `c->s` notification which contains lists of added and removed workspace
    folders.
  - We **implement** a listener for this notification so that we can track changes to the base
    directory of each workspace (and essentially the base directory of the
    ConTeXt document)
- [workspace/willCreateFiles](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_willCreateFiles)
  - a `c->s` request which allows the server to make changes to the workspace.
- [workspace/didCreateFiles](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didCreateFiles)
  - a `c->s` notification.
- [workspace/willRenameFiles](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_willRenameFiles)
  - a `c->s` request which allows the server to make changes to the workspace.
- [workspace/didRenameFiles](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didRenameFiles)
  - a `c->s` notification.
- [workspace/willDeleteFiles](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_willDeleteFiles)
  - a `c->s` request which allows the server to make changes to the workspace.
- [workspace/didDeleteFiles](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didDeleteFiles)
  - a `c->s` notification.
- [workspace/getConfiguration](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_configuration)
  - a `s->c` request which provides the configuration associated with each item
    in a list of requested
    [ConfigurationItem](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#configurationItem)s
  - unfortunately there is no list of what configuration items we could request
    (and so why we might be interested in the values)
- [workspace/didChangeConfiguration](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeConfiguration)
  - a `c->s` notification containing a list(?) of configuration changes
- [workspace/didChangeWatchedFiles](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWatchedFiles)
  - a `c->s` notification which provides a "central" file-system change service
    for all lanaguage servers registered with a given editor.
  - While, for editor managed files, we get this directly via the existing
    `textDocument/didChange` notifications, we *do not* get this information for
    files which might have been altered *outside* of the editor.
  - We **implement** a listener for this notification so we can identify when we
    need to re-parse the ConTeXt document's structure.

## Questions

**QUESTION**: how do we determine the base directory of a root folder?
  - **ANSWER**: the only place this *might* be found is as the URI of a
    workspaceFolder

