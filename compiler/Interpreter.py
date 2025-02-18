import sys
from antlr4 import *
sys.path.append('./')  # if you want to avoid PYTHONPATH
from grammar.WhileLexer import WhileLexer
from grammar.WhileParser import WhileParser
from grammar.WhileVisitor import WhileVisitor
import logging
from textwrap import indent, dedent

class Interpreter(WhileVisitor):
    def __init__(self):
        self.symtab = {}

    # Visit a parse tree produced by WhileParser#Assignment.
    def visitAssignment(self, ctx:WhileParser.AssignmentContext):
        varName = ctx.ID().getText()
        expr = self.visit(ctx.a())
        self.symtab[varName] = expr
        return expr

    # Visit a parse tree produced by WhileParser#Skip.
    def visitSkip(self, ctx:WhileParser.SkipContext):
        return None

    # Visit a parse tree produced by WhileParser#If.
    def visitIf(self, ctx:WhileParser.IfContext):
        conditional = self.visit(ctx.b())
        if(conditional):
            return self.visit(ctx.s(0))
        elif(ctx.s(1)):
            return self.visit(ctx.s(1))
        return None

    # Visit a parse tree produced by WhileParser#While.
    def visitWhile(self, ctx:WhileParser.WhileContext):
        while(self.visit(ctx.b())):
            self.visit(ctx.s())
        return None

    # Visit a parse tree produced by WhileParser#Compound.
    def visitCompound(self, ctx:WhileParser.CompoundContext):
        for expr in ctx.s():
            self.visit(expr)
        return None

    # Visit a parse tree produced by WhileParser#Not.
    def visitNot(self, ctx:WhileParser.NotContext):
        return not self.visit(ctx.b())


    # Visit a parse tree produced by WhileParser#ROp.
    def visitROp(self, ctx:WhileParser.ROpContext):
        left = self.visit(ctx.a(0))
        op = ctx.op.text
        right = self.visit(ctx.a(1))

        if op == '>':
            return left > right
        elif op == '>=':
            return left >= right
        elif op == '<':
            return left < right
        elif op == '<=':
            return left <= right
        elif op == '=':
            return left == right
        return False


    # Visit a parse tree produced by WhileParser#Or.
    def visitOr(self, ctx:WhileParser.OrContext):
        return self.visit(ctx.b(0)) or self.visit(ctx.b(1))

    # Visit a parse tree produced by WhileParser#And.
    def visitAnd(self, ctx:WhileParser.AndContext):
        return self.visit(ctx.b(0)) and self.visit(ctx.b(1))

    # Visit a parse tree produced by WhileParser#True.
    def visitTrue(self, ctx:WhileParser.TrueContext):
        return True


    # Visit a parse tree produced by WhileParser#False.
    def visitFalse(self, ctx:WhileParser.FalseContext):
        return False


    # Visit a parse tree produced by WhileParser#BParen.
    def visitBParen(self, ctx:WhileParser.BParenContext):
        return self.visit(ctx.b())


    # Visit a parse tree produced by WhileParser#AOp.
    def visitAOp(self, ctx:WhileParser.AOpContext):
        left = self.visit(ctx.a(0))
        op = ctx.op.text
        right = self.visit(ctx.a(1))

        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left // right
        return 0

    # Visit a parse tree produced by WhileParser#Var.
    def visitVar(self, ctx:WhileParser.VarContext):
        varName = ctx.ID().getText()
        return self.symtab[varName]

    # Visit a parse tree produced by WhileParser#Num.
    def visitNum(self, ctx:WhileParser.NumContext):
        return int(ctx.NUM().getText())


    # Visit a parse tree produced by WhileParser#AParen.
    def visitAParen(self, ctx:WhileParser.AParenContext):
        return self.visit(ctx.a())

input_stream = StdinStream()
lexer = WhileLexer(input_stream)
stream = CommonTokenStream(lexer)
parser = WhileParser(stream)
tree = parser.s()
if parser.getNumberOfSyntaxErrors() > 0:
  print("syntax errors")
  exit(1)
interpreter = Interpreter()
interpreter.visit(tree)

#print("Symbol Table:")
print("\n".join([ f"symtab[{name}]: {interpreter.symtab[name]}" for name in interpreter.symtab ]))
