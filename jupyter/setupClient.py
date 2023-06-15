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

import yaml

from lsprotocol.types import CLIENT_REGISTER_CAPABILITY
from lsprotocol.types import RegistrationParams
from lsprotocol.types import ClientCapabilities
from lsprotocol.types import InitializeParams

from pygls.lsp.client import LanguageClient

client = LanguageClient('lspClient', 'v0.1')

@client.feature(CLIENT_REGISTER_CAPABILITY)
def registerCapability(client: LanguageClient, params: RegistrationParams) :
  return None

