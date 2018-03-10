# :construction: unbox 

:gift: *Unpack and Decompile the $h*! out of things*


**Unbox** is a convenient one-click unpack and decompiler tool that wraps existing 3rd party applications like *IDA Pro,
JD-Cli, Dex2Src*, and others to provide a convenient archiver liker command line interfaces to unpack and decompile
various types of files. It currently features support for compiled binaries (*.net, PE, elf, mach, ...*), *java classes,
android application packages* and various types of archives or browser extensions. The goal of this tool is mainly to
take off the extra efford needed to deal with the various decompiler tools and give a standard yet easy to use
interface.

Requires: :snake: python-2

*Dependencies:*

* cigma - https://github.com/7h3rAm/cigma
* patool - https://pypi.python.org/pypi/patool  

# Usage :sheep:

      example: unbox.py <command> [options] <target> [<target>, ...]
      options:
	       -y, --yes    ...   answer prompts with yes
	       -n, --no     ...   answer prompts with no

      command  ... list <target>
	       ... extract <target> <destination path>

	       ... check-dependencies

      target   ... file
      
  
*One interface to rule them all...*
  
| usage | command |
|-------|---------|
| unpack and decompile all ***.jar** files | `#> unbox/cli.py extract \lib\Adv*.jar c:\_tmp\decompiled` |
| decompile a **Windows DDL** | `#> unbox/cli.py extract samples\7-zip32.dll c:\_tmp\decompiled` | 
| decompile an **elf executable** | `#> unbox/cli.py extract samples\crackme1 /tmp/decompiled` | 
| unpack and decompile an **apk** | `#> unbox/cli.py extract test.apk c:\_tmp\decompiled` |
| decompile a **.net** application | `#> unbox/cli.py extract test.exe c:\_tmp\decompiled` | 
| unpack a **browser extension** | `#> unbox/cli.py extract sample.crx c:\_tmp\decompiled` | 
| unpack **anything** | `#> unbox/cli.py extract * c:\_tmp\decompiled` |
	
*I think you got the idea now. It does not matter what you want to decompile or unpack, its the same call...*

# Configuration

* in case a 3rd party tools is not generally available via *PATH* configure it in `unbox.json`

search-path for `unbox.json` is 

* current working dir OR
* `~/unbox.json` OR
* `~/.unbox/unbox.json`


# Setup

* install
* check dependencies `python cli.py check-dependencies`  
  * install missing 3rd party applications (see table below)
  * make them available in PATH or configure them in unbox.json
  
  
# As a Library

```python

from unbox import UnboxPath

target = "path/to/target/file"

dst = UnboxPath(target)		# crate an unbox path instance
for p in dst.files.walk():	# auto-decompile/unpack and walk resulting files (source-code, etc..)
	print p.path		# print the unpacked files' path
```

# Live Action

### List contents of windows DLL

```
#> unbox/cli.py list "samples\7-zip32.dll"
[handler.base/2808][DEBUG     ] [base.get_path      ] unknown: 7-zip32.dll
[handler.base/2808][DEBUG     ] [base.get_path      ] {'source': 'databuffer', 'magic': {'mimetype': 'application/x-executable-mz', 'patterns': [{'regex': '\\x4D\\x5A', 'offset': 0, 'size': 2}], 'shortname': 'EXE', 'id': 31, 'longname': 'Windows Executable'}}
[handler.base/2808][DEBUG     ] [base.get_path      ] 2
[handler.commands.commands/2808][DEBUG     ] [commands.decompile     ] [u'ida\\idaw.exe', '-B', '-M', '-S"home\\.unbox\\ida_batch_decompile.py -o\\"tmpfolder\\unbox3fcvpg\\7-zip32.c\\""', '"7-zip32.dll"']
[handler.base/2808][DEBUG     ] [base.get_path      ] scheme: c
[handler.base/2808][DEBUG     ] [base.get_path      ] <Application32Bits encoding=None path=WindowsPath('tmpfolder/unbox3fcvpg')>
[handler.local/2808][DEBUG     ] [local.walk          ] walk: tmpfolder

[handler.base/2808][DEBUG     ] [base.get_path      ] unknown: tmpfolder\7-zip32.c
[handler.base/2808][DEBUG     ] [base.get_path      ] {'source': 'databuffer', 'magic': None}
[handler.base/2808][DEBUG     ] [base.get_path      ] scheme: c
[handler.base/2808][DEBUG     ] [base.get_path      ] <LocalPath encoding=None path=WindowsPath('tmpfolder/unbox3fcvpg/7-zip32.c')>
tmpfolder/unbox3fcvpg/7-zip32.c

```

