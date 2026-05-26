import pytest

from scholia.students import STUDENTS_FILENAME, Student, Students


def _make_csv(names: list[str], encoding: str) -> bytes:
    """Build a minimal students CSV encoded."""
    rows = ["student_id,q1"] + [f"{name},a" for name in names]
    return "\n".join(rows).encode(encoding)


def test_load_students(students_path):
    students = Students.load(students_path)
    assert len(students.students) == 2
    assert students.students[0].student_id == "s001"
    assert students.students[0].assignments["q1(a)"] == "b"
    assert students.question_names == ["q1(a)", "q1(b)"]


def test_load_no_question_columns(tmp_path):
    path = tmp_path / "students.csv"
    path.write_text("student_id\ns001\n")
    students = Students.load(path)
    assert len(students.students) == 1
    assert students.question_names == []


def test_load_empty_roster(tmp_path):
    path = tmp_path / "students.csv"
    path.write_text("student_id\n")
    students = Students.load(path)
    assert students.students == []
    assert students.question_names == []


def test_save_roundtrip(tmp_path, students_path):
    students = Students.load(students_path)
    out_path = tmp_path / "out.csv"
    students.save(out_path)
    loaded = Students.load(out_path)
    assert len(loaded.students) == 2
    assert loaded.students[0].student_id == "s001"
    assert loaded.students[1].assignments["q1(b)"] == "a"


def test_save_fills_missing_assignments(tmp_path):
    path = tmp_path / "students.csv"
    path.write_text("student_id\ns001\n")
    students = Students.load(path)
    students.question_names = ["q1(a)"]
    out_path = tmp_path / "out.csv"
    students.save(out_path)
    loaded = Students.load(out_path)
    assert loaded.students[0].assignments["q1(a)"] == ""


def test_update_existing_question(students_path):
    students = Students.load(students_path)
    students.update("s001", "q1(a)", "a")
    assert students.students[0].assignments["q1(a)"] == "a"


def test_update_new_question(students_path):
    students = Students.load(students_path)
    students.update("s001", "q2(a)", "b")
    assert "q2(a)" in students.question_names
    assert students.students[0].assignments["q2(a)"] == "b"


def test_update_missing_student(students_path):
    students = Students.load(students_path)
    with pytest.raises(ValueError, match="'s999' not found"):
        students.update("s999", "q1(a)", "a")


def test_get_student_found(students_path):
    students = Students.load(students_path)
    student = students.get_student("s002")
    assert student is not None
    assert student.student_id == "s002"


def test_get_student_not_found(students_path):
    students = Students.load(students_path)
    assert students.get_student("s999") is None


def test_students_filename_constant():
    assert STUDENTS_FILENAME == "students.csv"


def test_student_dataclass():
    student = Student(student_id="s001")
    assert student.assignments == {}


def test_sync_headers_adds_new_question(tmp_path):
    path = tmp_path / "students.csv"
    path.write_text("student_id,q1(a)\ns001,b\n")
    students = Students.load(path)
    students.sync_headers(["q1(a)", "q1(b)"])
    assert students.question_names == ["q1(a)", "q1(b)"]
    assert students.students[0].assignments["q1(b)"] == ""
    assert students.students[0].assignments["q1(a)"] == "b"


def test_sync_headers_reorders(students_path):
    students = Students.load(students_path)
    students.sync_headers(["q1(b)", "q1(a)"])
    assert students.question_names == ["q1(b)", "q1(a)"]
    assert students.students[0].assignments["q1(a)"] == "b"


def test_sync_headers_appends_extra_columns(students_path):
    students = Students.load(students_path)
    students.sync_headers(["q1(a)"])
    assert students.question_names == ["q1(a)", "q1(b)"]


def test_load_note_column(tmp_path):
    path = tmp_path / "students.csv"
    path.write_text('student_id,q1,note\ns001,a,"Good work, overall."\n')
    students = Students.load(path)
    assert students.students[0].note == "Good work, overall."
    assert students.question_names == ["q1"]


def test_load_missing_note_column(tmp_path):
    path = tmp_path / "students.csv"
    path.write_text("student_id,q1\ns001,a\n")
    students = Students.load(path)
    assert students.students[0].note == ""


def test_save_includes_note_column(tmp_path):
    students = Students(
        students=[Student(student_id="s001", note="Excellent effort.")],
        question_names=[],
    )
    out_path = tmp_path / "out.csv"
    students.save(out_path)
    content = out_path.read_text()
    assert "note" in content
    assert "Excellent effort." in content


def test_save_roundtrip_with_note(tmp_path):
    students = Students(
        students=[
            Student(
                student_id="s001",
                assignments={"q1": "a"},
                note="Great effort.",
            )
        ],
        question_names=["q1"],
    )
    out_path = tmp_path / "out.csv"
    students.save(out_path)
    loaded = Students.load(out_path)
    assert loaded.students[0].note == "Great effort."


def test_save_note_with_commas_and_quotes(tmp_path):
    note = 'Said "I ran out of time," but work was strong.'
    students = Students(
        students=[Student(student_id="s001", note=note)],
        question_names=[],
    )
    out_path = tmp_path / "out.csv"
    students.save(out_path)
    loaded = Students.load(out_path)
    assert loaded.students[0].note == note


