# DCP-o-matic remote server encoding
[![Tests](https://github.com/jozef-sabo/dcp-remote/actions/workflows/main.yml/badge.svg)](https://github.com/jozef-sabo/dcp-remote/actions/workflows/main.yml)  
This Python app helps you to easily send and process media files and DCP-O-Matic projects, assign an encoding job, queue the jobs and finally download encoded DCPs.

## Structure of the program
```bash
/
├── usr
│   ├── sbin  # main script
│   │   └── dcp-remote
│   └── bin   # scripts which program uses (without root)
│       └── dcp-remote
│           └── python scripts
│   └── lib   # scripts which program uses (need root)
│       └── dcp-remote
├── etc
│   ├── pam.d # pam file used for vsftpd authentication
│   └── ufw   # custom rules for ufw
│       └── applications.d
```
Graph shows only basic structure without end files.  
  
Actual version of application can show and differentiate files, folders and projects in browser. Also, it can show raw info about project and start encoding project without further control. It's the first working version. However, cannot be built for any OS yet (only usable manually).

---
Made real by Jozef Sabo
