
from skillhub_mcp.skill_manager.add import detect_skills, add_local


def test_add_local_custom_namespace(tmp_path):
    source = tmp_path / "collection"
    (source / "skill-a").mkdir(parents=True)
    (source / "skill-a" / "SKILL.md").write_text(
        "---\nname: skill-a\ndescription: A\n---\nbody", encoding="utf-8"
    )
    (source / "skill-b").mkdir(parents=True)
    (source / "skill-b" / "SKILL.md").write_text(
        "---\nname: skill-b\ndescription: B\n---\nbody", encoding="utf-8"
    )

    skills = detect_skills(source)
    target = tmp_path / "dest"

    results = add_local(
        source_path=source,
        skills=skills,
        target_dir=target,
        keep_structure=True,
        namespace_override="customns",
        force=False,
    )

    added_ids = [r.skill_id for r in results if r.success]
    assert set(added_ids) == {"customns/skill-a", "customns/skill-b"}
    assert (target / "customns" / "skill-a" / "SKILL.md").exists()
