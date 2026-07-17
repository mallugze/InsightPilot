import pytest
import os
from app.services.ai.prompt_manager import PromptManager

def test_prompt_manager_loads_and_formats():
    manager = PromptManager()
    
    # 1. Test load template
    template = manager.load_template("executive_summary")
    assert "{business_pulse}" in template
    assert "{health_label}" in template

    # 2. Test format prompt
    formatted = manager.format_prompt(
        "executive_summary",
        business_pulse="93.3",
        health_label="READY",
        rows_count="100",
        cols_count="5",
        hero_metric="Revenue",
        zero_metric="Cost",
        context="Sample context detail"
    )
    assert "93.3" in formatted
    assert "READY" in formatted
    assert "Sample context detail" in formatted

def test_prompt_manager_not_found():
    manager = PromptManager()
    with pytest.raises(FileNotFoundError):
        manager.load_template("non_existent_prompt_template_name")
