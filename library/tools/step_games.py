"""Per-game switch for the tag-fix steps (final comparison: a game that a step makes worse is left out of it)."""
def step_games(step):
    """Games a step may change (tools/step_games.json, written by the final comparison; missing = all games)."""
    import json as _j, os as _o
    f = _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), 'step_games.json')
    if _o.environ.get('TB_STEP_GAMES'): f = _o.environ['TB_STEP_GAMES']
    if not _o.path.exists(f): return None
    return set(_j.load(open(f)).get(step, [])) if step in _j.load(open(f)) else None
