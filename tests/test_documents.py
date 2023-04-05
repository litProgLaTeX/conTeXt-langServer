
import pytest
import yaml

from contextLangServer.processor.documents import (
  Document, DocumentIter, DocumentCache
)

# The test.tex document has 8 lines

def test_loadDocument() :
  docPath = 'tests/docs/test.tex'
  if not DocumentCache.hasDocument(docPath) :
    DocumentCache.loadFromFile(docPath)
  print("-----------------------------------------------------------------")
  print(yaml.dump(DocumentCache.documents))
  print("-----------------------------------------------------------------")
  assert docPath in DocumentCache.documents
  theDoc = DocumentCache.documents[docPath]
  assert len(theDoc.docLines) == 8
  assert '  \\component partA' in theDoc.docLines
  assert theDoc.docName == docPath
  assert theDoc.filePath == docPath
  assert DocumentCache.hasDocument(docPath)
  assert DocumentCache.getDocument(docPath) == theDoc
  assert not DocumentCache.hasDocument('no document')
  assert DocumentCache.getDocument('no document') == None
  #assert False

def test_removeComment() :
  aStr = "this is a test"
  result = Document.removeComment(aStr)
  assert result == aStr
  aStr = "This is a test with % a comment"
  result = Document.removeComment(aStr)
  assert result == 'This is a test with '
  aStr = "This is a test with \\% no comment"
  result = Document.removeComment(aStr)
  assert result == aStr
  aStr = "This is a test with \\% no comment % and a comment"
  result = Document.removeComment(aStr)
  assert result == 'This is a test with \\% no comment '
  aStr = "This is another test with % a comment \\% and no comment"
  result = Document.removeComment(aStr)
  assert result == 'This is another test with '

def test_docIter() :
  docPath = 'tests/docs/test.tex'
  if not DocumentCache.hasDocument(docPath) :
    DocumentCache.loadFromFile(docPath)
  theDoc = DocumentCache.getDocument(docPath)
  print("------------------------------------------------------------------")
  print(yaml.dump(theDoc))
  print("------------------------------------------------------------------")
  print(len(theDoc.docLines))
  print("------------------------------------------------------------------")
  iterA = theDoc.getDocIter()
  lines = theDoc.docLines
  curIndex = 0
  for aLine in iterA :
    assert aLine == lines[curIndex]
    curIndex += 1
  assert curIndex == len(lines)
  startLine = 2
  endLine   = len(lines) - 2
  iterB = theDoc.getDocIter(startLine=startLine, endLine=endLine)
  curIndex = startLine
  for aLine in iterB :
    assert aLine == lines[curIndex]
    curIndex += 1
  assert curIndex == endLine
  #assert False

def test_subDoc() :
  docPath = 'tests/docs/test.tex'
  if not DocumentCache.hasDocument(docPath) :
    DocumentCache.loadFromFile(docPath)
  theDoc = DocumentCache.getDocument(docPath)
  lines = theDoc.docLines
  startLine = 2
  endLine   = len(lines) - 2
  subDoc = theDoc.getScopedDoc(
    'source.lpic', startLine=startLine, endLine=endLine
  )
  assert subDoc.scope     == 'source.lpic'
  assert subDoc.startLine == startLine
  assert subDoc.endLine   == endLine
  iterA = subDoc.getDocIter()
  curIndex = startLine
  for aLine in iterA :
    assert aLine == lines[curIndex]
    curIndex += 1
  assert curIndex == endLine
  startLine += 1
  endLine   -= 1
  iterB = subDoc.getDocIter(startLine=startLine, endLine=endLine)
  curIndex = startLine
  for aLine in iterB :
    assert aLine == lines[curIndex]
    curIndex += 1
  assert curIndex == endLine
  #assert False

@pytest.mark.skip
def test_parse() :
  docPath = 'tests/docs/test.tex'
  if not DocumentCache.hasDocument(docPath) :
    DocumentCache.loadFromFile(docPath)
  DocumentCache.parse(docPath, 'source.lpic')
  
  assert False