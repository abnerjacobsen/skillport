
from skillhub_mcp.skill_manager import origin as origin_mod


def test_record_and_remove_origin(tmp_path, monkeypatch):
    monkeypatch.setattr(origin_mod, "ORIGIN_PATH", tmp_path / "origins.json")

    origin_mod.record_origin("abc", {"source": "local"})
    assert origin_mod.ORIGIN_PATH.exists()

    data = origin_mod.ORIGIN_PATH.read_text(encoding="utf-8")
    assert "abc" in data

    origin_mod.remove_origin("abc")
    assert origin_mod.ORIGIN_PATH.read_text(encoding="utf-8") == "{}"
