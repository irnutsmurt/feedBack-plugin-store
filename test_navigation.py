from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_catalog_exposes_installed_plugin_navigation_metadata():
    src = (ROOT / "storelib.py").read_text(encoding="utf-8")
    assert '"has_settings": False' in src
    assert '"has_screen": False' in src
    assert '"nav_screen": None' in src
    assert 'settings.get("html")' in src
    assert 'nav.get("screen")' in src


def test_frontend_uses_native_feedback_navigation():
    src = (ROOT / "screen.js").read_text(encoding="utf-8")
    assert 'window.showScreen("settings")' in src
    assert '"#plugin-settings details[data-plugin-id]"' in src
    assert 'window.showScreen(screenId)' in src
    assert '"Settings"' in src
    assert '"Open Plugin"' in src


def test_installed_card_prefers_settings_when_clicked():
    src = (ROOT / "screen.js").read_text(encoding="utf-8")
    assert "function openInstalledPlugin(plugin)" in src
    settings_pos = src.index("if (plugin.has_settings)", src.index("function openInstalledPlugin"))
    screen_pos = src.index("else if (plugin.has_screen)", settings_pos)
    assert settings_pos < screen_pos




def test_open_plugin_tries_host_screen_id_before_nav_screen():
    # The host mounts plugin screens as `plugin-<id>`; nav.screen values such
    # as "practice" are not element ids, so they must not be tried first.
    src = (ROOT / "screen.js").read_text(encoding="utf-8")
    body = src[src.index("function openPluginScreen(plugin)"):src.index("function openInstalledPlugin")]
    host_pos = body.index("`plugin-${plugin.id}`")
    nav_pos = body.index("plugin.nav_screen")
    assert host_pos < nav_pos
    assert "plugin.nav_screen || `plugin-${plugin.id}`" not in body
