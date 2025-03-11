all: WhileParser.py TypeWhileParser.py

TypeWhileParser.py:	TypeWhile.g4
	antlr4 -Dlanguage=Python3 -visitor $<

WhileParser.py:	While.g4
	antlr4 -Dlanguage=Python3 -visitor $<

clean:
	rm -f While.interp WhileLexer.interp WhileLexer.py WhileLexer.tokens WhileListener.py WhileVisitor.py WhileParser.py While.tokens
	rm -f TypeWhile.interp TypeWhileLexer.interp TypeWhileLexer.py TypeWhileLexer.tokens TypeWhileListener.py TypeWhileVisitor.py TypeWhileParser.py TypeWhile.tokens