
"""
 * @author nhphung
"""
from abc import ABC, abstractmethod, ABCMeta
from dataclasses import dataclass
from typing import List, Tuple
from AST import *
from Visitor import *
from StaticError import *
from functools import *


class Type(ABC):
    __metaclass__ = ABCMeta
    pass


class Prim(Type):
    __metaclass__ = ABCMeta
    pass


class IntType(Prim):
    pass


class FloatType(Prim):
    pass


class StringType(Prim):
    pass


class BoolType(Prim):
    pass


class VoidType(Type):
    pass


class Unknown(Type):
    pass


@dataclass
class ArrayType(Type):
    dimen: List[int]
    eletype: Type


@dataclass
class MType:
    intype: List[Type]
    restype: Type


@dataclass
class Symbol:
    name: str
    mtype: Type


class StaticChecker(BaseVisitor):
    def __init__(self, ast):
        self.ast = ast
        self.global_envi = [
            Symbol("int_of_float", MType([FloatType()], IntType())),
            Symbol("float_of_int", MType([IntType()], FloatType())),
            Symbol("int_of_string", MType([StringType()], IntType())),
            Symbol("string_of_int", MType([IntType()], StringType())),
            Symbol("float_of_string", MType([StringType()], FloatType())),
            Symbol("string_of_float", MType([FloatType()], StringType())),
            Symbol("bool_of_string", MType([StringType()], BoolType())),
            Symbol("string_of_bool", MType([BoolType()], StringType())),
            Symbol("read", MType([], StringType())),
            Symbol("printLn", MType([], VoidType())),
            Symbol("printStr", MType([StringType()], VoidType())),
            Symbol("printStrLn", MType([StringType()], VoidType()))]

    def check(self):
        return self.visit(self.ast, self.global_envi)

    def visitProgram(self, ast, c):
        # c = reduce(lambda acc, ele: [acc[0] + [self.visit(ele, acc)], acc[1] + [self.visit(ele, acc)]], ast.decl, [[], []])
        c = [[],[],[], True]
        for x in ast.decl:
            temp = self.visit(x,c)
            if isinstance(x,VarDecl):
                c[0].append(temp)
                c[1].append(temp)
            
        # Flag to second traverser
        c[3] = False
        
        # Check has no main function
        for x in c[2]:  
            if 'main' not in [x[0].name for x in c[2]]:
                raise NoEntryPoint()
        
        for x in ast.decl:
            if isinstance(x, FuncDecl):
                temp = self.visit(x,c)
                c[0].append(temp)
                c[1].append(temp)
        # print([ (x[0].name,x[1],x[2]) for x in c[0]]) 

    def visitVarDecl(self, ast, c):
        if list(filter(lambda x: x[0].variable == ast.variable, c[0])):
            raise Redeclared(Variable(), ast.variable.name)
        typ = Unknown()

        # Check redeclare built-in function name
        if ast.variable.name in [x.name for x in self.global_envi]:
            raise Redeclared(Variable(), ast.variable.name)
        
        # Case function parameter
        if ast.varDimen == None:
            typ = Unknown()
        else:
            if ast.varInit:
                # if isinstance(ast.varInit, ArrayLiteral): typ = ArrayType(ast.varDimen, ast.varInit)
                if isinstance(ast.varInit, ArrayLiteral): typ = ArrayType(ast.varDimen, ast.varInit)
                if isinstance(ast.varInit, IntLiteral): typ = IntType()
                if isinstance(ast.varInit, FloatLiteral): typ = FloatType()
                if isinstance(ast.varInit, BooleanLiteral): typ = BoolType()
                if isinstance(ast.varInit, StringLiteral): typ = StringType()
        return [ast, typ]

    def visitFuncDecl(self, ast, c):
        # Default Unknown type if has no return stmt
        if c[3] == True:
            param_list = [self.visit(x, [[],[]])[1] for x in ast.param]
            
            func = [ast.name, param_list, Unknown()]
            c[2].append(func)
            return
        
        # Check redeclare name of function
        for x in c[0]:
            if isinstance(x[0], FuncDecl):
                if x[0].name == ast.name:
                    raise Redeclared(Function(), ast.name.name)
            else:
                if x[0].variable.name == ast.name.name:
                    raise Redeclared(Function(), ast.name.name)

        # Check name with buil-in function
        if ast.name.name in [x.name for x in self.global_envi]:
            raise Redeclared(Function(), ast.name.name)
        
        # Add the function to calllee recursive
        temp_env = c[1] + [[ast, Unknown()]]
        # pre_declare = c[2]
        
        #check = reduce(lambda acc, ele: [acc[0] + [self.visit(ele, acc)], acc[1] + [self.visit(ele, acc)]], ast.param + ast.body[0], [[], temp_env])
        # local | glbal | funcDecl | return_typ 
        # check = [[],temp_env,[],[Unknown()], pre_declare]
        
        # Check redeclare parameter
        name_para = [x.variable.name for x in ast.param]
        i = 1
        for x in name_para: 
            if x in name_para[i:]:
                raise Redeclared(Parameter(), x) 
            i = i + 1
        
        check = [[],temp_env,c[2]]
        for x in ast.param + ast.body[0]:
            temp = self.visit(x,check)
            check[0].append(temp)
            check[1].append(temp)

        # print(check[0])
        
        # Update parameter first
        for x in c[2]:
            # print(check[0][3][1])
            if ast.name.name == x[0].name:
                for index in range(0, len(ast.param)):
                    check[0][index][1] = x[1][index]
                    # check[1][len(check[1]) - len(ast.param) + index][1] = x[1][index]
            # print(check[0][3][1])
                break
        # Visit statement statement
        for x in ast.body[1]:
            self.visit(x, check)
        # print(ast.name, check[0])
        # Update changes
        for x in range(0, len(c[1])):
            c[0][x] = check[1][x]
            c[1][x] = check[1][x]
        
        # Return type of this function
        for x in c[2]:
            if ast.name.name == x[0].name:
                for index in range(0, len(ast.param)):
                    x[1][index] = check[0][index][1]
                return [ast, x[2]]
        
        return [ast,typ]

    def visitAssign(self, ast, c):
        left = self.visit(ast.lhs, c)
        right = self.visit(ast.rhs, c)
        # print(c[0])
        if right == 1 : raise TypeCannotBeInferred(ast)
        if isinstance(left, Unknown) and isinstance(right, Unknown):
            raise TypeCannotBeInferred(ast)
        
        if type(left) == Unknown and type(right) == VoidType:
            raise TypeMismatchInStatement(ast)
        
        if isinstance(left, Unknown):
            # left = IntType()
            if isinstance(ast.lhs, Id):
                if ast.lhs.name not in [x[0].variable.name for x in c[0]]:
                    for x in c[1]:
                        if isinstance(x[0], VarDecl):
                            if ast.lhs.name == x[0].variable.name:
                                x[1] = right
                                return
                else:
                    for x in c[0]:
                        if isinstance(x[0], VarDecl):
                            if ast.lhs.name == x[0].variable.name:
                                x[1] = right
                                return
            else:
                if ast.lhs.arr.name not in [x[0].variable.name for x in c[0]]:
                    for x in c[1]:
                        if isinstance(x[0], VarDecl):
                            if ast.lhs.arr.name == x[0].variable.name:
                                x[1] = right
                                return
                else:
                    for x in c[0]:
                        if isinstance(x[0], VarDecl):
                            if ast.lhs.arr.name == x[0].variable.name:
                                x[1] = right
                                return
                
        if isinstance(right, Unknown):
            # right = IntType()
            if ast.rhs.name not in [x[0].variable.name for x in c[0]]:
                for x in c[1]:
                    if isinstance(x[0], VarDecl):
                        if ast.rhs.name == x[0].variable.name:
                            x[1] = left
                            return
            else:
                for x in c[0]:
                    if isinstance(x[0], VarDecl):
                        if ast.rhs.name == x[0].variable.name:
                            x[1] = left
                            return
        # Return from function call
        if isinstance(right, VoidType):
            right = left
            for par in c[2]:
                if ast.rhs.method.name == par[0].name:
                    par[2] = right
        if type(left) != type(right) or type(left) == VoidType:
            raise TypeMismatchInStatement(ast)

    def visitBinaryOp(self, ast, param):
        left_typ = Unknown()
        right_typ = Unknown()
        return_typ = Unknown()
        if ast.op in ['+', '-', '*', '\\', '%']:
            return_typ = IntType()
            left_typ = IntType()
            right_typ = IntType()
        if ast.op in ['+.', '-.', '*.', '\\.']:
            return_typ = FloatType()
            left_typ = FloatType()
            right_typ = FloatType()
        if ast.op in ['==', '!=', '<', '>','<=','>=']:
            return_typ = BoolType()
            left_typ = IntType()
            right_typ = IntType()
        if ast.op in ['=/=','<.', '>.','<=.','>=.']:
            return_typ = BoolType()
            left_typ = FloatType()
            right_typ = FloatType()
        if ast.op in ['&&','||']:
            return_typ = BoolType()
            left_typ = BoolType()
            right_typ = BoolType()
        
        left = self.visit(ast.left, param)
        if left == 1: return 1
        if isinstance(left, Unknown):
            left = left_typ
            # Check local first, that mean check param[1]
            if not isinstance(ast.left, ArrayCell):
                if ast.left.name not in [x[0].name.name if isinstance(x[0], FuncDecl) else x[0].variable.name for x in param[0]]:
                    # Check global envi
                    for x in param[1]:
                        if isinstance(x[0], VarDecl):
                            if x[0].variable.name == ast.left.name:
                                x[1] = left_typ
                        else:
                            if x[0].name.name == ast.left.name:
                                x[1] = left_typ
                else: # Local envi
                    for x in param[0]:
                        if isinstance(x[0], VarDecl):
                            if x[0].variable.name == ast.left.name:
                                x[1] = left_typ
                        else:
                            if x[0].name.name == ast.left.name:
                                x[1] = left_typ
        # Return from function call
        if isinstance(left, VoidType):
            left = left_typ
            for par in param[2]:
                if ast.left.method.name == par[0].name:
                    par[2] = left_typ
            

        right = self.visit(ast.right, param)
        if right == 1: return 1
        if isinstance(right, Unknown):
            right = right_typ
            # Check local first, that mean check param[1]
            if ast.right.name not in [x[0].name.name if isinstance(x[0], FuncDecl) else x[0].variable.name for x in param[0]]:
                # Check global envi
                for x in param[1]:
                    if isinstance(x[0], VarDecl):
                        if x[0].variable.name == ast.right.name:
                            x[1] = right_typ
                    else:
                        if x[0].name.name == ast.right.name:
                            x[1] = right_typ
            else: # Local envi
                    for x in param[0]:
                        if isinstance(x[0], VarDecl):
                            if x[0].variable.name == ast.right.name:
                                x[1] = right_typ
                        else:
                            if x[0].name.name == ast.right.name:
                                x[1] = right_typ
        # Return from function call
        if isinstance(right, VoidType):
            right = right_typ
            for par in param[2]:
                if ast.right.method.name == par[0].name:
                    par[2] = right_typ
                            
        if type(left) != type(left_typ) or type(right) != type(right_typ):
            raise TypeMismatchInExpression(ast)
        return return_typ
        
    def visitId(self, ast, c):
        # Check local first
        for x in c[0]:
            if isinstance(x[0], VarDecl):
                if ast == x[0].variable:
                    return x[1]
            # else:
            #     if ast == x[0].name:
            #         return x[1]
                
        for x in c[1]:
            if isinstance(x[0], VarDecl):
                if ast == x[0].variable:
                    return x[1]
            # else:
            #     if ast == x[0].name:
            #         return x[1]
        raise Undeclared(Identifier(), ast.name)

    def visitUnaryOp(self, ast, param):
        body = self.visit(ast.body, param)
        if body == 1: return 1
        if ast.op in ['-','-.','!']:
            typ = IntType() if ast.op=='-' else ( FloatType() if ast.op=='-.' else BoolType())
            if isinstance(body, Unknown):
                # Check local first, that mean check param[1]
                body = typ
                if not isinstance(ast.body, ArrayCell):
                    if ast.body.name not in [x[0].name.name if isinstance(x[0], FuncDecl) else x[0].variable.name for x in param[0]]:
                        # Check global envi
                        for x in param[1]:
                            if isinstance(x[0], VarDecl):
                                if x[0].variable.name == ast.body.name:
                                    x[1] = typ
                            else:
                                if x[0].name.name == ast.body.name:
                                    x[1] = typ
                    else: # Local envi
                        for x in param[0]:
                            if isinstance(x[0], VarDecl):
                                if x[0].variable.name == ast.body.name:
                                    x[1] = typ
                            else:
                                if x[0].name.name == ast.body.name:
                                    x[1] = typ
            # Return from function call
            if isinstance(body, VoidType):
                body = typ
                for par in param[2]:
                    if ast.body.method.name == par[0].name:
                        par[2] = typ
            if ast.op=='-' and type(body)!=IntType: raise TypeMismatchInExpression(ast) 
            if ast.op=='-.' and type(body)!=FloatType: raise TypeMismatchInExpression(ast) 
            if ast.op=='!' and type(body)!=BoolType: raise TypeMismatchInExpression(ast) 
            
            return typ

    def visitArrayCell(self, ast, param):
        for x in ast.idx:
            temp = self.visit(x, param)
            if type(temp) != IntType: raise TypeMismatchInExpression(ast)

        typ_arr = self.visit(ast.arr, param)
        if type(typ_arr) != ArrayType and type(typ_arr) != Unknown: raise TypeMismatchInExpression(ast)
        return typ_arr

    def visitIf(self, ast, param):
        #ifthenStmt:List[Tuple[Expr,List[VarDecl],List[Stmt]]]
        #elseStmt:Tuple[List[VarDecl],List[Stmt]]
        temp_env = param[1]
        check = [[],temp_env, param[2]]
        for ifstmt in ast.ifthenStmt:
            check = [[],check[1], param[2]]
            return_exp = self.visit(ifstmt[0], check)
            if type(return_exp) != BoolType and type(return_exp) != Unknown: raise TypeMismatchInStatement(ast)
            
            if type(return_exp) == Unknown: self.visitIfUpdate(ifstmt[0], check)

            
            for var_stmt in ifstmt[1]:
                temp = self.visit(var_stmt, check)
                check[0].append(temp)
                check[1].insert(0,temp)
            
            for stmt in ifstmt[2]: self.visit(stmt,check)
            
            check[1] = check[1][len(check[0]):]
            # update changes
            
            # for x in len(ifstmt)
        
        check_for = [[], temp_env, param[2]]
        for var_else in ast.elseStmt[0]:
            temp = self.visit(var_else, check_for)
            check_for[0].append(temp)
            check_for[1].insert(0, temp)
        for stmt_else in ast.elseStmt[1]: self.visit(stmt_else, check_for)
        check_for[1] = check_for[1][len(check_for[0]):]
    
    def visitIfUpdate(self, id, c):
        for x in c[0]:
            if isinstance(x[0], VarDecl):
                if id == x[0].variable:
                    x[1] = BoolType()
            else:
                if id == x[0].name:
                    x[1] = BoolType()
                
        for x in c[1]:
            if isinstance(x[0], VarDecl):
                if id  == x[0].variable:
                    x[1] = BoolType()
            else:
                if id == x[0].name:
                    x[1] = BoolType()

    def visitFor(self, ast, param):
        ret_exp1 = self.visit(ast.expr1, param)
        if type(ret_exp1) != IntType: raise TypeMismatchInStatement(ast)
        ret_exp2 = self.visit(ast.expr2, param)
        if type(ret_exp2) != BoolType: raise TypeMismatchInStatement(ast)
        ret_exp3 = self.visit(ast.expr3, param)
        if type(ret_exp3) != IntType: raise TypeMismatchInStatement(ast)
        
        check = [[],param[1], param[2]]
        
        for x in ast.loop[0]:
            temp = self.visit(x, check)
            check[0].append(temp)
            check[1].insert(0,temp)
        for x in ast.loop[1]:
            self.visit(x,check)
        check[1] = check[1][len(check[0]):]
        
    def visitContinue(self, ast, param):
        return None

    def visitBreak(self, ast, param):
        return None

    def visitDowhile(self, ast, param):
        check = [[],param[1],param[2]]
        for x in ast.sl[0] :
            temp = self.visit(x, check)
            check[0].append(temp)
            check[1].insert(0,temp)
        for x in ast.sl[1]: self.visit(x, check)
        check[1] = check[1][len(check[0]):]
        
        ret_exp = self.visit(ast.exp, param)
        if type(ret_exp) != BoolType: raise TypeMismatchInStatement(ast)

    def visitWhile(self, ast, param):
        ret_exp = self.visit(ast.exp, param)
        if type(ret_exp) != BoolType: raise TypeMismatchInStatement(ast)
        check = [[],param[1].copy(),param[2]]
        
        for x in ast.sl[0] :
            temp = self.visit(x, check)
            check[0].append(temp)
            check[1].insert(0,temp)
        for x in ast.sl[1]: self.visit(x, check)
        check[1] = check[1][len(check[0]):]

    # Simple function call
    def visitCallStmt(self, ast, param):
        return_typ = VoidType()
        func_param = [self.visit(x, param) for x in ast.param]
        # Check function declared befores
        index_fun = len(param[1]) - len(param[0]) - 1
        if ast.method.name in [x.name for x in self.global_envi]:
            if ast.method.name == 'printLn':
                if len(func_param) != 0:
                    raise TypeMismatchInStatement(ast)
            elif ast.method.name in ['printStr','printStrLn' ]:
                if len(func_param) != 1 or type(func_param[0]) != StringType:
                    raise TypeMismatchInStatement(ast)
            else: raise TypeMismatchInStatement(ast)
        if ast.method.name not in [x[0].name for x in param[2]]: raise Undeclared(Function(), ast.method.name)
        for x in param[2]:
            if ast.method.name == x[0].name:
                if len(x[1]) != len(func_param):
                    raise TypeMismatchInStatement(ast)
                else:
                    for index in range(0, len(func_param)):
                        if type(func_param[index]) == Unknown and type(x[1][index]) == Unknown:
                            raise TypeCannotBeInferred(ast)
                        if type(x[1][index]) != type(func_param[index]) and type(x[1][index]) != Unknown:
                            if type(func_param[index]) == Unknown:
                                name = ast.param[index].name
                                if name not in [var[0].variable.name for var in param[0]]:
                                    for var in param[1]:
                                        if isinstance(var[0], VarDecl):
                                            if name == var[0].variable.name:
                                                var[1] = x[1][index]
                                else:
                                    for var in param[0]:
                                        if isinstance(var[0], VarDecl):
                                            if name == var[0].variable.name:
                                                var[1] = x[1][index]
                            else: raise TypeMismatchInStatement(ast)
                        x[1][index] = func_param[index]

                # nghĩa là hàm được gọi sau khai báo của nó
                if type(x[2]) != Unknown: pass 
                    # return type(x[2])
                else: 
                    x[2] = return_typ
        # return IntType()
    
    # Return from function call with another operators
    def visitCallExpr(self, ast, param):
        func_param = [self.visit(x, param) for x in ast.param]
        if ast.method.name in [x.name for x in self.global_envi]:
            if ast.method.name in ['printLn', 'printStr', 'printStrLn']:
                if ast.method.name == 'printLn':
                    if len(func_param) != 0:
                        raise TypeMismatchInStatement(ast)
                    return VoidType()
                elif ast.method.name in ['printStr','printStrLn' ]:
                    if len(func_param) != 1 or type(func_param[0]) != StringType:
                        raise TypeMismatchInStatement(ast)
                    return VoidType()
            else:
                if ast.method.name == 'int_of_float':
                    if len(func_param) != 1 or type(func_param[0]) != FloatType: raise TypeMismatchInExpression(ast)
                    return IntType()
                if ast.method.name == 'float_of_int':
                    if len(func_param) != 1 or type(func_param[0]) != IntType: raise TypeMismatchInExpression(ast)
                    return FloatType()
                if ast.method.name == 'int_of_string':
                    if len(func_param) != 1 or type(func_param[0]) != StringType: raise TypeMismatchInExpression(ast)
                    return IntType()
                if ast.method.name == 'string_of_int':
                    if len(func_param) != 1 or type(func_param[0]) != IntType: raise TypeMismatchInExpression(ast)
                    return StringType()
                if ast.method.name == 'float_of_string':
                    if len(func_param) != 1 or type(func_param[0]) != StringType: raise TypeMismatchInExpression(ast)
                    return FloatType()
                if ast.method.name == 'string_of_float':
                    if len(func_param) != 1 or type(func_param[0]) != FloatType: raise TypeMismatchInExpression(ast)
                    return StringType()
                if ast.method.name == 'bool_of_string':
                    if len(func_param) != 1 or type(func_param[0]) != StringType: raise TypeMismatchInExpression(ast)
                    return BoolType()
                if ast.method.name == 'string_of_bool':
                    if len(func_param) != 1 or type(func_param[0]) != BoolType: raise TypeMismatchInExpression(ast)
                    return StringType()
        
        if ast.method.name not in [x[0].name for x in param[2]]: raise Undeclared(Function(), ast.method.name)
        
        for x in param[2]:
            if ast.method.name == x[0].name:
                if len(func_param) != len(x[1]):
                    raise TypeMismatchInStatement(ast)
                else:
                    for index in range(0, len(func_param)):
                        if type(func_param[index]) == Unknown and type(x[1][index]) == Unknown:
                            # raise TypeCannotBeInferred(ast)
                            return 1
                        if type(x[1][index]) != type(func_param[index]) and type(x[1][index]) != Unknown:
                            if type(func_param[index]) == Unknown:
                                name = ast.param[index].name
                                if name not in [var[0].variable.name for var in param[0]]:
                                    for var in param[1]:
                                        if isinstance(var[0], VarDecl):
                                            if name == var[0].variable.name:
                                                var[1] = x[1][index]
                                else:
                                    for var in param[0]:
                                        if isinstance(var[0], VarDecl):
                                            if name == var[0].variable.name:
                                                var[1] = x[1][index]
                            else: raise TypeMismatchInStatement(ast)
                        x[1][index] = func_param[index]
                        
                        
                if type(x[2]) != Unknown:
                    return x[2]
                else: 
                    x[2] = VoidType()
                    return VoidType()
        raise Undeclared(Function(), ast.method.name)
    
    def visitReturn(self, ast, param):
        return_typ = VoidType()        
        index_fun = len(param[1]) - len(param[0] ) - 1
        if not ast.expr:
            return_typ = VoidType()
        else:
            return_typ  = self.visit(ast.expr,param)
        
        for x in param[2]:
            # print(param[1], index_fun)
            if param[1][index_fun][0].name.name == x[0].name:
                if type(x[2]) != Unknown and type(x[2]) != type(return_typ):
                    raise TypeMismatchInStatement(ast)
                else: 
                    x[2] = return_typ
                
    def visitIntLiteral(self, ast, param):
        return IntType()

    def visitFloatLiteral(self, ast, param):
        return FloatType()

    def visitStringLiteral(self, ast, param):
        return StringType()

    def visitBooleanLiteral(self, ast, param):
        return BoolType()

    def visitArrayLiteral(self, ast, param):
        # print(ast)
        
        # Assume that all element is the same type
        dimen = len(ast.value)
        eletyp = self.visit(ast.value[0], param)
        return ArrayType(dimen, eletyp)


# Declaration programming code here
