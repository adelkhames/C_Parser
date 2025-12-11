
class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def current(self):
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        return ("EOF", "EOF")

    def advance(self):
        self.index += 1

    def eat(self, expected_type=None, expected_value=None):
        tok_type, tok_value = self.current()

        while tok_type in ["COMMENT", "NEWLINE"]:
            self.advance()
            tok_type, tok_value = self.current()

        if expected_type and tok_type != expected_type:
            raise ParseError(f"Syntax Error: Expected type {expected_type}, got {tok_type}")

        if expected_value and tok_value != expected_value:
            raise ParseError(f"Syntax Error: Expected value '{expected_value}', got '{tok_value}'")

        self.advance()
        return tok_type, tok_value

    def parse(self):
        return self.parse_function()

    def parse_function(self):
        self.eat("KEYWORD", "int")
        _, name = self.eat("IDENTIFIER")
        self.eat("SPECIAL CHARACTER", "(")
        self.eat("SPECIAL CHARACTER", ")")
        body = self.parse_block()
        return ("Function", name, body)

    def parse_block(self):
        self.eat("SPECIAL CHARACTER", "{")
        statements = []

        while self.current()[1] != "}":
            statements.append(self.parse_statement())

        self.eat("SPECIAL CHARACTER", "}")
        return ("Block", statements)

    def parse_statement(self):
        tok_type, tok_value = self.current()

        if tok_type == "KEYWORD" and tok_value == "int":
            return self.parse_declaration()
        if tok_type == "KEYWORD" and tok_value == "if":
            return self.parse_if()
        if tok_type == "KEYWORD" and tok_value == "return":
            return self.parse_return()
        
        return self.parse_assignment()

    def parse_declaration(self):
        self.eat("KEYWORD", "int")
        _, name = self.eat("IDENTIFIER")
        names = [name]

        while self.current()[1] == ",":
            self.eat("SPECIAL CHARACTER", ",")
            _, next_name = self.eat("IDENTIFIER")
            names.append(next_name)

        self.eat("SPECIAL CHARACTER", ";")
        return ("Declaration", names)

    def parse_if(self):
        self.eat("KEYWORD", "if")
        self.eat("SPECIAL CHARACTER", "(")
        condition = self.parse_expression()
        self.eat("SPECIAL CHARACTER", ")")
        then_block = self.parse_block()

        self.eat("KEYWORD", "else")
        else_block = self.parse_block()

        return ("If", condition, then_block, else_block)

    def parse_return(self):
        self.eat("KEYWORD", "return")
        value = self.parse_expression()
        self.eat("SPECIAL CHARACTER", ";")
        return ("Return", value)

    def parse_assignment(self):
        _, name = self.eat("IDENTIFIER")
        self.eat("OPERATOR", "=")
        expr = self.parse_expression()
        self.eat("SPECIAL CHARACTER", ";")
        return ("Assign", name, expr)

    def parse_expression(self):
        left = self.parse_primary()
        tok_type, tok_value = self.current()

        if tok_type == "OPERATOR" and tok_value in ["==", "-"]:
            op = tok_value
            self.eat("OPERATOR")
            right = self.parse_primary()
            return ("BinOp", op, left, right)

        return left

    def parse_primary(self):
        tok_type, tok_value = self.current()

        if tok_type == "IDENTIFIER":
            self.eat("IDENTIFIER")
            return ("Var", tok_value)

        if tok_type == "NUMERIC CONSTANT":
            self.eat("NUMERIC CONSTANT")
            return ("Num", tok_value)

        raise ParseError(f"Invalid expression token: {tok_type}, {tok_value}")



def get_tokens_from_user():
    print("\n Enter Tokens 1 By 1 : ")
    print("<TYPE, value>")
    print("If You Finished Write : done\n")

    tokens = []

    while True:
        line = input("Token: ").strip()

        if line.lower() == "done":
            break

        try:
            line = line.replace("<", "").replace(">", "")
            token_type, value = line.split(",", 1)
            tokens.append((token_type.strip(), value.strip()))
        except:
            print("Syntax Error Must Be  : <TYPE, value>")

    return tokens



if __name__ == "__main__":
    print("=== Simple C Parser ===")

    tokens = get_tokens_from_user()
    print("\n Received Tokens:")
    for t in tokens:
        print(t)

    parser = Parser(tokens)

    try:
        ast = parser.parse()
        print("\n AST Output:")
        print(ast)
    except ParseError as e:
        print("\n Syntax Error:")
        print(e)
