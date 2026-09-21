# Putting this project on GitHub

Two ways. Method 1 needs no tools at all. Method 2 is the "proper" developer way.

---

## Method 1 — Upload in the browser (no git, no terminal, ~5 minutes)

### 1. Create a GitHub account (skip if you have one)
Go to **https://github.com/signup**. You need an email, a username and a password.
Pick a username you're happy to show employers — it becomes your portfolio address,
for example `github.com/ngaruiya`.

### 2. Create the repository
Go to **https://github.com/new** and fill in:
- **Repository name:** `llm-answer-grader`
- **Description:** Give every AI answer a report card — see what is good, what is wrong, and how to fix it.
- Select **Public**
- **Do NOT tick "Add a README file"**, "Add .gitignore" or "Choose a license"
  (this project already includes all three — ticking them causes a conflict)

Click **Create repository**. You'll land on an empty repo page.

### 3. Unzip this folder
Unzip the file you downloaded so you can see the contents:
`README.md`, `LICENSE`, `Makefile`, `ROADMAP.md`, `grader/`, `tests/`, `data/`,
`docs/`, `.github/`, `.gitignore`

### 4. Upload the contents
On your new repository page:
1. Click **Add file** → **Upload files**
2. Open the unzipped folder, select **everything inside it** (not the folder itself)
3. Drag it all into the browser window

**Important:** the `.github` folder and `.gitignore` start with a dot, so some file
browsers hide them.
- **Windows:** in File Explorer → View → tick **Hidden items**
- **macOS:** press **Cmd + Shift + .** to reveal hidden files

If you can't get them, upload everything else — the site still works; you'd just lose the
CI badge and the ignore rules. You can add them later with **Add file → Create new file**.

### 5. Commit
Scroll to the bottom, leave the message as *"Add files via upload"*, click **Commit changes**.

### Done
Your project is live at `https://github.com/<your-username>/llm-answer-grader`

Optional polish:
- Click the **star** on your own repo (it looks good)
- Go to your profile → **Customize your pins** → pin `llm-answer-grader`
- Add **topics** on the repo page: `python`, `llm`, `evaluation`, `testing`, `ai`

---

## Method 2 — Push with git (if you have a computer with git installed)

Open a terminal in the unzipped folder and run:

```bash
git init
git add -A
git commit -m "llm-answer-grader v0.1.0 — grades AI answers and explains every problem it finds"
git branch -M main
git remote add origin https://github.com/<YOUR-USERNAME>/llm-answer-grader.git
git push -u origin main
```

When it asks for a password, GitHub no longer accepts your account password — you need a
**personal access token** instead:

1. Go to **https://github.com/settings/tokens?type=beta**
2. **Generate new token** → name it `upload` → expiration 7 days
3. **Repository access:** Only select repositories → `llm-answer-grader`
4. **Permissions** → Repository permissions → **Contents: Read and write**
5. Generate, copy the token (starts with `github_pat_`), and paste it when git asks for
   the password
6. **Delete the token** afterwards on the same page

---

## After the upload — check these three things

1. **The README renders** on the repo home page with the screenshot visible
2. **The file list shows** `grader/`, `tests/`, `data/` as folders
3. **CI is green** — click the **Actions** tab. If `.github/workflows/ci.yml` uploaded,
   you'll see a workflow run; it tests the code and grades the sample answers on every push.

If Actions shows a red X, don't panic: open the run, read the failing step, and the fix is
almost always a missing dot-file (`ci.yml` not uploaded).

---

## Tell me when it's live

Send me the URL and I will:
- update your CV and LinkedIn to point at it
- write the profile README (the special repo named after your username) that links to it
- start v0.2 (configurable TOML rubrics) as your next visible commit
