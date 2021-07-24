import error, compiler, functions

def return_outsides(tokens: list[str]) -> list[str]:
    inside = False
    level = 0
    outsides: list[str] = []
    starters = ["function", "object", "for", "while", "if", "else", "elif"]

    for token in tokens:
        if inside:
            if level == 0:
                inside = False

            if token == "{":
                level += 0.5
            if token == "}":
                level -= 1

        if token in starters: # going inside
            inside = True
            level += 0.5
        
        if not inside:
            outsides.append(token)

    result = []
    for outside in outsides:
        if outside != "":
            result.append(outside)

    return result

def return_insides(tokens: list[str]) -> list[str]:
    inside = False
    level = 0
    insides: list[str] = [[]]
    i = 0
    starters = ["function", "object", "for", "while", "if", "else", "elif"]

    for token in tokens:
        if inside:
            if level == 0:
                inside = False
                i += 1
                insides.append([])

            elif token == "{":
                level += 0.5
            elif token == "}":
                level -= 1

        if token in starters:
            inside = True
            level += 0.5

        if inside:
            insides[i].append(token)

    result = []
    for inside in insides:
        if inside != [""]:
            result.append(inside)

    return result

def in_scope(tokens: list[str], enter: str, exit: str) -> list[str]:
    level = 0
    inside = False
    result = []

    for token in tokens:
        if inside:
            if token == exit:
                level -= 1

            if level == 0:
                return result

            elif token == enter:
                level += 1

        if inside:
            result.append(token)

        if token == enter:
            level += 1
            inside = True

    return result

def parse(tokens: list[str], func = False): # new parse
    expr = []
    print(f"tokens to parse {tokens}")
    tokens += ";"

    i = -1
    #//for i, token in enumerate(tokens):
    while i < len(tokens) - 1:
        i += 1
        token = tokens[i]

        if token == ";":
            if expr != [] and len(expr) >= 2:
                if expr[0] == "function":
                    compiler.compile_func(expr + in_scope(tokens[i-len(expr):] + ["}"], "{", "}"))
                    i += len(in_scope(tokens[i-len(expr):], "{", "}"))

                elif expr[0] == "object":
                    error.error("objects arent implemented yet. try again later")

                elif expr[1] == "=" or expr[0] in functions.types:
                    if not func:
                        compiler.compile_expr(expr)
                    else:
                        compiler.add_funcrcl(compiler.compile_expr(expr, True))

                expr = []
        else:
            expr.append(token)

def parse_old(tokens: list[str], func = False): # todo parse better
    # step 1: get all the tokens that are outside functions or classes
    outsides = return_outsides(tokens)
    out_expressions = " ".join(outsides).split(";")
    out_expressions = [x.removeprefix(" ").removesuffix(" ").split(" ") for x in out_expressions]

    new_out = []
    for out in out_expressions:
        if out != [""]:
            new_out.append(out)
    out_expressions: list[list[str]] = new_out
    
    # step 2: compile those
    print(out_expressions)

    for expr in out_expressions:
        if not func:
            compiler.compile_expr(expr)
        else:
            compiler.add_funcrcl(compiler.compile_expr(expr, True))


    # step 3: call parser again with all groups of tokens inside
    insides = return_insides(tokens)
    print(insides)

    if insides != [[]]:
        for block in insides:
            print(block)
            if block[0] == "function":
                compiler.compile_func(block)
            elif block[0] == "object":
                error.error("objects arent supported yet")
