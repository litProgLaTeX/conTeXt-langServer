
from contextLangServer.processor.scopeActions import ScopeActions

# for the scope actions tests
#
@ScopeActions.method('??')
def loadedStrParam(disp, ctx, aMessage, **kwargs) :
  print("-----------------------------------------")
  print('loadedStrParam')
  print(aMessage)
  print("-----------------------------------------")
  ctx.append({
    'method'   : 'loadedStrParam',
    'msg'      : aMessage,
    'kwargs'   : kwargs,
    'dispType' : type(disp)
  })

"""
document:
  - sections
  - index
  - figures
  - tables
  - glossary 
  - cross-references
  - citations/references
  - code sections (Lua/MetaPost/MetaFun)

command:
  - definitions?
  - uses?

modules:
  - uses?

# see: http://www.pragma-ade.nl/general/manuals/ma-cb-en.pdf

\abbreviation
\adaptlayout
\at
\bf
\blank
\bTABLE
\bTD
\bTR
\cap
\chapter
\chemical
\color
\column
\completecontent
\completeindex
\completelistofabbreviations
\completelistofsorts
\completeregister
\crlf
\currentdate
\DC
\DL
\DR
\definebodyfont
\definecolor
\definecombinedlist
\definedescription
\defineenumeration
\definefloat
\definelist
\definemakeup
\defineregister
\definesorting
\definesymbol
\definesynonyms
\definetabulate
\definetextbackground
\em
\en
\eTABLE
\eTD
\eTR
\externalfigure
\FLOWchart
\FR
\fixedspaces
\footnote
\framed
\from
\getbuffer
\getvariable
\goto
\HL
\hairline
\head
\high
\hskip
\in
\indenting
\index
\inframed
\infull
\inleft
\inmargin
\input
\inright
\item
\LOW
\LR
\language
\leftlines
\loadabbreviations
\lohi
\low
\MR
\mainlanguage
\margintext
\margintitle
\midaligned
\NC
\NR
\nl
\noheaderandfooterlines
\noindenting
\nowhitespace
\overstrikes
\page
\pagereference
\par
\paragraph
\periods
\placecontent
\placefigure
\placeformula
\placeindex
\placeintermezzo
\placelistofabbreviations
\placelistofsorts
\placepublications
\placeregister
\placetable
\quote
\rightaligned
\rm
\rotate
\SR
\savebuffer
\scale
\setup
\setup tolerance
\setupalign
\setupbackgrounds
\setupbibtex
\setupblank
\setupbodyfont
\setupbuffer
\setupcaptions
\setupcolors
\setupcolumns
\setupcombinedlist
\setupdescriptions
\setupenumerations
\setupfigures
\setupfloat
\setupfloats
\setupfooter
\setupfootertexts
\setupfootnotes
\setupformulas
\setupframed
\setupframedtext
\setuphead
\setupheader
\setupheadertexts
\setupheads
\setupindenting
\setupinteraction
\setupitemize
\setuplayout
\setuplist
\setupmakeup
\setuppagenumbering
\setuppublications
\setupregister
\setupscale
\setupsorting
\setupsynonyms
\setupTABLE
\setuptables
\setuptabulate
\setuptextbackground
\setupthinrules
\setuptype
\setuptyping
\setupuserpagenumber
\setupwhitespace
\setupxtable
\setvariables
\showframe
\showlayout
\showmakeup
\showsetups
\sl
\sort
\space
\ss
\startbuffer
\startcolums
\startcombination
\startcomment
\startfiguretext
\startformula
\startframedtext
\starthiding
\startitemize
\startlinecorrection
\startlines 
\startlocal
\startpacked
\startstandardmakeup
\starttable
\starttabulate
\starttextbackground
\starttextrule
\starttyping
\startunpacked
\startxcell
\startxrow
\startxtable
\stopxtable
\subject
\subparagraph
\subsubject
\switchtobodyfont
\THREE
\TWO
\tfa
\tfb
\tfc
\tfd
\thinrule
\thinrules
\title
\tt
\type
\typebuffer
\underbar
\unit
\useexternaldocument
\usemodule
\VL
\vskip
\whitespace
\writebetweenlist
\writetolist
"""