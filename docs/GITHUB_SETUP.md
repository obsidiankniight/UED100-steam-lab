# Publish real UED100 development history to GitHub

The project contains an actual local Git commit history. A repository URL **does not exist yet**. Do not submit `https://github.com/USERNAME/REPO` as if it were real.

The history is distributed as `docs/ued100_complete_history.bundle`. On Windows, install Git for Windows first. These commands use a terminal/PowerShell in the extracted **UED100_Steam_Prototype** folder.

## 1. Recover the full history

```powershell
git clone docs/ued100_complete_history.bundle UED100-SteamLab-GitHub
cd UED100-SteamLab-GitHub
git log --oneline -10
git branch -M main
```

This creates a working Git repository from the archived commits rather than pretending a ZIP download contains `.git` history.

## 2. Publish on GitHub

1. Create a **new empty GitHub repository** named `ued100-steam-lab` (omit the optional auto-generated README/license/gitignore; this project already contains these).
2. Copy the real HTTPS repository URL from GitHub (it should belong to **your account**).
3. In the recovered repository, run:

```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_ACCOUNT/ued100-steam-lab.git
git push -u origin main
```

Replace the sample HTTPS URL with the actual URL GitHub gave you. GitHub may require browser authentication or a credential manager. Do not provide passwords or personal tokens in ChatGPT. Verify the files and commit messages are visible on the live repository and copy the **real** link into your UED100 submission.

## 3. Continue honest development

Make future changes inside the cloned repository, then commit with descriptive messages:

```powershell
git add .
git commit -m "Improve browsing after participant feedback"
git push
```

Only use a message like that if a participant actually gave feedback. Add actual usability and cross-browser results, then document the changes made because of them. Publish a further commit after testing and keep any screenshots free of sensitive data.

**Note:** the original source ZIP is sufficient to run the prototype, but the bundle is supplied to preserve development evidence. This is a student UX concept, not an official Steam product.
