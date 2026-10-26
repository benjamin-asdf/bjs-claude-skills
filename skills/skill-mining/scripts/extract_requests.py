#!/usr/bin/env python3
"""Extract the user's own messages and the skills used from the last N Claude Code sessions.

Usage: extract_requests.py [N=100] [OUT=requests.txt] [--skip <session-id-substring>]

Writes one block per session:
  === <project>/<session>.jsonl <date> skills=[...]
  -- <user message, truncated>
and prints skill / slash-command / tool counts plus sessions per project.
Harness noise (task notifications, compaction summaries, system reminders, interrupts) is dropped.
"""
import collections, datetime, glob, json, os, re, sys

args = [a for a in sys.argv[1:]]
skip = None
if '--skip' in args:
    i = args.index('--skip'); skip = args[i + 1]; del args[i:i + 2]
N = int(args[0]) if args else 100
OUT = args[1] if len(args) > 1 else 'requests.txt'
MAXLEN = 350

NOISE = ('<task-notification', '<system-reminder', 'This session is being continued',
         'Caveat:', '[Request interrupted')

files = glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl'))
files.sort(key=os.path.getmtime, reverse=True)

skills, cmds, tools = collections.Counter(), collections.Counter(), collections.Counter()
sessions = []
for f in files:
    if skip and skip in f:
        continue
    msgs, used = [], []
    try:
        lines = open(f).read().splitlines()
    except OSError:
        continue
    for line in lines:
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get('isMeta') or d.get('isSidechain'):
            continue
        m = d.get('message') or {}
        if d.get('type') == 'user' and m.get('role') == 'user':
            c = m.get('content')
            if isinstance(c, list):
                c = ' '.join(x.get('text', '') for x in c
                             if isinstance(x, dict) and x.get('type') == 'text')
            if not isinstance(c, str) or not c.strip():
                continue
            for cm in re.findall(r'<command-name>/?([^<]+)</command-name>', c):
                cmds[cm] += 1; used.append('/' + cm)
            if c.startswith('<') and ('command-' in c or 'local-command' in c):
                a = re.search(r'<command-args>(.*?)</command-args>', c, re.S)
                if a and a.group(1).strip():
                    msgs.append('[cmd args] ' + a.group(1).strip()[:MAXLEN])
                continue
            if c.lstrip().startswith(NOISE):
                continue
            msgs.append(c.strip()[:MAXLEN])
        elif d.get('type') == 'assistant':
            for x in m.get('content') or []:
                if isinstance(x, dict) and x.get('type') == 'tool_use':
                    tools[x['name']] += 1
                    if x['name'] == 'Skill':
                        s = x['input'].get('skill'); skills[s] += 1; used.append(s)
    if msgs:
        sessions.append((f.split('projects/')[1], os.path.getmtime(f), used, msgs))
    if len(sessions) >= N:
        break

with open(OUT, 'w') as w:
    for name, mtime, used, msgs in sessions:
        w.write(f"\n=== {name} {datetime.date.fromtimestamp(mtime)} skills={used}\n")
        for mm in msgs:
            w.write(f"-- {mm}\n")

print(f"{len(sessions)} sessions, oldest {datetime.date.fromtimestamp(sessions[-1][1])} -> {OUT}")
print('SKILLS', skills.most_common())
print('SLASH ', cmds.most_common())
print('TOOLS ', tools.most_common(20))
print('PROJECTS', collections.Counter(s[0].split('/')[0] for s in sessions).most_common())
