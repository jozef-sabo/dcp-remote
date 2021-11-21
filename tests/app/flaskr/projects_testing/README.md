# Projects testing folder
In this folder there are some DCP-o-matic projects to properly test the code. 
The whole code and belonging tests depend on hypothesis, that every DCP-o-matic project must have the "___metadata.xml___"
folder (proven to be right [here](https://git.carlh.net/gitweb/?p=dcpomatic.git;a=blob_plain;f=doc/manual/diagrams/file-structure.svg;hb=HEAD)).
Each of the projects (except two) in this folder has at least one mistake in it in order to  Python code throws an error.  

## Mistakes in projects
### Project A
```
Everything right, original copy of an existing project.
```

### Project B
```
Everything right, shorter version of an existing project.
```
### Project C
```
Everything right, but subtitle language not included.
10: - <SubtitleLanguage>CZ</SubtitleLanguage>
```
### Project D
```
Everything right, 2 content tags removed.
17-34: - <Content>
43-61: - <Content>
```
### Project E
```
Removed obligatory line
21: - <VideoWidth>1920</VideoWidth>
```
### Project F
```
Changed type of value
21: <VideoWidth>1920</VideoWidth> --> <VideoWidth>Null</VideoWidth>
```