### Decompile a windows DLL

```
#> unbox/cli.py extract "samples\7-zip32.dll"
[handler.base/9848][DEBUG     ] [base.get_path      ] unknown: 7-zip32.dll
[handler.base/9848][DEBUG     ] [base.get_path      ] {'source': 'databuffer', 'magic': {'mimetype': 'application/x-executable-mz', 'patterns': [{'regex': '\\x4D\\x5A', 'offset': 0, 'size': 2}], 'shortname': 'EXE', 'id': 31, 'longname': 'Windows Executable'}}
[handler.base/9848][DEBUG     ] [base.get_path      ] 2
[handler.commands.commands/9848][DEBUG     ] [commands.decompile     ] [u'ida\\idaw.exe', '-B', '-M', '-S"home\\.unbox\\ida_batch_decompile.py -o\\"tmpfolder\\unboxdaj2bd\\7-zip32.c\\""', '"7-zip32.dll"']
[handler.base/9848][DEBUG     ] [base.get_path      ] scheme: c
[handler.base/9848][DEBUG     ] [base.get_path      ] <Application32Bits encoding=None path=WindowsPath('tmpfolder/unboxdaj2bd')>
[handler.local/9848][DEBUG     ] [local.walk          ] walk: tmpfolder\unboxdaj2bd

[handler.base/9848][DEBUG     ] [base.get_path      ] unknown: tmpfolder\unboxdaj2bd\7-zip32.c
[handler.base/9848][DEBUG     ] [base.get_path      ] {'source': 'databuffer', 'magic': None}
[handler.base/9848][DEBUG     ] [base.get_path      ] scheme: c
[handler.base/9848][DEBUG     ] [base.get_path      ] <LocalPath encoding=None path=WindowsPath('tmpfolder/unboxdaj2bd/7-zip32.c')>
tmpfolder\unboxdaj2bd\7-zip32.c
```

### Unpack and decompile apk

(java) while decompiling binary applications on the fly (see ida output below)

