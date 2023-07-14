"""
This Python script setups the ConTeXt-langServer explorer environment.

We use [pygls](https://github.com/openlawlibrary/pygls) 
to build a very simple Python LSP client.
"""

# We need the client and lsp/client modules from the pre-released pygls...
#
# To do this type:
#
# pip install git+https://github.com/openlawlibrary/pygls.git
#
# We may also need:
#
# pipx runpip jupyterlab install git+https://github.com/openlawlibrary/pygls.git
#
# I am very unsure where the lsprotocol and pygls libraries are being
# loaded from.

import copy
import json
import os
import yaml

from lsprotocol.types import CLIENT_REGISTER_CAPABILITY
from lsprotocol.types import RegistrationParams
from lsprotocol.types import ClientCapabilities
from lsprotocol.types import InitializeParams
from lsprotocol.types import InitializedParams
from lsprotocol.types import WorkspaceClientCapabilities
from lsprotocol.types import DidChangeConfigurationClientCapabilities
from lsprotocol.types import CompletionParams
from lsprotocol.types import PublishDiagnosticsClientCapabilities
from lsprotocol.types import TextDocumentClientCapabilities
from lsprotocol.types import TextDocumentIdentifier
from lsprotocol.types import Position

from pygls.lsp.client import LanguageClient

class ExplorerServerConfig :
    hasConfigurationCapability : bool
    hasWorkspaceFolderCapability : bool
    hasDiagnosticRelatedInformationCapability : bool

class ExplorerLanguageClient(LanguageClient) :
    async def server_configuration_async(self, params) -> ExplorerServerConfig :
        if self.stopped:
            raise RuntimeError("Client has been stopped.")
        response = await self.protocol.send_request_async("server/configuration", params)
        return json.loads(response)

client = ExplorerLanguageClient('lspClient', 'v0.1')

# Setup the LPIC logger to provide trace level logging
clientEnv = copy.deepcopy(os.environ)
clientEnv['LPIC_LOG_LEVEL'] = '0'

registrations = []

@client.feature(CLIENT_REGISTER_CAPABILITY)
def registerCapability(client: ExplorerLanguageClient, params: RegistrationParams) :
  registrations.append(params)
  return None

