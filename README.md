# **MDK-huawei-gen**

## **Overview**

**PyangBind** is a plugin for [Pyang][pyang] that generates a Python class hierarchy from a YANG data model. The resulting classes can be directly interacted with in Python. Particularly, **PyangBind** will allow you to:

 * Create new data instances - through setting values in the Python class hierarchy.
 * Load data instances from external sources - taking input data from an external source and allowing it to be addressed through the Python classes.
 * Serialise populated objects into formats that can be stored, or sent to another system (e.g., a network element).

Development of **PyangBind** has been motivated by consuming the  [OpenConfig][openconfig] data models; and is intended to be well-tested against these models. The Python classes generated, and serialisation methods are intended to provide network operators with a starting point for loading data instances from network elements, manipulating them, and sending them to a network device. **PyangBind** classes also have functionality which allows additional methods to be associated with the classes, such that it can be used for the foundation of a NMS.

## **Installation**
### **Prerequisites**

OS: Ubuntu, CentOS, Suse  
Python: 3.7  
Required Python package:pyang,bitarray,lxml,regex,six,enum34,ncclient,pyangbind

### Build From Source  

1.Clone the mdk repository:
 ```
 git clone https://github.com/HuaweiDatacomm/mdk.git
 ```
2.Install required Python package:
```
 pip3 install pyangbind
 pip3 install ncclient
 pip3 install -r requirments.txt
 python3 setup.py install
 pip3 list
```

## Getting Used

### use Yang model generation python class:
To generate your first set of classes, you will need a YANG module, and its dependencies. A number of simple modules can be found in the tests directory (e.g., tests/base-test.yang).
To generate a set of Python classes, Pyang needs to be provided a pointer to where PyangBind's plugin is installed. This location can be found by running:

```
$ export PYBINDPLUGIN=`/usr/bin/env python3 -c \
'import pyangbind; import os; print ("{}/plugin".format(os.path.dirname(pyangbind.__file__)))'`
$ echo $PYBINDPLUGIN
```
Once this path is known, it can be provided to the --plugin-dir argument to Pyang. Here is an example of huawei-ifm.yang:
```
$ pyang --plugindir $PYBINDPLUGIN -f pybind -o huawei_ifm.py yang/huawei-ifm.yang
```
## Note:  
if you want to generate Python Classes in batches,you can put yang modules in dir yang,then run generate.py.you also can upate
the generate_py.
```
cd mdk
mkdir python-gen
mkdir translate-gen
cd yang
chmod +x generate_py.sh
./generate_py.sh
```









