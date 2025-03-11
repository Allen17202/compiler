import sys
from antlr4 import *
sys.path.append('./')
from grammar.TypeWhileLexer import TypeWhileLexer
from grammar.TypeWhileParser import TypeWhileParser
from grammar.TypeWhileVisitor import TypeWhileVisitor
import logging
from textwrap import indent, dedent

symtab = {}  # E - environment

def check(condition, message):
    if not condition:
        sys.stderr.write(f"type error: {message}\n")

        print("1")
        exit(1)
    else:
        # no type error
        pass

class TypeChecker(TypeWhileVisitor):
    # Visit a parse tree produced by TypeWhileParser#Assignment.
    def visitAssignment(self, ctx:TypeWhileParser.AssignmentContext):
        varName = ctx.ID().getText()
        check(varName in symtab, f"Var [{varName}]: no declaraction bf assignment.")

        varType = symtab[varName]
        exprType = self.visit(ctx.e())

        check(varType == exprType, f"TypeMismatch: [{varName}] Expected: [{varType}] Received: [{exprType}]")
        return varType


    # Visit a parse tree produced by TypeWhileParser#Skip.
    def visitSkip(self, ctx:TypeWhileParser.SkipContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeWhileParser#Compound.
    def visitCompound(self, ctx:TypeWhileParser.CompoundContext):
        for expr in ctx.s():
            self.visit(expr)
        return None


    # Visit a parse tree produced by TypeWhileParser#If.
    def visitIf(self, ctx:TypeWhileParser.IfContext):
        conditional = self.visit(ctx.e())
        check(conditional == "bool", "Condition in 'if' must be of type bool")
        self.visit(ctx.s(0))
        self.visit(ctx.s(1))
        return None


    # Visit a parse tree produced by TypeWhileParser#While.
    def visitWhile(self, ctx:TypeWhileParser.WhileContext):
        conditional = self.visit(ctx.e())
        check(conditional == "bool", "Condition in 'while' must be of type bool")
        self.visit(ctx.s())
        return None


    # Visit a parse tree produced by TypeWhileParser#Declaration.
    def visitDeclaration(self, ctx:TypeWhileParser.DeclarationContext):
        varName = ctx.ID().getText()
        varType = ctx.typeName.text

        check(varName not in symtab, f"Var[{varName}] has already been declared")
        symtab[varName] = varType
        return varType

    # Visit a parse tree produced by TypeWhileParser#Not.
    def visitNot(self, ctx:TypeWhileParser.NotContext):
        exprType = self.visit(ctx.e())
        check(exprType == "bool", "Not Op requires a bool operand")
        return "bool"


    # Visit a parse tree produced by TypeWhileParser#Var.
    def visitVar(self, ctx:TypeWhileParser.VarContext):
        varName = ctx.ID().getText()
        check(varName in symtab, f"variable [{varName}]: used bf declaraction.")
        return symtab[varName]


    # Visit a parse tree produced by TypeWhileParser#Num.
    def visitNum(self, ctx:TypeWhileParser.NumContext):
        return "int"


    # Visit a parse tree produced by TypeWhileParser#True.
    def visitTrue(self, ctx:TypeWhileParser.TrueContext):
        return "bool"


    # Visit a parse tree produced by TypeWhileParser#False.
    def visitFalse(self, ctx:TypeWhileParser.FalseContext):
        return "bool"


    # Visit a parse tree produced by TypeWhileParser#BinOp.
    def visitBinOp(self, ctx:TypeWhileParser.BinOpContext):
        left = self.visit(ctx.e(0))
        op = ctx.op.text
        right = self.visit(ctx.e(1))
        
    
        if op in {"+", "-", "*", "/"}:
            check(left == "int" and right == "int", f"Operator '{op}' need two int operands")
            return "int"
        elif op in {"and", "or"}:
            check(left == "bool" and right == "bool", f"Operator '{op}' need two bool operands")
            return "bool"
        elif op in {"<", "<=", ">", ">="}:
            check(left == "int" and right == "int", f"Comparision '{op}' need two int operands")
            return "bool"
        else:
            check(False,f"Unknown Operator '{op}'")
            return None


    # Visit a parse tree produced by TypeWhileParser#Paren.
    def visitParen(self, ctx:TypeWhileParser.ParenContext):
        return self.visit(ctx.e())


input_stream = StdinStream()
lexer = TypeWhileLexer(input_stream)
stream = CommonTokenStream(lexer)
parser = TypeWhileParser(stream)
tree = parser.s()

if parser.getNumberOfSyntaxErrors() > 0:
  print("syntax errors")
  exit(1)
typechecker = TypeChecker()
typechecker.visit(tree)
print("\n".join([ f"symtab[{name}]: {symtab[name]}" for name in symtab ]))
print("0")