```
#> unbox/cli.py extract test.apk
[handler.decompilable/13668][DEBUG     ] [decompilable._fetch        ] destination: test.apk.jar
[handler.utils.shell/13668][DEBUG     ] [shell.execute       ] [u'dex-tools-2.0\\dex2jar-2.0\\d2j-dex2jar.bat', '-o', 'tmpfolder\\unboxsmansz\\test.apk.jar', 'test.apk']
dex2jar test.apk -> tmpfolder\unboxsmansz\test.apk.jar
[handler.decompilable/13668][DEBUG     ] [decompilable._fetch        ] unpack .apk to tmpfolder\unboxsmansz\.apk
[handler.decompilable/13668][DEBUG     ] [decompilable._fetch        ] decompile .jar to tmpfolder\unboxsmansz\.source
[handler.utils.shell/13668][DEBUG     ] [shell.execute       ] [u'jd-cli\\jd-cli.bat', '--outputDir', 'tmpfolder\\unboxsmansz\\.source', 'test.apk.jar']
21:05:30.434 INFO  jd.cli.Main - Decompiling tmpfolder\unboxsmansz\test.apk.jar
21:05:30.467 INFO  jd.core.output.DirOutput - Directory output will be initialized for path tmpfolder\unboxsmansz\.source
21:05:30.787 WARN  jd.core.output.DirOutput - Class name or java source is null
ReferenceMap.add: InvalidParameterException(android/util/SparseArray<Landroid/support/v4/app/Fragment;>)
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ReferenceMap.add: InvalidParameterException(java/util/Map<Ljava/lang/String;Ljava/lang/String;>)
ReferenceMap.add: InvalidParameterException(java/util/Map<Ljava/lang/String;Ljava/lang/String;>)
Undefined type catch
Undefined type catch
Undefined type catch
Undefined type catch
Undefined type catch
Undefined type catch
Undefined type catch
Undefined type catch
java.lang.Throwable: NameGenerator.generateParameterNameFromSignature: invalid signature 'TT;'
	at jd.core.process.analyzer.variable.DefaultVariableNameGenerator.generateLocalVariableNameFromSignature(DefaultVariableNameGenerator.java:106)
	at jd.core.process.analyzer.classfile.LocalVariableAnalyzer.GenerateLocalVariableNames(LocalVariableAnalyzer.java:1733)
	at jd.core.process.analyzer.classfile.LocalVariableAnalyzer.Analyze(LocalVariableAnalyzer.java:206)
	at jd.core.process.analyzer.classfile.ClassFileAnalyzer.PreAnalyzeMethods(ClassFileAnalyzer.java:698)
	at jd.core.process.analyzer.classfile.ClassFileAnalyzer.AnalyzeClass(ClassFileAnalyzer.java:126)
	at jd.core.process.analyzer.classfile.ClassFileAnalyzer.Analyze(ClassFileAnalyzer.java:84)
	at jd.commonide.IdeDecompiler.decompile(IdeDecompiler.java:49)
	at jd.core.JavaDecompiler.decompile(JavaDecompiler.java:121)
	at jd.core.JavaDecompiler.decompileClass(JavaDecompiler.java:58)
	at jd.core.input.ZipFileInput.decompile(ZipFileInput.java:87)
	at jd.cli.Main.main(Main.java:118)
21:05:56.837 WARN  jd.core.output.DirOutput - Class name or java source is null
21:05:56.848 WARN  jd.core.output.DirOutput - Class name or java source is null
21:05:57.270 WARN  jd.core.output.DirOutput - Class name or java source is null
21:05:57.293 WARN  jd.core.output.DirOutput - Class name or java source is null
21:05:57.441 WARN  jd.core.output.DirOutput - Class name or java source is null
21:05:57.445 WARN  jd.core.output.DirOutput - Class name or java source is null
21:05:57.501 WARN  jd.core.output.DirOutput - Class name or java source is null
21:05:57.502 WARN  jd.core.output.DirOutput - Class name or java source is null
21:05:57.506 WARN  jd.core.output.DirOutput - Class name or java source is null
21:05:57.507 WARN  jd.core.output.DirOutput - Class name or java source is null
21:05:57.510 WARN  jd.core.output.DirOutput - Class name or java source is null
21:05:57.522 WARN  jd.core.output.DirOutput - Class name or java source is null
21:05:57.527 WARN  jd.core.output.DirOutput - Class name or java source is null
21:05:57.543 WARN  jd.core.output.DirOutput - Class name or java source is null
21:05:57.547 WARN  jd.core.output.DirOutput - Class name or java source is null
21:05:58.220 WARN  jd.core.output.DirOutput - Class name or java source is null
21:05:58.414 WARN  jd.core.output.DirOutput - Class name or java source is null
Undefined type catch
Undefined type catch
Undefined type catch
Undefined type catch
ReferenceMap.add: InvalidParameterException(java/util/Map<Ljava/lang/String;Ljava/lang/String;>)
21:06:04.651 WARN  jd.core.output.DirOutput - Class name or java source is null
ReferenceMap.add: InvalidParameterException(java/util/Map<Ljava/lang/String;Ljava/lang/String;>)
ReferenceMap.add: InvalidParameterException(java/util/Map<Ljava/lang/String;Ljava/lang/String;>)
ReferenceMap.add: InvalidParameterException(java/util/Map<Ljava/lang/String;Ljava/lang/String;>)
ReferenceMap.add: InvalidParameterException(java/util/Map<Ljava/lang/String;Ljava/lang/String;>)
ReferenceMap.add: InvalidParameterException(java/util/Map<Ljava/lang/String;Ljava/lang/String;>)
ReferenceMap.add: InvalidParameterException(java/util/Map<Ljava/lang/String;Ljava/lang/String;>)
Undefined type catch
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ReferenceMap.add: InvalidParameterException(java/util/Map<Ljava/lang/String;Ljava/lang/String;>)
ReferenceMap.add: InvalidParameterException(java/util/ArrayList<Ljava/lang/String;>)
21:06:11.038 WARN  jd.core.output.DirOutput - Class name or java source is null
java.lang.Throwable: NameGenerator.generateParameterNameFromSignature: invalid signature 'TT;'
	at jd.core.process.analyzer.variable.DefaultVariableNameGenerator.generateLocalVariableNameFromSignature(DefaultVariableNameGenerator.java:106)
	at jd.core.process.analyzer.classfile.LocalVariableAnalyzer.GenerateLocalVariableNames(LocalVariableAnalyzer.java:1733)
	at jd.core.process.analyzer.classfile.LocalVariableAnalyzer.Analyze(LocalVariableAnalyzer.java:206)
	at jd.core.process.analyzer.classfile.ClassFileAnalyzer.PreAnalyzeMethods(ClassFileAnalyzer.java:698)
	at jd.core.process.analyzer.classfile.ClassFileAnalyzer.AnalyzeClass(ClassFileAnalyzer.java:126)
	at jd.core.process.analyzer.classfile.ClassFileAnalyzer.Analyze(ClassFileAnalyzer.java:84)
	at jd.commonide.IdeDecompiler.decompile(IdeDecompiler.java:49)
	at jd.core.JavaDecompiler.decompile(JavaDecompiler.java:121)
	at jd.core.JavaDecompiler.decompileClass(JavaDecompiler.java:58)
	at jd.core.input.ZipFileInput.decompile(ZipFileInput.java:87)
	at jd.cli.Main.main(Main.java:118)
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
Undefined type catch
Undefined type catch
Undefined type catch
Undefined type catch
Undefined type catch
Undefined type catch
Undefined type catch
Undefined type catch
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
ConstantPool.addConstantClass: invalid name index
21:06:19.486 INFO  jd.core.output.DirOutput - Finished with 2593 class file(s) and 0 resource file(s) written.
[handler.decompilable/13668][DEBUG     ] [decompilable._fetch        ] remove .jar - we do not need it anymore
[handler.base/13668][DEBUG     ] [base.get_path      ] scheme: c
[handler.base/13668][DEBUG     ] [base.get_path      ] <Apk encoding=None path=WindowsPath('tmpfolder/unboxsmansz')>
[handler.local/13668][DEBUG     ] [local.walk          ] walk: tmpfolder\unboxsmansz
21:06:19.486 INFO  jd.core.output.DirOutput - Finished with 2593 class file(s) and 0 resource file(s) written.
[handler.decompilable/13668][DEBUG     ] [decompilable._fetch        ] remove .jar - we do not need it anymore
[handler.base/13668][DEBUG     ] [base.get_path      ] scheme: c
[handler.base/13668][DEBUG     ] [base.get_path      ] <Apk encoding=None path=WindowsPath('tmpfolder/unboxsmansz')>
[handler.local/13668][DEBUG     ] [local.walk          ] walk: tmpfolder\unboxsmansz

[handler.base/13668][DEBUG     ] [base.get_path      ] unknown: tmpfolder\unboxsmansz\.apk\AndroidManifest.xml
tmpfolder\unboxsmansz\.apk\AndroidManifest.xml
[handler.base/13668][DEBUG     ] [base.get_path      ] {'source': 'databuffer', 'magic': None}
[handler.base/13668][DEBUG     ] [base.get_path      ] scheme: c
[handler.base/13668][DEBUG     ] [base.get_path      ] <LocalPath encoding=None path=WindowsPath('tmpfolder/unboxsmansz/.apk/AndroidManifest.xml')>
[handler.base/13668][DEBUG     ] [base.get_path      ] unknown: tmpfolder\unboxsmansz\.apk\classes.dex
[handler.base/13668][DEBUG     ] [base.get_path      ] {'source': 'databuffer', 'magic': None}
tmpfolder\unboxsmansz\.apk\classes.dex
[handler.base/13668][DEBUG     ] [base.get_path      ] scheme: c
[handler.base/13668][DEBUG     ] [base.get_path      ] <LocalPath encoding=None path=WindowsPath('tmpfolder/unboxsmansz/.apk/classes.dex')>
[handler.base/13668][DEBUG     ] [base.get_path      ] unknown: tmpfolder\unboxsmansz\.apk\resources.arsc
[handler.base/13668][DEBUG     ] [base.get_path      ] {'source': 'databuffer', 'magic': None}
tmpfolder\unboxsmansz\.apk\resources.arsc
[handler.base/13668][DEBUG     ] [base.get_path      ] scheme: c
[handler.base/13668][DEBUG     ] [base.get_path      ] <LocalPath encoding=None path=WindowsPath('tmpfolder/unboxsmansz/.apk/resources.arsc')>
[handler.base/13668][DEBUG     ] [base.get_path      ] unknown: tmpfolder\unboxsmansz\.apk\assets\fonts\eurostilebold.ttf
[handler.base/13668][DEBUG     ] [base.get_path      ] {'source': 'databuffer', 'magic': {'mimetype': 'application/x-font-ttf', 'patterns': [{'regex': '\\x00\\x01\\x00\\x00\\x00', 'offset': 0, 'size': 5}], 'shortname': 'TTF', 'id': 32, 'longname': 'TrueType Font'}}
[handler.base/13668][DEBUG     ] [base.get_path      ] None
[handler.commands.commands/13668][DEBUG     ] [commands.decompile     ] [u'ida\\idaw.exe', '-B', '-M', '-S"home\\.unbox\\ida_batch_decompile.py -o\\"tmpfolder\\unboxeqk0no\\eurostilebold.c\\""', '"tmpfolder\\unboxsmansz\\.apk\\assets\\fonts\\eurostilebold.ttf"']
[handler.base/13668][DEBUG     ] [base.get_path      ] scheme: c
[handler.base/13668][DEBUG     ] [base.get_path      ] <Application32Bits encoding=None path=WindowsPath('tmpfolder/unboxeqk0no')>
[handler.local/13668][DEBUG     ] [local.walk          ] walk: tmpfolder\unboxeqk0no
...

...
tmpfolder\unboxsmansz\.source\org\stockchart\e\h$a.java
tmpfolder\unboxsmansz\.source\org\stockchart\e\h.java
[handler.base/13668][DEBUG     ] [base.get_path      ] {'source': 'databuffer', 'magic': None}
[handler.base/13668][DEBUG     ] [base.get_path      ] scheme: c
[handler.base/13668][DEBUG     ] [base.get_path      ] <LocalPath encoding=None path=WindowsPath('tmpfolder/unboxsmansz/.source/org/stockchart/e/h.java')>
[handler.base/13668][DEBUG     ] [base.get_path      ] unknown: tmpfolder\unboxsmansz\.source\org\stockchart\e\i.java
[handler.base/13668][DEBUG     ] [base.get_path      ] {'source': 'databuffer', 'magic': None}
[handler.base/13668][DEBUG     ] [base.get_path      ] scheme: c
[handler.base/13668][DEBUG     ] [base.get_path      ] <LocalPath encoding=None path=WindowsPath('tmpfolder//unboxsmansz/.source/org/stockchart/e/i.java')>
tmpfolder\unboxsmansz\.source\org\stockchart\e\i.java
```

