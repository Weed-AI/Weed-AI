import pytest
from weedcoco.utils import lookup_growth_stage_name


@pytest.mark.parametrize("idx,scheme,expected", [
    [10, "fine", "First leaf through coleoptile"],
    [13, "fine", "3 leaves unfolded"],
    [19, "fine", "9 or more leaves unfolded"],
    [20, "fine", "No tillers"],
    [10, "grain_ranges", "Seedling"],
    [13, "grain_ranges", "Seedling"],
    [19, "grain_ranges", "Seedling"],
    [20, "grain_ranges", "Tillering"],
    [10, "bbch_ranges", "Leaf development"],
    [13, "bbch_ranges", "Leaf development"],
    [19, "bbch_ranges", "Leaf development"],
    [20, "bbch_ranges", "Formation of side shoots, tillering"],
])
def test_lookup_growth_stage_name(idx, scheme, expected):
    assert expected == lookup_growth_stage_name(idx=idx, scheme=scheme)


@pytest.mark.parametrize("idx,scheme", [
    [10, "grains"],
    [100, "grain_ranges"],
    ["10", "grain_ranges"],
    ["10", "bbch_ranges"],
    ["10", "fine"],
])
def test_lookup_growth_stage_name_invalid(idx, scheme):
    with pytest.raises(Exception):
        assert lookup_growth_stage_name(idx=idx, scheme=scheme)
