/**
 * StudentID 1810998 - Nguyen Huynh Huu Khiem
 */
grammar BKIT;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    result = super().emit()
    if tk == self.UNCLOSE_STRING:       
        raise UncloseString(result.text)
    elif tk == self.ILLEGAL_ESCAPE:
        raise IllegalEscape(result.text)
    elif tk == self.ERROR_CHAR:
        raise ErrorToken(result.text)
    elif tk == self.UNTERMINATED_COMMENT:
        raise UnterminatedComment()
    else:
        return result;
}

options {
	language = Python3;
}

/**
 * 2 Program Structure
 */
program: (var_declare* func_declare*) EOF;

// 2.1 Variable declaration var_declare_part: var_declare+;

var_declare: VAR COLON variable_list SEMI;

variable_list: variable (COMMA variable)*; // var1,var2 = b,var3

variable: ID dimension? (ASSIGN literal)?;

dimension: (LSB INTEGER_LITERAL RSB)+;

literal:
	boolean_literal
	| INTEGER_LITERAL
	| STRING_LITERAL
	| FLOAT_LITERAL
	| array_literal;

boolean_literal: TRUE | FALSE;
//2.2 Function declaration func_declare_part: func_declare*;

func_declare:
	FUNCTION COLON ID (PARAMETER COLON parameters_list)? BODY COLON stm_list ENDBODY DOT;

parameters_list: parameter (COMMA parameter)*;
parameter: ID dimension?;

/**
 * 7 Statements
 */

stm_list: var_declare* stm*;

stm:
	stm_assign
	| stm_if
	| stm_for
	| stm_while
	| stm_dowhile
	| stm_break
	| stm_continue
	| stm_call
	| stm_return;

stm_assign: variable_ ASSIGN exp SEMI;

variable_: (ID | index_exp);

stm_if:
	IF exp THEN stm_list (ELSEIF exp THEN stm_list)* (
		ELSE stm_list
	)? ENDIF DOT;
// stm_list = (var_declare* stm*)
stm_for:
	FOR LP ID ASSIGN exp COMMA exp COMMA exp RP DO stm_list ENDFOR DOT;
stm_while: WHILE exp DO stm_list ENDWHILE DOT;
stm_dowhile: DO stm_list WHILE exp ENDDO DOT;
stm_break: BREAK SEMI;
stm_continue: CONTINUE SEMI;
stm_call: ID LP (exp (COMMA exp)*)? RP SEMI;
stm_return: RETURN (exp)? SEMI;

/**
 * 6 Expression
 */

exp_bool: exp;

exp_int: exp;

exp_real: exp;

exp_str: exp;

exp:
	exp1 (
		EQ
		| LTE
		| GTE
		| NEQ
		| LT
		| GT
		| LTEF
		| GTEF
		| NEQF
		| LTF
		| GTF
	) exp1
	| exp1;

exp1: exp1 ( AND | OR) exp2 | exp2;

exp2: exp2 ( ADD | ADDF | SUB | SUBF) exp3 | exp3;

exp3: exp3 ( MUL | MULF | DIV | DIVF | MOD) exp4 | exp4;

exp4: (NOT | SUB) exp4 | exp5;

exp5: NOT exp5 | exp6;

exp6: (SUB | SUBF) exp6 | exp7;

exp7: index_exp | exp8;

exp8: call_exp | exp9;

exp9: literal | ID | LP exp RP; //() uu tien cao nhat

// operands: literal | ID | call_exp | LP exp RP | index_exp;

// primary_exp: literal | ID;

//index_exp: (ID | call_exp) index_operator;

index_exp: exp_forindex index_operator;

exp_forindex: ID | call_exp;

call_exp: ID LP (exp (COMMA exp)*)? RP;

index_operator: (LSB exp RSB)+;
// | LSB exp_int RSB index_operator;

/** Lexers Declaration */

/**
 * Keywords
 */

// Methods
FUNCTION: 'Function';

// Parameter
PARAMETER: 'Parameter';

// Scope
BODY: 'Body';
ENDBODY: 'EndBody';

// Value
TRUE: 'True';
FALSE: 'False';

