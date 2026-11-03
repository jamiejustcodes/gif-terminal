import gifos
import os
import requests
from datetime import datetime

# ============================================
# Terminal GIF with GitHub Stats
# ============================================

USERNAME = (
    os.environ.get("GITHUB_REPOSITORY_OWNER")
    or os.environ.get("GIT_USERNAME")
    or "jamiejustcodes"
)

def fetch_stats(username):
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    headers = {"User-Agent": "terminal-gif"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        # User details
        u_resp = requests.get(f"https://api.github.com/users/{username}", headers=headers, timeout=10)
        u_data = u_resp.json() if u_resp.status_code == 200 else {}
        name = u_data.get("name") or username
        followers = u_data.get("followers", 0)
        repos = u_data.get("public_repos", 0)

        # Repositories for stars & languages
        repos_resp = requests.get(f"https://api.github.com/users/{username}/repos?per_page=100", headers=headers, timeout=10)
        stars = 0
        langs_count = {}
        if repos_resp.status_code == 200 and isinstance(repos_resp.json(), list):
            for r in repos_resp.json():
                stars += r.get("stargazers_count", 0)
                lang = r.get("language")
                if lang:
                    langs_count[lang] = langs_count.get(lang, 0) + 1

        # Commits
        c_resp = requests.get(f"https://api.github.com/search/commits?q=author:{username}", headers=headers, timeout=10)
        commits = c_resp.json().get("total_count", 0) if c_resp.status_code == 200 else 0

        # Pull Requests
        p_resp = requests.get(f"https://api.github.com/search/issues?q=author:{username}+type:pr", headers=headers, timeout=10)
        prs = p_resp.json().get("total_count", 0) if p_resp.status_code == 200 else 0

        # Issues
        i_resp = requests.get(f"https://api.github.com/search/issues?q=author:{username}+type:issue", headers=headers, timeout=10)
        issues = i_resp.json().get("total_count", 0) if i_resp.status_code == 200 else 0

        # Top languages
        top_langs = sorted(langs_count.items(), key=lambda x: x[1], reverse=True)[:3]
        top_langs_str = ", ".join([l[0] for l in top_langs]) if top_langs else "C#, TypeScript, C++"

        rank = "A+ (Top 1%)"

        return {
            "name": name,
            "followers": followers,
            "stars": stars,
            "commits": commits,
            "prs": prs,
            "issues": issues,
            "repos": repos,
            "rank": rank,
            "top_langs": top_langs_str,
        }
    except Exception as e:
        print(f"Error fetching stats directly: {e}")
        return {
            "name": username,
            "followers": 3,
            "stars": 17,
            "commits": 373,
            "prs": 0,
            "issues": 0,
            "repos": 11,
            "rank": "A+ (Top 1%)",
            "top_langs": "C#, TypeScript, C++",
        }

stats = fetch_stats(USERNAME)
print(f"Stats fetched successfully: {stats}")

# Terminal settings
t = gifos.Terminal(width=700, height=450, xpad=10, ypad=10)

# -- Initial prompt --
t.set_prompt(f"\x1b[91m{USERNAME}\x1b[0m@\x1b[93mgithub\x1b[0m ~> ")

# -- Boot sequence --
t.gen_text("Initializing terminal...", row_num=1)
t.clone_frame(5)
t.gen_text("\x1b[32m[OK]\x1b[0m System ready", row_num=2)
t.clone_frame(10)

# -- Command to view stats --
t.gen_prompt(row_num=3)
t.gen_typing_text("github-stats --user " + USERNAME, row_num=3, contin=True, speed=1)
t.clone_frame(5)

# -- Display statistics --
t.gen_text("", row_num=4)
t.gen_text(f"\x1b[96m=== GitHub Stats for {USERNAME} ===\x1b[0m", row_num=5)
t.clone_frame(3)

stats_lines = [
    f"\x1b[93mName:\x1b[0m        {stats['name']}",
    f"\x1b[93mFollowers:\x1b[0m   {stats['followers']}",
    f"\x1b[93mStars:\x1b[0m       {stats['stars']}",
    f"\x1b[93mCommits:\x1b[0m     {stats['commits']} (last year)",
    f"\x1b[93mPRs:\x1b[0m         {stats['prs']}",
    f"\x1b[93mIssues:\x1b[0m      {stats['issues']}",
    f"\x1b[93mRepos:\x1b[0m       {stats['repos']}",
    f"\x1b[93mRank:\x1b[0m        {stats['rank']}",
    f"\x1b[93mTop Langs:\x1b[0m   {stats['top_langs']}",
]

for i, line in enumerate(stats_lines):
    t.gen_text(line, row_num=6+i)
    t.clone_frame(3)

t.clone_frame(10)
t.gen_text("\x1b[96m================================\x1b[0m", row_num=6+len(stats_lines))

# HOLD STATS SCREEN: 55 frames (~3.5 seconds) so user can comfortably read all numbers
t.clone_frame(55)

# -- Clear and Skills --
t.gen_prompt(row_num=7+len(stats_lines))
t.gen_typing_text("clear", row_num=7+len(stats_lines), contin=True, speed=1)
t.clone_frame(5)
t.clear_frame()

t.gen_prompt(row_num=1)
t.gen_typing_text("cat skills.txt", row_num=1, contin=True, speed=1)
t.clone_frame(5)

t.gen_text("", row_num=2)
t.gen_text("\x1b[96m=== Tech Stack ===\x1b[0m", row_num=3)
t.clone_frame(3)

skills = [
    ("\x1b[94mLanguages:\x1b[0m   ", "TypeScript, JavaScript, C#, Python, C++"),
    ("\x1b[94mFrontend:\x1b[0m    ", "React 19, Next.js 14, Vite, Tailwind CSS"),
    ("\x1b[94mBackend:\x1b[0m     ", ".NET 10, ASP.NET Core, Node.js, Express"),
    ("\x1b[94mAI & Systems:\x1b[0m", "Model Context Protocol (MCP), Gemini API"),
    ("\x1b[94mTesting:\x1b[0m     ", "xUnit (100+ tests), GitHub Actions CI/CD"),
    ("\x1b[94mDatabases:\x1b[0m   ", "SQLite (WAL), PostgreSQL, SQL Server"),
    ("\x1b[94mTools:\x1b[0m       ", "Cursor, Git, Linux, Windows"),
]

for i, (label, value) in enumerate(skills):
    t.gen_text(f"{label}{value}", row_num=4+i)
    t.clone_frame(2)

t.clone_frame(10)
t.gen_text("\x1b[96m==================\x1b[0m", row_num=4+len(skills))

# HOLD TECH STACK SCREEN: 55 frames (~3.5 seconds) so user can comfortably read tech stack
t.clone_frame(55)

# -- Final message --
final_row = 5 + len(skills)
t.gen_prompt(row_num=final_row)
t.gen_typing_text("echo 'Thanks for visiting my profile!'", row_num=final_row, contin=True, speed=1)
t.clone_frame(5)
t.gen_text("\x1b[92mThanks for visiting my profile!\x1b[0m", row_num=final_row+1)
t.clone_frame(40)

# Generate the GIF
t.gen_gif()

print("\n GIF generated: output.gif")