# Contribute :trophy:

## Add new tools and file formats

TBD

* add external command wrapper to `handler.commands.commands`
* add the file handler to `handler.<archive,decompilable,local,remote>`
* route the file to the correct handler in `handler.base.UniversalPath.get_path`


## Supported Formats and implemented 3rd Party Applications:

| Status   | Type |  Tool Dependency | ref |
|--------|--------|------------------|-----|
| :heavy_check_mark: | archive | patool or 7z | - |
| :heavy_check_mark: | browser extension | patool or 7z | - |
| :heavy_check_mark: | .net application | JustDecompile (windows) | https://github.com/telerik/JustDecompileEngine |
| :heavy_check_mark: | apk | dex2jar and jd-cli | https://github.com/pxb1988/dex2jar |
| :heavy_check_mark: | compiled java | jd-cli | https://github.com/kwart/jd-cmd |
| :heavy_check_mark: | binary applications |IDA PRO / RetDec  :x: | https://www.hex-rays.com/products/ida/  https://github.com/avast-tl/retdec |
| :x: | Ethereum solidity smart contract | porosity | https://github.com/comaeio/porosity/ |
| :x: | compiled python | python-uncompyle6 | https://github.com/rocky/python-uncompyle6/ |


Are you missing your favorite decompiler? Let me know or create a PR
