import pathlib
s = pathlib.Path('c603.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("  function chSave() { try { localStorage.setItem('rd_save_v1', JSON.stringify(CH_SV)); } catch (e) {} }",
    """  function chSave() { try { localStorage.setItem('rd_save_v1', JSON.stringify(CH_SV)); } catch (e) {} }
  {   // c604: 홈 화면 앱을 다시 열었을 때 — 새 버전이 올라가 있으면 아웃게임 화면에서만 새로고침 (판 중에는 안 바뀐다)
    const CH_BUILD = (((document.getElementById('ver') || {}).textContent || '').match(/c\\d+/) || [''])[0];
    const chVerCheck = () => { if (document.visibilityState !== 'visible' || !CH_BUILD || !document.getElementById('outg')) return;
      fetch('version.txt?t=' + Date.now(), { cache: 'no-store' }).then((r) => (r.ok ? r.text() : '')).then((t) => { t = (t || '').trim(); if (!/^c\\d+$/.test(t) || t === CH_BUILD || !document.getElementById('outg')) return; let tried = ''; try { tried = sessionStorage.getItem('rd_vr') || ''; } catch (e) {} if (tried === t) return; try { sessionStorage.setItem('rd_vr', t); } catch (e) {} location.reload();   /* 같은 새 버전으로는 한 번만 (어긋나도 계속 새로고침하지 않게) */ }).catch(() => {}); };
    document.addEventListener('visibilitychange', chVerCheck); window.addEventListener('pageshow', chVerCheck);
  }""")
pathlib.Path('c604_patch.py').write_text('C604_R = ' + repr(R) + '\n')
print(len(R))
