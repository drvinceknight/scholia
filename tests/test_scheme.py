from scholia.scheme import SCHEME_FILENAME, Band, Category, Criterion, Scheme


def test_load_scheme(scheme_path):
    scheme = Scheme.load(scheme_path)
    assert "q1(a)" in scheme.criteria
    assert "q1(b)" in scheme.criteria
    assert "a" in scheme.criteria["q1(a)"].categories
    assert scheme.criteria["q1(a)"].categories["a"].marks == 0
    assert scheme.criteria["q1(a)"].categories["a"].feedback == "Did not attempt"


def test_load_empty_dict(tmp_path):
    path = tmp_path / "scheme.yaml"
    path.write_text("{}")
    scheme = Scheme.load(path)
    assert scheme.criteria == {}


def test_load_empty_file(tmp_path):
    path = tmp_path / "scheme.yaml"
    path.write_text("")
    scheme = Scheme.load(path)
    assert scheme.criteria == {}


def test_save_roundtrip(tmp_path, scheme_path):
    scheme = Scheme.load(scheme_path)
    out_path = tmp_path / "out.yaml"
    scheme.save(out_path)
    loaded = Scheme.load(out_path)
    assert loaded.criteria.keys() == scheme.criteria.keys()
    assert (
        loaded.criteria["q1(a)"].categories["b"].marks
        == scheme.criteria["q1(a)"].categories["b"].marks
    )


def test_save_empty_scheme(tmp_path):
    path = tmp_path / "scheme.yaml"
    Scheme().save(path)
    loaded = Scheme.load(path)
    assert loaded.criteria == {}


def test_criterion_names(scheme_path):
    scheme = Scheme.load(scheme_path)
    names = scheme.criterion_names()
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


def test_criterion_dataclass():
    criterion = Criterion()
    assert criterion.categories == {}


def test_band_dataclass():
    band = Band(name="Pass", min=40)
    assert band.name == "Pass"
    assert band.min == 40


def test_load_scheme_no_bands(scheme_path):
    scheme = Scheme.load(scheme_path)
    assert scheme.bands == []


def test_load_scheme_with_bands(tmp_path):
    import yaml

    path = tmp_path / "scheme.yaml"
    with open(path, "w") as file_handle:
        yaml.dump(
            {
                "bands": [
                    {"name": "Fail", "min": 0},
                    {"name": "Pass", "min": 40},
                    {"name": "First class", "min": 70},
                ],
                "q1": {"a": {"marks": 0, "feedback": "x"}},
            },
            file_handle,
            sort_keys=False,
        )
    scheme = Scheme.load(path)
    assert len(scheme.bands) == 3
    assert scheme.bands[0].name == "Fail"
    assert scheme.bands[0].min == 0
    assert scheme.bands[1].name == "Pass"
    assert scheme.bands[1].min == 40
    assert scheme.bands[2].name == "First class"
    assert scheme.bands[2].min == 70
    assert "q1" in scheme.criteria


def test_save_roundtrip_with_bands(tmp_path):
    import yaml

    path = tmp_path / "scheme.yaml"
    with open(path, "w") as file_handle:
        yaml.dump(
            {
                "bands": [
                    {"name": "Fail", "min": 0},
                    {"name": "Pass", "min": 40},
                ],
                "q1": {"a": {"marks": 0, "feedback": "x"}},
            },
            file_handle,
        )
    scheme = Scheme.load(path)
    out = tmp_path / "out.yaml"
    scheme.save(out)
    reloaded = Scheme.load(out)
    assert len(reloaded.bands) == 2
    assert reloaded.bands[1].name == "Pass"
    assert reloaded.bands[1].min == 40
