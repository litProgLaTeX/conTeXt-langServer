# ConTeXt-langserver client/server test tool

This directory contains a simple Python `client` script and an associated
collection of LanguageServerProtocol request/notification sequences.

The `client` script loads a single YAML file containing a sequence of
LanguageServerProtocol request/notifications to send to the
`context-langserver` in order to test the `context-langserver`.

The YAML LanguageServerProtocol request/notification scripts can be used
to test various aspects of the `context-langserver`.

For example, to run the `initScript.yaml` test, type:

```
  ./client initScript.yaml
```
