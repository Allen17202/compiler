all: WhileParser.py

WhileParser.py:	While.g4
	antlr4 -Dlanguage=Python3 -visitor $<

clean:
	rm -f While.interp WhileLexer.interp WhileLexer.py WhileLexer.tokens WhileListener.py WhileVisitor.py WhileParser.py While.tokens
