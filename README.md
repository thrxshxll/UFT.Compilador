## PL0MOD Programming Language

O presente repositório contém a implementação de uma mini linguagem de programação proposta pela disciplina de compiladores da universidade.

Implementar uma mini linguagem de programação é uma experiência interessante pois a construção de uma mini linguagem envolve aprender como os compiladores funcionam em um nível fundamental. Isso inclui etapas como análise léxica, análise sintática, análise semântica, geração de código intermediário e tradução. Conhecer esses processos em detalhes 
ajuda em uma melhor compreensão de como as linguagens de programação interpretam e executam códigos.

O **Analisador Léxico (Scanner)** se dedica a dividir a sequência de caracteres de um código fonte escrito em PL0MOD em partes significativas, que são os tokens, e classificá-las de acordo com a grámática especificada em `pl0mod.grammar`. Se um token que não pertence à gramática for encontrado, o Lexer emitirá um erro (LexerError).

O **Analisador Sintático (Parser)** é dedicado a avaliar se os token repassados pelo **Scanner** estão de acordo com a gramática; isto é, se o token foi escrito corretamente no código fonte em questão, sendo isso avaliado considerando, além da gramática da linguagem  (`pl0mod.grammar`), a classe e a ordem que o token foi escrito no código fonte. O Parser da PL0MOD é um Analisador Descendente Recursivo, caso surja a curiosidade.

O **Tradutor (Translator)** é dedicado a gerar códigos para a arquitetura-alvo, que no caso da PL0MOD a arquitetura-alvo são códigos em Python. Ou seja, se o token, ou o conjunto de token, passou pelo Lexer e Parser sem erros, então o **Translator** faz a conversão para código Python.

A PLOMOD é uma linguagem de programação simplificada, mas, como será mostrado adiante, pode ser usada para escrever programas simples, como um programa para verificar se um número é ímpar ou par e até mesmo verificar quais os números primos em um dado intervalo!

A PLOMOD possui as estruturas básicas que normalmente são encontradas em uma linguagem de programação, como as estruturas condicionais, estruturas derepetição, funções, operadores matemáticos e relacionais, e variáves.

O compilador da PL0MOD foi implementado em Python e o código "de máquina" gerado pelo compilador é o "Pytcode", que na verdade é um código em Python que será executado pelo interpredor Python. Ou seja:

    +--------------+        +----------------------------+        +--------------+
    |              |        |                            |        |              |
    |   *.pl0mod   |   =>   | Lexer > Parser > Traslator |   =>   |     *.py     |
    |              |        |                            |        |              |
    +--------------+        +----------------------------+        +--------------+
                                       compiler

Esse processo de conversão, ou tradução, é o fundamento envolvido no processo de compilação real de linguagens compiladas. Os processos geralmente envolve a análise léxica, análise sintática, análise semântica, geração de código intermediário e a geração do código final. Está última etapa é a conversão do código intermediário em código de máquina específico para a arquitetura alvo (como x86, ARM, etc.). O código gerado é o que a máquina realmente pode entender e executar.

Mas na PL0MOD os projetistas decidiram se aproveitar do interpretador Python e por isso o arquivo final final do compilador é um Pytcode (*.py), sendo este interpretador pelo interpretador Python.


### PL0MOD Compiler (PLC)

O utilitário `plc` é o compilador e carregador da PL0MOD; ele recebe um arquivo como parâmetro tal que o conteúdo do arquivo é um programa escrito em PL0MOD. Recebido o arquivo, ele faz a compilação para código Python e, posteriormente, passa o arquivo gerado para o interpretador Python.


## PL0MOD Em Ação!

Feita as devidas apresentações, agora é hora de ver a PL0MOD em ação!



## Experimente Em Sua Máquina

Instale o Python em sua máquina. O projeto foi desenvolvido utilizando o Python na versão `3.11.2`. Então a única garantia que lhe pode ser dada é que nessa versão irá funcionar heheh.


#### Clone o repositório e entre nele

    git clone -b main https://github.com/yurincmt/pl0mod-language.git ; cd pl0mod-language


#### Progame e execute em pl0mod

Dado que você programou em pl0m0d, rode o programa usando o `plc` da seguinte forma:

    ./plc seuprograma.pl0mod

No diretório `data/` há alguns programas prontos para serem usados como testes e como exemplo para criar ou seu. Execute-os como o exemplo a seguir:

    ./plc /data/checkprimes.pl0mod


## Estrutura Do Projeto

    .
    ├── pl0mod.grammar
    ├── plc
    ├── README.md
    ├── data
    │   ├── checkprimes.pl0mod
    │   ├── evennums.pl0mod
    │   ├── loopprint.pl0mod
    │   ├── oddnums.pl0mod
    │   └── syntaxerror.pl0mod
    └── src
        ├── lexer
        │   ├── lex.py
        │   ├── main.py
        │   ├── regex-regras
        │   ├── rules.py
        │   └── token.py
        ├── parser
        │   ├── lex.py -> ../lexer/lex.py
        │   ├── main.py
        │   ├── parser.py
        │   ├── rules.py -> ../lexer/rules.py
        │   └── token.py -> ../lexer/token.py
        └── translator
            ├── lex.py -> ../lexer/lex.py
            ├── main.py
            ├── rules.py -> ../lexer/rules.py
            ├── test.py
            ├── token.py -> ../lexer/token.py
            └── translator.py


## Obs:

Caso tenha interesse em saber mais sobre os processos intermediários do compilador da PL0MOD, como Lexer, Parser e Translator, terá um README.md para cada um deles nas suas devidas branches. Então dê uma olhada.


## Gramática Formal da PL0MOD


    <program>            --> <block>"."

    <block>              --> <constants>? <variables>? <procedures>? <statement>?

    <constants>          --> "CONST" <constdecl> ";"

    <constdecl>          --> <constdef> "," <constdecl>
                        | <constdef>

    <constdef>           --> <Ident> "=" <Number>

    <variables>          --> "VAR" <vardecl> ";"

    <vardecl>            --> <Ident> "," <vardecl>
                        | <Ident>

    <arg>            --> <Ident> "," <arg>
                        | <Ident>

    <procedures>         --> <procdecl> <procedures>?

    <procdecl>           --> "PROCEDURE" <Ident> <arg>? ";" <block> ";"

    <statement>          --> <Ident> "<-" <expression>
                        | "RETURN" <Ident>
                        | "CALL" (<Ident> "<-")? <Ident> <arg>?
                        | "BEGIN" <compound statement> "END"
                        | "IF" "NOT"? <condition> "THEN" <statement>
                        | "WHILE" "NOT"? <condition> "DO" <statement>
                        | "PRINT" <expression>

    <compound statement> --> (<statement> ";")*

    <condition>          --> "ODD" <expression>
                        | "EVEN" <expression>
                        | <expression> <relation> <expression>

    <relation>           --> "="
                        | "#"
                        | "<"
                        | "<="
                        | ">"
                        | ">="
                        | "/?"

    <expression>         --> <sign>? <term> <terms>?

    <sign>               --> "+"
                        | "-"

    <terms>              --> "+" <term>
                        | "-" <term>

    <term>               --> <factor> <factors>?

    <factors>            --> "/" <factor>
                        | "*" <factor>

    <factor>             --> <Ident>
                        | <Number>
                        | "(" <expression> ")"