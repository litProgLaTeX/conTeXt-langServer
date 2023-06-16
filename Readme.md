# ConTeXt Language Server

A Language Server for the ConTeXt typesetting system.

Other than providing a small collection of
[snippets](https://code.visualstudio.com/api/language-extensions/snippet-guide)
and a [TextMate Grammar](https://macromates.com/manual/en/language_grammars) for
direct use by the [VSCode syntax
highlighting](https://code.visualstudio.com/api/language-extensions/syntax-highlight-guide),
this [LanguageServer](https://microsoft.github.io/language-server-protocol/)
provides:

- an overview of a ConTeXt's document structure (eventually across all files in
  the document), (either workspace/symbol (global search) or
  textDocument/documentSymbols (local tree))

- (eventually) links to all references (both where they are defined and where
  they are used), (either workspace/symbol (global search) or
  textDocument/references (local search) or as part of the
  textDocument/documentSymbols (local tree) or textDocument/gotoDeclaration or
  textDocument/gotoDefinition or textDocument/gotoImplementation or textDocument/gotoTypeDefinition)

- (eventually) diagnostic messages (about unstopped starts...)

QUESTION: how do we determine the base directory of a root folder?
ANSWER: the only place this *might* be found is as the URI of a workspaceFolder

The following are only sent when a document is actually opened for editing in
the editor:

- textDocument/didOpen
- textDocument/didChange
- textDocument/willSave (do we care?)
- textDocument/willSaveWaitUntil (do we care? (allows text edits from server))
- textDocument/didSave (do we care?)
- textDocument/didClose

The following are only sent when a jupyter notebook is opened for use in the
editor:

- notebookDocument/didOpen (exists, do we need it? "jupyter notebook")
- notebookDocument/didChange (exists, do we need it? "jupyter notebook")
- notebookDocument/didClose (exists, do we need it? "jupyter notebook")

If we want to know about changes to file in the "workspace" (which are not
currently open) then we need to listen to the following:

- workspace/workspaceFolders (root folders in current tool)
- workspace/didChangeWorkspaceFolders
- workspace/willCreateFiles
- workspace/didCreateFiles
- workspace/willRenameFiles
- workspace/didRenameFiles
- workspace/willDeleteFiles
- workspace/didDeleteFiles
- workspace/getConfiguration (to pull editor/workspace configuration -- but what?)
- workspace/didChangeConfiguration (pushed notifications of any/all changes)
- workspace/didChangeWatchedFiles (we get this directly via textDocument/didChange)
- 