// Flow Statement
IF: 'If';
THEN: 'Then';
ELSEIF: 'ElseIf';
ELSE: 'Else';
ENDIF: 'EndIf';

// Loop Statement
FOR: 'For';
ENDFOR: 'EndFor';
WHILE: 'While';
ENDWHILE: 'EndWhile';
DO: 'Do';
ENDDO: 'EndDo';

// Stop Statement
RETURN: 'Return';
BREAK: 'Break';
CONTINUE: 'Continue';

// Others Types
VAR: 'Var';

/**
 * Operators
 */
ASSIGN: '=';

ADD: '+';
SUB: '-';
MUL: '*';
DIV: '\\';
MOD: '%';

ADDF: '+.';
SUBF: '-.';
MULF: '*.';
DIVF: '\\.';

EQ: '==';
LTE: '<=';
GTE: '>=';
NEQ: '!=';
LT: '<';
GT: '>';

LTEF: '<=.';
GTEF: '>=.';
NEQF: '=/=';
LTF: '<.';
GTF: '>.';

NOT: '!';
AND: '&&';
OR: '||';

// Domain Values
BOOLEAN_LITERAL: TRUE | FALSE;

STRING_LITERAL:
	'"' STR_CHAR* '"' {
		y = str(self.text)
		self.text = y[1:-1]
	};

fragment STR_CHAR: ESC_SEQ | ~[\n'"\\] | '\'' '"';

fragment ESC_SEQ:
	'\\b'
	| '\\f'
	| '\\r'
	| '\\n'
	| '\\t'
	| '\\\''
	| '\\\\';
fragment ESC_ILLEGAL: ('\\' ~[btnfr'\\]) | '\'' ~'"';
FLOAT_LITERAL:
	DIGIT+ DOT (DIGIT)* EXPONENT? //1.5 2.0 3. 3.e+3 4.E-2
	| (DIGIT)+ EXPONENT; //	| ([1-9][0-9]*)* EXPONENT // e3

INTEGER_LITERAL:
	'0'
	| [1-9][0-9]*
	| '0' [Xx] [1-9A-F][0-9A-F]*
	| '0' [Oo] [1-7][0-7]*;

array_literal: LCB (literal (COMMA literal)*)? RCB;

//element: (literal (COMMA literal)*);

literal_:
	BOOLEAN_LITERAL
	| INTEGER_LITERAL
	| STRING_LITERAL
	| FLOAT_LITERAL
	| array_literal;

fragment EXPONENT: [eE] SIGN? DIGIT+;

fragment DIGIT: [0-9];

fragment SIGN: [+-];

LITERAL:
	BOOLEAN_LITERAL
	| INTEGER_LITERAL
	| STRING_LITERAL
	| FLOAT_LITERAL;

// Identifier

ID: [a-z][a-zA-Z_0-9]*;

/**
 * Specific characters Please search name for characters here https://www.compart.com
 */

LP: '('; // Left Parenthesis
RP: ')'; // Right Parenthesis 
LCB: '{'; // Left Curly Bracket
RCB: '}'; // Right Curly Bracket
LSB: '['; // Left Square Bracket
RSB: ']'; // Right Square Bracket

SEMI: ';'; // Semicolon
COMMA: ','; // Comma
COLON: ':'; // Colon
//DOTDOT: '..'; // Dot Dot should be before Dot
DOT: '.';

// Skip comments
BLOCK_COMMENT: ('**' .*? '**') -> skip;

// Skip spaces, tabs, newlines
WS: [ \t\r\n\f]+ -> skip; // skip spaces, tabs, newlines

ERROR_CHAR:
	. { 
		raise ErrorToken(self.text)
	};
UNCLOSE_STRING:
	'"' STR_CHAR* EOF {
		y = str(self.text)
		raise UncloseString(y[1:])
	};
ILLEGAL_ESCAPE:
	'"' STR_CHAR* ESC_ILLEGAL {
		y = str(self.text)
		raise IllegalEscape(y[1:])
	};
UNTERMINATED_COMMENT:
	'**' .*? {
		raise UnterminatedComment()
	};