def test_sync_headers_no_students(scheme_path):
    from scholia.scheme import Scheme

    scheme = Scheme.load(scheme_path)
    students = Students(students=[], question_names=[])
    students.sync_headers(scheme.question_names())
    assert students.question_names == scheme.question_names()


# ---------------------------------------------------------------------------
# Encoding tests
# ---------------------------------------------------------------------------

# UTF-8 (plain and with Excel BOM)


def test_load_utf8_bom(tmp_path):
    path = tmp_path / "students.csv"
    path.write_bytes("student_id,q1\nÉlodie,a\nJoão,b\n".encode("utf-8-sig"))
    students = Students.load(path)
    assert students.students[0].student_id == "Élodie"
    assert students.students[1].student_id == "João"


@pytest.mark.parametrize(
    "names,label",
    [
        (
            ["Émile Zola", "Renée Dupont", "François Trémeau", "Héloïse Bernard"],
            "western european (french)",
        ),
        (
            ["José García", "Ángela López", "Martínez Pérez", "Núñez Rodríguez"],
            "western european (spanish)",
        ),
        (
            ["Müller Ångström", "Björn Eriksson", "Söderström Västra"],
            "western european (swedish/german)",
        ),
        (
            ["Władysław Reymont", "Józef Piłsudski", "Małgorzata Nowak"],
            "eastern european (polish)",
        ),
        (
            ["Αλέξανδρος Παπαδόπουλος", "Ελένη Κωνσταντίνου", "Νίκος Παπαδάκης"],
            "greek",
        ),
        (
            ["Мария Иванова", "Александр Петров", "Наталья Кузнецова"],
            "cyrillic",
        ),
        (
            ["محمد علي", "فاطمة الزهراء", "أحمد إبراهيم"],
            "arabic",
        ),
        (
            ["王小明", "李华", "张伟", "陈静"],
            "chinese",
        ),
        (
            ["田中太郎", "山田花子", "鈴木一郎"],
            "japanese",
        ),
        (
            ["Émile Zola", "Αλέξανδρος", "王小明", "محمد علي", "Мария"],
            "mixed scripts",
        ),
    ],
)
def test_load_utf8_scripts(tmp_path, names, label):
    path = tmp_path / "students.csv"
    path.write_bytes(_make_csv(names, "utf-8"))
    students = Students.load(path)
    assert [s.student_id for s in students.students] == names


# Legacy single-byte encodings (non-UTF-8 fallback via charset-normalizer)


def test_load_mac_roman(tmp_path):
    # The four names that triggered the original UnicodeDecodeError.
    # Mac Roman bytes: 0x83=É, 0x89=â, 0x8e=é, 0xd5=’ (right single quote).
    path = tmp_path / "students.csv"
    path.write_bytes(
        b"student_id,q1\n"
        b"Cathy O\xd5Neil,a\n"
        b"\x83milie du Ch\x89telet,b\n"
        b"\x83variste Galois,c\n"
        b"Henri Poincar\x8e,a\n"
    )
    students = Students.load(path)
    ids = [s.student_id for s in students.students]
    assert ids[0] == "Cathy O’Neil"
    assert ids[1] == "Émilie du Châtelet"
    assert ids[2] == "Évariste Galois"
    assert ids[3] == "Henri Poincaré"


def test_load_windows_1252(tmp_path):
    # Windows-1252 uses 0xA0-0xFF for Latin accented characters. We use only
    # characters whose byte values are identical in cp1252 and cp1250 (e.g.
    # é=0xE9, ü=0xFC, ç=0xE7) so the test is robust regardless of which of
    # those two near-identical encodings charset-normalizer selects.
    # Avoided: è (0xE8=č in cp1250), à (0xE0=ŕ), ø (0xF8=ř), ñ (0xF1=ń).
    names = [
        "José García",
        "François Dupont",
        "Cédric Moreau",
        "Müller Hans",
        "Björn Eriksson",
        "Ángela Martínez",
        "Renée Bélanger",
        "Véronique Blanc",
    ]
    path = tmp_path / "students.csv"
    path.write_bytes(_make_csv(names, "windows-1252"))
    students = Students.load(path)
    assert [s.student_id for s in students.students] == names


def test_load_fallback_when_detection_returns_none(tmp_path, monkeypatch):
    # Simulate charset-normalizer finding no best match: falls back to mac_roman.
    # Raw byte 0x83 = É in mac_roman.
    class _FakeResults:
        def best(self):
            return None

    monkeypatch.setattr("charset_normalizer.from_bytes", lambda _: _FakeResults())
    path = tmp_path / "students.csv"
    path.write_bytes(b"student_id,q1\n\x83milie,a\n")
    students = Students.load(path)
    assert students.students[0].student_id == "Émilie"


def test_load_fallback_when_detected_encoding_cannot_decode(tmp_path, monkeypatch):
    # Simulate charset-normalizer returning an encoding that cannot decode
    # the raw bytes (e.g. ascii for a file with non-ASCII bytes): falls back
    # to mac_roman. Raw byte 0x83 = É in mac_roman.
    class _FakeResult:
        encoding = "ascii"

    class _FakeResults:
        def best(self):
            return _FakeResult()

    monkeypatch.setattr("charset_normalizer.from_bytes", lambda _: _FakeResults())
    path = tmp_path / "students.csv"
    path.write_bytes(b"student_id,q1\n\x83milie,a\n")
    students = Students.load(path)
    assert students.students[0].student_id == "Émilie"
