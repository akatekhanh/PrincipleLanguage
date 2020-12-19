from BKITVisitor import BKITVisitor
from BKITParser import BKITParser
from AST import *
#from test2string.ASTString import *
from functools import reduce

class ASTGeneration(BKITVisitor):
    # def visitProgram(self,ctx:BKITParser.ProgramContext):
    #     return Program([VarDecl(Id(ctx.ID().getText()),[],None)])

    def visitProgram(self,ctx:BKITParser.ProgramContext):
        var = reduce(lambda x,y:x+self.visitVar_declare(y),ctx.var_declare(),[])
        func = reduce(lambda x,y:x+self.visitFunc_declare(y),ctx.func_declare(),[])
        return Program(var + func)

    def visitVar_declare(self,ctx:BKITParser.Var_declareContext):
        return self.visit(ctx.variable_list())

    def visitVariable_list(self,ctx:BKITParser.Variable_listContext):
        i = ctx.getChildCount()
        i = i - int(i/2)
        return [self.visit(ctx.variable(j)) for j in range(i)]

    def visitVariable(self,ctx:BKITParser.VariableContext):
        variable = Id(ctx.ID().getText())
        varDimen = self.visit(ctx.dimension()) if ctx.dimension() else []
        varInit = self.visit(ctx.literal()) if ctx.literal() else None
        return VarDecl(variable, varDimen, varInit)

    def visitDimension(self,ctx:BKITParser.DimensionContext):
        i = ctx.getChildCount()
        i = int(i/3)
        return [int(ctx.INTEGER_LITERAL(j).getText()) for j in range(i)]

    def visitLiteral(self,ctx:BKITParser.LiteralContext):
        if ctx.boolean_literal():
            return self.visit(ctx.boolean_literal())
        if ctx.STRING_LITERAL():
            return StringLiteral(ctx.STRING_LITERAL().getText())
        if ctx.array_literal():
            return self.visit(ctx.array_literal())
        if ctx.FLOAT_LITERAL():
            return FloatLiteral(float(ctx.FLOAT_LITERAL().getText()))
        if ctx.INTEGER_LITERAL():
            tmp = str(ctx.INTEGER_LITERAL().getText())
            for i in range(len(tmp)):
                if tmp[i] == "O":
                    return IntLiteral(int(ctx.INTEGER_LITERAL().getText(),8))
                if tmp[i] == "o":
                    return IntLiteral(int(ctx.INTEGER_LITERAL().getText(),8))
                if tmp[i] == "X":
                    return IntLiteral(int(ctx.INTEGER_LITERAL().getText(),16))
                if tmp[i] == "x":
                    return IntLiteral(int(ctx.INTEGER_LITERAL().getText(),16))
            return IntLiteral(int(ctx.INTEGER_LITERAL().getText()))

    def visitBoolean_literal(self, ctx:BKITParser.Boolean_literalContext):
        val = True if ctx.TRUE() else False
        return BooleanLiteral(val)

    def visitArray_literal(self, ctx:BKITParser.Array_literalContext):
        i = ctx.getChildCount() - 2
        i = i - int(i/2)
        return ArrayLiteral([self.visit(ctx.literal(j)) for j in range(i)])

    # def visitElement(self, ctx:BKITParser.ElementContext):
    #     i = ctx.getChildCount()
    #     i = i - int(i/2)
    #     return [self.visit(ctx.literal(j)) for j in range(i)]

    def visitFunc_declare(self, ctx:BKITParser.Func_declareContext):
        name = Id(ctx.ID().getText())
        param = self.visit(ctx.parameters_list()) if ctx.parameters_list() else []
        body = self.visit(ctx.stm_list())
        return [FuncDecl(name,param,body)]

    def visitParameters_list(self, ctx:BKITParser.Parameters_listContext):
        i = ctx.getChildCount()
        i = i - int(i/2)
        return [self.visit(ctx.parameter(j)) for j in range(i)]

    def visitParameter(self, ctx:BKITParser.ParameterContext):
        if (ctx.dimension()):
            return VarDecl(Id(ctx.ID().getText()),self.visit(ctx.dimension()),None)
        else:
            return VarDecl(Id(ctx.ID().getText()),None,None)

    def visitStm_list(self, ctx:BKITParser.Stm_listContext):
        var_declare = reduce(lambda x,y:x+self.visitVar_declare(y),ctx.var_declare(),[])
        stm = reduce(lambda x,y:x+self.visitStm(y),ctx.stm(),[])
        return (var_declare,stm)

    def visitStm(self, ctx:BKITParser.StmContext):
        if(ctx.stm_assign()):
            return self.visit(ctx.stm_assign())
        if(ctx.stm_if()):
            return self.visit(ctx.stm_if())
        if(ctx.stm_for()):
            return self.visit(ctx.stm_for())
        if(ctx.stm_while()):
            return self.visit(ctx.stm_while())
        if(ctx.stm_dowhile()):
            return self.visit(ctx.stm_dowhile())            
        if(ctx.stm_break()):
            return self.visit(ctx.stm_break())
        if(ctx.stm_continue()):
            return self.visit(ctx.stm_continue())
        if(ctx.stm_call()):
            return self.visit(ctx.stm_call())
        if(ctx.stm_return()):
            return self.visit(ctx.stm_return())

    def visitStm_if(self, ctx: BKITParser.Stm_ifContext):
        if ctx.ELSE():
            stm_list_ = self.visit(ctx.stm_list()[-1]) 
            j = ctx.getChildCount() - 8
            j = int(j/4)
            ifthenStmt = [(self.visit(ctx.exp(i)),self.visit(ctx.stm_list(i))[0],self.visit(ctx.stm_list(i))[1]) for i in range(j+1)]
            elseStmt = (stm_list_)
            return [If(ifthenStmt,elseStmt)]
        else:
            j = ctx.getChildCount() - 6
            j = int(j/4)
            ifthenStmt = [(self.visit(ctx.exp(i)),self.visit(ctx.stm_list(i))[0],self.visit(ctx.stm_list(i))[1]) for i in range(j+1)]
            return [If(ifthenStmt,([],[]))]

    def visitStm_for(self, ctx: BKITParser.Stm_forContext):
        idx1 = Id(ctx.ID().getText())
        expr1 = self.visit(ctx.exp()[0])
        expr2 = self.visit(ctx.exp()[1])
        expr3 = self.visit(ctx.exp()[2])
        Loop = (self.visit(ctx.stm_list()))
        return [For(idx1,expr1,expr2,expr3,Loop)]

    def visitStm_while(self, ctx:BKITParser.Stm_whileContext):
        exp = self.visit(ctx.exp())
        sl0 = self.visit(ctx.stm_list())[0]
        sl1 = self.visit(ctx.stm_list())[1]
        return [While(exp,(sl0,sl1))]

    def visitStm_dowhile(self, ctx:BKITParser.Stm_dowhileContext):
        exp = self.visit(ctx.exp())
        sl0 = self.visit(ctx.stm_list())[0]
        sl1 = self.visit(ctx.stm_list())[1]
        return [Dowhile((sl0,sl1),exp)]

    def visitStm_break(self, ctx:BKITParser.Stm_breakContext):
        return [Break()]

    def visitStm_continue(self, ctx:BKITParser.Stm_continueContext):
        return [Continue()]

    def visitStm_return(self, ctx:BKITParser.Stm_returnContext):
        if ctx.exp():
            expr = self.visit(ctx.exp())
        else:
            expr = None
        return [Return(expr)]

    def visitStm_call(self, ctx:BKITParser.Stm_callContext):
        Id_ = Id(ctx.ID().getText())
        i = ctx.getChildCount() - 4
        i = i - int(i/2)
        param = [self.visit(ctx.exp(j)) for j in range(i)]
        return [CallStmt(Id_,param)]

    def visitStm_assign(self, ctx:BKITParser.Stm_assignContext):
        lhs = self.visit(ctx.variable_())
        rhs = self.visit(ctx.exp())
        return [Assign(lhs,rhs)]

    def visitVariable_(self, ctx:BKITParser.Variable_Context):
        if ctx.ID():
            return Id(ctx.ID().getText())
        if ctx.index_exp():
            return self.visit(ctx.index_exp())

    def visitExp(self, ctx:BKITParser.ExpContext):
        if ctx.getChildCount()>1:
            left = self.visit(ctx.exp1()[0])
            right = self.visit(ctx.exp1()[1])
            if ctx.EQ():
                op = str(ctx.EQ().getText())  
            if ctx.LTE():
                op = str(ctx.LTE().getText()) 
            if ctx.GTE():
                op = str(ctx.GTE().getText())
            if ctx.NEQ(): 
                op = str(ctx.NEQ().getText()) 
            if ctx.LT():
                op = str(ctx.LT().getText()) 
            if ctx.GT():
                op = str(ctx.GT().getText()) 
            if ctx.LTEF():
                op = str(ctx.LTEF().getText())
            if ctx.GTEF():
                op = str(ctx.GTEF().getText()) 
            if ctx.NEQF():
                op = str(ctx.NEQF().getText())
            if ctx.LTF():
                op = str(ctx.LTF().getText()) 
            if ctx.GTF():
                op = str(ctx.GTF().getText()) 
            return BinaryOp(op,left,right)
        else:
            return self.visit(ctx.exp1()[0])

    def visitExp1(self, ctx:BKITParser.Exp1Context):
        if ctx.getChildCount()>1:
            left = self.visit(ctx.exp1())
            right = self.visit(ctx.exp2())
            if ctx.AND():
                op = str(ctx.AND().getText()) 
            if ctx.OR():
                op = str(ctx.OR().getText()) 
            return BinaryOp(op,left,right)
        else:
            return self.visit(ctx.exp2())

    def visitExp2(self, ctx:BKITParser.Exp2Context):
        if ctx.getChildCount()>1:
            left = self.visit(ctx.exp2())
            right = self.visit(ctx.exp3())
            if ctx.ADD():
                op = str(ctx.ADD().getText()) 
            if ctx.ADDF():
                op = str(ctx.ADDF().getText()) 
            if ctx.SUB():
                op = str(ctx.SUB().getText()) 
            if ctx.SUBF():
                op = str(ctx.SUBF().getText()) 
            return BinaryOp(op,left,right)
        else:
            return self.visit(ctx.exp3())

    def visitExp3(self, ctx:BKITParser.Exp3Context):
        if ctx.getChildCount()>1:
            left = self.visit(ctx.exp3())
            right = self.visit(ctx.exp4())
            if ctx.MUL():
                op = str(ctx.MUL().getText()) 
            if ctx.MULF():
                op = str(ctx.MULF().getText())
            if ctx.DIV():
                op = str(ctx.DIV().getText())
            if ctx.DIVF():
                op = str(ctx.DIVF().getText()) 
            if ctx.MOD():
                op = str(ctx.MOD().getText()) 
            return BinaryOp(op,left,right)
        else:
            return self.visit(ctx.exp4())

    def visitExp4(self, ctx:BKITParser.Exp4Context):
        if ctx.getChildCount()>1:
            body = self.visit(ctx.exp4())
            if ctx.NOT():
                op = str(ctx.NOT().getText()) 
            if ctx.SUB():
                op = str(ctx.SUB().getText()) 
            return UnaryOp(op,body)
        else: 
            return self.visit(ctx.exp5())

    def visitExp5(self, ctx:BKITParser.Exp5Context):
        if ctx.getChildCount()>1:
            body = self.visit(ctx.exp5())
            if ctx.NOT():
                op = str(ctx.NOT().getText()) 
            return UnaryOp(op,body)
        else: 
            return self.visit(ctx.exp6())

    def visitExp6(self, ctx:BKITParser.Exp6Context):
        if ctx.getChildCount()>1:
            body = self.visit(ctx.exp6())
            if ctx.SUB():
                op = str(ctx.SUB().getText())
            if ctx.SUBF():
                op = str(ctx.SUBF().getText()) 
            return UnaryOp(op,body)
        else:
            return self.visit(ctx.exp7())

    def visitExp7(self, ctx:BKITParser.Exp7Context):
        if ctx.index_exp():
            return self.visit(ctx.index_exp()) 
        if ctx.exp8():
            return self.visit(ctx.exp8()) 

    def visitExp8(self, ctx:BKITParser.Exp8Context):
        if ctx.call_exp():
            return self.visit(ctx.call_exp()) 
        if ctx.exp9():
            return self.visit(ctx.exp9()) 

    def visitExp9(self, ctx:BKITParser.Exp9Context):
        if ctx.ID():
            return Id(ctx.ID().getText()) 
        if ctx.literal():
            return self.visit(ctx.literal()) 
        if ctx.exp():
            return self.visit(ctx.exp())

    def visitIndex_exp(self, ctx:BKITParser.Index_expContext):
        return ArrayCell(self.visit(ctx.exp_forindex()),self.visit(ctx.index_operator()))

    def visitExp_forindex(self, ctx:BKITParser.Exp_forindexContext):
        if ctx.ID():
            return Id(ctx.ID().getText()) 
        else:
            return self.visit(ctx.call_exp())

    def visitCall_exp(self, ctx:BKITParser.Call_expContext):
        method = Id(ctx.ID().getText()) 
        i = ctx.getChildCount() - 3
        i = i - int(i/2)
        param = [self.visit(ctx.exp(j)) for j in range(i)]
        return CallExpr(method,param)

    def visitIndex_operator(self, ctx:BKITParser.Index_operatorContext):
        i = ctx.getChildCount()
        i = int(i/3)
        return [self.visit(ctx.exp(j)) for j in range(i)]



    
