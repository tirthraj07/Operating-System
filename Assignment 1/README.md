## Assembler Pass 1

How to run
```powershell
javac Assembler.java
java Assember <file-name>
```

### Test case 1
```powershell
java Assembler testcase1.asm
```

```bash
(AD, 1)(C, 101)
(IS, 9)(S, 1)
(IS, 4)(2)(S, 2)
(IS, 5)(2)(S, 3)
(IS, 3)(2)(S, 3)
(IS, 4)(3)(S, 3)
(IS, 1)(3)(S, 2)
(IS, 5)(3)(S, 3)
(IS, 6)(3)(S, 1)
(IS, 7)(2)(S, 4)
(IS, 8)(2)(S, 5)
(IS, 5)(2)(S, 6)
(IS, 10)(S, 6)
(IS, 0)
(DL, 2)(C, 1)
(DL, 2)(C, 1)
(DL, 1)(C, 1)
(DL, 2)(C, 1)
(DL, 1)(C, 2)
(AD, 2)
---- Symbol Table ----
N : 114
ONE : 116
TERM : 117
AGAIN : 104
TWO : 118
RESULT : 115

---- Literal Table ----
NULL
```

### Test case 2
```powershell
java Assembler testcase2.asm
```

```bash
(AD, 1)(C, 101)
(IS, 9)(S, 1)
(IS, 4)(2)(S, 2)
(IS, 5)(2)(S, 3)
(IS, 3)(2)(S, 3)
(IS, 4)(3)(S, 3)
(IS, 1)(3)(S, 2)
(IS, 5)(3)(S, 3)
(IS, 6)(3)(S, 1)
(IS, 7)(2)(S, 4)
(IS, 8)(2)(S, 5)
(IS, 5)(2)(S, 5)
(IS, 10)(S, 5)
(IS, 0)
(DL, 2)(C, 1)
(DL, 2)(C, 1)
(DL, 1)(C, 1)
(DL, 2)(C, 100)
(DL, 1)(C, 2)
(AD, 2)
---- Symbol Table ----
N : 114
ONE : 116
TERM : 117
AGAIN : 104
RESULT : 115
TWO : 217

---- Literal Table ----
NULL
```

### Test case 3
```powershell
java Assembler testcase3.asm
```

```bash
(AD, 1)(C, 100)
(DL, 2)(C, 3)
(IS, 4)(1)(S, 3)
(IS, 1)(1)(S, 4)
(IS, 5)(1)(S, 5)
(AD, 4)(C, 101)
(IS, 10)(S, 5)
(AD, 3)(C, 99)
(DL, 1)(C, 5)
(AD, 3)(C, 107)
(IS, 0)
(DL, 1)(C, 1)
(AD, 2)(S, 2)
---- Symbol Table ----
A : 100
L1 : 103
B : 108
C : 99
D : 101
L2 : 106

---- Literal Table ----
NULL

```

### Test case 4
```powershell
java Assembler testcase4.asm
```

```bash
(AD, 1)(C, 100)
(DL, 2)(C, 3)
(IS, 4)(1)(S, 3)
(IS, 1)(1)(S, 4)
(IS, 5)(1)(S, 5)
(AD, 4)(C, 101)
(IS, 10)(S, 5)
(AD, 3)(C, 99)
(DL, 1)(C, 5)
(AD, 3)(C, 107)
(IS, 0)
(DL, 1)(C, 1)
(AD, 2)(S, 2)
---- Symbol Table ----
A : 100
L1 : 103
B : 108
C : 99
D : 101
L2 : 106

---- Literal Table ----
NULL
```


### Test case 5
```powershell
java Assembler testcase5.asm
```

```bash
(AD, 1)(C, 200)
(IS, 4)(1)(L, 1)
(IS, 5)(1)(S, 1)
(IS, 4)(1)(S, 1)
(IS, 4)(3)(S, 3)
(IS, 1)(3)(L, 2)
(IS, 4)(1)(S, 1)
(IS, 4)(3)(S, 3)
(IS, 4)(1)(S, 1)
(IS, 4)(3)(S, 3)
(IS, 4)(1)(S, 1)
(IS, 7)(6)(S, 4)
(AD, 5)
(IS, 4)(1)(S, 1)
(IS, 2)(1)(L, 3)
(IS, 7)(1)(S, 5)
(IS, 0)
(AD, 3)(C, 204)
(IS, 3)(3)
(AD, 3)(C, 217)
(DL, 2)(C, 1)
(AD, 4)(S, 2)
(DL, 2)(C, 1)
(AD, 2)
---- Symbol Table ----
A : 217
LOOP : 202
B : 218
NEXT : 214
BACK : 202
LAST : 216

---- Literal Table ----
='5' : 211
='1' : 212

='1' : 219
```