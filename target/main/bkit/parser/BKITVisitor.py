# Generated from main/bkit/parser/BKIT.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .BKITParser import BKITParser
else:
    from BKITParser import BKITParser

# This class defines a complete generic visitor for a parse tree produced by BKITParser.

class BKITVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by BKITParser#program.
    def visitProgram(self, ctx:BKITParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#var_declare.
    def visitVar_declare(self, ctx:BKITParser.Var_declareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#variable_list.
    def visitVariable_list(self, ctx:BKITParser.Variable_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#variable.
    def visitVariable(self, ctx:BKITParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#dimension.
    def visitDimension(self, ctx:BKITParser.DimensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#literal.
    def visitLiteral(self, ctx:BKITParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#boolean_literal.
    def visitBoolean_literal(self, ctx:BKITParser.Boolean_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#func_declare.
    def visitFunc_declare(self, ctx:BKITParser.Func_declareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#parameters_list.
    def visitParameters_list(self, ctx:BKITParser.Parameters_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#parameter.
    def visitParameter(self, ctx:BKITParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#stm_list.
    def visitStm_list(self, ctx:BKITParser.Stm_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#stm.
    def visitStm(self, ctx:BKITParser.StmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#stm_assign.
    def visitStm_assign(self, ctx:BKITParser.Stm_assignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#variable_.
    def visitVariable_(self, ctx:BKITParser.Variable_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#stm_if.
    def visitStm_if(self, ctx:BKITParser.Stm_ifContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#stm_for.
    def visitStm_for(self, ctx:BKITParser.Stm_forContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#stm_while.
    def visitStm_while(self, ctx:BKITParser.Stm_whileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#stm_dowhile.
    def visitStm_dowhile(self, ctx:BKITParser.Stm_dowhileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#stm_break.
    def visitStm_break(self, ctx:BKITParser.Stm_breakContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#stm_continue.
    def visitStm_continue(self, ctx:BKITParser.Stm_continueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#stm_call.
    def visitStm_call(self, ctx:BKITParser.Stm_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#stm_return.
    def visitStm_return(self, ctx:BKITParser.Stm_returnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp_bool.
    def visitExp_bool(self, ctx:BKITParser.Exp_boolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp_int.
    def visitExp_int(self, ctx:BKITParser.Exp_intContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp_real.
    def visitExp_real(self, ctx:BKITParser.Exp_realContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp_str.
    def visitExp_str(self, ctx:BKITParser.Exp_strContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp.
    def visitExp(self, ctx:BKITParser.ExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp1.
    def visitExp1(self, ctx:BKITParser.Exp1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp2.
    def visitExp2(self, ctx:BKITParser.Exp2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp3.
    def visitExp3(self, ctx:BKITParser.Exp3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp4.
    def visitExp4(self, ctx:BKITParser.Exp4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp5.
    def visitExp5(self, ctx:BKITParser.Exp5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp6.
    def visitExp6(self, ctx:BKITParser.Exp6Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp7.
    def visitExp7(self, ctx:BKITParser.Exp7Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp8.
    def visitExp8(self, ctx:BKITParser.Exp8Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp9.
    def visitExp9(self, ctx:BKITParser.Exp9Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#index_exp.
    def visitIndex_exp(self, ctx:BKITParser.Index_expContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp_forindex.
    def visitExp_forindex(self, ctx:BKITParser.Exp_forindexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#call_exp.
    def visitCall_exp(self, ctx:BKITParser.Call_expContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#index_operator.
    def visitIndex_operator(self, ctx:BKITParser.Index_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#array_literal.
    def visitArray_literal(self, ctx:BKITParser.Array_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#literal_.
    def visitLiteral_(self, ctx:BKITParser.Literal_Context):
        return self.visitChildren(ctx)



del BKITParser