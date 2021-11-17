# DCP-o-matic remote Server Encoding
This Python app helps you to easily send and process media files and DCP-O-Matic projects, assign an encoding job, queue the jobs and finally download encoded DCPs.

## Structure of the program
```bash
/
├── usr
│   ├── sbin  # main script
│   │   └── dcp-remote
│   └── bin   # scripts which program uses (without root)
│       └── dcp-remote
│   └── lib   # scripts which program uses (need root)
│       └── dcp-remote
├── etc
│   ├── pam.d # pam file used for vsftpd authentication
│   └── ufw   # custom rules for ufw
│       └── applications.d
```
Graph shows only basic structure without end files.

---
Made real by Jozef Sabo
