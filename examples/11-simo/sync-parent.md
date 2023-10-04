# Notes for merges

## merge after v3

### Sync at local client
```
github\section-properties> git remote add parent https://github.com/robbievanleeuwen/section-properties
github\section-properties> git pull parent master
CONFLICT (modify/delete): sectionproperties/analysis/section.py deleted in 2ea83cdd5394450fd51fed22321c8ea94550d258 and modified in HEAD.
Version HEAD of sectionproperties/analysis/section.py left in tree.
Automatic merge failed; fix conflicts and then commit the result.
github\section-properties\sectionproperties\analysis> git status
Unmerged paths:
  (use "git add/rm <file>..." as appropriate to mark resolution)
        deleted by them: section.py
section-properties\sectionproperties\analysis> git rm section.py
section-properties\sectionproperties\analysis> git commit -m"merge from parent"
section-properties\sectionproperties\analysis> git push
```
### Disable workflow runs
