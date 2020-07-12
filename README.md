# JHook
Create hooks to files and web easily services using this robust Python module!

#### Section 1. jfile

jfile comes with the JFileWatcher and JDirWatcher, both launch daemon threads that are 
highly customizable with custom timing, status watching options, console logging, and custom 
events when triggered.

#### Part 1-1. JFileWatcher

Here is how to create your first file hook that triggers a pre-built event to reload data into the 
object instances **data** variable.

```python
from jhook import jfile

watcher = jfile.JFileHook(file_abs_path="/testfile.text")
watcher.run_hook()
```

When the file **/testfile.text** is modified the daemon will call **__load_file_data()** which is
the default pre-built function that comes with JFileWatcher. You can access this data from the **data**
variable.

```python
watcher.data
```

You can easily create custom functions to be called instead of the default. **Note the data variable 
will remain empty and will not be loaded if you override the default.** In the example below a new function
is created and it's reference is passed into our JFileWatcher overriding the default trigger event.

```python
from jhook import jfile

def hello_custom():
  print("Hello custom event!")

watcher = jfile.JFileHook(file_abs_path="/testfile.text", change_function=hello_custom)
watcher.run_hook()
```

Passing arguments to your change_function can be done by simply including a dictionary to be unpacked when the
function is called.


```python
from jhook import jfile

def hello_custom(data):
  print(f"Hello custom {data} event!")

watcher = jfile.JFileHook(file_abs_path="/testfile.text", change_function=(hello_custom, {"data":"function with arguments"})
watcher.run_hook()
```

Accessing data from within the watcher is simple but must follow some slightly more complicated but not painful rules. 
When creating the argument dictionary, if we use the reserved keywords **last_st_data**, **jfile_data**, or **file_abs_path**
with empty values, they will be filled, unpacked, and passed in as arguments.

```python
from jhook import jfile

def hello_custom(last_st_time, file_abs_path):
  print(f"{file_abs_path} was last modified {last_st_data}")

watcher = jfile.JFileHook(file_abs_path="/testfile.text", change_function=(hello_custom, {"last_st_data":"", "file_abs_path":""})
watcher.run_hook()
```

You might not want to have the event be triggered based on the **st_mtime** which is the files last modification
time. Instead you can override the default for this by choosing from a variety of file statuses available from
os.stat().

List of available file stats:
| Stat code | Description |
|-|-|
| st_mode | file type and file mode bits (permissions). |
| st_ino | inode number on Unix and the file index on Windows platform. |
| st_dev | identifier of the device on which this file resides. |
| st_nlink | number of hard links. |
| st_uid | user identifier of the file owner. |
| st_gid | group identifier of the file owner. |
| st_size | size of the file in bytes. |
| st_atime | time of most recent access in seconds. |
| st_mtime | time of most recent content modification in seconds. |
| st_ctime | time of most recent metadata change on Unix and creation time on Windows in seconds. |
| st_atime_ns | time of most recent access in nanoseconds. |
| st_mtime_ns | time of most recent content modification in nanoseconds. |
| st_ctime_ns | time of most recent metadata change on Unix and creation time on Windows in nanoseconds. |
| st_blocks | number of 512-byte blocks allocated for file. |
| st_rdev | type of device, if an inode device. |
| st_flags | user defined flags for file. |

Accessing the data from your file_stat_opt is stored in last_st_data.

```python
from jhook import jfile

def hello(last_st_data, file_abs_path):
  print(f"{file_abs_path} permissions were changed to {last_st_data}")

watcher = jfile.JFileHook(file_abs_path="/testfile.text", file_stat_opt="st_mode", change_function=(hello, {"last_st_data":"", "file_abs_path":""})
watcher.run_hook()
```

Stopping the daemon is as easy as calling
```python3
watcher.stop_hook()
```

If you would like debug logs from the file watchers operations you can set **logging** to True.

```python3
from jhook import jfile

watcher = jfile.JFileHook(file_abs_path="/testfile.text", logging=True)
watcher.run_hook()
```

output: 
```
File watcher started on /testfile.text on status st_mtime
```


Simple dynamic configuration file change using JFileWatcher example project:

```python3
from jhook import jfile
import json
import time

configs = {"user1": {"permissions":"admin"}, "user2":{"permissions":"developer"}}

def update_configs(file_abs_path):
  with open (file_abs_path, "r") as config_file_json:
    configs = json.load(config_file_json)
    config_file_json.close()
  print(configs)
  print()
  print("Updated program configuration!")
  
watcher = jfile.JFileHook(file_abs_path="/config.json", change_function=(update_configs, {"file_abs_path":""})
watcher.run_hook()
```
Now we can dynamically change user's permissions while our program is running straight from the config file **config.json**
