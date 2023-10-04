# Notes for merges

## merge after v3

### Sync at local client
```
github\section-properties> git remote add parent https://github.com/robbievanleeuwen/section-properties
github\section-properties> git pull parent master
CONFLICT (modify/delete): sectionproperties/analysis/section.py deleted in
  2ea83cdd5394450fd51fed22321c8ea94550d258 and modified in HEAD.
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
https://github.com/simo-11/section-properties/settings/actions

### uninstall sectionproperties 2.1.5 and switch python from 3.10.11 to 3.11.6 (default)
```
> pip -v uninstall sectionproperties
..
Removing file or directory c:\users\simon\.pyenv\pyenv-win\versions\3.10.11\lib\site-packages\sectionproperties\
  Successfully uninstalled sectionproperties-2.1.5
github\section-properties> pyenv local --unset
```
Switch python in spyder (Tools/Preferences/Python) and install spyder-kernels pygltflib and sectionproperties
```
github\section-properties> pip install spyder-kernels==2.4.* pygltflib sectionproperties
```

