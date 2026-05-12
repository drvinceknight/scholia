from scholia.scheme import SCHEME_FILENAME, Category, Question, Scheme


def test_load_scheme(scheme_path):
    scheme = Scheme.load(scheme_path)
    assert "q1(a)" in scheme.questions
    assert "q1(b)" in scheme.questions
    assert "a" in scheme.questions["q1(a)"].categories
    assert scheme.questions["q1(a)"].categories["a"].marks == 0
    assert scheme.questions["q1(a)"].categories["a"].feedback == "Did not attempt"


def test_load_empty_dict(tmp_path):
    path = tmp_path / "scheme.yaml"
    path.write_text("{}")
    scheme = Scheme.load(path)
    assert scheme.questions == {}


def test_load_empty_file(tmp_path):
    path = tmp_path / "scheme.yaml"
    path.write_text("")
    scheme = Scheme.load(path)
    assert scheme.questions == {}


def test_save_roundtrip(tmp_path, scheme_path):
    scheme = Scheme.load(scheme_path)
    out_path = tmp_path / "out.yaml"
    scheme.save(out_path)
    loaded = Scheme.load(out_path)
    assert loaded.questions.keys() == scheme.questions.keys()
    assert (
        loaded.questions["q1(a)"].categories["b"].marks
        == scheme.questions["q1(a)"].categories["b"].marks
    )


def test_save_empty_scheme(tmp_path):
    path = tmp_path / "scheme.yaml"
    Scheme().save(path)
    loaded = Scheme.load(path)
    assert loaded.questions == {}


def test_question_names(scheme_path):
    scheme = Scheme.load(scheme_path)
    names = scheme.question_names()
    assert "q1(a)" in names
    assert "q1(b)" in names


def test_get_category_exists(scheme_path):
    scheme = Scheme.load(scheme_path)
    cat = scheme.get_category("q1(a)", "b")
    assert cat is not None
    assert cat.marks == 8
    assert cat.feedback == "Perfect solution"


def test_get_category_missing_question(scheme_path):
    scheme = Scheme.load(scheme_path)
    assert scheme.get_category("q99", "a") is None


def test_get_category_missing_category(scheme_path):
    scheme = Scheme.load(scheme_path)
    assert scheme.get_category("q1(a)", "z") is None


def test_scheme_filename_constant():
    assert SCHEME_FILENAME == "scheme.yaml"


def test_category_dataclass():
    cat = Category(marks=5, feedback="Good")
    assert cat.marks == 5
    assert cat.feedback == "Good"


def test_question_dataclass():
    question = Question()
    assert question.categories == {}
