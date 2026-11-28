import pathlib
s = pathlib.Path('c592.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("<div class=\"gg\">${Array.from({ length: 10 }, (_, i) => `<i class=\"${i < f ? 'on' : ''}\"></i>`).join('')}</div>",
    "<div class=\"gg\"><i style=\"width:${f * 10}%\"></i></div>")
rep("#outg .ug .gg{display:flex;gap:3px;margin-top:7px}#outg .ug .gg i{flex:1;height:9px;border-radius:3px;background:#11161e;border:1px solid #2a3442}#outg .ug .gg i.on{background:#7fe3ff;border-color:#7fe3ff;box-shadow:0 0 6px rgba(127,227,255,.6)}",
    "#outg .ug .gg{position:relative;height:10px;margin-top:8px;border-radius:5px;background:#11161e;border:1px solid #2a3442;overflow:hidden}#outg .ug .gg i{position:absolute;left:0;top:0;bottom:0;border-radius:5px;background:linear-gradient(90deg,#4fc3f7,#7fe3ff);box-shadow:0 0 8px rgba(127,227,255,.6);transition:width .15s}   /* c593: 칸 없는 게이지 */")
rep("#outg .ug.pop .gg i{background:#fff;border-color:#fff;box-shadow:0 0 10px #7fe3ff}", "#outg .ug.pop .gg i{background:#fff;box-shadow:0 0 12px #7fe3ff}")
pathlib.Path('c593_patch.py').write_text('C593_R = ' + repr(R) + '\n')
print(len(R))
