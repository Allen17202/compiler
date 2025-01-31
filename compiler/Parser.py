import sys
from antlr4 import *
sys.path.append('./')  # if you want to avoid PYTHONPATH
from grammar.WhileLexer import WhileLexer
from grammar.WhileParser import WhileParser
from grammar.WhileVisitor import WhileVisitor
import logging
from textwrap import indent, dedent

class Printer(WhileVisitor):
    def __init__(self):
        self.indentationLevel = 0
        
    def incrementIndentation(self):
        self.indentationLevel += 4
        
    def decrementIndentation(self):
         self.indentationLevel = max(0,self.indentationLevel - 4)
        
    def getIndentation(self):
        return " " * self.indentationLevel

    # visit a parse tree produced by WhileParser#Assignment.
    def visitAssignment(self, ctx:WhileParser.AssignmentContext):
        varName = ctx.ID().getText()
        expr = self.visit(ctx.a())
        return f"{self.getIndentation()}{varName} := {expr};\n"

    # visit a parse tree produced by WhileParser#Skip.
    def visitSkip(self, ctx:WhileParser.SkipContext):
        return f"{self.getIndentation()}skip"

    # visitChildren a parse tree produced by WhileParser#If. ND
    def visitIf(self, ctx:WhileParser.IfContext):
        conditional = self.visit(ctx.b())
        self.incrementIndentation()
        thenStat = self.visit(ctx.s(0))
        self.decrementIndentation()
        elseStat = ""
        if(ctx.s(1)):
            self.incrementIndentation()
            elseStat = f"else\n{self.visit(ctx.s(1))}"
            self.decrementIndentation()
        return f"{self.getIndentation()}if {conditional} then\n{thenStat}{self.getIndentation()}{elseStat}{self.getIndentation()}"


    # visit a parse tree produced by WhileParser#While. ND
    def visitWhile(self, ctx:WhileParser.WhileContext):
        conditional = self.visit(ctx.b())
        self.incrementIndentation()
        doStat = self.visit(ctx.s())
        self.decrementIndentation()
        return f"{self.getIndentation()}while {conditional} do\n{doStat}{self.getIndentation()}"

    # visit a parse tree produced by WhileParser#Compound. ND
    def visitCompound(self, ctx:WhileParser.CompoundContext):
        self.incrementIndentation()
        statements = [self.visit(statement) for statement in ctx.s()]
        self.decrementIndentation()
        return f"{self.getIndentation()}begin\n{''.join(statements)}{self.getIndentation()}end\n"


    # visit a parse tree produced by WhileParser#Not.
    def visitNot(self, ctx:WhileParser.NotContext):
        return f"not {self.visit(ctx.b())}"
     


    # visit a parse tree produced by WhileParser#ROp.
    def visitROp(self, ctx:WhileParser.ROpContext):
        left = self.visit(ctx.a(0))
        op = ctx.op.text
        right = self.visit(ctx.a(1))
        return f"({left} {op} {right})"


    # visit a parse tree produced by WhileParser#Or.
    def visitOr(self, ctx:WhileParser.OrContext):
        return f"({self.visit(ctx.b(0))} or {self.visit(ctx.b(1))})"


    # visit a parse tree produced by WhileParser#And.
    def visitAnd(self, ctx:WhileParser.AndContext):
        return f"({self.visit(ctx.b(0))} and {self.visit(ctx.b(1))})"


    # visit a parse tree produced by WhileParser#True.
    def visitTrue(self, ctx:WhileParser.TrueContext):
        return "true"


    # visit a parse tree produced by WhileParser#False.
    def visitFalse(self, ctx:WhileParser.FalseContext):
        return "false"


    # visit a parse tree produced by WhileParser#BParen.
    def visitBParen(self, ctx:WhileParser.BParenContext):
        return f"({self.visit(ctx.b())})"


    # visit a parse tree produced by WhileParser#AOp.
    def visitAOp(self, ctx:WhileParser.AOpContext):
        left = self.visit(ctx.a(0))
        op = ctx.op.text
        right = self.visit(ctx.a(1))
        return f"({left} {op} {right})"

    # visit a parse tree produced by WhileParser#Var.
    def visitVar(self, ctx:WhileParser.VarContext):
        return ctx.ID().getText()


    # visit a parse tree produced by WhileParser#Num.
    def visitNum(self, ctx:WhileParser.NumContext):
        return ctx.NUM().getText()


    # visit a parse tree produced by WhileParser#AParen.
    def visitAParen(self, ctx:WhileParser.AParenContext):
        return f"({self.visit(ctx.a())})"

input_stream = StdinStream()
lexer = WhileLexer(input_stream)
stream = CommonTokenStream(lexer)
parser = WhileParser(stream)
tree = parser.s()

if parser.getNumberOfSyntaxErrors() > 0:
  print("syntax errors")
  exit(1)
  
printer = Printer()
prettyPrintedText = printer.visit(tree)
preModifiedText = input_stream
print("Pre-Modified text:")
print(input_stream)
print("Modified text:")
print(prettyPrintedText)