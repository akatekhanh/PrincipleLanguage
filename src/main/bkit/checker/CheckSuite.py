import unittest
from TestUtils import TestChecker
from StaticError import *
from AST import *

from main.bkit.checker.StaticError import TypeMismatchInStatement


class CheckSuite(unittest.TestCase):

    def test_undeclared_var_0(self):
        """Simple program: main"""
        input = """
        Var: b;
        Var: c;

        Function: foo
        Body:
            b = 10;
            main();
        EndBody.

        Function: main
        Body:
            Return 1;
        EndBody.

        """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_undeclared_var_1(self):
        """Simple program: main"""
        input = """
        Var: b;
        Var: c;

        Function: foo
        Body:
            b = 10;
            b = a + c;
        EndBody.

        Function: main
        Body:
        EndBody.

        """
        expect = str(Undeclared(Identifier(),"a"))
        self.assertTrue(TestChecker.test(input,expect,401))

    def test_undeclared_var_2(self):
        """Simple program: main"""
        input = """
        Var: b;
        Var: c = 1.0;
        Var: e;
        Function: foo
        Body:
            b = 10;
            b = e + c;
        EndBody.

        Function: main
        Body:
        EndBody.

        """
        expect = str(TypeMismatchInExpression(BinaryOp('+', Id('e'), Id('c'))))
        self.assertTrue(TestChecker.test(input,expect,402))

    def test_undeclared_var_3(self):
        """Simple program: main"""
        input = """
            Var: b;
            Var: c;
            Var: e;
            Function: foo
            Body:
                b = 10;
                b = e +. c;
            EndBody.

            Function: main
            Body:
            EndBody.

            """
        expect = str(TypeMismatchInStatement(Assign(Id('b'),BinaryOp('+.', Id('e'), Id('c')))))
        self.assertTrue(TestChecker.test(input, expect, 403))

    def test_undeclared_var_4(self):
        """Simple program: main"""
        input = """
            Var: b = 1;
            Var: c;
            Var: e;
            Function: foo
            Body:
                Var: b = True;
                Var: c = 2.0;
                b = e  == c;
            EndBody.

            Function: main
            Body:
            EndBody.

            """
        expect = str(TypeMismatchInExpression(BinaryOp('==', Id('e'), Id('c'))))
        self.assertTrue(TestChecker.test(input, expect, 404))

    def test_undeclared_var_5(self):
        """Simple program: main"""
        input = """
            Var: b = 1.0;
            Var: c;
            Var: e;
            Function: foo
            Body:
                Var: c = 2.0;
                b =  e =/= c;
            EndBody.

            Function: main
            Body:
            EndBody.

            """
        expect = str(TypeMismatchInStatement(Assign(Id('b'),BinaryOp('=/=',Id('e'),Id('c')))))
        self.assertTrue(TestChecker.test(input, expect, 405))

    def test_undeclared_var_6(self):
        """Simple program: main"""
        input = """
            Var: b;
            Var: c;
            Var: e;
            Function: foo
            Body:
                **b =  e =/= c;**
                Var: c = False;
                b = -c;
            EndBody.

            Function: main
            Body:
            EndBody.

            """
        expect = str(TypeMismatchInExpression(UnaryOp('-',Id('c'))))
        self.assertTrue(TestChecker.test(input, expect, 406))

    def test_undeclared_var_7(self):
        """Simple program: main"""
        input = """
            Var: b = 10;
            Var: c;
            Var: e;
            Function: foo
            Body:
                **b =  e =/= c;**
                Var: c = False;
                b = !c;
            EndBody.

            Function: main
            Body:
            EndBody.

            """
        expect = str(TypeMismatchInStatement(Assign(Id('b'),UnaryOp('!',Id('c')))))
        self.assertTrue(TestChecker.test(input, expect, 407))

    def test_undeclared_var_8(self):
        """Simple program: main"""
        input = """
            Var: b = 10;
            Var: c;
            Var: e;
            Var: f,g;
            Function: foo
            Body:
                **b =  e =/= c;**
                c = !e;
            EndBody.

            Function: main
            Body:
            g = 1.0;
            f = b + g;
            EndBody.

            """
        expect = str(TypeMismatchInExpression(BinaryOp('+',Id('b'),Id('g'))))
        self.assertTrue(TestChecker.test(input, expect, 408))

    def test_undeclared_var_9(self):
        """Simple program: main"""
        input = """
            Var: b = 10;
            Var: c;
            Var: e;
            Var: f,g;
            Function: foo
            Body:
                **b =  e =/= c;**
                c = !e;
            EndBody.

            Function: main
            Body:
            Var : b = 1.0;
            g = 1.0;
            **f = b +. g + 1.0;**
            f = 10.0 + 10;
            EndBody.

            """
        expect = str(TypeMismatchInExpression(BinaryOp('+',FloatLiteral(10.0),IntLiteral(10))))
        self.assertTrue(TestChecker.test(input, expect, 409))

    def test_undeclared_var_10(self):
        """Simple program: main"""
        input = """
            Var: b = 10;
            Var: c;
            Var: e;
            Var: f,g;
            Function: foo
            Body:

            EndBody.

            Function: main
            Body:
            Var : b = 1.0;
            g = 1.0;
            f = b +. g + 1.0;
            EndBody.

            """
        expect = str(TypeMismatchInExpression(BinaryOp('+',BinaryOp('+.',Id('b'),Id('g')),FloatLiteral(1.0))))
        self.assertTrue(TestChecker.test(input, expect, 410))

    def test_undeclared_var_11(self):
        """Simple program: main"""
        input = """
            Var: b[1] = 1;
            Function: foo

            Body:

            EndBody.

            Function: main
            Parameter: x, y ,z
            Body:
            y = x || (x>z);
            EndBody.

            """
        expect = str(TypeMismatchInExpression(BinaryOp('>',Id('x'),Id('z'))))
        self.assertTrue(TestChecker.test(input, expect, 411))

    def test_undeclared_var_12(self):
        """Simple program: main"""
        input = """

            Function: foo
            Parameter: a,b,c
            Body:
                main();
                foo1();
                foo2();

            EndBody.

            Function: foo1
            Body:
                Return 1;
            EndBody.

            Function: foo2
            Body:

            EndBody.

            Function: main
            Parameter: a, b, c
            Body:
                Return ;
            EndBody.

            """
        expect = str(TypeMismatchInStatement(CallStmt(Id('main'),[])))
        self.assertTrue(TestChecker.test(input, expect, 412))

    def test_undeclared_var_13(self):
        """Simple program: main"""
        input = """

            Function: foo
            Parameter: a,b,c
            Body:
                a = 2;
                main();
                Return;
            EndBody.

            Function: foo1
            Parameter: d
            Body:
                d = 10;
                Return;
            EndBody.

            Function: foo2
            Body:
                Return;
            EndBody.

            Function: main
            Parameter: a, b, c
            Body:
                Return "str";
            EndBody.

            """
        expect = str(TypeMismatchInStatement(CallStmt(Id('main'),[])))
        self.assertTrue(TestChecker.test(input, expect, 413))

    def test_undeclared_var_14(self):
        """Simple program: main"""
        input = """

            Function: foo
            Parameter: a,b,c
            Body:
                a = 2;

                foo1(1,2,"das");
                main(2,3,1.0);
                Return;
            EndBody.

            Function: foo1
            Parameter: d, c, e
            Body:
                d = 10;
                Return;
            EndBody.

            Function: foo2
            Body:
                Return;
            EndBody.

            Function: main
            Parameter: a, b, c
            Body:
                a = 10.1;
                Return ;
            EndBody.

            """
        expect = str(TypeMismatchInStatement(Assign(Id('a'),FloatLiteral(10.1))))
        self.assertTrue(TestChecker.test(input, expect, 414))

    def test_undeclared_var_15(self):
        """Simple program: main"""
        input = """

            Function: foo
            Parameter: a,b,c
            Body:
                a = 2;

                foo1(1,2,"das");
                main(2,3,1.0);
                Return;
            EndBody.

            Function: foo1
            Parameter: d, c, e
            Body:
                d = 10;
                e = 0;
                Return;
            EndBody.

            Function: foo2
            Body:
                Return;
            EndBody.

            Function: main
            Parameter: a, b, c
            Body:
                a = 10.1;
                Return ;
            EndBody.

            """
        expect = str(TypeMismatchInStatement(Assign(Id('e'),IntLiteral(0))))
        self.assertTrue(TestChecker.test(input, expect, 415))

    def test_undeclared_var_16(self):
        """Simple program: main"""
        input = """

            Function: foo
            Parameter: a,b,c
            Body:
                a = 2;

                foo1(1,2,"das");
                main(2,3,1.0);
                Return;
            EndBody.

            Function: foo1
            Parameter: d, c, e
            Body:
                d = 10;
                e = "Khanh";
                Return 1;
            EndBody.

            Function: foo2
            Body:
                Return;
            EndBody.

            Function: main
            Parameter: a, b, c
            Body:
                a = 10;
                Return ;
            EndBody.

            """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(1))))
        self.assertTrue(TestChecker.test(input, expect, 416))

    def test_undeclared_var_17(self):
        """Simple program: main"""
        input = """
            Var: a;

            Function: foo

            Body:
                Return;
            EndBody.

            Function: foo
            Parameter: a,b,c
            Body:

            EndBody.

            Function: main
            Parameter: a, b, c
            Body:
                Return ;
            EndBody.

            """
        expect = str(Redeclared(Function(),'foo'))
        self.assertTrue(TestChecker.test(input, expect, 417))

    def test_undeclared_var_18(self):
        """Simple program: main"""
        input = """
            Var: a;
            Var: a,c;
            Function: foo
            Parameter: a,b,c
            Body:
                Return;
            EndBody.

            Function: foo
            Body:

            EndBody.

            Function: main
            Parameter: a, b, c
            Body:
                Return ;
            EndBody.

            """
        expect = str(Redeclared(Variable(),'a'))
        self.assertTrue(TestChecker.test(input, expect, 418))

    def test_undeclared_var_19(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Parameter: a,b,c
            Body:
                Return;
            EndBody.

            Function: main1
            Parameter: a, b, c
            Body:
                Return ;
            EndBody.

            """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input, expect, 419))

    def test_undeclared_var_20(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Parameter: a,b,c
            Body:
                Return 1;
                main(1,2,3);
            EndBody.

            Function: main
            Parameter: a, b, c
            Body:
                Return 1;
            EndBody.

            """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(1))))
        self.assertTrue(TestChecker.test(input, expect, 420))

    def test_undeclared_var_21(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Parameter: a,b,c
            Body:
                Var: f = 10;
                a = 1;
                b = 2;
                main(1,2,x);
                Return 1;
            EndBody.

            Function: foo1
            Body:
                Return 1;
            EndBody.

            Function: main
            Parameter: a, b, c
            Body:
                foo1();
                Return ;
            EndBody.

            """
        expect = str(Undeclared(Identifier(),'x'))
        self.assertTrue(TestChecker.test(input, expect, 421))

    def test_undeclared_var_22(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Parameter: a,b,c
            Body:
                Var: f = 10;
                Var: x;
                a = 1;
                b = 2;
                main(1,2,x);
                Return 1;
            EndBody.

            Function: foo1
            Body:
                Return 1;
            EndBody.

            Function: main
            Parameter: a, b, c
            Body:
                foo1();
                Return ;
            EndBody.

            """
        expect = str(TypeCannotBeInferred(CallStmt(Id('main'),[IntLiteral(1),IntLiteral(2),Id('x')])))
        self.assertTrue(TestChecker.test(input, expect, 422))

    def test_undeclared_var_23(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Body:
                Var:x ;
                **Var: a = 10;**
                **x = a  + main() + foo1();**
                main(1,2,"string");
                Return 1;
            EndBody.

            Function: main
            Parameter: a,b,c
            Body:
                c = 10;
                **foo1();**
                Return ;
            EndBody.

            """
        expect = str(TypeMismatchInStatement(Assign(Id('c'),IntLiteral(10))))
        self.assertTrue(TestChecker.test(input, expect, 423))

    def test_undeclared_var_24(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Parameter: a,b
            Body:
                a = 10;
                b = 10.0;
                **Var: a = 10;**
                **x = a  + main() + foo1();**
                main(1,2,"string");
                Return 1;
            EndBody.

            Function: main
            Parameter: a,b,c
            Body:

                foo(1,2);
                Return ;
            EndBody.

            """
        expect = str(TypeMismatchInStatement(CallStmt(Id('foo'),[IntLiteral(1),IntLiteral(2)])))
        self.assertTrue(TestChecker.test(input, expect, 424))

    def test_undeclared_var_25(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Parameter: a,b
            Body:
                a = 10;
                b = 10.0;
                **Var: a = 10;**
                **x = a  + main() + foo1();**
                a = 1 + main(1,2,"string") + foo1();
                Return 1;
            EndBody.

            Function: foo1
            Body:
                Return "string";
            EndBody

            Function: main
            Parameter: a,b,c
            Body:

                foo(1,2.0);
                Return 1;
            EndBody.

            """
        expect = str(TypeMismatchInStatement(Return(StringLiteral('string'))))
        self.assertTrue(TestChecker.test(input, expect, 425))

    def test_undeclared_var_26(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Parameter: a,b
            Body:
                a = 10.0;
                b = 10.0;
                **Var: a = 10;**
                **x = a  + main() + foo1();**
                a = 1 + main(1,2,"string") + foo1();
                Return 1;
            EndBody.

            Function: foo1
            Body:
                Return "string";
            EndBody

            Function: main
            Parameter: a,b,c
            Body:

                foo(1,2.0);
                Return 1;
            EndBody.

            """
        expect = str(TypeMismatchInStatement(Assign(Id('a'),BinaryOp('+',BinaryOp('+',IntLiteral(1),CallExpr(Id('main'),[IntLiteral(1),IntLiteral(2),StringLiteral("string")])),CallExpr(Id('foo1'),[])))))
        self.assertTrue(TestChecker.test(input, expect, 426))

    def test_undeclared_var_27(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Parameter: a,b
            Body:
                a = 10.0;
                b = 10.0;
                **Var: a = 10;**
                **x = a  + main() + foo1();**
                Return 1.0;
            EndBody.

            Function: foo1
            Body:
                Var: a = 10;
                a = foo(1.0,2.0);
                Return "string";
            EndBody

            Function: main
            Parameter: a,b,c
            Body:

                Return 1;
            EndBody.

            """
        expect = str(TypeMismatchInStatement(Assign(Id('a'),CallExpr(Id('foo'),[FloatLiteral(1.0),FloatLiteral(2.0)]))))
        self.assertTrue(TestChecker.test(input, expect, 427))

    def test_undeclared_var_28(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Parameter: a,b
            Body:
                a = 10.0;
                b = 10.0;
                Return ;
            EndBody.

            Function: foo1
            Body:
                Var: a ;
                a = foo(1.0,2.0);
                Return "string";
            EndBody.

            Function: main
            Parameter: a,b,c
            Body:

                Return 1;
            EndBody.

            """
        expect = str(TypeMismatchInStatement(Assign(Id('a'),CallExpr(Id('foo'),[FloatLiteral(1.0),FloatLiteral(2.0)]))))
        self.assertTrue(TestChecker.test(input, expect, 428))

    def test_undeclared_var_29(self):
        """Simple program: main"""
        input = """
            Var: c = 10;
            Function: main
            Body:
                If 1 != 2 Then
                    Var: a = 1, b;
                    b = a;
                    main();
                    c = 1;
                Else
                    Var: b = 1;

                EndIf.
                Return 1;
            EndBody.

            """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(1))))
        self.assertTrue(TestChecker.test(input, expect, 429))

    def test_undeclared_var_30(self):
        """Simple program: main"""
        input = """
            Var: c = 10;

            Function: main
            Body:
                If 1 != 2 Then
                    Var: a = 1, b;
                    b = a;
                    int_of_float(1.0);
                    c = 1;
                Else
                    Var: b = 1;

                EndIf.
                Return 1;
            EndBody.

            """
        expect = str(TypeMismatchInStatement(CallStmt(Id('int_of_float'),[FloatLiteral(1.0)])))
        self.assertTrue(TestChecker.test(input, expect, 430))

    def test_undeclared_var_31(self):
        """Simple program: main"""
        input = """
            Var: c = 10;

            Function: main
            Body:
                printLn(1);
                Return 1;
            EndBody.

            """
        expect = str(TypeMismatchInStatement(CallStmt(Id('printLn'),[IntLiteral(1)])))
        self.assertTrue(TestChecker.test(input, expect, 431))

    def test_undeclared_var_32(self):
        """Simple program: main"""
        input = """
            Var: c = 10;

            Function: main
            Body:
                printStr("s","s");
                Return 1;
            EndBody.

            """
        expect = str(TypeMismatchInStatement(CallStmt(Id('printStr'),[StringLiteral('s'),StringLiteral('s')])))
        self.assertTrue(TestChecker.test(input, expect, 432))

    def test_undeclared_var_33(self):
        """Simple program: main"""
        input = """
            Var: c = 10;

            Function: main
            Body:
                printStrLn(1,2);
                Return 1;
            EndBody.

            """
        expect = str(TypeMismatchInStatement(CallStmt(Id('printStrLn'),[IntLiteral(1),IntLiteral(2)])))
        self.assertTrue(TestChecker.test(input, expect, 433))

    def test_undeclared_var_34(self):
        """Simple program: main"""
        input = """
            Var: c = 10;
            Function: main
            Body:
                Var: a;
                c = a + int_of_float(1);
                Return 1;
            EndBody.

            """
        expect = str(TypeMismatchInExpression(CallExpr(Id('int_of_float'),[IntLiteral(1)])))
        self.assertTrue(TestChecker.test(input, expect, 434))

    def test_undeclared_var_35(self):
        """Simple program: main"""
        input = """
            Var: c = 10;
            Function: main
            Body:
                Var: a;
                c = a + float_of_int(1);
                Return 1;
            EndBody.

            """
        expect = str(TypeMismatchInExpression(BinaryOp('+',Id('a'),CallExpr(Id('float_of_int'),[IntLiteral(1)]))))
        self.assertTrue(TestChecker.test(input, expect, 435))

    def test_undeclared_var_36(self):
        """Simple program: main"""
        input = """
            Var: c = 10;
            Function: main
            Body:
                Var: a;
                c = a + int_of_string("string",1);
                Return 1;
            EndBody.

            """
        expect = str(TypeMismatchInExpression(CallExpr(Id('int_of_string'),[StringLiteral('string'),IntLiteral(1)])))
        self.assertTrue(TestChecker.test(input, expect, 436))

    def test_undeclared_var_37(self):
        """Simple program: main"""
        input = """
            Var: c = 10;
            Function: main
            Body:
                Var: a;
                c = a + bool_of_string(1);
                Return 1;
            EndBody.

            """
        expect = str(TypeMismatchInExpression(CallExpr(Id('bool_of_string'),[IntLiteral(1)])))
        self.assertTrue(TestChecker.test(input, expect, 437))

    def test_undeclared_var_38(self):
        """Simple program: main"""
        input = """
            Var: c = 10;
            Function: main
            Body:
                Var: a;
                c = a + foo1(1);
                Return 1;
            EndBody.

            """
        expect = str(Undeclared(Function(), 'foo1'))
        self.assertTrue(TestChecker.test(input, expect, 438))

    def test_undeclared_var_39(self):
        """Simple program: main"""
        input = """
            Var: c = 10;
            Function: main
            Parameter: b,a,b
            Body:
                Var: a;
                c = a + foo1(1);
                Return 1;
            EndBody.

            """
        expect = str(Redeclared(Parameter(), 'b'))
        self.assertTrue(TestChecker.test(input, expect, 439))

    def test_undeclared_var_40(self):
        """Simple program: main"""
        input = """
            Var: c = 10;
            Function: main
            Parameter: a, a
            Body:
                Var: a;
                c = a + foo1(1);
                Return 1;
            EndBody.

            """
        expect = str(Redeclared(Parameter(), 'a'))
        self.assertTrue(TestChecker.test(input, expect, 440))

    def test_undeclared_var_41(self):
        """Simple program: main"""
        input = """
            Var: x;
            Function: foo
            Parameter: y
            Body:
                Return 1;
            EndBody.

            Function: main
            Body:
                Var:  a = 10;
                a = 1 + foo(x);
                **foo(x);**
                x = 0.0;
                Return 1;
            EndBody.

            """
        expect = str(TypeCannotBeInferred(Assign(Id('a'),BinaryOp('+',IntLiteral(1),CallExpr(Id('foo'),[Id('x')])))))
        self.assertTrue(TestChecker.test(input, expect, 441))

    def test_undeclared_var_42(self):
        """Simple program: main"""
        input = """
            Var: x;
            Function: foo
            Parameter: y
            Body:
                Return 1;
            EndBody.

            Function: main
            Body:
                Var:  a = 10;
                a = 1 + foo(1);
                a = 1 + foo(x);
                **foo(x);**
                x = 0.0;
                Return 1;
            EndBody.

            """
        expect = str(TypeMismatchInStatement(Assign(Id('x'),FloatLiteral(0.0))))
        self.assertTrue(TestChecker.test(input, expect, 442))

    def test_undeclared_var_43(self):
        """Simple program: main"""
        input = """
        Function: main
        Parameter: y
        Body:
        Var: a,b=3;
        a = -foo(y) + b;
        EndBody.
        Function: foo
        Parameter: x
        Body:
            x = 1;
            Return 1;
        EndBody.

            """
        expect = str(TypeCannotBeInferred(Assign(Id('a'),BinaryOp('+',UnaryOp('-',CallExpr(Id('foo'),[Id('y')])),Id('b')))))
        self.assertTrue(TestChecker.test(input, expect, 443))
    
    def test_infer_14(self):
        input = r"""
        Function: main
            Body:
            If 5 == 2 Then Var:a;
            ElseIf 1 Then Var:b;
            EndIf.
            EndBody.
        """
        expect = """Type Mismatch In Statement: If(BinaryOp(==,IntLiteral(5),IntLiteral(2)),[VarDecl(Id(a))],[])ElseIf(IntLiteral(1),[VarDecl(Id(b))],[])Else([],[])"""
        self.assertTrue(TestChecker.test(input, expect, 444))
    
    def test_infer_15(self):
        input = r"""
        Function: main
            Body:
            If 5 == 2 Then Var:a;
            ElseIf 3 Then Var:b;
            EndIf.
            EndBody.
        """
        expect = """Type Mismatch In Statement: If(BinaryOp(==,IntLiteral(5),IntLiteral(2)),[VarDecl(Id(a))],[])ElseIf(IntLiteral(3),[VarDecl(Id(b))],[])Else([],[])"""
        self.assertTrue(TestChecker.test(input, expect, 445))
        
    def test_infer_16(self):
        input = r"""
        Function: main
            Body:
            Var:a;
            If 5 == 2 Then Var:a;
            ElseIf 1==2 Then
                Var:b;
                If a Then
                a = 10;
                EndIf.
            EndIf.
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id('a'),IntLiteral(10))))
        self.assertTrue(TestChecker.test(input, expect, 446))
    
    def test_infer_17(self):
        input = r"""
        Function: main
            Body:
            If 5 Then
            EndIf.
            EndBody.
        """
        expect = "Type Mismatch In Statement: If(IntLiteral(5),[],[])Else([],[])"
        self.assertTrue(TestChecker.test(input, expect, 447))

    def test_infer_18(self):
        input = r"""
        Function: main
            Body:
            If False Then 
            ElseIf 5 Then
            EndIf.
            EndBody.
        """
        expect = "Type Mismatch In Statement: If(BooleanLiteral(false),[],[])ElseIf(IntLiteral(5),[],[])Else([],[])"
        self.assertTrue(TestChecker.test(input, expect, 448))

    def test_infer_19(self):
        input = r"""
        Function: main
            Body:
            Var: a;
            If a Then
            a = 5;
            EndIf.
            Return 1;
            EndBody.
        """
        expect = "Type Mismatch In Statement: Assign(Id(a),IntLiteral(5))"
        self.assertTrue(TestChecker.test(input, expect, 449))
    
    def test_infer_20(self):
        input = r"""
        Var: x;
        Function: foo
        Body:
            Return False;
        EndBody.
        Function: main
            Body:
            Var: a;
            If foo() Then
            a = True;
            a = foo();
            a = 10;
            EndIf.
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id('a'),IntLiteral(10))))
        self.assertTrue(TestChecker.test(input, expect, 450))
    
    def test_array_lit_0(self):
        input = r"""
        Var: b[2] = {1,2};
        Function: foo
            Body:
                Return;
            EndBody.
        Function: main
            Parameter: x, y
            Body:
                Var: a;
                a[1] = {1};
                Return 3 ;
            EndBody.
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 451))

    def test_array_lit_1(self):
        input = r"""
        Var: x[2][3] = {{1,2,3},{4,5,6}};
        Function: main
            Body:
            Var: a;
            a = x[1][2];
            a = a +. 1.5;
            EndBody.
        """
        expect = "Type Mismatch In Expression: BinaryOp(+.,Id(a),FloatLiteral(1.5))"
        self.assertTrue(TestChecker.test(input, expect, 452))

    def test_array_lit_2(self):
        input = r"""
        Var: x[3];
        Function: main
            Body:
            Var: a;
            x[1] = 5;
            a = x[1];
            EndBody.
        """
        expect = str(TypeMismatchInExpression(ArrayCell(Id('x'),[IntLiteral(1)])))
        self.assertTrue(TestChecker.test(input, expect, 453))
    
    def test_array_lit_4(self):
        input = r"""
        Var: x[3] = {1,2,3};
        Function: main
            Body:
            Var: a;
            EndBody.
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 454))
        
    def test_array_lit_5(self):
        input = r"""
        Var: x[3] = {1,2,3};
        Function: main
            Body:
            main()[1] = 5;
            EndBody.
        """
        expect = str(TypeMismatchInExpression(ArrayCell(CallExpr(Id('main'),[]),[IntLiteral(1)])))
        self.assertTrue(TestChecker.test(input, expect, 455))
    
    def test_func_56(self):
        input = r"""
        Function: foo
            Body:
                Var: x = 3.1, y = 5.2;
                y = -. main(x, 2);
            EndBody.
        Function: main
            Parameter: x, y
            Body:
                Var: a = 3;
                Return 3 + a;
            EndBody.
        """
        expect = "Type Mismatch In Statement: Return(BinaryOp(+,IntLiteral(3),Id(a)))"
        self.assertTrue(TestChecker.test(input, expect, 456))
    
    def test_redecl_var_57(self):
        input = r""" Var: a;
                    Var: a = 5;"""
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect, 457))

    def test_redecl_func_58(self):
        input = r"""
        Function: main
            Body:
            EndBody.
        Function: main
            Body:
            EndBody.
        """
        expect = "Redeclared Function: main"
        self.assertTrue(TestChecker.test(input,expect, 458))

    def test_no_entry_59(self):
        input = r"""
        Var: x;
        Function: foo
        Parameter: x
        Body:
            Var: y;
        EndBody.
        """
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 459))

    def test_redecl_param_60(self):
        input = r"""
        Function: main
        Parameter: x, x
        Body:
            Var: y;
        EndBody.
        """
        expect = "Redeclared Parameter: x"
        self.assertTrue(TestChecker.test(input, expect, 460))

    def test_mismatch_stmt_61(self):
        input = r"""
        Function: main
        Body:
            Var: a, b;
            a = 1 + 2;
            b = a + 3.5;
        EndBody.
        """
        expect = "Type Mismatch In Expression: BinaryOp(+,Id(a),FloatLiteral(3.5))"
        self.assertTrue(TestChecker.test(input, expect, 461))

    def test_mismatch_stmt_62(self):
        input = r"""
        Function: main
        Body:
            Var: a = 5;
            a = 6.5;
        EndBody.
        """
        expect = "Type Mismatch In Statement: Assign(Id(a),FloatLiteral(6.5))"
        self.assertTrue(TestChecker.test(input, expect, 462))

    def test_mismatch_expr_63(self):
        input = r"""
        Function: main
        Body:
            Var: a = 5;
            a = 6 + 5.5;
        EndBody.
        """
        expect = "Type Mismatch In Expression: BinaryOp(+,IntLiteral(6),FloatLiteral(5.5))"
        self.assertTrue(TestChecker.test(input, expect, 463))

    def test_undecl_var_64(self):
        input = r"""
        Var: b;
        Function: main
            Body:
                Var: a;
                b = a + b;
            EndBody.
        Function: another1
            Body:
                b = 1.5;
            EndBody.
        """
        expect = "Type Mismatch In Statement: Assign(Id(b),FloatLiteral(1.5))"
        self.assertTrue(TestChecker.test(input, expect, 464))    
    
    def test_func_65(self):
        """ Restype and return type are different"""
        input = r"""
        Function: foo
            Body:
                Var: x = 3;
                x = main(1);
            EndBody.
        Function: main
            Parameter: x
            Body:
                Return 1.2;
            EndBody.
        """
        expect = "Type Mismatch In Statement: Return(FloatLiteral(1.2))"
        self.assertTrue(TestChecker.test(input, expect, 465))

    def test_func_66(self):
        input = r"""
        Function: foo
            Body:
                Var: x = 3.1;
                main(x, 2);
            EndBody.
        Function: main
            Parameter: x, y
            Body:
                Var: a = 3;
                a = x;
            EndBody.
        """
        expect = "Type Mismatch In Statement: Assign(Id(a),Id(x))"
        self.assertTrue(TestChecker.test(input, expect, 466))

    def test_func_67(self):
        input = r"""
        Function: foo
            Body:
                Var: x = 3.1, y = 5.2;
                y = x +. main(x, 2);
            EndBody.
        Function: main
            Parameter: x, y
            Body:
                Var: a = 3;
                Return 3 + a;
            EndBody.
        """
        expect = "Type Mismatch In Statement: Return(BinaryOp(+,IntLiteral(3),Id(a)))"
        self.assertTrue(TestChecker.test(input, expect, 467))  

    

    def test_func_68(self):
        input = r"""
            Function : print
            Parameter : x
            Body:
                Return;
            EndBody.
            Function: m
            Body:
                Var : value = 12345;
                Return value;
            EndBody.
            Function: main
            Parameter : x, y
            Body: 
                print(m1); 
                Return 0;
            EndBody.
            """
        expect = "Undeclared Identifier: m1"
        self.assertTrue(TestChecker.test(input, expect, 468))
    
    def test_func_69(self):
        input = r"""
        Function: main
        Parameter: a,b,c
        Body:
            Var: d, e;
            e = main(b, main(d, c, a), a + d); 
            e = 3.0; 
            Return 3;
        EndBody.
        """
        expect = "Type Cannot Be Inferred: Assign(Id(e),CallExpr(Id(main),[Id(b),CallExpr(Id(main),[Id(d),Id(c),Id(a)]),BinaryOp(+,Id(a),Id(d))]))"
        self.assertTrue(TestChecker.test(input, expect, 469))

    def test_func_70(self):
        input = r"""
            Function: main
            Parameter: x, y ,z
            Body:
            y = x || (x>z);
            EndBody.
            """
        expect ="Type Mismatch In Expression: BinaryOp(>,Id(x),Id(z))"
        self.assertTrue(TestChecker.test(input, expect, 470))

    def test_func_71(self):
        input = r"""
            Function: main
            Body:
                Var: i;
                For (i = 0, i < 10, 2) Do
                    Var: x;
                    x = 10;
                EndFor.
            EndBody.
            """
        expect = ''
        self.assertTrue(TestChecker.test(input, expect, 471))

    def test_func_72(self):
        input = r"""
            Function: main
            Body:
                For (i = 0, i < 10, 2) Do
                    Var: x;
                    x = 10;
                EndFor.
            EndBody.
            """
        expect = str(Undeclared(Identifier(), 'i'))
        self.assertTrue(TestChecker.test(input, expect, 472))
    
    def test_func_73(self):
        input = r"""
            Var: x = 10;
            Function: main
            Body:
                Var: i;
                For (i = 0, i < 10, 2) Do
                    If x > 10 Then
                        i = 202.2;
                        x = 1.0;
                    EndIf.
                EndFor.
            EndBody.
            """
        expect = str(TypeMismatchInStatement(Assign(Id('i'),FloatLiteral(202.2))))
        self.assertTrue(TestChecker.test(input, expect, 473))
    
    def test_func_74(self):
        input = r"""
            Var: x = 10;
            Function: main
            Body:
                Var: i;
                Var:  c = 20.0;
                For (i = 0, i < 10, 2) Do
                    If x > 10 Then
                        Var: c ;
                        c = 10;
                        i = 202;
                        If c == 1 Then
                        x = 1;
                        EndIf.
                    EndIf.
                EndFor.
            EndBody.
            """
        expect = ''
        self.assertTrue(TestChecker.test(input, expect, 474))
    
    def test_func_75(self):
        input = r"""
            Var: x = 10;
            Function: main
            Body:
                Var: a;
                If True Then a = 10;
                ElseIf False Then a = 10.0;
                EndIf.
            Return;
            EndBody.
            """
        expect = str(TypeMismatchInStatement(Assign(Id('a'),FloatLiteral(10.0))))
        self.assertTrue(TestChecker.test(input, expect, 475))
    
    def test_func_76(self):
        input = r"""
            Var: x = 10;
            Function: main
            Body:
                Var: a,b;
                While a >. b + 1 Do
                    main();
                EndWhile.
                Return;
            EndBody.
            """
        expect = str(TypeMismatchInExpression(BinaryOp('>.',Id('a'),BinaryOp('+',Id('b'),IntLiteral(1)))))
        self.assertTrue(TestChecker.test(input, expect, 476))
    
    def test_func_77(self):
        input = r"""
            Var: x = 10;
            Function: main
            Body:
                Var: a,b;
                While a >. b Do
                    main();
                EndWhile.
                Return;
            EndBody.
            """
        expect = ''
        self.assertTrue(TestChecker.test(input, expect, 477))
    
    def test_func_78(self):
        input = r"""
            Var: x = 10;
            Function: main
            Body:
                Var: a,b;
                Do main();
                While a > b EndDo.
                Return;
            EndBody.
            """
        expect = ''
        self.assertTrue(TestChecker.test(input, expect, 478))
    
    def test_func_79(self):
        input = r"""
            Var: x = 10;
            Function: main
            Body:
                Var: a = 10.0,b;
                Do main();
                While a > b EndDo.
                Return;
            EndBody.
            """
        expect = str(TypeMismatchInExpression(BinaryOp('>',Id('a'),Id('b'))))
        self.assertTrue(TestChecker.test(input, expect, 479))
    
    def test_func_80(self):
        input = r"""
            Var: x = 10;
            Function: main
            Body:
                Var: a = 10, b;
                Do main();
                While a > b + x EndDo.
                Return;
            EndBody.
            """
        expect = ''
        self.assertTrue(TestChecker.test(input, expect, 480))
    
    def test_func_81(self):
        input = r"""
            Var: x = 10;
            Function: i
            Body:
            EndBody.
            Function: main
            Body:
                Var:  c = 20.0;
                For (i = 0, i < 10, 2) Do
                    If x > 10 Then
                        Var: c ;
                        c = 10;
                        i = 202;
                        If c == 1 Then
                        x = 1;
                        EndIf.
                    EndIf.
                EndFor.
            EndBody.
            """
        expect = str(Undeclared(Identifier(), 'i'))
        self.assertTrue(TestChecker.test(input, expect, 481))


    def test_type_cannot_be_inferred82(self):
        input = """
        Function: main
        Body:
            Var: x;
            If True Then
                Var: x = 3;
            ElseIf False Then
                Var: y, z = 3;

            Else
                y = 10;
            EndIf.
            Return;
        EndBody.
                   """
        expect = str(Undeclared(Identifier(),'y'))
        self.assertTrue(TestChecker.test(input,expect,482))
    
    def test_type_cannot_be_inferred83(self):
        input = """
        Function: main
        Body:
            Var: x;
            If True Then
                Var: x = 3;
            ElseIf False Then
                Var: y, z = 3;
                y = x;
            Else
            EndIf.
            Return;
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(Assign(Id('y'),Id('x'))))
        self.assertTrue(TestChecker.test(input,expect,483))
    
    def test_func_84(self):
        input = r"""
            Var: x = 10;
            Function: main
            Body:
                Var: a = 10, b;
                Do main();
                While a > b + x EndDo.
                Return;
            EndBody.
            """
        expect = ''
        self.assertTrue(TestChecker.test(input, expect, 484))
    
    def test_func_85(self):
        input = r"""
            Var: x = 10;
            Function: i
            Body:
            EndBody.
            Function: main
            Body:
                Var:  c = 20.0;
                For (i = 0, i < 10, 2) Do
                    If x > 10 Then
                        Var: c ;
                        c = 10;
                        i = 202;
                        If c == 1 Then
                        x = 1;
                        EndIf.
                    EndIf.
                EndFor.
            EndBody.
            """
        expect = str(Undeclared(Identifier(), 'i'))
        self.assertTrue(TestChecker.test(input, expect, 485))


    def test_type_cannot_be_inferred86(self):
        input = """
        Function: main
        Body:
            Var: x;
            If True Then
                Var: x = 3;
            ElseIf False Then
                Var: y, z = 3;

            Else
                y = 10;
            EndIf.
            Return;
        EndBody.
                   """
        expect = str(Undeclared(Identifier(),'y'))
        self.assertTrue(TestChecker.test(input,expect,486))
    
    def test_type_cannot_be_inferred87(self):
        input = """
        Function: main
        Body:
            Var: x;
            If True Then
                Var: x = 3;
            ElseIf False Then
                Var: y, z = 3;
                y = x;
            Else
            EndIf.
            Return;
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(Assign(Id('y'),Id('x'))))
        self.assertTrue(TestChecker.test(input,expect,487))
    
    def test_type_cannot_be_inferred88(self):
        input = """
        Function: main
        Body:
            Var: x;
            If True Then
                Var: x = 3;
            ElseIf False Then
                Var: y, z = 3;
            Else
                main(x);
            EndIf.
            Return;
        EndBody.
                   """
        expect = str(TypeMismatchInStatement(CallStmt(Id('main'),[Id('x')])))
        self.assertTrue(TestChecker.test(input,expect,488))
    
    def test_type_cannot_be_inferred89(self):
        input = """
        Function: main
        Body:
            Var: x;
            If True Then
                Var: x = 3;
            ElseIf False Then
                Var: y, z = 3;
            Else
                main(x);
            EndIf.
            Return;
        EndBody.
                   """
        expect = str(TypeMismatchInStatement(CallStmt(Id('main'),[Id('x')])))
        self.assertTrue(TestChecker.test(input,expect,489))
        
    def test_type_cannot_be_inferred90(self):
        input = """
        Function: main
        Body:
            Var: xy;
            If True Then
                Var: x = 3;
            ElseIf False Then
                Var: y, z = 3;
            Else
                main(xy);
            EndIf.
            Return;
        EndBody.
                   """
        expect = str(TypeMismatchInStatement(CallStmt(Id('main'),[Id('xy')])))
        self.assertTrue(TestChecker.test(input,expect,490))
        
    def test_infer_91(self):
        input = r"""
        Var: x;
        Function: foo
        Body:
            Return False;
        EndBody.
        Function: main
            Body:
            Var: a;
            If foo() Then
            a = True;
            a = foo();
            a = 10;
            EndIf.
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id('a'),IntLiteral(10))))
        self.assertTrue(TestChecker.test(input, expect, 491))
    
    def test_array_lit_92(self):
        input = r"""
        Var: b[2] = {1,2};
        Function: foo
            Body:
                Return;
            EndBody.
        Function: main
            Parameter: x, y
            Body:
                Var: a;
                a[1] = {1};
                Return 3 ;
            EndBody.
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 492))

    def test_array_lit_93(self):
        input = r"""
        Var: x[2][3] = {{1,2,3},{4,5,6}};
        Function: main
            Body:
            Var: a;
            a = x[1][2];
            a = a +. 1.5;
            EndBody.
        """
        expect = "Type Mismatch In Expression: BinaryOp(+.,Id(a),FloatLiteral(1.5))"
        self.assertTrue(TestChecker.test(input, expect, 493))

    def test_array_lit_94(self):
        input = r"""
        Var: x[3];
        Function: main
            Body:
            Var: a;
            x[1] = 5;
            a = x[1];
            EndBody.
        """
        expect = str(TypeMismatchInExpression(ArrayCell(Id('x'),[IntLiteral(1)])))
        self.assertTrue(TestChecker.test(input, expect, 494))
    
    def test_array_lit_94(self):
        input = r"""
        Var: x[3] = {1,2,3};
        Function: main
            Body:
            Var: a;
            EndBody.
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 495))
        
    def test_array_lit_96(self):
        input = r"""
        Var: x[3] = {1,2,3};
        Function: main
            Body:
            main()[1] = 5;
            EndBody.
        """
        expect = str(TypeMismatchInExpression(ArrayCell(CallExpr(Id('main'),[]),[IntLiteral(1)])))
        self.assertTrue(TestChecker.test(input, expect, 496))
    
    def test_func_97(self):
        input = r"""
        Function: foo
            Body:
                Var: x = 3.1, y = 5.2;
                y = -. main(x, 2);
            EndBody.
        Function: main
            Parameter: x, y
            Body:
                Var: a = 3;
                Return 3 + a;
            EndBody.
        """
        expect = "Type Mismatch In Statement: Return(BinaryOp(+,IntLiteral(3),Id(a)))"
        self.assertTrue(TestChecker.test(input, expect, 497))
    
    def test_redecl_var_98(self):
        input = r""" Var: a;
                    Var: a = 5;"""
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect, 498))

    def test_redecl_func_99(self):
        input = r"""
        Function: main
            Body:
            EndBody.
        Function: main
            Body:
            EndBody.
        """
        expect = "Redeclared Function: main"
        self.assertTrue(TestChecker.test(input,expect, 499))

    def test_no_entry_100(self):
        input = r"""
        Var: x;
        Function: foo
        Parameter: x
        Body:
            Var: y;
        EndBody.
        """
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 500))
