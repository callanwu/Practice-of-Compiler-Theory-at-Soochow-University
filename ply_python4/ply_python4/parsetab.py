
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "CLASS DEF NUMBER PRINT SELF STR VARIABLEprogram : statementsstatements : statements statement\n                  | statement statement : assignment\n                  | operation\n                  | print\n                  | function\n                  | run_function\n                  | classassignment : VARIABLE '=' NUMBER\n                  | VARIABLE '[' expression ']' '=' NUMBER\n                  | VARIABLE '=' VARIABLE\n                  | VARIABLE '=' VARIABLE '[' expression ']'\n                  | self '=' VARIABLE\n                  | VARIABLE '=' VARIABLE '(' expressions ')' self : SELF '.' VARIABLEoperation : VARIABLE '=' expression\n                 | VARIABLE '+' '=' expression\n                 | VARIABLE '-' '=' expression\n                 | VARIABLE '[' expression ']' '=' expression\n                 | self '=' expressionexpression : expression '+' term\n                  | expression '-' term\n                  | termterm : term '*' factor\n            | term '/' factor\n            | factorfactor : NUMBER\n              | VARIABLE\n              | STR\n              | self\n              | VARIABLE '[' expression ']'\n              | '(' expression ')' print : PRINT '(' variables ')' function : DEF VARIABLE '(' variables ')' '{' statements '}'\n                | DEF VARIABLE '(' SELF ')' '{' statements '}'\n                | DEF VARIABLE '(' SELF ',' variables ')' '{' statements '}' run_function : VARIABLE '(' expressions ')'\n                    | VARIABLE '.' VARIABLE '(' expressions ')' variables :\n                 | VARIABLE\n                 | variables ',' VARIABLE\n                 | self\n                 | variables ',' selfexpressions :\n                   | expression\n                   | expressions ',' expressionclass : CLASS VARIABLE '{' statements '}' "
    
