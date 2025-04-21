from proof_helper.core.symbols import substitute_symbols

def test_basic_expansion():
    assert substitute_symbols("A$B") == "A→B"

def test_multiple_symbols():
    assert substitute_symbols("~A & B | C") == "¬A ∧ B ∨ C"

def test_comments_preserved():
    input_text = "A$B ; this is a comment"
    expected = "A→B ; this is a comment"
    assert substitute_symbols(input_text) == expected

def test_comment_with_symbols_not_replaced():
    input_text = "A & B ; this should not change: ~ $ /"
    expected = "A ∧ B ; this should not change: ~ $ /"
    assert substitute_symbols(input_text) == expected