_lr_action_items = {'*':([32,33,34,36,37,38,41,42,47,51,76,77,78,80,81,91,93,95,],[56,-31,-28,-30,-27,-29,-28,-29,-29,-16,-25,-26,-33,56,56,-32,-32,-28,]),']':([32,33,34,36,37,47,50,51,76,77,78,79,80,81,84,91,],[-24,-31,-28,-30,-27,-29,70,-16,-25,-26,-33,91,-23,-22,93,-32,]),')':([17,25,28,29,30,31,32,33,34,36,37,47,48,49,51,54,55,58,63,67,71,72,75,76,77,78,80,81,83,85,86,90,91,],[-40,-45,52,-41,-43,-40,-24,-31,-28,-30,-27,-29,68,-46,-16,73,74,78,-45,-45,-44,-42,-40,-25,-26,-33,-23,-22,92,94,-47,99,-32,]),'(':([3,13,18,19,21,25,26,35,42,44,45,46,56,57,59,60,61,63,64,67,69,87,],[17,25,31,35,35,35,35,35,63,35,35,67,35,35,35,35,35,35,35,35,35,35,]),'SELF':([0,1,2,4,8,9,11,12,14,16,17,19,21,25,26,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,47,51,52,53,56,57,59,60,61,62,63,64,65,66,67,68,69,75,76,77,78,80,81,82,87,88,89,91,92,93,94,95,96,97,98,100,101,102,103,104,],[15,15,-8,-5,-3,-6,-7,-4,-9,-2,15,15,15,15,15,55,-24,-31,-28,15,-30,-27,-14,-21,15,-10,-12,-17,15,15,-29,-16,-34,15,15,15,15,15,15,15,15,15,-18,-19,15,-38,15,15,-25,-26,-33,-23,-22,-48,15,15,15,-32,-15,-13,-39,-11,-20,15,15,-35,-36,15,15,-37,]),'=':([6,13,22,23,51,70,],[19,21,44,45,-16,87,]),'-':([13,32,33,34,36,37,38,39,41,42,43,47,49,50,51,58,65,66,76,77,78,79,80,81,84,86,91,93,95,96,],[23,-24,-31,-28,-30,-27,-29,60,-28,-29,60,-29,60,60,-16,60,60,60,-25,-26,-33,60,-23,-22,60,60,-32,-32,-28,60,]),',':([17,25,28,29,30,31,32,33,34,36,37,47,48,49,51,54,55,63,67,71,72,75,76,77,78,80,81,83,85,86,90,91,],[-40,-45,53,-41,-43,-40,-24,-31,-28,-30,-27,-29,69,-46,-16,53,75,-45,-45,-44,-42,-40,-25,-26,-33,-23,-22,69,69,-47,53,-32,]),'/':([32,33,34,36,37,38,41,42,47,51,76,77,78,80,81,91,93,95,],[57,-31,-28,-30,-27,-29,-28,-29,-29,-16,-25,-26,-33,57,57,-32,-32,-28,]),'.':([13,15,55,],[24,27,27,]),'PRINT':([0,1,2,4,8,9,11,12,14,16,32,33,34,36,37,38,39,40,41,42,43,47,51,52,62,65,66,68,76,77,78,80,81,82,88,89,91,92,93,94,95,96,97,98,100,101,102,103,104,],[3,3,-8,-5,-3,-6,-7,-4,-9,-2,-24,-31,-28,-30,-27,-14,-21,3,-10,-12,-17,-29,-16,-34,3,-18,-19,-38,-25,-26,-33,-23,-22,-48,3,3,-32,-15,-13,-39,-11,-20,3,3,-35,-36,3,3,-37,]),'NUMBER':([19,21,25,26,35,44,45,56,57,59,60,61,63,64,67,69,87,],[34,41,34,34,34,34,34,34,34,34,34,34,34,34,34,34,95,]),'STR':([19,21,25,26,35,44,45,56,57,59,60,61,63,64,67,69,87,],[36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,]),'+':([13,32,33,34,36,37,38,39,41,42,43,47,49,50,51,58,65,66,76,77,78,79,80,81,84,86,91,93,95,96,],[22,-24,-31,-28,-30,-27,-29,61,-28,-29,61,-29,61,61,-16,61,61,61,-25,-26,-33,61,-23,-22,61,61,-32,-32,-28,61,]),'VARIABLE':([0,1,2,4,5,8,9,10,11,12,14,16,17,19,21,24,25,26,27,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,47,51,52,53,56,57,59,60,61,62,63,64,65,66,67,68,69,75,76,77,78,80,81,82,87,88,89,91,92,93,94,95,96,97,98,100,101,102,103,104,],[13,13,-8,-5,18,-3,-6,20,-7,-4,-9,-2,29,38,42,46,47,47,51,29,-24,-31,-28,47,-30,-27,-14,-21,13,-10,-12,-17,47,47,-29,-16,-34,72,47,47,47,47,47,13,47,47,-18,-19,47,-38,47,29,-25,-26,-33,-23,-22,-48,47,13,13,-32,-15,-13,-39,-11,-20,13,13,-35,-36,13,13,-37,]),'{':([20,73,74,99,],[40,88,89,102,]),'[':([13,38,42,47,],[26,59,64,59,]),'}':([2,4,8,9,11,12,14,16,32,33,34,36,37,38,39,41,42,43,47,51,52,62,65,66,68,76,77,78,80,81,82,91,92,93,94,95,96,97,98,100,101,103,104,],[-8,-5,-3,-6,-7,-4,-9,-2,-24,-31,-28,-30,-27,-14,-21,-10,-12,-17,-29,-16,-34,82,-18,-19,-38,-25,-26,-33,-23,-22,-48,-32,-15,-13,-39,-11,-20,100,101,-35,-36,104,-37,]),'CLASS':([0,1,2,4,8,9,11,12,14,16,32,33,34,36,37,38,39,40,41,42,43,47,51,52,62,65,66,68,76,77,78,80,81,82,88,89,91,92,93,94,95,96,97,98,100,101,102,103,104,],[10,10,-8,-5,-3,-6,-7,-4,-9,-2,-24,-31,-28,-30,-27,-14,-21,10,-10,-12,-17,-29,-16,-34,10,-18,-19,-38,-25,-26,-33,-23,-22,-48,10,10,-32,-15,-13,-39,-11,-20,10,10,-35,-36,10,10,-37,]),'DEF':([0,1,2,4,8,9,11,12,14,16,32,33,34,36,37,38,39,40,41,42,43,47,51,52,62,65,66,68,76,77,78,80,81,82,88,89,91,92,93,94,95,96,97,98,100,101,102,103,104,],[5,5,-8,-5,-3,-6,-7,-4,-9,-2,-24,-31,-28,-30,-27,-14,-21,5,-10,-12,-17,-29,-16,-34,5,-18,-19,-38,-25,-26,-33,-23,-22,-48,5,5,-32,-15,-13,-39,-11,-20,5,5,-35,-36,5,5,-37,]),'$end':([1,2,4,7,8,9,11,12,14,16,32,33,34,36,37,38,39,41,42,43,47,51,52,65,66,68,76,77,78,80,81,82,91,92,93,94,95,96,100,101,104,],[-1,-8,-5,0,-3,-6,-7,-4,-9,-2,-24,-31,-28,-30,-27,-14,-21,-10,-12,-17,-29,-16,-34,-18,-19,-38,-25,-26,-33,-23,-22,-48,-32,-15,-13,-39,-11,-20,-35,-36,-37,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'function':([0,1,40,62,88,89,97,98,102,103,],[11,11,11,11,11,11,11,11,11,11,]),'term':([19,21,25,26,35,44,45,59,60,61,63,64,67,69,87,],[32,32,32,32,32,32,32,32,80,81,32,32,32,32,32,]),'statements':([0,40,88,89,102,],[1,62,97,98,103,]),'assignment':([0,1,40,62,88,89,97,98,102,103,],[12,12,12,12,12,12,12,12,12,12,]),'self':([0,1,17,19,21,25,26,31,35,40,44,45,53,56,57,59,60,61,62,63,64,67,69,75,87,88,89,97,98,102,103,],[6,6,30,33,33,33,33,30,33,6,33,33,71,33,33,33,33,33,6,33,33,33,33,30,33,6,6,6,6,6,6,]),'class':([0,1,40,62,88,89,97,98,102,103,],[14,14,14,14,14,14,14,14,14,14,]),'expressions':([25,63,67,],[48,83,85,]),'program':([0,],[7,]),'statement':([0,1,40,62,88,89,97,98,102,103,],[8,16,8,16,8,8,16,16,8,16,]),'factor':([19,21,25,26,35,44,45,56,57,59,60,61,63,64,67,69,87,],[37,37,37,37,37,37,37,76,77,37,37,37,37,37,37,37,37,]),'print':([0,1,40,62,88,89,97,98,102,103,],[9,9,9,9,9,9,9,9,9,9,]),'variables':([17,31,75,],[28,54,90,]),'run_function':([0,1,40,62,88,89,97,98,102,103,],[2,2,2,2,2,2,2,2,2,2,]),'expression':([19,21,25,26,35,44,45,59,63,64,67,69,87,],[39,43,49,50,58,65,66,79,49,84,49,86,96,]),'operation':([0,1,40,62,88,89,97,98,102,103,],[4,4,4,4,4,4,4,4,4,4,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> statements','program',1,'p_program','py_yacc.py',18),
  ('statements -> statements statement','statements',2,'p_statements','py_yacc.py',25),
  ('statements -> statement','statements',1,'p_statements','py_yacc.py',26),
  ('statement -> assignment','statement',1,'p_statement','py_yacc.py',37),
  ('statement -> operation','statement',1,'p_statement','py_yacc.py',38),
  ('statement -> print','statement',1,'p_statement','py_yacc.py',39),
  ('statement -> function','statement',1,'p_statement','py_yacc.py',40),
  ('statement -> run_function','statement',1,'p_statement','py_yacc.py',41),
  ('statement -> class','statement',1,'p_statement','py_yacc.py',42),
  ('assignment -> VARIABLE = NUMBER','assignment',3,'p_assignment','py_yacc.py',49),
  ('assignment -> VARIABLE [ expression ] = NUMBER','assignment',6,'p_assignment','py_yacc.py',50),
  ('assignment -> VARIABLE = VARIABLE','assignment',3,'p_assignment','py_yacc.py',51),
  ('assignment -> VARIABLE = VARIABLE [ expression ]','assignment',6,'p_assignment','py_yacc.py',52),
  ('assignment -> self = VARIABLE','assignment',3,'p_assignment','py_yacc.py',53),
  ('assignment -> VARIABLE = VARIABLE ( expressions )','assignment',6,'p_assignment','py_yacc.py',54),
  ('self -> SELF . VARIABLE','self',3,'p_self','py_yacc.py',95),
  ('operation -> VARIABLE = expression','operation',3,'p_operation','py_yacc.py',104),
  ('operation -> VARIABLE + = expression','operation',4,'p_operation','py_yacc.py',105),
  ('operation -> VARIABLE - = expression','operation',4,'p_operation','py_yacc.py',106),
  ('operation -> VARIABLE [ expression ] = expression','operation',6,'p_operation','py_yacc.py',107),
  ('operation -> self = expression','operation',3,'p_operation','py_yacc.py',108),
  ('expression -> expression + term','expression',3,'p_expression','py_yacc.py',134),
  ('expression -> expression - term','expression',3,'p_expression','py_yacc.py',135),
  ('expression -> term','expression',1,'p_expression','py_yacc.py',136),
  ('term -> term * factor','term',3,'p_term','py_yacc.py',148),
  ('term -> term / factor','term',3,'p_term','py_yacc.py',149),
  ('term -> factor','term',1,'p_term','py_yacc.py',150),
  ('factor -> NUMBER','factor',1,'p_factor','py_yacc.py',162),
  ('factor -> VARIABLE','factor',1,'p_factor','py_yacc.py',163),
  ('factor -> STR','factor',1,'p_factor','py_yacc.py',164),
  ('factor -> self','factor',1,'p_factor','py_yacc.py',165),
  ('factor -> VARIABLE [ expression ]','factor',4,'p_factor','py_yacc.py',166),
  ('factor -> ( expression )','factor',3,'p_factor','py_yacc.py',167),
  ('print -> PRINT ( variables )','print',4,'p_print','py_yacc.py',191),
  ('function -> DEF VARIABLE ( variables ) { statements }','function',8,'p_function','py_yacc.py',198),
  ('function -> DEF VARIABLE ( SELF ) { statements }','function',8,'p_function','py_yacc.py',199),
  ('function -> DEF VARIABLE ( SELF , variables ) { statements }','function',10,'p_function','py_yacc.py',200),
  ('run_function -> VARIABLE ( expressions )','run_function',4,'p_run_function','py_yacc.py',223),
  ('run_function -> VARIABLE . VARIABLE ( expressions )','run_function',6,'p_run_function','py_yacc.py',224),
  ('variables -> <empty>','variables',0,'p_variables','py_yacc.py',238),
  ('variables -> VARIABLE','variables',1,'p_variables','py_yacc.py',239),
  ('variables -> variables , VARIABLE','variables',3,'p_variables','py_yacc.py',240),
  ('variables -> self','variables',1,'p_variables','py_yacc.py',241),
  ('variables -> variables , self','variables',3,'p_variables','py_yacc.py',242),
  ('expressions -> <empty>','expressions',0,'p_expressions','py_yacc.py',265),
  ('expressions -> expression','expressions',1,'p_expressions','py_yacc.py',266),
  ('expressions -> expressions , expression','expressions',3,'p_expressions','py_yacc.py',267),
  ('class -> CLASS VARIABLE { statements }','class',5,'p_class','py_yacc.py',281),
]
