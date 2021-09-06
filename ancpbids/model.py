#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Wed Sep  1 20:38:20 2021 by generateDS.py version 2.39.7.
# Python 3.9.5 (default, May 11 2021, 08:20:37)  [GCC 10.3.0]
#
# Command line options:
#   ('-f', '')
#   ('--export', 'etree validate generator')
#   ('--member-specs', 'dict')
#   ('--always-export-default', '')
#   ('-o', '../ancpbids/model.py')
#
# Command line arguments:
#   ../ancpbids/data/schema-files/bids.xsd
#
# Command line:
#   ../../../hg-repos/generateds-code/generateDS.py -f --export="etree validate generator" --member-specs="dict" --always-export-default -o "../ancpbids/model.py" ../ancpbids/data/schema-files/bids.xsd
#
# Current working directory (os.getcwd()):
#   tools
#

import sys
try:
    ModulenotfoundExp_ = ModuleNotFoundError
except NameError:
    ModulenotfoundExp_ = ImportError
from six.moves import zip_longest
import os
import re as re_
import base64
import datetime as datetime_
import decimal as decimal_
from lxml import etree as etree_


Validate_simpletypes_ = True
SaveElementTreeNode = True
if sys.version_info.major == 2:
    BaseStrType_ = basestring
else:
    BaseStrType_ = str


def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    try:
        if isinstance(infile, os.PathLike):
            infile = os.path.join(infile)
    except AttributeError:
        pass
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

def parsexmlstring_(instring, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    element = etree_.fromstring(instring, parser=parser, **kwargs)
    return element

#
# Namespace prefix definition table (and other attributes, too)
#
# The module generatedsnamespaces, if it is importable, must contain
# a dictionary named GeneratedsNamespaceDefs.  This Python dictionary
# should map element type names (strings) to XML schema namespace prefix
# definitions.  The export method for any class for which there is
# a namespace prefix definition, will export that definition in the
# XML representation of that element.  See the export method of
# any generated element type class for an example of the use of this
# table.
# A sample table is:
#
#     # File: generatedsnamespaces.py
#
#     GenerateDSNamespaceDefs = {
#         "ElementtypeA": "http://www.xxx.com/namespaceA",
#         "ElementtypeB": "http://www.xxx.com/namespaceB",
#     }
#
# Additionally, the generatedsnamespaces module can contain a python
# dictionary named GenerateDSNamespaceTypePrefixes that associates element
# types with the namespace prefixes that are to be added to the
# "xsi:type" attribute value.  See the _exportAttributes method of
# any generated element type and the generation of "xsi:type" for an
# example of the use of this table.
# An example table:
#
#     # File: generatedsnamespaces.py
#
#     GenerateDSNamespaceTypePrefixes = {
#         "ElementtypeC": "aaa:",
#         "ElementtypeD": "bbb:",
#     }
#

try:
    from generatedsnamespaces import GenerateDSNamespaceDefs as GenerateDSNamespaceDefs_
except ModulenotfoundExp_ :
    GenerateDSNamespaceDefs_ = {}
try:
    from generatedsnamespaces import GenerateDSNamespaceTypePrefixes as GenerateDSNamespaceTypePrefixes_
except ModulenotfoundExp_ :
    GenerateDSNamespaceTypePrefixes_ = {}

#
# You can replace the following class definition by defining an
# importable module named "generatedscollector" containing a class
# named "GdsCollector".  See the default class definition below for
# clues about the possible content of that class.
#
try:
    from generatedscollector import GdsCollector as GdsCollector_
except ModulenotfoundExp_ :

    class GdsCollector_(object):

        def __init__(self, messages=None):
            if messages is None:
                self.messages = []
            else:
                self.messages = messages

        def add_message(self, msg):
            self.messages.append(msg)

        def get_messages(self):
            return self.messages

        def clear_messages(self):
            self.messages = []

        def print_messages(self):
            for msg in self.messages:
                print("Warning: {}".format(msg))

        def write_messages(self, outstream):
            for msg in self.messages:
                outstream.write("Warning: {}\n".format(msg))


#
# The super-class for enum types
#

try:
    from enum import Enum
except ModulenotfoundExp_ :
    Enum = object

#
# The root super-class for element type classes
#
# Calls to the methods in these classes are generated by generateDS.py.
# You can replace these methods by re-implementing the following class
#   in a module named generatedssuper.py.

try:
    from generatedssuper import GeneratedsSuper
except ModulenotfoundExp_ as exp:
    try:
        from generatedssupersuper import GeneratedsSuperSuper
    except ModulenotfoundExp_ as exp:
        class GeneratedsSuperSuper(object):
            pass
    
    class GeneratedsSuper(GeneratedsSuperSuper):
        __hash__ = object.__hash__
        tzoff_pattern = re_.compile(r'(\+|-)((0\d|1[0-3]):[0-5]\d|14:00)$')
        class _FixedOffsetTZ(datetime_.tzinfo):
            def __init__(self, offset, name):
                self.__offset = datetime_.timedelta(minutes=offset)
                self.__name = name
            def utcoffset(self, dt):
                return self.__offset
            def tzname(self, dt):
                return self.__name
            def dst(self, dt):
                return None
        def gds_format_string(self, input_data, input_name=''):
            return input_data
        def gds_parse_string(self, input_data, node=None, input_name=''):
            return input_data
        def gds_validate_string(self, input_data, node=None, input_name=''):
            if not input_data:
                return ''
            else:
                return input_data
        def gds_format_base64(self, input_data, input_name=''):
            return base64.b64encode(input_data)
        def gds_validate_base64(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_integer(self, input_data, input_name=''):
            return '%d' % input_data
        def gds_parse_integer(self, input_data, node=None, input_name=''):
            try:
                ival = int(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires integer value: %s' % exp)
            return ival
        def gds_validate_integer(self, input_data, node=None, input_name=''):
            try:
                value = int(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires integer value')
            return value
        def gds_format_integer_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return '%s' % ' '.join(input_data)
        def gds_validate_integer_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    int(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of integer values')
            return values
        def gds_format_float(self, input_data, input_name=''):
            return ('%.15f' % input_data).rstrip('0')
        def gds_parse_float(self, input_data, node=None, input_name=''):
            try:
                fval_ = float(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires float or double value: %s' % exp)
            return fval_
        def gds_validate_float(self, input_data, node=None, input_name=''):
            try:
                value = float(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires float value')
            return value
        def gds_format_float_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return '%s' % ' '.join(input_data)
        def gds_validate_float_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    float(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of float values')
            return values
        def gds_format_decimal(self, input_data, input_name=''):
            return_value = '%s' % input_data
            if '.' in return_value:
                return_value = return_value.rstrip('0')
                if return_value.endswith('.'):
                    return_value = return_value.rstrip('.')
            return return_value
        def gds_parse_decimal(self, input_data, node=None, input_name=''):
            try:
                decimal_value = decimal_.Decimal(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires decimal value')
            return decimal_value
        def gds_validate_decimal(self, input_data, node=None, input_name=''):
            try:
                value = decimal_.Decimal(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires decimal value')
            return value
        def gds_format_decimal_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return ' '.join([self.gds_format_decimal(item) for item in input_data])
        def gds_validate_decimal_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    decimal_.Decimal(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of decimal values')
            return values
        def gds_format_double(self, input_data, input_name=''):
            return '%s' % input_data
        def gds_parse_double(self, input_data, node=None, input_name=''):
            try:
                fval_ = float(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires double or float value: %s' % exp)
            return fval_
        def gds_validate_double(self, input_data, node=None, input_name=''):
            try:
                value = float(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires double or float value')
            return value
        def gds_format_double_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return '%s' % ' '.join(input_data)
        def gds_validate_double_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    float(value)
                except (TypeError, ValueError):
                    raise_parse_error(
                        node, 'Requires sequence of double or float values')
            return values
        def gds_format_boolean(self, input_data, input_name=''):
            return ('%s' % input_data).lower()
        def gds_parse_boolean(self, input_data, node=None, input_name=''):
            if input_data in ('true', '1'):
                bval = True
            elif input_data in ('false', '0'):
                bval = False
            else:
                raise_parse_error(node, 'Requires boolean value')
            return bval
        def gds_validate_boolean(self, input_data, node=None, input_name=''):
            if input_data not in (True, 1, False, 0, ):
                raise_parse_error(
                    node,
                    'Requires boolean value '
                    '(one of True, 1, False, 0)')
            return input_data
        def gds_format_boolean_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return '%s' % ' '.join(input_data)
        def gds_validate_boolean_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                value = self.gds_parse_boolean(value, node, input_name)
                if value not in (True, 1, False, 0, ):
                    raise_parse_error(
                        node,
                        'Requires sequence of boolean values '
                        '(one of True, 1, False, 0)')
            return values
        def gds_validate_datetime(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_datetime(self, input_data, input_name=''):
            if input_data.microsecond == 0:
                _svalue = '%04d-%02d-%02dT%02d:%02d:%02d' % (
                    input_data.year,
                    input_data.month,
                    input_data.day,
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                )
            else:
                _svalue = '%04d-%02d-%02dT%02d:%02d:%02d.%s' % (
                    input_data.year,
                    input_data.month,
                    input_data.day,
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                    ('%f' % (float(input_data.microsecond) / 1000000))[2:],
                )
            if input_data.tzinfo is not None:
                tzoff = input_data.tzinfo.utcoffset(input_data)
                if tzoff is not None:
                    total_seconds = tzoff.seconds + (86400 * tzoff.days)
                    if total_seconds == 0:
                        _svalue += 'Z'
                    else:
                        if total_seconds < 0:
                            _svalue += '-'
                            total_seconds *= -1
                        else:
                            _svalue += '+'
                        hours = total_seconds // 3600
                        minutes = (total_seconds - (hours * 3600)) // 60
                        _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
            return _svalue
        @classmethod
        def gds_parse_datetime(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            time_parts = input_data.split('.')
            if len(time_parts) > 1:
                micro_seconds = int(float('0.' + time_parts[1]) * 1000000)
                input_data = '%s.%s' % (
                    time_parts[0], "{}".format(micro_seconds).rjust(6, "0"), )
                dt = datetime_.datetime.strptime(
                    input_data, '%Y-%m-%dT%H:%M:%S.%f')
            else:
                dt = datetime_.datetime.strptime(
                    input_data, '%Y-%m-%dT%H:%M:%S')
            dt = dt.replace(tzinfo=tz)
            return dt
        def gds_validate_date(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_date(self, input_data, input_name=''):
            _svalue = '%04d-%02d-%02d' % (
                input_data.year,
                input_data.month,
                input_data.day,
            )
            try:
                if input_data.tzinfo is not None:
                    tzoff = input_data.tzinfo.utcoffset(input_data)
                    if tzoff is not None:
                        total_seconds = tzoff.seconds + (86400 * tzoff.days)
                        if total_seconds == 0:
                            _svalue += 'Z'
                        else:
                            if total_seconds < 0:
                                _svalue += '-'
                                total_seconds *= -1
                            else:
                                _svalue += '+'
                            hours = total_seconds // 3600
                            minutes = (total_seconds - (hours * 3600)) // 60
                            _svalue += '{0:02d}:{1:02d}'.format(
                                hours, minutes)
            except AttributeError:
                pass
            return _svalue
        @classmethod
        def gds_parse_date(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            dt = datetime_.datetime.strptime(input_data, '%Y-%m-%d')
            dt = dt.replace(tzinfo=tz)
            return dt.date()
        def gds_validate_time(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_time(self, input_data, input_name=''):
            if input_data.microsecond == 0:
                _svalue = '%02d:%02d:%02d' % (
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                )
            else:
                _svalue = '%02d:%02d:%02d.%s' % (
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                    ('%f' % (float(input_data.microsecond) / 1000000))[2:],
                )
            if input_data.tzinfo is not None:
                tzoff = input_data.tzinfo.utcoffset(input_data)
                if tzoff is not None:
                    total_seconds = tzoff.seconds + (86400 * tzoff.days)
                    if total_seconds == 0:
                        _svalue += 'Z'
                    else:
                        if total_seconds < 0:
                            _svalue += '-'
                            total_seconds *= -1
                        else:
                            _svalue += '+'
                        hours = total_seconds // 3600
                        minutes = (total_seconds - (hours * 3600)) // 60
                        _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
            return _svalue
        def gds_validate_simple_patterns(self, patterns, target):
            # pat is a list of lists of strings/patterns.
            # The target value must match at least one of the patterns
            # in order for the test to succeed.
            found1 = True
            for patterns1 in patterns:
                found2 = False
                for patterns2 in patterns1:
                    mo = re_.search(patterns2, target)
                    if mo is not None and len(mo.group(0)) == len(target):
                        found2 = True
                        break
                if not found2:
                    found1 = False
                    break
            return found1
        @classmethod
        def gds_parse_time(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            if len(input_data.split('.')) > 1:
                dt = datetime_.datetime.strptime(input_data, '%H:%M:%S.%f')
            else:
                dt = datetime_.datetime.strptime(input_data, '%H:%M:%S')
            dt = dt.replace(tzinfo=tz)
            return dt.time()
        def gds_check_cardinality_(
                self, value, input_name,
                min_occurs=0, max_occurs=1, required=None):
            if value is None:
                length = 0
            elif isinstance(value, list):
                length = len(value)
            else:
                length = 1
            if required is not None :
                if required and length < 1:
                    self.gds_collector_.add_message(
                        "Required value {}{} is missing".format(
                            input_name, self.gds_get_node_lineno_()))
            if length < min_occurs:
                self.gds_collector_.add_message(
                    "Number of values for {}{} is below "
                    "the minimum allowed, "
                    "expected at least {}, found {}".format(
                        input_name, self.gds_get_node_lineno_(),
                        min_occurs, length))
            elif length > max_occurs:
                self.gds_collector_.add_message(
                    "Number of values for {}{} is above "
                    "the maximum allowed, "
                    "expected at most {}, found {}".format(
                        input_name, self.gds_get_node_lineno_(),
                        max_occurs, length))
        def gds_validate_builtin_ST_(
                self, validator, value, input_name,
                min_occurs=None, max_occurs=None, required=None):
            if value is not None:
                try:
                    validator(value, input_name=input_name)
                except GDSParseError as parse_error:
                    self.gds_collector_.add_message(str(parse_error))
        def gds_validate_defined_ST_(
                self, validator, value, input_name,
                min_occurs=None, max_occurs=None, required=None):
            if value is not None:
                try:
                    validator(value)
                except GDSParseError as parse_error:
                    self.gds_collector_.add_message(str(parse_error))
        def gds_str_lower(self, instring):
            return instring.lower()
        def get_path_(self, node):
            path_list = []
            self.get_path_list_(node, path_list)
            path_list.reverse()
            path = '/'.join(path_list)
            return path
        Tag_strip_pattern_ = re_.compile(r'\{.*\}')
        def get_path_list_(self, node, path_list):
            if node is None:
                return
            tag = GeneratedsSuper.Tag_strip_pattern_.sub('', node.tag)
            if tag:
                path_list.append(tag)
            self.get_path_list_(node.getparent(), path_list)
        def get_class_obj_(self, node, default_class=None):
            class_obj1 = default_class
            if 'xsi' in node.nsmap:
                classname = node.get('{%s}type' % node.nsmap['xsi'])
                if classname is not None:
                    names = classname.split(':')
                    if len(names) == 2:
                        classname = names[1]
                    class_obj2 = globals().get(classname)
                    if class_obj2 is not None:
                        class_obj1 = class_obj2
            return class_obj1
        def gds_build_any(self, node, type_name=None):
            # provide default value in case option --disable-xml is used.
            content = ""
            content = etree_.tostring(node, encoding="unicode")
            return content
        @classmethod
        def gds_reverse_node_mapping(cls, mapping):
            return dict(((v, k) for k, v in mapping.items()))
        @staticmethod
        def gds_encode(instring):
            if sys.version_info.major == 2:
                if ExternalEncoding:
                    encoding = ExternalEncoding
                else:
                    encoding = 'utf-8'
                return instring.encode(encoding)
            else:
                return instring
        @staticmethod
        def convert_unicode(instring):
            if isinstance(instring, str):
                result = quote_xml(instring)
            elif sys.version_info.major == 2 and isinstance(instring, unicode):
                result = quote_xml(instring).encode('utf8')
            else:
                result = GeneratedsSuper.gds_encode(str(instring))
            return result
        def __eq__(self, other):
            def excl_select_objs_(obj):
                return (obj[0] != 'parent_object_' and
                        obj[0] != 'gds_collector_')
            if type(self) != type(other):
                return False
            return all(x == y for x, y in zip_longest(
                filter(excl_select_objs_, self.__dict__.items()),
                filter(excl_select_objs_, other.__dict__.items())))
        def __ne__(self, other):
            return not self.__eq__(other)
        # Django ETL transform hooks.
        def gds_djo_etl_transform(self):
            pass
        def gds_djo_etl_transform_db_obj(self, dbobj):
            pass
        # SQLAlchemy ETL transform hooks.
        def gds_sqa_etl_transform(self):
            return 0, None
        def gds_sqa_etl_transform_db_obj(self, dbobj):
            pass
        def gds_get_node_lineno_(self):
            if (hasattr(self, "gds_elementtree_node_") and
                    self.gds_elementtree_node_ is not None):
                return ' near line {}'.format(
                    self.gds_elementtree_node_.sourceline)
            else:
                return ""
    
    
    def getSubclassFromModule_(module, class_):
        '''Get the subclass of a class from a specific module.'''
        name = class_.__name__ + 'Sub'
        if hasattr(module, name):
            return getattr(module, name)
        else:
            return None


#
# If you have installed IPython you can uncomment and use the following.
# IPython is available from http://ipython.scipy.org/.
#

## from IPython.Shell import IPShellEmbed
## args = ''
## ipshell = IPShellEmbed(args,
##     banner = 'Dropping into IPython',
##     exit_msg = 'Leaving Interpreter, back to program.')

# Then use the following line where and when you want to drop into the
# IPython shell:
#    ipshell('<some message> -- Entering ipshell.\nHit Ctrl-D to exit')

#
# Globals
#

ExternalEncoding = ''
# Set this to false in order to deactivate during export, the use of
# name space prefixes captured from the input document.
UseCapturedNS_ = True
CapturedNsmap_ = {}
Tag_pattern_ = re_.compile(r'({.*})?(.*)')
String_cleanup_pat_ = re_.compile(r"[\n\r\s]+")
Namespace_extract_pat_ = re_.compile(r'{(.*)}(.*)')
CDATA_pattern_ = re_.compile(r"<!\[CDATA\[.*?\]\]>", re_.DOTALL)

# Change this to redirect the generated superclass module to use a
# specific subclass module.
CurrentSubclassModule_ = None

#
# Support/utility functions.
#


def showIndent(outfile, level, pretty_print=True):
    if pretty_print:
        for idx in range(level):
            outfile.write('    ')


def quote_xml(inStr):
    "Escape markup chars, but do not modify CDATA sections."
    if not inStr:
        return ''
    s1 = (isinstance(inStr, BaseStrType_) and inStr or '%s' % inStr)
    s2 = ''
    pos = 0
    matchobjects = CDATA_pattern_.finditer(s1)
    for mo in matchobjects:
        s3 = s1[pos:mo.start()]
        s2 += quote_xml_aux(s3)
        s2 += s1[mo.start():mo.end()]
        pos = mo.end()
    s3 = s1[pos:]
    s2 += quote_xml_aux(s3)
    return s2


def quote_xml_aux(inStr):
    s1 = inStr.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    return s1


def quote_attrib(inStr):
    s1 = (isinstance(inStr, BaseStrType_) and inStr or '%s' % inStr)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    if '"' in s1:
        if "'" in s1:
            s1 = '"%s"' % s1.replace('"', "&quot;")
        else:
            s1 = "'%s'" % s1
    else:
        s1 = '"%s"' % s1
    return s1


def quote_python(inStr):
    s1 = inStr
    if s1.find("'") == -1:
        if s1.find('\n') == -1:
            return "'%s'" % s1
        else:
            return "'''%s'''" % s1
    else:
        if s1.find('"') != -1:
            s1 = s1.replace('"', '\\"')
        if s1.find('\n') == -1:
            return '"%s"' % s1
        else:
            return '"""%s"""' % s1


def get_all_text_(node):
    if node.text is not None:
        text = node.text
    else:
        text = ''
    for child in node:
        if child.tail is not None:
            text += child.tail
    return text


def find_attr_value_(attr_name, node):
    attrs = node.attrib
    attr_parts = attr_name.split(':')
    value = None
    if len(attr_parts) == 1:
        value = attrs.get(attr_name)
    elif len(attr_parts) == 2:
        prefix, name = attr_parts
        if prefix == 'xml':
            namespace = 'http://www.w3.org/XML/1998/namespace'
        else:
            namespace = node.nsmap.get(prefix)
        if namespace is not None:
            value = attrs.get('{%s}%s' % (namespace, name, ))
    return value


def encode_str_2_3(instr):
    return instr


class GDSParseError(Exception):
    pass


def raise_parse_error(node, msg):
    if node is not None:
        msg = '%s (element %s/line %d)' % (msg, node.tag, node.sourceline, )
    raise GDSParseError(msg)


class MixedContainer:
    # Constants for category:
    CategoryNone = 0
    CategoryText = 1
    CategorySimple = 2
    CategoryComplex = 3
    # Constants for content_type:
    TypeNone = 0
    TypeText = 1
    TypeString = 2
    TypeInteger = 3
    TypeFloat = 4
    TypeDecimal = 5
    TypeDouble = 6
    TypeBoolean = 7
    TypeBase64 = 8
    def __init__(self, category, content_type, name, value):
        self.category = category
        self.content_type = content_type
        self.name = name
        self.value = value
    def getCategory(self):
        return self.category
    def getContenttype(self, content_type):
        return self.content_type
    def getValue(self):
        return self.value
    def getName(self):
        return self.name
    def export(self, outfile, level, name, namespace,
               pretty_print=True):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip():
                outfile.write(self.value)
        elif self.category == MixedContainer.CategorySimple:
            self.exportSimple(outfile, level, name)
        else:    # category == MixedContainer.CategoryComplex
            self.value.export(
                outfile, level, namespace, name_=name,
                pretty_print=pretty_print)
    def exportSimple(self, outfile, level, name):
        if self.content_type == MixedContainer.TypeString:
            outfile.write('<%s>%s</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeInteger or \
                self.content_type == MixedContainer.TypeBoolean:
            outfile.write('<%s>%d</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeFloat or \
                self.content_type == MixedContainer.TypeDecimal:
            outfile.write('<%s>%f</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeDouble:
            outfile.write('<%s>%g</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeBase64:
            outfile.write('<%s>%s</%s>' % (
                self.name,
                base64.b64encode(self.value),
                self.name))
    def to_etree(self, element, mapping_=None, reverse_mapping_=None, nsmap_=None):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip():
                if len(element) > 0:
                    if element[-1].tail is None:
                        element[-1].tail = self.value
                    else:
                        element[-1].tail += self.value
                else:
                    if element.text is None:
                        element.text = self.value
                    else:
                        element.text += self.value
        elif self.category == MixedContainer.CategorySimple:
            subelement = etree_.SubElement(
                element, '%s' % self.name)
            subelement.text = self.to_etree_simple()
        else:    # category == MixedContainer.CategoryComplex
            self.value.to_etree(element)
    def to_etree_simple(self, mapping_=None, reverse_mapping_=None, nsmap_=None):
        if self.content_type == MixedContainer.TypeString:
            text = self.value
        elif (self.content_type == MixedContainer.TypeInteger or
                self.content_type == MixedContainer.TypeBoolean):
            text = '%d' % self.value
        elif (self.content_type == MixedContainer.TypeFloat or
                self.content_type == MixedContainer.TypeDecimal):
            text = '%f' % self.value
        elif self.content_type == MixedContainer.TypeDouble:
            text = '%g' % self.value
        elif self.content_type == MixedContainer.TypeBase64:
            text = '%s' % base64.b64encode(self.value)
        return text
    def exportLiteral(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s", "%s"),\n' % (
                    self.category, self.content_type,
                    self.name, self.value))
        elif self.category == MixedContainer.CategorySimple:
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s", "%s"),\n' % (
                    self.category, self.content_type,
                    self.name, self.value))
        else:    # category == MixedContainer.CategoryComplex
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s",\n' % (
                    self.category, self.content_type, self.name,))
            self.value.exportLiteral(outfile, level + 1)
            showIndent(outfile, level)
            outfile.write(')\n')


class MemberSpec_(object):
    def __init__(self, name='', data_type='', container=0,
            optional=0, child_attrs=None, choice=None):
        self.name = name
        self.data_type = data_type
        self.container = container
        self.child_attrs = child_attrs
        self.choice = choice
        self.optional = optional
    def set_name(self, name): self.name = name
    def get_name(self): return self.name
    def set_data_type(self, data_type): self.data_type = data_type
    def get_data_type_chain(self): return self.data_type
    def get_data_type(self):
        if isinstance(self.data_type, list):
            if len(self.data_type) > 0:
                return self.data_type[-1]
            else:
                return 'xs:string'
        else:
            return self.data_type
    def set_container(self, container): self.container = container
    def get_container(self): return self.container
    def set_child_attrs(self, child_attrs): self.child_attrs = child_attrs
    def get_child_attrs(self): return self.child_attrs
    def set_choice(self, choice): self.choice = choice
    def get_choice(self): return self.choice
    def set_optional(self, optional): self.optional = optional
    def get_optional(self): return self.optional


def _cast(typ, value):
    if typ is None or value is None:
        return value
    return typ(value)

#
# Data representation classes.
#


class DatasetTypeType(str, Enum):
    """DatasetTypeType -- @use: recommended
    
    """
    RAW='raw'
    DERIVATIVE='derivative'


class handednessType(str, Enum):
    LEFT='left'
    LEFT_1='Left'
    LEFT_2='LEFT'
    L='l'
    L_1='L'
    RIGHT='right'
    RIGHT_1='Right'
    RIGHT_2='RIGHT'
    R='r'
    R_1='R'
    AMBIDEXTROUS='ambidextrous'
    AMBIDEXTROUS_1='Ambidextrous'
    AMBIDEXTROUS_2='AMBIDEXTROUS'
    A='a'
    A_1='A'


class sexType(str, Enum):
    MALE='male'
    MALE_1='Male'
    MALE_2='MALE'
    M='m'
    M_1='M'
    FEMALE='female'
    FEMALE_1='Female'
    F='f'
    F_1='F'
    OTHER='other'
    OTHER_1='Other'
    OTHER_2='OTHER'
    O='o'
    O_1='O'


class File(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'name': MemberSpec_('name', 'string', 0, 0, {'use': 'required', 'name': 'name'}),
        'extension': MemberSpec_('extension', 'string', 0, 1, {'use': 'optional', 'name': 'extension'}),
        'uri': MemberSpec_('uri', 'anyURI', 0, 1, {'use': 'optional', 'name': 'uri'}),
    }
    subclass = None
    superclass = None
    def __init__(self, name=None, extension=None, uri=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name = _cast(None, name)
        self.name_nsprefix_ = None
        self.extension = _cast(None, extension)
        self.extension_nsprefix_ = None
        self.uri = _cast(None, uri)
        self.uri_nsprefix_ = None
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, File)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if File.subclass:
            return File.subclass(*args_, **kwargs_)
        else:
            return File(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_extension(self):
        return self.extension
    def set_extension(self, extension):
        self.extension = extension
    def get_uri(self):
        return self.uri
    def set_uri(self, uri):
        self.uri = uri
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='File', mapping_=None, reverse_mapping_=None, nsmap_=None):
        if parent_element is None:
            element = etree_.Element('{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        else:
            element = etree_.SubElement(parent_element, '{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        if self.extensiontype_ is not None:
            element.set('{http://www.w3.org/2001/XMLSchema-instance}type', self.extensiontype_)
        if self.name is not None:
            element.set('name', self.gds_format_string(self.name))
        if self.extension is not None:
            element.set('extension', self.gds_format_string(self.extension))
        if self.uri is not None:
            element.set('uri', self.gds_format_string(self.uri))
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.name, 'name')
        self.gds_check_cardinality_(self.name, 'name', required=True)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.extension, 'extension')
        self.gds_check_cardinality_(self.extension, 'extension', required=False)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.uri, 'uri')
        self.gds_check_cardinality_(self.uri, 'uri', required=False)
        # validate simple type children
        # validate complex type children
        if recursive:
            pass
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('name', node)
        if value is not None and 'name' not in already_processed:
            already_processed.add('name')
            self.name = value
        value = find_attr_value_('extension', node)
        if value is not None and 'extension' not in already_processed:
            already_processed.add('extension')
            self.extension = value
        value = find_attr_value_('uri', node)
        if value is not None and 'uri' not in already_processed:
            already_processed.add('uri')
            self.uri = value
        value = find_attr_value_('xsi:type', node)
        if value is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            self.extensiontype_ = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class File


class Folder(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'name': MemberSpec_('name', 'string', 0, 0, {'use': 'required', 'name': 'name'}),
        'files': MemberSpec_('files', 'File', 1, 1, {'maxOccurs': 'unbounded', 'minOccurs': '0', 'name': 'files', 'type': 'File'}, None),
        'folders': MemberSpec_('folders', 'Folder', 1, 1, {'maxOccurs': 'unbounded', 'minOccurs': '0', 'name': 'folders', 'type': 'Folder'}, None),
    }
    subclass = None
    superclass = None
    def __init__(self, name=None, files=None, folders=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name = _cast(None, name)
        self.name_nsprefix_ = None
        if files is None:
            self.files = []
        else:
            self.files = files
        self.files_nsprefix_ = None
        if folders is None:
            self.folders = []
        else:
            self.folders = folders
        self.folders_nsprefix_ = None
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Folder)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Folder.subclass:
            return Folder.subclass(*args_, **kwargs_)
        else:
            return Folder(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_files(self):
        return self.files
    def set_files(self, files):
        self.files = files
    def add_files(self, value):
        self.files.append(value)
    def insert_files_at(self, index, value):
        self.files.insert(index, value)
    def replace_files_at(self, index, value):
        self.files[index] = value
    def get_folders(self):
        return self.folders
    def set_folders(self, folders):
        self.folders = folders
    def add_folders(self, value):
        self.folders.append(value)
    def insert_folders_at(self, index, value):
        self.folders.insert(index, value)
    def replace_folders_at(self, index, value):
        self.folders[index] = value
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def _hasContent(self):
        if (
            self.files or
            self.folders
        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='Folder', mapping_=None, reverse_mapping_=None, nsmap_=None):
        if parent_element is None:
            element = etree_.Element('{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        else:
            element = etree_.SubElement(parent_element, '{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        if self.extensiontype_ is not None:
            element.set('{http://www.w3.org/2001/XMLSchema-instance}type', self.extensiontype_)
        if self.name is not None:
            element.set('name', self.gds_format_string(self.name))
        for files_ in self.files:
            files_.to_etree(element, name_='files', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        for folders_ in self.folders:
            folders_.to_etree(element, name_='folders', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.name, 'name')
        self.gds_check_cardinality_(self.name, 'name', required=True)
        # validate simple type children
        # validate complex type children
        self.gds_check_cardinality_(self.files, 'files', min_occurs=0, max_occurs=9999999)
        self.gds_check_cardinality_(self.folders, 'folders', min_occurs=0, max_occurs=9999999)
        if recursive:
            for item in self.files:
                item.validate_(gds_collector, recursive=True)
            for item in self.folders:
                item.validate_(gds_collector, recursive=True)
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
        # generate complex type children
        level += 1
        if self.files:
            for o in self.files:
                yield from o.generateRecursively_(level)
        if self.folders:
            for o in self.folders:
                yield from o.generateRecursively_(level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('name', node)
        if value is not None and 'name' not in already_processed:
            already_processed.add('name')
            self.name = value
        value = find_attr_value_('xsi:type', node)
        if value is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            self.extensiontype_ = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'files':
            class_obj_ = self.get_class_obj_(child_, File)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.files.append(obj_)
            obj_.original_tagname_ = 'files'
        elif nodeName_ == 'folders':
            class_obj_ = self.get_class_obj_(child_, Folder)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.folders.append(obj_)
            obj_.original_tagname_ = 'folders'
# end class Folder


class DatatypeFolder(Folder):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'artifacts': MemberSpec_('artifacts', 'Artifact', 1, 1, {'maxOccurs': 'unbounded', 'minOccurs': '0', 'name': 'artifacts', 'type': 'Artifact'}, None),
    }
    subclass = None
    superclass = Folder
    def __init__(self, name=None, files=None, folders=None, artifacts=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("DatatypeFolder"), self).__init__(name, files, folders,  **kwargs_)
        if artifacts is None:
            self.artifacts = []
        else:
            self.artifacts = artifacts
        self.artifacts_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatatypeFolder)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatatypeFolder.subclass:
            return DatatypeFolder.subclass(*args_, **kwargs_)
        else:
            return DatatypeFolder(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_artifacts(self):
        return self.artifacts
    def set_artifacts(self, artifacts):
        self.artifacts = artifacts
    def add_artifacts(self, value):
        self.artifacts.append(value)
    def insert_artifacts_at(self, index, value):
        self.artifacts.insert(index, value)
    def replace_artifacts_at(self, index, value):
        self.artifacts[index] = value
    def _hasContent(self):
        if (
            self.artifacts or
            super(DatatypeFolder, self)._hasContent()
        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='DatatypeFolder', mapping_=None, reverse_mapping_=None, nsmap_=None):
        element = super(DatatypeFolder, self).to_etree(parent_element, name_, mapping_, reverse_mapping_, nsmap_)
        for artifacts_ in self.artifacts:
            artifacts_.to_etree(element, name_='artifacts', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        # validate simple type children
        # validate complex type children
        self.gds_check_cardinality_(self.artifacts, 'artifacts', min_occurs=0, max_occurs=9999999)
        if recursive:
            for item in self.artifacts:
                item.validate_(gds_collector, recursive=True)
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
        # generate complex type children
        level += 1
        if self.artifacts:
            for o in self.artifacts:
                yield from o.generateRecursively_(level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        super(DatatypeFolder, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'artifacts':
            obj_ = Artifact.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.artifacts.append(obj_)
            obj_.original_tagname_ = 'artifacts'
        super(DatatypeFolder, self)._buildChildren(child_, node, nodeName_, True)
# end class DatatypeFolder


class Artifact(File):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'suffix': MemberSpec_('suffix', 'string', 0, 0, {'use': 'required', 'name': 'suffix'}),
        'entities': MemberSpec_('entities', 'EntityRef', 1, 0, {'maxOccurs': 'unbounded', 'minOccurs': '1', 'name': 'entities', 'type': 'EntityRef'}, None),
    }
    subclass = None
    superclass = File
    def __init__(self, name=None, extension=None, uri=None, suffix=None, entities=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("Artifact"), self).__init__(name, extension, uri,  **kwargs_)
        self.suffix = _cast(None, suffix)
        self.suffix_nsprefix_ = None
        if entities is None:
            self.entities = []
        else:
            self.entities = entities
        self.entities_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Artifact)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Artifact.subclass:
            return Artifact.subclass(*args_, **kwargs_)
        else:
            return Artifact(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_entities(self):
        return self.entities
    def set_entities(self, entities):
        self.entities = entities
    def add_entities(self, value):
        self.entities.append(value)
    def insert_entities_at(self, index, value):
        self.entities.insert(index, value)
    def replace_entities_at(self, index, value):
        self.entities[index] = value
    def get_suffix(self):
        return self.suffix
    def set_suffix(self, suffix):
        self.suffix = suffix
    def _hasContent(self):
        if (
            self.entities or
            super(Artifact, self)._hasContent()
        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='Artifact', mapping_=None, reverse_mapping_=None, nsmap_=None):
        element = super(Artifact, self).to_etree(parent_element, name_, mapping_, reverse_mapping_, nsmap_)
        if self.suffix is not None:
            element.set('suffix', self.gds_format_string(self.suffix))
        for entities_ in self.entities:
            entities_.to_etree(element, name_='entities', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.suffix, 'suffix')
        self.gds_check_cardinality_(self.suffix, 'suffix', required=True)
        # validate simple type children
        # validate complex type children
        self.gds_check_cardinality_(self.entities, 'entities', min_occurs=1, max_occurs=9999999)
        if recursive:
            for item in self.entities:
                item.validate_(gds_collector, recursive=True)
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
        # generate complex type children
        level += 1
        if self.entities:
            for o in self.entities:
                yield from o.generateRecursively_(level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('suffix', node)
        if value is not None and 'suffix' not in already_processed:
            already_processed.add('suffix')
            self.suffix = value
        super(Artifact, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'entities':
            obj_ = EntityRef.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.entities.append(obj_)
            obj_.original_tagname_ = 'entities'
        super(Artifact, self)._buildChildren(child_, node, nodeName_, True)
# end class Artifact


class EntityRef(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'key': MemberSpec_('key', 'string', 0, 1, {'use': 'optional', 'name': 'key'}),
        'value': MemberSpec_('value', 'string', 0, 1, {'use': 'optional', 'name': 'value'}),
    }
    subclass = None
    superclass = None
    def __init__(self, key=None, value=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.key = _cast(None, key)
        self.key_nsprefix_ = None
        self.value = _cast(None, value)
        self.value_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, EntityRef)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EntityRef.subclass:
            return EntityRef.subclass(*args_, **kwargs_)
        else:
            return EntityRef(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_key(self):
        return self.key
    def set_key(self, key):
        self.key = key
    def get_value(self):
        return self.value
    def set_value(self, value):
        self.value = value
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='EntityRef', mapping_=None, reverse_mapping_=None, nsmap_=None):
        if parent_element is None:
            element = etree_.Element('{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        else:
            element = etree_.SubElement(parent_element, '{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        if self.key is not None:
            element.set('key', self.gds_format_string(self.key))
        if self.value is not None:
            element.set('value', self.gds_format_string(self.value))
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.key, 'key')
        self.gds_check_cardinality_(self.key, 'key', required=False)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.value, 'value')
        self.gds_check_cardinality_(self.value, 'value', required=False)
        # validate simple type children
        # validate complex type children
        if recursive:
            pass
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('key', node)
        if value is not None and 'key' not in already_processed:
            already_processed.add('key')
            self.key = value
        value = find_attr_value_('value', node)
        if value is not None and 'value' not in already_processed:
            already_processed.add('value')
            self.value = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class EntityRef


class Entity(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'name': MemberSpec_('name', 'string', 0, 0, {'use': 'required', 'name': 'name'}),
        'label': MemberSpec_('label', 'string', 0, 1, {'use': 'optional', 'name': 'label'}),
        'key': MemberSpec_('key', 'string', 0, 0, {'use': 'required', 'name': 'key'}),
        'description': MemberSpec_('description', 'string', 0, 0, {'use': 'required', 'name': 'description'}),
        'type_': MemberSpec_('type_', 'string', 0, 0, {'use': 'required', 'name': 'type_'}),
        'format': MemberSpec_('format', 'string', 0, 1, {'use': 'optional', 'name': 'format'}),
    }
    subclass = None
    superclass = None
    def __init__(self, name=None, label=None, key=None, description=None, type_=None, format=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name = _cast(None, name)
        self.name_nsprefix_ = None
        self.label = _cast(None, label)
        self.label_nsprefix_ = None
        self.key = _cast(None, key)
        self.key_nsprefix_ = None
        self.description = _cast(None, description)
        self.description_nsprefix_ = None
        self.type_ = _cast(None, type_)
        self.type__nsprefix_ = None
        self.format = _cast(None, format)
        self.format_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Entity)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Entity.subclass:
            return Entity.subclass(*args_, **kwargs_)
        else:
            return Entity(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_label(self):
        return self.label
    def set_label(self, label):
        self.label = label
    def get_key(self):
        return self.key
    def set_key(self, key):
        self.key = key
    def get_description(self):
        return self.description
    def set_description(self, description):
        self.description = description
    def get_type(self):
        return self.type_
    def set_type(self, type_):
        self.type_ = type_
    def get_format(self):
        return self.format
    def set_format(self, format):
        self.format = format
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='Entity', mapping_=None, reverse_mapping_=None, nsmap_=None):
        if parent_element is None:
            element = etree_.Element('{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        else:
            element = etree_.SubElement(parent_element, '{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        if self.name is not None:
            element.set('name', self.gds_format_string(self.name))
        if self.label is not None:
            element.set('label', self.gds_format_string(self.label))
        if self.key is not None:
            element.set('key', self.gds_format_string(self.key))
        if self.description is not None:
            element.set('description', self.gds_format_string(self.description))
        if self.type_ is not None:
            element.set('type', self.gds_format_string(self.type_))
        if self.format is not None:
            element.set('format', self.gds_format_string(self.format))
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.name, 'name')
        self.gds_check_cardinality_(self.name, 'name', required=True)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.label, 'label')
        self.gds_check_cardinality_(self.label, 'label', required=False)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.key, 'key')
        self.gds_check_cardinality_(self.key, 'key', required=True)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.description, 'description')
        self.gds_check_cardinality_(self.description, 'description', required=True)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.type_, 'type_')
        self.gds_check_cardinality_(self.type_, 'type_', required=True)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.format, 'format')
        self.gds_check_cardinality_(self.format, 'format', required=False)
        # validate simple type children
        # validate complex type children
        if recursive:
            pass
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('name', node)
        if value is not None and 'name' not in already_processed:
            already_processed.add('name')
            self.name = value
        value = find_attr_value_('label', node)
        if value is not None and 'label' not in already_processed:
            already_processed.add('label')
            self.label = value
        value = find_attr_value_('key', node)
        if value is not None and 'key' not in already_processed:
            already_processed.add('key')
            self.key = value
        value = find_attr_value_('description', node)
        if value is not None and 'description' not in already_processed:
            already_processed.add('description')
            self.description = value
        value = find_attr_value_('type', node)
        if value is not None and 'type' not in already_processed:
            already_processed.add('type')
            self.type_ = value
        value = find_attr_value_('format', node)
        if value is not None and 'format' not in already_processed:
            already_processed.add('format')
            self.format = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class Entity


class Suffix(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'name': MemberSpec_('name', 'string', 0, 0, {'use': 'required', 'name': 'name'}),
        'description': MemberSpec_('description', 'string', 0, 0, {'use': 'required', 'name': 'description'}),
        'unit': MemberSpec_('unit', 'string', 0, 1, {'use': 'optional', 'name': 'unit'}),
    }
    subclass = None
    superclass = None
    def __init__(self, name=None, description=None, unit=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name = _cast(None, name)
        self.name_nsprefix_ = None
        self.description = _cast(None, description)
        self.description_nsprefix_ = None
        self.unit = _cast(None, unit)
        self.unit_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Suffix)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Suffix.subclass:
            return Suffix.subclass(*args_, **kwargs_)
        else:
            return Suffix(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_description(self):
        return self.description
    def set_description(self, description):
        self.description = description
    def get_unit(self):
        return self.unit
    def set_unit(self, unit):
        self.unit = unit
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='Suffix', mapping_=None, reverse_mapping_=None, nsmap_=None):
        if parent_element is None:
            element = etree_.Element('{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        else:
            element = etree_.SubElement(parent_element, '{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        if self.name is not None:
            element.set('name', self.gds_format_string(self.name))
        if self.description is not None:
            element.set('description', self.gds_format_string(self.description))
        if self.unit is not None:
            element.set('unit', self.gds_format_string(self.unit))
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.name, 'name')
        self.gds_check_cardinality_(self.name, 'name', required=True)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.description, 'description')
        self.gds_check_cardinality_(self.description, 'description', required=True)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.unit, 'unit')
        self.gds_check_cardinality_(self.unit, 'unit', required=False)
        # validate simple type children
        # validate complex type children
        if recursive:
            pass
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('name', node)
        if value is not None and 'name' not in already_processed:
            already_processed.add('name')
            self.name = value
        value = find_attr_value_('description', node)
        if value is not None and 'description' not in already_processed:
            already_processed.add('description')
            self.description = value
        value = find_attr_value_('unit', node)
        if value is not None and 'unit' not in already_processed:
            already_processed.add('unit')
            self.unit = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class Suffix


class Modality(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'key': MemberSpec_('key', 'string', 0, 1, {'use': 'optional', 'name': 'key'}),
        'name': MemberSpec_('name', 'string', 0, 1, {'use': 'optional', 'name': 'name'}),
        'datatypes': MemberSpec_('datatypes', 'string', 1, 0, {'maxOccurs': 'unbounded', 'minOccurs': '1', 'name': 'datatypes', 'type': 'string'}, None),
    }
    subclass = None
    superclass = None
    def __init__(self, key=None, name=None, datatypes=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.key = _cast(None, key)
        self.key_nsprefix_ = None
        self.name = _cast(None, name)
        self.name_nsprefix_ = None
        if datatypes is None:
            self.datatypes = []
        else:
            self.datatypes = datatypes
        self.datatypes_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Modality)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Modality.subclass:
            return Modality.subclass(*args_, **kwargs_)
        else:
            return Modality(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_datatypes(self):
        return self.datatypes
    def set_datatypes(self, datatypes):
        self.datatypes = datatypes
    def add_datatypes(self, value):
        self.datatypes.append(value)
    def insert_datatypes_at(self, index, value):
        self.datatypes.insert(index, value)
    def replace_datatypes_at(self, index, value):
        self.datatypes[index] = value
    def get_key(self):
        return self.key
    def set_key(self, key):
        self.key = key
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def _hasContent(self):
        if (
            self.datatypes
        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='Modality', mapping_=None, reverse_mapping_=None, nsmap_=None):
        if parent_element is None:
            element = etree_.Element('{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        else:
            element = etree_.SubElement(parent_element, '{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        if self.key is not None:
            element.set('key', self.gds_format_string(self.key))
        if self.name is not None:
            element.set('name', self.gds_format_string(self.name))
        for datatypes_ in self.datatypes:
            etree_.SubElement(element, '{https://bids.neuroimaging.io/1.6}datatypes').text = self.gds_format_string(datatypes_)
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.key, 'key')
        self.gds_check_cardinality_(self.key, 'key', required=False)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.name, 'name')
        self.gds_check_cardinality_(self.name, 'name', required=False)
        # validate simple type children
        for item in self.datatypes:
            self.gds_validate_builtin_ST_(self.gds_validate_string, item, 'datatypes')
        self.gds_check_cardinality_(self.datatypes, 'datatypes', min_occurs=1, max_occurs=9999999)
        # validate complex type children
        if recursive:
            pass
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('key', node)
        if value is not None and 'key' not in already_processed:
            already_processed.add('key')
            self.key = value
        value = find_attr_value_('name', node)
        if value is not None and 'name' not in already_processed:
            already_processed.add('name')
            self.name = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'datatypes':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'datatypes')
            value_ = self.gds_validate_string(value_, node, 'datatypes')
            self.datatypes.append(value_)
            self.datatypes_nsprefix_ = child_.prefix
# end class Modality


class Datatype(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'name': MemberSpec_('name', 'string', 0, 1, {'use': 'optional', 'name': 'name'}),
        'contexts': MemberSpec_('contexts', 'DatatypeContext', 1, 0, {'maxOccurs': 'unbounded', 'minOccurs': '1', 'name': 'contexts', 'type': 'DatatypeContext'}, None),
    }
    subclass = None
    superclass = None
    def __init__(self, name=None, contexts=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name = _cast(None, name)
        self.name_nsprefix_ = None
        if contexts is None:
            self.contexts = []
        else:
            self.contexts = contexts
        self.contexts_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Datatype)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Datatype.subclass:
            return Datatype.subclass(*args_, **kwargs_)
        else:
            return Datatype(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_contexts(self):
        return self.contexts
    def set_contexts(self, contexts):
        self.contexts = contexts
    def add_contexts(self, value):
        self.contexts.append(value)
    def insert_contexts_at(self, index, value):
        self.contexts.insert(index, value)
    def replace_contexts_at(self, index, value):
        self.contexts[index] = value
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def _hasContent(self):
        if (
            self.contexts
        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='Datatype', mapping_=None, reverse_mapping_=None, nsmap_=None):
        if parent_element is None:
            element = etree_.Element('{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        else:
            element = etree_.SubElement(parent_element, '{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        if self.name is not None:
            element.set('name', self.gds_format_string(self.name))
        for contexts_ in self.contexts:
            contexts_.to_etree(element, name_='contexts', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.name, 'name')
        self.gds_check_cardinality_(self.name, 'name', required=False)
        # validate simple type children
        # validate complex type children
        self.gds_check_cardinality_(self.contexts, 'contexts', min_occurs=1, max_occurs=9999999)
        if recursive:
            for item in self.contexts:
                item.validate_(gds_collector, recursive=True)
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
        # generate complex type children
        level += 1
        if self.contexts:
            for o in self.contexts:
                yield from o.generateRecursively_(level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('name', node)
        if value is not None and 'name' not in already_processed:
            already_processed.add('name')
            self.name = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'contexts':
            obj_ = DatatypeContext.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.contexts.append(obj_)
            obj_.original_tagname_ = 'contexts'
# end class Datatype


class EntityDep(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'key': MemberSpec_('key', 'string', 0, 0, {'use': 'required', 'name': 'key'}),
        'required': MemberSpec_('required', 'boolean', 0, 0, {'use': 'required', 'name': 'required'}),
    }
    subclass = None
    superclass = None
    def __init__(self, key=None, required=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.key = _cast(None, key)
        self.key_nsprefix_ = None
        self.required = _cast(bool, required)
        self.required_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, EntityDep)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EntityDep.subclass:
            return EntityDep.subclass(*args_, **kwargs_)
        else:
            return EntityDep(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_key(self):
        return self.key
    def set_key(self, key):
        self.key = key
    def get_required(self):
        return self.required
    def set_required(self, required):
        self.required = required
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='EntityDep', mapping_=None, reverse_mapping_=None, nsmap_=None):
        if parent_element is None:
            element = etree_.Element('{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        else:
            element = etree_.SubElement(parent_element, '{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        if self.key is not None:
            element.set('key', self.gds_format_string(self.key))
        if self.required is not None:
            element.set('required', self.gds_format_boolean(self.required))
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.key, 'key')
        self.gds_check_cardinality_(self.key, 'key', required=True)
        self.gds_validate_builtin_ST_(self.gds_validate_boolean, self.required, 'required')
        self.gds_check_cardinality_(self.required, 'required', required=True)
        # validate simple type children
        # validate complex type children
        if recursive:
            pass
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('key', node)
        if value is not None and 'key' not in already_processed:
            already_processed.add('key')
            self.key = value
        value = find_attr_value_('required', node)
        if value is not None and 'required' not in already_processed:
            already_processed.add('required')
            if value in ('true', '1'):
                self.required = True
            elif value in ('false', '0'):
                self.required = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class EntityDep


class DatatypeContext(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'name': MemberSpec_('name', 'string', 0, 1, {'use': 'optional', 'name': 'name'}),
        'suffixes': MemberSpec_('suffixes', 'string', 1, 0, {'maxOccurs': 'unbounded', 'minOccurs': '1', 'name': 'suffixes', 'type': 'string'}, None),
        'extensions': MemberSpec_('extensions', 'string', 1, 0, {'maxOccurs': 'unbounded', 'minOccurs': '1', 'name': 'extensions', 'type': 'string'}, None),
        'entities': MemberSpec_('entities', 'EntityDep', 1, 0, {'maxOccurs': 'unbounded', 'minOccurs': '1', 'name': 'entities', 'type': 'EntityDep'}, None),
    }
    subclass = None
    superclass = None
    def __init__(self, name=None, suffixes=None, extensions=None, entities=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name = _cast(None, name)
        self.name_nsprefix_ = None
        if suffixes is None:
            self.suffixes = []
        else:
            self.suffixes = suffixes
        self.suffixes_nsprefix_ = None
        if extensions is None:
            self.extensions = []
        else:
            self.extensions = extensions
        self.extensions_nsprefix_ = None
        if entities is None:
            self.entities = []
        else:
            self.entities = entities
        self.entities_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatatypeContext)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatatypeContext.subclass:
            return DatatypeContext.subclass(*args_, **kwargs_)
        else:
            return DatatypeContext(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_suffixes(self):
        return self.suffixes
    def set_suffixes(self, suffixes):
        self.suffixes = suffixes
    def add_suffixes(self, value):
        self.suffixes.append(value)
    def insert_suffixes_at(self, index, value):
        self.suffixes.insert(index, value)
    def replace_suffixes_at(self, index, value):
        self.suffixes[index] = value
    def get_extensions(self):
        return self.extensions
    def set_extensions(self, extensions):
        self.extensions = extensions
    def add_extensions(self, value):
        self.extensions.append(value)
    def insert_extensions_at(self, index, value):
        self.extensions.insert(index, value)
    def replace_extensions_at(self, index, value):
        self.extensions[index] = value
    def get_entities(self):
        return self.entities
    def set_entities(self, entities):
        self.entities = entities
    def add_entities(self, value):
        self.entities.append(value)
    def insert_entities_at(self, index, value):
        self.entities.insert(index, value)
    def replace_entities_at(self, index, value):
        self.entities[index] = value
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def _hasContent(self):
        if (
            self.suffixes or
            self.extensions or
            self.entities
        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='DatatypeContext', mapping_=None, reverse_mapping_=None, nsmap_=None):
        if parent_element is None:
            element = etree_.Element('{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        else:
            element = etree_.SubElement(parent_element, '{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        if self.name is not None:
            element.set('name', self.gds_format_string(self.name))
        for suffixes_ in self.suffixes:
            etree_.SubElement(element, '{https://bids.neuroimaging.io/1.6}suffixes').text = self.gds_format_string(suffixes_)
        for extensions_ in self.extensions:
            etree_.SubElement(element, '{https://bids.neuroimaging.io/1.6}extensions').text = self.gds_format_string(extensions_)
        for entities_ in self.entities:
            entities_.to_etree(element, name_='entities', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.name, 'name')
        self.gds_check_cardinality_(self.name, 'name', required=False)
        # validate simple type children
        for item in self.suffixes:
            self.gds_validate_builtin_ST_(self.gds_validate_string, item, 'suffixes')
        self.gds_check_cardinality_(self.suffixes, 'suffixes', min_occurs=1, max_occurs=9999999)
        for item in self.extensions:
            self.gds_validate_builtin_ST_(self.gds_validate_string, item, 'extensions')
        self.gds_check_cardinality_(self.extensions, 'extensions', min_occurs=1, max_occurs=9999999)
        # validate complex type children
        self.gds_check_cardinality_(self.entities, 'entities', min_occurs=1, max_occurs=9999999)
        if recursive:
            for item in self.entities:
                item.validate_(gds_collector, recursive=True)
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
        # generate complex type children
        level += 1
        if self.entities:
            for o in self.entities:
                yield from o.generateRecursively_(level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('name', node)
        if value is not None and 'name' not in already_processed:
            already_processed.add('name')
            self.name = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'suffixes':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'suffixes')
            value_ = self.gds_validate_string(value_, node, 'suffixes')
            self.suffixes.append(value_)
            self.suffixes_nsprefix_ = child_.prefix
        elif nodeName_ == 'extensions':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'extensions')
            value_ = self.gds_validate_string(value_, node, 'extensions')
            self.extensions.append(value_)
            self.extensions_nsprefix_ = child_.prefix
        elif nodeName_ == 'entities':
            obj_ = EntityDep.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.entities.append(obj_)
            obj_.original_tagname_ = 'entities'
# end class DatatypeContext


class Metadata(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'datatypes': MemberSpec_('datatypes', 'Datatype', 1, 1, {'maxOccurs': 'unbounded', 'minOccurs': '0', 'name': 'datatypes', 'type': 'Datatype'}, None),
        'entities': MemberSpec_('entities', 'Entity', 1, 1, {'maxOccurs': 'unbounded', 'minOccurs': '0', 'name': 'entities', 'type': 'Entity'}, None),
        'modalities': MemberSpec_('modalities', 'Modality', 1, 1, {'maxOccurs': 'unbounded', 'minOccurs': '0', 'name': 'modalities', 'type': 'Modality'}, None),
    }
    subclass = None
    superclass = None
    def __init__(self, datatypes=None, entities=None, modalities=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if datatypes is None:
            self.datatypes = []
        else:
            self.datatypes = datatypes
        self.datatypes_nsprefix_ = None
        if entities is None:
            self.entities = []
        else:
            self.entities = entities
        self.entities_nsprefix_ = None
        if modalities is None:
            self.modalities = []
        else:
            self.modalities = modalities
        self.modalities_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Metadata)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Metadata.subclass:
            return Metadata.subclass(*args_, **kwargs_)
        else:
            return Metadata(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_datatypes(self):
        return self.datatypes
    def set_datatypes(self, datatypes):
        self.datatypes = datatypes
    def add_datatypes(self, value):
        self.datatypes.append(value)
    def insert_datatypes_at(self, index, value):
        self.datatypes.insert(index, value)
    def replace_datatypes_at(self, index, value):
        self.datatypes[index] = value
    def get_entities(self):
        return self.entities
    def set_entities(self, entities):
        self.entities = entities
    def add_entities(self, value):
        self.entities.append(value)
    def insert_entities_at(self, index, value):
        self.entities.insert(index, value)
    def replace_entities_at(self, index, value):
        self.entities[index] = value
    def get_modalities(self):
        return self.modalities
    def set_modalities(self, modalities):
        self.modalities = modalities
    def add_modalities(self, value):
        self.modalities.append(value)
    def insert_modalities_at(self, index, value):
        self.modalities.insert(index, value)
    def replace_modalities_at(self, index, value):
        self.modalities[index] = value
    def _hasContent(self):
        if (
            self.datatypes or
            self.entities or
            self.modalities
        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='Metadata', mapping_=None, reverse_mapping_=None, nsmap_=None):
        if parent_element is None:
            element = etree_.Element('{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        else:
            element = etree_.SubElement(parent_element, '{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        for datatypes_ in self.datatypes:
            datatypes_.to_etree(element, name_='datatypes', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        for entities_ in self.entities:
            entities_.to_etree(element, name_='entities', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        for modalities_ in self.modalities:
            modalities_.to_etree(element, name_='modalities', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        # validate simple type children
        # validate complex type children
        self.gds_check_cardinality_(self.datatypes, 'datatypes', min_occurs=0, max_occurs=9999999)
        self.gds_check_cardinality_(self.entities, 'entities', min_occurs=0, max_occurs=9999999)
        self.gds_check_cardinality_(self.modalities, 'modalities', min_occurs=0, max_occurs=9999999)
        if recursive:
            for item in self.datatypes:
                item.validate_(gds_collector, recursive=True)
            for item in self.entities:
                item.validate_(gds_collector, recursive=True)
            for item in self.modalities:
                item.validate_(gds_collector, recursive=True)
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
        # generate complex type children
        level += 1
        if self.datatypes:
            for o in self.datatypes:
                yield from o.generateRecursively_(level)
        if self.entities:
            for o in self.entities:
                yield from o.generateRecursively_(level)
        if self.modalities:
            for o in self.modalities:
                yield from o.generateRecursively_(level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'datatypes':
            obj_ = Datatype.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.datatypes.append(obj_)
            obj_.original_tagname_ = 'datatypes'
        elif nodeName_ == 'entities':
            obj_ = Entity.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.entities.append(obj_)
            obj_.original_tagname_ = 'entities'
        elif nodeName_ == 'modalities':
            obj_ = Modality.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.modalities.append(obj_)
            obj_.original_tagname_ = 'modalities'
# end class Metadata


class JsonFile(File):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'keys': MemberSpec_('keys', 'JsonFileFlatEntry', 1, 1, {'maxOccurs': 'unbounded', 'minOccurs': '0', 'name': 'keys', 'type': 'JsonFileFlatEntry'}, None),
    }
    subclass = None
    superclass = File
    def __init__(self, name=None, extension=None, uri=None, keys=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("JsonFile"), self).__init__(name, extension, uri, extensiontype_,  **kwargs_)
        if keys is None:
            self.keys = []
        else:
            self.keys = keys
        self.keys_nsprefix_ = None
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, JsonFile)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if JsonFile.subclass:
            return JsonFile.subclass(*args_, **kwargs_)
        else:
            return JsonFile(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_keys(self):
        return self.keys
    def set_keys(self, keys):
        self.keys = keys
    def add_keys(self, value):
        self.keys.append(value)
    def insert_keys_at(self, index, value):
        self.keys.insert(index, value)
    def replace_keys_at(self, index, value):
        self.keys[index] = value
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def _hasContent(self):
        if (
            self.keys or
            super(JsonFile, self)._hasContent()
        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='JsonFile', mapping_=None, reverse_mapping_=None, nsmap_=None):
        element = super(JsonFile, self).to_etree(parent_element, name_, mapping_, reverse_mapping_, nsmap_)
        if self.extensiontype_ is not None:
            element.set('{http://www.w3.org/2001/XMLSchema-instance}type', self.extensiontype_)
        for keys_ in self.keys:
            keys_.to_etree(element, name_='keys', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        # validate simple type children
        # validate complex type children
        self.gds_check_cardinality_(self.keys, 'keys', min_occurs=0, max_occurs=9999999)
        if recursive:
            for item in self.keys:
                item.validate_(gds_collector, recursive=True)
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
        # generate complex type children
        level += 1
        if self.keys:
            for o in self.keys:
                yield from o.generateRecursively_(level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('xsi:type', node)
        if value is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            self.extensiontype_ = value
        super(JsonFile, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'keys':
            obj_ = JsonFileFlatEntry.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.keys.append(obj_)
            obj_.original_tagname_ = 'keys'
        super(JsonFile, self)._buildChildren(child_, node, nodeName_, True)
# end class JsonFile


class JsonFileFlatEntry(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'key': MemberSpec_('key', 'string', 0, 0, {'use': 'required', 'name': 'key'}),
        'value': MemberSpec_('value', 'string', 0, 0, {'use': 'required', 'name': 'value'}),
    }
    subclass = None
    superclass = None
    def __init__(self, key=None, value=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.key = _cast(None, key)
        self.key_nsprefix_ = None
        self.value = _cast(None, value)
        self.value_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, JsonFileFlatEntry)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if JsonFileFlatEntry.subclass:
            return JsonFileFlatEntry.subclass(*args_, **kwargs_)
        else:
            return JsonFileFlatEntry(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_key(self):
        return self.key
    def set_key(self, key):
        self.key = key
    def get_value(self):
        return self.value
    def set_value(self, value):
        self.value = value
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='JsonFileFlatEntry', mapping_=None, reverse_mapping_=None, nsmap_=None):
        if parent_element is None:
            element = etree_.Element('{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        else:
            element = etree_.SubElement(parent_element, '{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        if self.key is not None:
            element.set('key', self.gds_format_string(self.key))
        if self.value is not None:
            element.set('value', self.gds_format_string(self.value))
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.key, 'key')
        self.gds_check_cardinality_(self.key, 'key', required=True)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.value, 'value')
        self.gds_check_cardinality_(self.value, 'value', required=True)
        # validate simple type children
        # validate complex type children
        if recursive:
            pass
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('key', node)
        if value is not None and 'key' not in already_processed:
            already_processed.add('key')
            self.key = value
        value = find_attr_value_('value', node)
        if value is not None and 'value' not in already_processed:
            already_processed.add('value')
            self.value = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class JsonFileFlatEntry


class FileMatcher(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
    }
    subclass = None
    superclass = None
    def __init__(self, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, FileMatcher)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if FileMatcher.subclass:
            return FileMatcher.subclass(*args_, **kwargs_)
        else:
            return FileMatcher(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='FileMatcher', mapping_=None, reverse_mapping_=None, nsmap_=None):
        if parent_element is None:
            element = etree_.Element('{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        else:
            element = etree_.SubElement(parent_element, '{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        # validate simple type children
        # validate complex type children
        if recursive:
            pass
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class FileMatcher


class TsvSidecarFile(JsonFile):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'columns': MemberSpec_('columns', 'SidecarColumnDescriptor', 1, 0, {'maxOccurs': 'unbounded', 'minOccurs': '1', 'name': 'columns', 'type': 'SidecarColumnDescriptor'}, None),
    }
    subclass = None
    superclass = JsonFile
    def __init__(self, name=None, extension=None, uri=None, keys=None, columns=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("TsvSidecarFile"), self).__init__(name, extension, uri, keys,  **kwargs_)
        if columns is None:
            self.columns = []
        else:
            self.columns = columns
        self.columns_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TsvSidecarFile)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TsvSidecarFile.subclass:
            return TsvSidecarFile.subclass(*args_, **kwargs_)
        else:
            return TsvSidecarFile(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_columns(self):
        return self.columns
    def set_columns(self, columns):
        self.columns = columns
    def add_columns(self, value):
        self.columns.append(value)
    def insert_columns_at(self, index, value):
        self.columns.insert(index, value)
    def replace_columns_at(self, index, value):
        self.columns[index] = value
    def _hasContent(self):
        if (
            self.columns or
            super(TsvSidecarFile, self)._hasContent()
        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='TsvSidecarFile', mapping_=None, reverse_mapping_=None, nsmap_=None):
        element = super(TsvSidecarFile, self).to_etree(parent_element, name_, mapping_, reverse_mapping_, nsmap_)
        for columns_ in self.columns:
            columns_.to_etree(element, name_='columns', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        # validate simple type children
        # validate complex type children
        self.gds_check_cardinality_(self.columns, 'columns', min_occurs=1, max_occurs=9999999)
        if recursive:
            for item in self.columns:
                item.validate_(gds_collector, recursive=True)
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
        # generate complex type children
        level += 1
        if self.columns:
            for o in self.columns:
                yield from o.generateRecursively_(level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        super(TsvSidecarFile, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'columns':
            obj_ = SidecarColumnDescriptor.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.columns.append(obj_)
            obj_.original_tagname_ = 'columns'
        super(TsvSidecarFile, self)._buildChildren(child_, node, nodeName_, True)
# end class TsvSidecarFile


class TsvFile(File):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
    }
    subclass = None
    superclass = File
    def __init__(self, name=None, extension=None, uri=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("TsvFile"), self).__init__(name, extension, uri, extensiontype_,  **kwargs_)
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TsvFile)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TsvFile.subclass:
            return TsvFile.subclass(*args_, **kwargs_)
        else:
            return TsvFile(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def _hasContent(self):
        if (
            super(TsvFile, self)._hasContent()
        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='TsvFile', mapping_=None, reverse_mapping_=None, nsmap_=None):
        element = super(TsvFile, self).to_etree(parent_element, name_, mapping_, reverse_mapping_, nsmap_)
        if self.extensiontype_ is not None:
            element.set('{http://www.w3.org/2001/XMLSchema-instance}type', self.extensiontype_)
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        # validate simple type children
        # validate complex type children
        if recursive:
            pass
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('xsi:type', node)
        if value is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            self.extensiontype_ = value
        super(TsvFile, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        super(TsvFile, self)._buildChildren(child_, node, nodeName_, True)
        pass
# end class TsvFile


class ParticipantsTsvFileEntry(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'participant_id': MemberSpec_('participant_id', 'string', 0, 0, {'use': 'required', 'name': 'participant_id'}),
        'age': MemberSpec_('age', 'float', 0, 1, {'use': 'optional', 'name': 'age'}),
        'sex': MemberSpec_('sex', 'sexType', 0, 1, {'use': 'optional', 'name': 'sex'}),
        'handedness': MemberSpec_('handedness', 'handednessType', 0, 1, {'use': 'optional', 'name': 'handedness'}),
    }
    subclass = None
    superclass = None
    def __init__(self, participant_id=None, age=None, sex=None, handedness=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.participant_id = _cast(None, participant_id)
        self.participant_id_nsprefix_ = None
        self.age = _cast(float, age)
        self.age_nsprefix_ = None
        self.sex = _cast(None, sex)
        self.sex_nsprefix_ = None
        self.handedness = _cast(None, handedness)
        self.handedness_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ParticipantsTsvFileEntry)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ParticipantsTsvFileEntry.subclass:
            return ParticipantsTsvFileEntry.subclass(*args_, **kwargs_)
        else:
            return ParticipantsTsvFileEntry(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_participant_id(self):
        return self.participant_id
    def set_participant_id(self, participant_id):
        self.participant_id = participant_id
    def get_age(self):
        return self.age
    def set_age(self, age):
        self.age = age
    def get_sex(self):
        return self.sex
    def set_sex(self, sex):
        self.sex = sex
    def get_handedness(self):
        return self.handedness
    def set_handedness(self, handedness):
        self.handedness = handedness
    def validate_sexType(self, value):
        # Validate type sexType, a restriction on string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['male', 'Male', 'MALE', 'm', 'M', 'female', 'Female', 'f', 'F', 'other', 'Other', 'OTHER', 'o', 'O']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on sexType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
    def validate_handednessType(self, value):
        # Validate type handednessType, a restriction on string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['left', 'Left', 'LEFT', 'l', 'L', 'right', 'Right', 'RIGHT', 'r', 'R', 'ambidextrous', 'Ambidextrous', 'AMBIDEXTROUS', 'a', 'A']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on handednessType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='ParticipantsTsvFileEntry', mapping_=None, reverse_mapping_=None, nsmap_=None):
        if parent_element is None:
            element = etree_.Element('{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        else:
            element = etree_.SubElement(parent_element, '{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        if self.participant_id is not None:
            element.set('participant_id', self.gds_format_string(self.participant_id))
        if self.age is not None:
            element.set('age', self.gds_format_float(self.age))
        if self.sex is not None:
            element.set('sex', self.gds_format_string(self.sex))
        if self.handedness is not None:
            element.set('handedness', self.gds_format_string(self.handedness))
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.participant_id, 'participant_id')
        self.gds_check_cardinality_(self.participant_id, 'participant_id', required=True)
        self.gds_validate_builtin_ST_(self.gds_validate_float, self.age, 'age')
        self.gds_check_cardinality_(self.age, 'age', required=False)
        self.gds_validate_defined_ST_(self.validate_sexType, self.sex, 'sex')
        self.gds_check_cardinality_(self.sex, 'sex', required=False)
        self.gds_validate_defined_ST_(self.validate_handednessType, self.handedness, 'handedness')
        self.gds_check_cardinality_(self.handedness, 'handedness', required=False)
        # validate simple type children
        # validate complex type children
        if recursive:
            pass
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('participant_id', node)
        if value is not None and 'participant_id' not in already_processed:
            already_processed.add('participant_id')
            self.participant_id = value
        value = find_attr_value_('age', node)
        if value is not None and 'age' not in already_processed:
            already_processed.add('age')
            value = self.gds_parse_float(value, node, 'age')
            self.age = value
        value = find_attr_value_('sex', node)
        if value is not None and 'sex' not in already_processed:
            already_processed.add('sex')
            self.sex = value
            self.validate_sexType(self.sex)    # validate type sexType
        value = find_attr_value_('handedness', node)
        if value is not None and 'handedness' not in already_processed:
            already_processed.add('handedness')
            self.handedness = value
            self.validate_handednessType(self.handedness)    # validate type handednessType
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class ParticipantsTsvFileEntry


class SidecarColumnDescriptor(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'Name': MemberSpec_('Name', 'string', 0, 0, {'use': 'required', 'name': 'Name'}),
        'LongName': MemberSpec_('LongName', 'string', 0, 1, {'use': 'optional', 'name': 'LongName'}),
        'Description': MemberSpec_('Description', 'string', 0, 1, {'use': 'optional', 'name': 'Description'}),
        'Units': MemberSpec_('Units', 'string', 0, 1, {'use': 'optional', 'name': 'Units'}),
        'TermURL': MemberSpec_('TermURL', 'string', 0, 1, {'use': 'optional', 'name': 'TermURL'}),
        'Levels': MemberSpec_('Levels', 'KeyValuePair', 1, 1, {'maxOccurs': 'unbounded', 'minOccurs': '0', 'name': 'Levels', 'type': 'KeyValuePair'}, None),
    }
    subclass = None
    superclass = None
    def __init__(self, Name=None, LongName=None, Description=None, Units=None, TermURL=None, Levels=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Name = _cast(None, Name)
        self.Name_nsprefix_ = None
        self.LongName = _cast(None, LongName)
        self.LongName_nsprefix_ = None
        self.Description = _cast(None, Description)
        self.Description_nsprefix_ = None
        self.Units = _cast(None, Units)
        self.Units_nsprefix_ = None
        self.TermURL = _cast(None, TermURL)
        self.TermURL_nsprefix_ = None
        if Levels is None:
            self.Levels = []
        else:
            self.Levels = Levels
        self.Levels_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SidecarColumnDescriptor)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SidecarColumnDescriptor.subclass:
            return SidecarColumnDescriptor.subclass(*args_, **kwargs_)
        else:
            return SidecarColumnDescriptor(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Levels(self):
        return self.Levels
    def set_Levels(self, Levels):
        self.Levels = Levels
    def add_Levels(self, value):
        self.Levels.append(value)
    def insert_Levels_at(self, index, value):
        self.Levels.insert(index, value)
    def replace_Levels_at(self, index, value):
        self.Levels[index] = value
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def get_LongName(self):
        return self.LongName
    def set_LongName(self, LongName):
        self.LongName = LongName
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def get_Units(self):
        return self.Units
    def set_Units(self, Units):
        self.Units = Units
    def get_TermURL(self):
        return self.TermURL
    def set_TermURL(self, TermURL):
        self.TermURL = TermURL
    def _hasContent(self):
        if (
            self.Levels
        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='SidecarColumnDescriptor', mapping_=None, reverse_mapping_=None, nsmap_=None):
        if parent_element is None:
            element = etree_.Element('{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        else:
            element = etree_.SubElement(parent_element, '{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        if self.Name is not None:
            element.set('Name', self.gds_format_string(self.Name))
        if self.LongName is not None:
            element.set('LongName', self.gds_format_string(self.LongName))
        if self.Description is not None:
            element.set('Description', self.gds_format_string(self.Description))
        if self.Units is not None:
            element.set('Units', self.gds_format_string(self.Units))
        if self.TermURL is not None:
            element.set('TermURL', self.gds_format_string(self.TermURL))
        for Levels_ in self.Levels:
            Levels_.to_etree(element, name_='Levels', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.Name, 'Name')
        self.gds_check_cardinality_(self.Name, 'Name', required=True)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.LongName, 'LongName')
        self.gds_check_cardinality_(self.LongName, 'LongName', required=False)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.Description, 'Description')
        self.gds_check_cardinality_(self.Description, 'Description', required=False)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.Units, 'Units')
        self.gds_check_cardinality_(self.Units, 'Units', required=False)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.TermURL, 'TermURL')
        self.gds_check_cardinality_(self.TermURL, 'TermURL', required=False)
        # validate simple type children
        # validate complex type children
        self.gds_check_cardinality_(self.Levels, 'Levels', min_occurs=0, max_occurs=9999999)
        if recursive:
            for item in self.Levels:
                item.validate_(gds_collector, recursive=True)
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
        # generate complex type children
        level += 1
        if self.Levels:
            for o in self.Levels:
                yield from o.generateRecursively_(level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('Name', node)
        if value is not None and 'Name' not in already_processed:
            already_processed.add('Name')
            self.Name = value
        value = find_attr_value_('LongName', node)
        if value is not None and 'LongName' not in already_processed:
            already_processed.add('LongName')
            self.LongName = value
        value = find_attr_value_('Description', node)
        if value is not None and 'Description' not in already_processed:
            already_processed.add('Description')
            self.Description = value
        value = find_attr_value_('Units', node)
        if value is not None and 'Units' not in already_processed:
            already_processed.add('Units')
            self.Units = value
        value = find_attr_value_('TermURL', node)
        if value is not None and 'TermURL' not in already_processed:
            already_processed.add('TermURL')
            self.TermURL = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Levels':
            obj_ = KeyValuePair.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Levels.append(obj_)
            obj_.original_tagname_ = 'Levels'
# end class SidecarColumnDescriptor


class KeyValuePair(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'key': MemberSpec_('key', 'string', 0, 0, {'use': 'required', 'name': 'key'}),
        'value': MemberSpec_('value', 'string', 0, 0, {'use': 'required', 'name': 'value'}),
    }
    subclass = None
    superclass = None
    def __init__(self, key=None, value=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.key = _cast(None, key)
        self.key_nsprefix_ = None
        self.value = _cast(None, value)
        self.value_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, KeyValuePair)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if KeyValuePair.subclass:
            return KeyValuePair.subclass(*args_, **kwargs_)
        else:
            return KeyValuePair(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_key(self):
        return self.key
    def set_key(self, key):
        self.key = key
    def get_value(self):
        return self.value
    def set_value(self, value):
        self.value = value
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='KeyValuePair', mapping_=None, reverse_mapping_=None, nsmap_=None):
        if parent_element is None:
            element = etree_.Element('{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        else:
            element = etree_.SubElement(parent_element, '{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        if self.key is not None:
            element.set('key', self.gds_format_string(self.key))
        if self.value is not None:
            element.set('value', self.gds_format_string(self.value))
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.key, 'key')
        self.gds_check_cardinality_(self.key, 'key', required=True)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.value, 'value')
        self.gds_check_cardinality_(self.value, 'value', required=True)
        # validate simple type children
        # validate complex type children
        if recursive:
            pass
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('key', node)
        if value is not None and 'key' not in already_processed:
            already_processed.add('key')
            self.key = value
        value = find_attr_value_('value', node)
        if value is not None and 'value' not in already_processed:
            already_processed.add('value')
            self.value = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class KeyValuePair


class GeneratedBy(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'Name': MemberSpec_('Name', 'string', 0, 0, {'use': 'required', 'name': 'Name'}),
        'Version': MemberSpec_('Version', 'string', 0, 1, {'use': 'optional', 'name': 'Version'}),
        'Description': MemberSpec_('Description', 'string', 0, 1, {'use': 'optional', 'name': 'Description'}),
        'CodeURL': MemberSpec_('CodeURL', 'string', 0, 1, {'use': 'optional', 'name': 'CodeURL'}),
        'Container': MemberSpec_('Container', 'GeneratedByContainer', 0, 1, {'maxOccurs': '1', 'minOccurs': '0', 'name': 'Container', 'type': 'GeneratedByContainer'}, None),
    }
    subclass = None
    superclass = None
    def __init__(self, Name=None, Version=None, Description=None, CodeURL=None, Container=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Name = _cast(None, Name)
        self.Name_nsprefix_ = None
        self.Version = _cast(None, Version)
        self.Version_nsprefix_ = None
        self.Description = _cast(None, Description)
        self.Description_nsprefix_ = None
        self.CodeURL = _cast(None, CodeURL)
        self.CodeURL_nsprefix_ = None
        self.Container = Container
        self.Container_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GeneratedBy)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GeneratedBy.subclass:
            return GeneratedBy.subclass(*args_, **kwargs_)
        else:
            return GeneratedBy(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Container(self):
        return self.Container
    def set_Container(self, Container):
        self.Container = Container
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def get_CodeURL(self):
        return self.CodeURL
    def set_CodeURL(self, CodeURL):
        self.CodeURL = CodeURL
    def _hasContent(self):
        if (
            self.Container is not None
        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='GeneratedBy', mapping_=None, reverse_mapping_=None, nsmap_=None):
        if parent_element is None:
            element = etree_.Element('{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        else:
            element = etree_.SubElement(parent_element, '{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        if self.Name is not None:
            element.set('Name', self.gds_format_string(self.Name))
        if self.Version is not None:
            element.set('Version', self.gds_format_string(self.Version))
        if self.Description is not None:
            element.set('Description', self.gds_format_string(self.Description))
        if self.CodeURL is not None:
            element.set('CodeURL', self.gds_format_string(self.CodeURL))
        if self.Container is not None:
            Container_ = self.Container
            Container_.to_etree(element, name_='Container', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.Name, 'Name')
        self.gds_check_cardinality_(self.Name, 'Name', required=True)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.Version, 'Version')
        self.gds_check_cardinality_(self.Version, 'Version', required=False)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.Description, 'Description')
        self.gds_check_cardinality_(self.Description, 'Description', required=False)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.CodeURL, 'CodeURL')
        self.gds_check_cardinality_(self.CodeURL, 'CodeURL', required=False)
        # validate simple type children
        # validate complex type children
        self.gds_check_cardinality_(self.Container, 'Container', min_occurs=0, max_occurs=1)
        if recursive:
            if self.Container is not None:
                self.Container.validate_(gds_collector, recursive=True)
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
        # generate complex type children
        level += 1
        if self.Container:
            yield from self.Container.generateRecursively_(level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('Name', node)
        if value is not None and 'Name' not in already_processed:
            already_processed.add('Name')
            self.Name = value
        value = find_attr_value_('Version', node)
        if value is not None and 'Version' not in already_processed:
            already_processed.add('Version')
            self.Version = value
        value = find_attr_value_('Description', node)
        if value is not None and 'Description' not in already_processed:
            already_processed.add('Description')
            self.Description = value
        value = find_attr_value_('CodeURL', node)
        if value is not None and 'CodeURL' not in already_processed:
            already_processed.add('CodeURL')
            self.CodeURL = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Container':
            obj_ = GeneratedByContainer.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Container = obj_
            obj_.original_tagname_ = 'Container'
# end class GeneratedBy


class SourceDatasets(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'DOI': MemberSpec_('DOI', 'string', 0, 1, {'use': 'optional', 'name': 'DOI'}),
        'URL': MemberSpec_('URL', 'anyURI', 0, 1, {'use': 'optional', 'name': 'URL'}),
        'Version': MemberSpec_('Version', 'string', 0, 1, {'use': 'optional', 'name': 'Version'}),
    }
    subclass = None
    superclass = None
    def __init__(self, DOI=None, URL=None, Version=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DOI = _cast(None, DOI)
        self.DOI_nsprefix_ = None
        self.URL = _cast(None, URL)
        self.URL_nsprefix_ = None
        self.Version = _cast(None, Version)
        self.Version_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SourceDatasets)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SourceDatasets.subclass:
            return SourceDatasets.subclass(*args_, **kwargs_)
        else:
            return SourceDatasets(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DOI(self):
        return self.DOI
    def set_DOI(self, DOI):
        self.DOI = DOI
    def get_URL(self):
        return self.URL
    def set_URL(self, URL):
        self.URL = URL
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='SourceDatasets', mapping_=None, reverse_mapping_=None, nsmap_=None):
        if parent_element is None:
            element = etree_.Element('{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        else:
            element = etree_.SubElement(parent_element, '{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        if self.DOI is not None:
            element.set('DOI', self.gds_format_string(self.DOI))
        if self.URL is not None:
            element.set('URL', self.gds_format_string(self.URL))
        if self.Version is not None:
            element.set('Version', self.gds_format_string(self.Version))
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.DOI, 'DOI')
        self.gds_check_cardinality_(self.DOI, 'DOI', required=False)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.URL, 'URL')
        self.gds_check_cardinality_(self.URL, 'URL', required=False)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.Version, 'Version')
        self.gds_check_cardinality_(self.Version, 'Version', required=False)
        # validate simple type children
        # validate complex type children
        if recursive:
            pass
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('DOI', node)
        if value is not None and 'DOI' not in already_processed:
            already_processed.add('DOI')
            self.DOI = value
        value = find_attr_value_('URL', node)
        if value is not None and 'URL' not in already_processed:
            already_processed.add('URL')
            self.URL = value
        value = find_attr_value_('Version', node)
        if value is not None and 'Version' not in already_processed:
            already_processed.add('Version')
            self.Version = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class SourceDatasets


class GeneratedByContainer(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'Type': MemberSpec_('Type', 'string', 0, 1, {'use': 'optional', 'name': 'Type'}),
        'Tag': MemberSpec_('Tag', 'string', 0, 1, {'use': 'optional', 'name': 'Tag'}),
        'URI': MemberSpec_('URI', 'anyURI', 0, 1, {'use': 'optional', 'name': 'URI'}),
    }
    subclass = None
    superclass = None
    def __init__(self, Type=None, Tag=None, URI=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Type = _cast(None, Type)
        self.Type_nsprefix_ = None
        self.Tag = _cast(None, Tag)
        self.Tag_nsprefix_ = None
        self.URI = _cast(None, URI)
        self.URI_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GeneratedByContainer)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GeneratedByContainer.subclass:
            return GeneratedByContainer.subclass(*args_, **kwargs_)
        else:
            return GeneratedByContainer(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def get_Tag(self):
        return self.Tag
    def set_Tag(self, Tag):
        self.Tag = Tag
    def get_URI(self):
        return self.URI
    def set_URI(self, URI):
        self.URI = URI
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='GeneratedByContainer', mapping_=None, reverse_mapping_=None, nsmap_=None):
        if parent_element is None:
            element = etree_.Element('{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        else:
            element = etree_.SubElement(parent_element, '{https://bids.neuroimaging.io/1.6}' + name_, nsmap=nsmap_)
        if self.Type is not None:
            element.set('Type', self.gds_format_string(self.Type))
        if self.Tag is not None:
            element.set('Tag', self.gds_format_string(self.Tag))
        if self.URI is not None:
            element.set('URI', self.gds_format_string(self.URI))
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.Type, 'Type')
        self.gds_check_cardinality_(self.Type, 'Type', required=False)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.Tag, 'Tag')
        self.gds_check_cardinality_(self.Tag, 'Tag', required=False)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.URI, 'URI')
        self.gds_check_cardinality_(self.URI, 'URI', required=False)
        # validate simple type children
        # validate complex type children
        if recursive:
            pass
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('Type', node)
        if value is not None and 'Type' not in already_processed:
            already_processed.add('Type')
            self.Type = value
        value = find_attr_value_('Tag', node)
        if value is not None and 'Tag' not in already_processed:
            already_processed.add('Tag')
            self.Tag = value
        value = find_attr_value_('URI', node)
        if value is not None and 'URI' not in already_processed:
            already_processed.add('URI')
            self.URI = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class GeneratedByContainer


class ParticipantsTsvFile(TsvFile):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'entries': MemberSpec_('entries', 'ParticipantsTsvFileEntry', 1, 0, {'maxOccurs': 'unbounded', 'minOccurs': '1', 'name': 'entries', 'type': 'ParticipantsTsvFileEntry'}, None),
    }
    subclass = None
    superclass = TsvFile
    def __init__(self, name=None, extension=None, uri=None, entries=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("ParticipantsTsvFile"), self).__init__(name, extension, uri,  **kwargs_)
        if entries is None:
            self.entries = []
        else:
            self.entries = entries
        self.entries_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ParticipantsTsvFile)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ParticipantsTsvFile.subclass:
            return ParticipantsTsvFile.subclass(*args_, **kwargs_)
        else:
            return ParticipantsTsvFile(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_entries(self):
        return self.entries
    def set_entries(self, entries):
        self.entries = entries
    def add_entries(self, value):
        self.entries.append(value)
    def insert_entries_at(self, index, value):
        self.entries.insert(index, value)
    def replace_entries_at(self, index, value):
        self.entries[index] = value
    def _hasContent(self):
        if (
            self.entries or
            super(ParticipantsTsvFile, self)._hasContent()
        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='ParticipantsTsvFile', mapping_=None, reverse_mapping_=None, nsmap_=None):
        element = super(ParticipantsTsvFile, self).to_etree(parent_element, name_, mapping_, reverse_mapping_, nsmap_)
        for entries_ in self.entries:
            entries_.to_etree(element, name_='entries', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        # validate simple type children
        # validate complex type children
        self.gds_check_cardinality_(self.entries, 'entries', min_occurs=1, max_occurs=9999999)
        if recursive:
            for item in self.entries:
                item.validate_(gds_collector, recursive=True)
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
        # generate complex type children
        level += 1
        if self.entries:
            for o in self.entries:
                yield from o.generateRecursively_(level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        super(ParticipantsTsvFile, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'entries':
            obj_ = ParticipantsTsvFileEntry.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.entries.append(obj_)
            obj_.original_tagname_ = 'entries'
        super(ParticipantsTsvFile, self)._buildChildren(child_, node, nodeName_, True)
# end class ParticipantsTsvFile


class DatasetDescriptionFile(JsonFile):
    """HEDVersion -- @use: recommended
    DatasetType -- @use: recommended
    License -- @use: recommended
    
    """
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'Name': MemberSpec_('Name', 'string', 0, 0, {'use': 'required', 'name': 'Name'}),
        'BIDSVersion': MemberSpec_('BIDSVersion', 'string', 0, 0, {'use': 'required', 'name': 'BIDSVersion'}),
        'HEDVersion': MemberSpec_('HEDVersion', 'string', 0, 1, {'use': 'optional', 'name': 'HEDVersion'}),
        'DatasetType': MemberSpec_('DatasetType', 'DatasetTypeType', 0, 1, {'use': 'optional', 'name': 'DatasetType'}),
        'License': MemberSpec_('License', 'string', 0, 1, {'use': 'optional', 'name': 'License'}),
        'Acknowledgements': MemberSpec_('Acknowledgements', 'string', 0, 1, {'use': 'optional', 'name': 'Acknowledgements'}),
        'HowToAcknowledge': MemberSpec_('HowToAcknowledge', 'string', 0, 1, {'use': 'optional', 'name': 'HowToAcknowledge'}),
        'DatasetDOI': MemberSpec_('DatasetDOI', 'string', 0, 1, {'use': 'optional', 'name': 'DatasetDOI'}),
        'Authors': MemberSpec_('Authors', 'string', 1, 1, {'maxOccurs': 'unbounded', 'minOccurs': '0', 'name': 'Authors', 'type': 'string'}, None),
        'Funding': MemberSpec_('Funding', 'string', 1, 1, {'maxOccurs': 'unbounded', 'minOccurs': '0', 'name': 'Funding', 'type': 'string'}, None),
        'EthicsApprovals': MemberSpec_('EthicsApprovals', 'string', 1, 1, {'maxOccurs': 'unbounded', 'minOccurs': '0', 'name': 'EthicsApprovals', 'type': 'string'}, None),
        'ReferencesAndLinks': MemberSpec_('ReferencesAndLinks', 'string', 1, 1, {'maxOccurs': 'unbounded', 'minOccurs': '0', 'name': 'ReferencesAndLinks', 'type': 'string'}, None),
        'GeneratedBy': MemberSpec_('GeneratedBy', 'GeneratedBy', 1, 1, {'maxOccurs': 'unbounded', 'minOccurs': '0', 'name': 'GeneratedBy', 'type': 'GeneratedBy'}, None),
        'SourceDatasets': MemberSpec_('SourceDatasets', 'SourceDatasets', 1, 1, {'maxOccurs': 'unbounded', 'minOccurs': '0', 'name': 'SourceDatasets', 'type': 'SourceDatasets'}, None),
    }
    subclass = None
    superclass = JsonFile
    def __init__(self, name=None, extension=None, uri=None, keys=None, Name=None, BIDSVersion=None, HEDVersion=None, DatasetType='raw', License=None, Acknowledgements=None, HowToAcknowledge=None, DatasetDOI=None, Authors=None, Funding=None, EthicsApprovals=None, ReferencesAndLinks=None, GeneratedBy=None, SourceDatasets=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("DatasetDescriptionFile"), self).__init__(name, extension, uri, keys,  **kwargs_)
        self.Name = _cast(None, Name)
        self.Name_nsprefix_ = None
        self.BIDSVersion = _cast(None, BIDSVersion)
        self.BIDSVersion_nsprefix_ = None
        self.HEDVersion = _cast(None, HEDVersion)
        self.HEDVersion_nsprefix_ = None
        self.DatasetType = _cast(None, DatasetType)
        self.DatasetType_nsprefix_ = None
        self.License = _cast(None, License)
        self.License_nsprefix_ = None
        self.Acknowledgements = _cast(None, Acknowledgements)
        self.Acknowledgements_nsprefix_ = None
        self.HowToAcknowledge = _cast(None, HowToAcknowledge)
        self.HowToAcknowledge_nsprefix_ = None
        self.DatasetDOI = _cast(None, DatasetDOI)
        self.DatasetDOI_nsprefix_ = None
        if Authors is None:
            self.Authors = []
        else:
            self.Authors = Authors
        self.Authors_nsprefix_ = None
        if Funding is None:
            self.Funding = []
        else:
            self.Funding = Funding
        self.Funding_nsprefix_ = None
        if EthicsApprovals is None:
            self.EthicsApprovals = []
        else:
            self.EthicsApprovals = EthicsApprovals
        self.EthicsApprovals_nsprefix_ = None
        if ReferencesAndLinks is None:
            self.ReferencesAndLinks = []
        else:
            self.ReferencesAndLinks = ReferencesAndLinks
        self.ReferencesAndLinks_nsprefix_ = None
        if GeneratedBy is None:
            self.GeneratedBy = []
        else:
            self.GeneratedBy = GeneratedBy
        self.GeneratedBy_nsprefix_ = None
        if SourceDatasets is None:
            self.SourceDatasets = []
        else:
            self.SourceDatasets = SourceDatasets
        self.SourceDatasets_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatasetDescriptionFile)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatasetDescriptionFile.subclass:
            return DatasetDescriptionFile.subclass(*args_, **kwargs_)
        else:
            return DatasetDescriptionFile(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Authors(self):
        return self.Authors
    def set_Authors(self, Authors):
        self.Authors = Authors
    def add_Authors(self, value):
        self.Authors.append(value)
    def insert_Authors_at(self, index, value):
        self.Authors.insert(index, value)
    def replace_Authors_at(self, index, value):
        self.Authors[index] = value
    def get_Funding(self):
        return self.Funding
    def set_Funding(self, Funding):
        self.Funding = Funding
    def add_Funding(self, value):
        self.Funding.append(value)
    def insert_Funding_at(self, index, value):
        self.Funding.insert(index, value)
    def replace_Funding_at(self, index, value):
        self.Funding[index] = value
    def get_EthicsApprovals(self):
        return self.EthicsApprovals
    def set_EthicsApprovals(self, EthicsApprovals):
        self.EthicsApprovals = EthicsApprovals
    def add_EthicsApprovals(self, value):
        self.EthicsApprovals.append(value)
    def insert_EthicsApprovals_at(self, index, value):
        self.EthicsApprovals.insert(index, value)
    def replace_EthicsApprovals_at(self, index, value):
        self.EthicsApprovals[index] = value
    def get_ReferencesAndLinks(self):
        return self.ReferencesAndLinks
    def set_ReferencesAndLinks(self, ReferencesAndLinks):
        self.ReferencesAndLinks = ReferencesAndLinks
    def add_ReferencesAndLinks(self, value):
        self.ReferencesAndLinks.append(value)
    def insert_ReferencesAndLinks_at(self, index, value):
        self.ReferencesAndLinks.insert(index, value)
    def replace_ReferencesAndLinks_at(self, index, value):
        self.ReferencesAndLinks[index] = value
    def get_GeneratedBy(self):
        return self.GeneratedBy
    def set_GeneratedBy(self, GeneratedBy):
        self.GeneratedBy = GeneratedBy
    def add_GeneratedBy(self, value):
        self.GeneratedBy.append(value)
    def insert_GeneratedBy_at(self, index, value):
        self.GeneratedBy.insert(index, value)
    def replace_GeneratedBy_at(self, index, value):
        self.GeneratedBy[index] = value
    def get_SourceDatasets(self):
        return self.SourceDatasets
    def set_SourceDatasets(self, SourceDatasets):
        self.SourceDatasets = SourceDatasets
    def add_SourceDatasets(self, value):
        self.SourceDatasets.append(value)
    def insert_SourceDatasets_at(self, index, value):
        self.SourceDatasets.insert(index, value)
    def replace_SourceDatasets_at(self, index, value):
        self.SourceDatasets[index] = value
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def get_BIDSVersion(self):
        return self.BIDSVersion
    def set_BIDSVersion(self, BIDSVersion):
        self.BIDSVersion = BIDSVersion
    def get_HEDVersion(self):
        return self.HEDVersion
    def set_HEDVersion(self, HEDVersion):
        self.HEDVersion = HEDVersion
    def get_DatasetType(self):
        return self.DatasetType
    def set_DatasetType(self, DatasetType):
        self.DatasetType = DatasetType
    def get_License(self):
        return self.License
    def set_License(self, License):
        self.License = License
    def get_Acknowledgements(self):
        return self.Acknowledgements
    def set_Acknowledgements(self, Acknowledgements):
        self.Acknowledgements = Acknowledgements
    def get_HowToAcknowledge(self):
        return self.HowToAcknowledge
    def set_HowToAcknowledge(self, HowToAcknowledge):
        self.HowToAcknowledge = HowToAcknowledge
    def get_DatasetDOI(self):
        return self.DatasetDOI
    def set_DatasetDOI(self, DatasetDOI):
        self.DatasetDOI = DatasetDOI
    def validate_DatasetTypeType(self, value):
        # Validate type DatasetTypeType, a restriction on string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['raw', 'derivative']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DatasetTypeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
    def _hasContent(self):
        if (
            self.Authors or
            self.Funding or
            self.EthicsApprovals or
            self.ReferencesAndLinks or
            self.GeneratedBy or
            self.SourceDatasets or
            super(DatasetDescriptionFile, self)._hasContent()
        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='DatasetDescriptionFile', mapping_=None, reverse_mapping_=None, nsmap_=None):
        element = super(DatasetDescriptionFile, self).to_etree(parent_element, name_, mapping_, reverse_mapping_, nsmap_)
        if self.Name is not None:
            element.set('Name', self.gds_format_string(self.Name))
        if self.BIDSVersion is not None:
            element.set('BIDSVersion', self.gds_format_string(self.BIDSVersion))
        if self.HEDVersion is not None:
            element.set('HEDVersion', self.gds_format_string(self.HEDVersion))
        if self.DatasetType is not None:
            element.set('DatasetType', self.gds_format_string(self.DatasetType))
        if self.License is not None:
            element.set('License', self.gds_format_string(self.License))
        if self.Acknowledgements is not None:
            element.set('Acknowledgements', self.gds_format_string(self.Acknowledgements))
        if self.HowToAcknowledge is not None:
            element.set('HowToAcknowledge', self.gds_format_string(self.HowToAcknowledge))
        if self.DatasetDOI is not None:
            element.set('DatasetDOI', self.gds_format_string(self.DatasetDOI))
        for Authors_ in self.Authors:
            etree_.SubElement(element, '{https://bids.neuroimaging.io/1.6}Authors').text = self.gds_format_string(Authors_)
        for Funding_ in self.Funding:
            etree_.SubElement(element, '{https://bids.neuroimaging.io/1.6}Funding').text = self.gds_format_string(Funding_)
        for EthicsApprovals_ in self.EthicsApprovals:
            etree_.SubElement(element, '{https://bids.neuroimaging.io/1.6}EthicsApprovals').text = self.gds_format_string(EthicsApprovals_)
        for ReferencesAndLinks_ in self.ReferencesAndLinks:
            etree_.SubElement(element, '{https://bids.neuroimaging.io/1.6}ReferencesAndLinks').text = self.gds_format_string(ReferencesAndLinks_)
        for GeneratedBy_ in self.GeneratedBy:
            GeneratedBy_.to_etree(element, name_='GeneratedBy', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        for SourceDatasets_ in self.SourceDatasets:
            SourceDatasets_.to_etree(element, name_='SourceDatasets', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.Name, 'Name')
        self.gds_check_cardinality_(self.Name, 'Name', required=True)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.BIDSVersion, 'BIDSVersion')
        self.gds_check_cardinality_(self.BIDSVersion, 'BIDSVersion', required=True)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.HEDVersion, 'HEDVersion')
        self.gds_check_cardinality_(self.HEDVersion, 'HEDVersion', required=False)
        self.gds_validate_defined_ST_(self.validate_DatasetTypeType, self.DatasetType, 'DatasetType')
        self.gds_check_cardinality_(self.DatasetType, 'DatasetType', required=False)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.License, 'License')
        self.gds_check_cardinality_(self.License, 'License', required=False)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.Acknowledgements, 'Acknowledgements')
        self.gds_check_cardinality_(self.Acknowledgements, 'Acknowledgements', required=False)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.HowToAcknowledge, 'HowToAcknowledge')
        self.gds_check_cardinality_(self.HowToAcknowledge, 'HowToAcknowledge', required=False)
        self.gds_validate_builtin_ST_(self.gds_validate_string, self.DatasetDOI, 'DatasetDOI')
        self.gds_check_cardinality_(self.DatasetDOI, 'DatasetDOI', required=False)
        # validate simple type children
        for item in self.Authors:
            self.gds_validate_builtin_ST_(self.gds_validate_string, item, 'Authors')
        self.gds_check_cardinality_(self.Authors, 'Authors', min_occurs=0, max_occurs=9999999)
        for item in self.Funding:
            self.gds_validate_builtin_ST_(self.gds_validate_string, item, 'Funding')
        self.gds_check_cardinality_(self.Funding, 'Funding', min_occurs=0, max_occurs=9999999)
        for item in self.EthicsApprovals:
            self.gds_validate_builtin_ST_(self.gds_validate_string, item, 'EthicsApprovals')
        self.gds_check_cardinality_(self.EthicsApprovals, 'EthicsApprovals', min_occurs=0, max_occurs=9999999)
        for item in self.ReferencesAndLinks:
            self.gds_validate_builtin_ST_(self.gds_validate_string, item, 'ReferencesAndLinks')
        self.gds_check_cardinality_(self.ReferencesAndLinks, 'ReferencesAndLinks', min_occurs=0, max_occurs=9999999)
        # validate complex type children
        self.gds_check_cardinality_(self.GeneratedBy, 'GeneratedBy', min_occurs=0, max_occurs=9999999)
        self.gds_check_cardinality_(self.SourceDatasets, 'SourceDatasets', min_occurs=0, max_occurs=9999999)
        if recursive:
            for item in self.GeneratedBy:
                item.validate_(gds_collector, recursive=True)
            for item in self.SourceDatasets:
                item.validate_(gds_collector, recursive=True)
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
        # generate complex type children
        level += 1
        if self.GeneratedBy:
            for o in self.GeneratedBy:
                yield from o.generateRecursively_(level)
        if self.SourceDatasets:
            for o in self.SourceDatasets:
                yield from o.generateRecursively_(level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('Name', node)
        if value is not None and 'Name' not in already_processed:
            already_processed.add('Name')
            self.Name = value
        value = find_attr_value_('BIDSVersion', node)
        if value is not None and 'BIDSVersion' not in already_processed:
            already_processed.add('BIDSVersion')
            self.BIDSVersion = value
        value = find_attr_value_('HEDVersion', node)
        if value is not None and 'HEDVersion' not in already_processed:
            already_processed.add('HEDVersion')
            self.HEDVersion = value
        value = find_attr_value_('DatasetType', node)
        if value is not None and 'DatasetType' not in already_processed:
            already_processed.add('DatasetType')
            self.DatasetType = value
            self.validate_DatasetTypeType(self.DatasetType)    # validate type DatasetTypeType
        value = find_attr_value_('License', node)
        if value is not None and 'License' not in already_processed:
            already_processed.add('License')
            self.License = value
        value = find_attr_value_('Acknowledgements', node)
        if value is not None and 'Acknowledgements' not in already_processed:
            already_processed.add('Acknowledgements')
            self.Acknowledgements = value
        value = find_attr_value_('HowToAcknowledge', node)
        if value is not None and 'HowToAcknowledge' not in already_processed:
            already_processed.add('HowToAcknowledge')
            self.HowToAcknowledge = value
        value = find_attr_value_('DatasetDOI', node)
        if value is not None and 'DatasetDOI' not in already_processed:
            already_processed.add('DatasetDOI')
            self.DatasetDOI = value
        super(DatasetDescriptionFile, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Authors':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Authors')
            value_ = self.gds_validate_string(value_, node, 'Authors')
            self.Authors.append(value_)
            self.Authors_nsprefix_ = child_.prefix
        elif nodeName_ == 'Funding':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Funding')
            value_ = self.gds_validate_string(value_, node, 'Funding')
            self.Funding.append(value_)
            self.Funding_nsprefix_ = child_.prefix
        elif nodeName_ == 'EthicsApprovals':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EthicsApprovals')
            value_ = self.gds_validate_string(value_, node, 'EthicsApprovals')
            self.EthicsApprovals.append(value_)
            self.EthicsApprovals_nsprefix_ = child_.prefix
        elif nodeName_ == 'ReferencesAndLinks':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ReferencesAndLinks')
            value_ = self.gds_validate_string(value_, node, 'ReferencesAndLinks')
            self.ReferencesAndLinks.append(value_)
            self.ReferencesAndLinks_nsprefix_ = child_.prefix
        elif nodeName_ == 'GeneratedBy':
            obj_ = GeneratedBy.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GeneratedBy.append(obj_)
            obj_.original_tagname_ = 'GeneratedBy'
        elif nodeName_ == 'SourceDatasets':
            obj_ = SourceDatasets.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.SourceDatasets.append(obj_)
            obj_.original_tagname_ = 'SourceDatasets'
        super(DatasetDescriptionFile, self)._buildChildren(child_, node, nodeName_, True)
# end class DatasetDescriptionFile


class Session(Folder):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'datatypes': MemberSpec_('datatypes', 'DatatypeFolder', 1, 0, {'maxOccurs': 'unbounded', 'minOccurs': '1', 'name': 'datatypes', 'type': 'DatatypeFolder'}, None),
    }
    subclass = None
    superclass = Folder
    def __init__(self, name=None, files=None, folders=None, datatypes=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("Session"), self).__init__(name, files, folders,  **kwargs_)
        if datatypes is None:
            self.datatypes = []
        else:
            self.datatypes = datatypes
        self.datatypes_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Session)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Session.subclass:
            return Session.subclass(*args_, **kwargs_)
        else:
            return Session(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_datatypes(self):
        return self.datatypes
    def set_datatypes(self, datatypes):
        self.datatypes = datatypes
    def add_datatypes(self, value):
        self.datatypes.append(value)
    def insert_datatypes_at(self, index, value):
        self.datatypes.insert(index, value)
    def replace_datatypes_at(self, index, value):
        self.datatypes[index] = value
    def _hasContent(self):
        if (
            self.datatypes or
            super(Session, self)._hasContent()
        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='Session', mapping_=None, reverse_mapping_=None, nsmap_=None):
        element = super(Session, self).to_etree(parent_element, name_, mapping_, reverse_mapping_, nsmap_)
        for datatypes_ in self.datatypes:
            datatypes_.to_etree(element, name_='datatypes', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        # validate simple type children
        # validate complex type children
        self.gds_check_cardinality_(self.datatypes, 'datatypes', min_occurs=1, max_occurs=9999999)
        if recursive:
            for item in self.datatypes:
                item.validate_(gds_collector, recursive=True)
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
        # generate complex type children
        level += 1
        if self.datatypes:
            for o in self.datatypes:
                yield from o.generateRecursively_(level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        super(Session, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'datatypes':
            obj_ = DatatypeFolder.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.datatypes.append(obj_)
            obj_.original_tagname_ = 'datatypes'
        super(Session, self)._buildChildren(child_, node, nodeName_, True)
# end class Session


class Subject(Folder):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'sessions': MemberSpec_('sessions', 'Session', 1, 1, {'maxOccurs': 'unbounded', 'minOccurs': '0', 'name': 'sessions', 'type': 'Session'}, None),
        'datatypes': MemberSpec_('datatypes', 'DatatypeFolder', 1, 0, {'maxOccurs': 'unbounded', 'minOccurs': '1', 'name': 'datatypes', 'type': 'DatatypeFolder'}, None),
    }
    subclass = None
    superclass = Folder
    def __init__(self, name=None, files=None, folders=None, sessions=None, datatypes=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("Subject"), self).__init__(name, files, folders,  **kwargs_)
        if sessions is None:
            self.sessions = []
        else:
            self.sessions = sessions
        self.sessions_nsprefix_ = None
        if datatypes is None:
            self.datatypes = []
        else:
            self.datatypes = datatypes
        self.datatypes_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Subject)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Subject.subclass:
            return Subject.subclass(*args_, **kwargs_)
        else:
            return Subject(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_sessions(self):
        return self.sessions
    def set_sessions(self, sessions):
        self.sessions = sessions
    def add_sessions(self, value):
        self.sessions.append(value)
    def insert_sessions_at(self, index, value):
        self.sessions.insert(index, value)
    def replace_sessions_at(self, index, value):
        self.sessions[index] = value
    def get_datatypes(self):
        return self.datatypes
    def set_datatypes(self, datatypes):
        self.datatypes = datatypes
    def add_datatypes(self, value):
        self.datatypes.append(value)
    def insert_datatypes_at(self, index, value):
        self.datatypes.insert(index, value)
    def replace_datatypes_at(self, index, value):
        self.datatypes[index] = value
    def _hasContent(self):
        if (
            self.sessions or
            self.datatypes or
            super(Subject, self)._hasContent()
        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='Subject', mapping_=None, reverse_mapping_=None, nsmap_=None):
        element = super(Subject, self).to_etree(parent_element, name_, mapping_, reverse_mapping_, nsmap_)
        for sessions_ in self.sessions:
            sessions_.to_etree(element, name_='sessions', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        for datatypes_ in self.datatypes:
            datatypes_.to_etree(element, name_='datatypes', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        # validate simple type children
        # validate complex type children
        self.gds_check_cardinality_(self.sessions, 'sessions', min_occurs=0, max_occurs=9999999)
        self.gds_check_cardinality_(self.datatypes, 'datatypes', min_occurs=1, max_occurs=9999999)
        if recursive:
            for item in self.sessions:
                item.validate_(gds_collector, recursive=True)
            for item in self.datatypes:
                item.validate_(gds_collector, recursive=True)
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
        # generate complex type children
        level += 1
        if self.sessions:
            for o in self.sessions:
                yield from o.generateRecursively_(level)
        if self.datatypes:
            for o in self.datatypes:
                yield from o.generateRecursively_(level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        super(Subject, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'sessions':
            obj_ = Session.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.sessions.append(obj_)
            obj_.original_tagname_ = 'sessions'
        elif nodeName_ == 'datatypes':
            obj_ = DatatypeFolder.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.datatypes.append(obj_)
            obj_.original_tagname_ = 'datatypes'
        super(Subject, self)._buildChildren(child_, node, nodeName_, True)
# end class Subject


class Dataset(Folder):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = {
        'subjects': MemberSpec_('subjects', 'Subject', 1, 1, {'maxOccurs': 'unbounded', 'minOccurs': '0', 'name': 'subjects', 'type': 'Subject'}, None),
        'dataset_description': MemberSpec_('dataset_description', 'DatasetDescriptionFile', 0, 0, {'maxOccurs': '1', 'minOccurs': '1', 'name': 'dataset_description', 'type': 'DatasetDescriptionFile'}, None),
        'README': MemberSpec_('README', 'File', 0, 1, {'maxOccurs': '1', 'minOccurs': '0', 'name': 'README', 'type': 'File'}, None),
        'CHANGES': MemberSpec_('CHANGES', 'File', 0, 1, {'maxOccurs': '1', 'minOccurs': '0', 'name': 'CHANGES', 'type': 'File'}, None),
        'LICENSE': MemberSpec_('LICENSE', 'File', 0, 1, {'maxOccurs': '1', 'minOccurs': '0', 'name': 'LICENSE', 'type': 'File'}, None),
        'genetic_info': MemberSpec_('genetic_info', 'JsonFile', 0, 1, {'maxOccurs': '1', 'minOccurs': '0', 'name': 'genetic_info', 'type': 'JsonFile'}, None),
        'samples': MemberSpec_('samples', 'JsonFile', 0, 1, {'maxOccurs': '1', 'minOccurs': '0', 'name': 'samples', 'type': 'JsonFile'}, None),
        'participants_tsv': MemberSpec_('participants_tsv', 'ParticipantsTsvFile', 0, 1, {'maxOccurs': '1', 'minOccurs': '0', 'name': 'participants.tsv', 'type': 'ParticipantsTsvFile'}, None),
        'participants_json': MemberSpec_('participants_json', 'TsvSidecarFile', 0, 1, {'maxOccurs': '1', 'minOccurs': '0', 'name': 'participants.json', 'type': 'TsvSidecarFile'}, None),
        'code': MemberSpec_('code', 'Folder', 0, 1, {'maxOccurs': '1', 'minOccurs': '0', 'name': 'code', 'type': 'Folder'}, None),
        'derivatives': MemberSpec_('derivatives', 'Folder', 0, 1, {'maxOccurs': '1', 'minOccurs': '0', 'name': 'derivatives', 'type': 'Folder'}, None),
        'sourcedata': MemberSpec_('sourcedata', 'Folder', 0, 1, {'maxOccurs': '1', 'minOccurs': '0', 'name': 'sourcedata', 'type': 'Folder'}, None),
        'stimuli': MemberSpec_('stimuli', 'Folder', 0, 1, {'maxOccurs': '1', 'minOccurs': '0', 'name': 'stimuli', 'type': 'Folder'}, None),
    }
    subclass = None
    superclass = Folder
    def __init__(self, name=None, files=None, folders=None, subjects=None, dataset_description=None, README=None, CHANGES=None, LICENSE=None, genetic_info=None, samples=None, participants_tsv=None, participants_json=None, code=None, derivatives=None, sourcedata=None, stimuli=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("Dataset"), self).__init__(name, files, folders,  **kwargs_)
        if subjects is None:
            self.subjects = []
        else:
            self.subjects = subjects
        self.subjects_nsprefix_ = None
        self.dataset_description = dataset_description
        self.dataset_description_nsprefix_ = None
        self.README = README
        self.README_nsprefix_ = None
        self.CHANGES = CHANGES
        self.CHANGES_nsprefix_ = None
        self.LICENSE = LICENSE
        self.LICENSE_nsprefix_ = None
        self.genetic_info = genetic_info
        self.genetic_info_nsprefix_ = None
        self.samples = samples
        self.samples_nsprefix_ = None
        self.participants_tsv = participants_tsv
        self.participants_tsv_nsprefix_ = None
        self.participants_json = participants_json
        self.participants_json_nsprefix_ = None
        self.code = code
        self.code_nsprefix_ = None
        self.derivatives = derivatives
        self.derivatives_nsprefix_ = None
        self.sourcedata = sourcedata
        self.sourcedata_nsprefix_ = None
        self.stimuli = stimuli
        self.stimuli_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Dataset)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Dataset.subclass:
            return Dataset.subclass(*args_, **kwargs_)
        else:
            return Dataset(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_subjects(self):
        return self.subjects
    def set_subjects(self, subjects):
        self.subjects = subjects
    def add_subjects(self, value):
        self.subjects.append(value)
    def insert_subjects_at(self, index, value):
        self.subjects.insert(index, value)
    def replace_subjects_at(self, index, value):
        self.subjects[index] = value
    def get_dataset_description(self):
        return self.dataset_description
    def set_dataset_description(self, dataset_description):
        self.dataset_description = dataset_description
    def get_README(self):
        return self.README
    def set_README(self, README):
        self.README = README
    def get_CHANGES(self):
        return self.CHANGES
    def set_CHANGES(self, CHANGES):
        self.CHANGES = CHANGES
    def get_LICENSE(self):
        return self.LICENSE
    def set_LICENSE(self, LICENSE):
        self.LICENSE = LICENSE
    def get_genetic_info(self):
        return self.genetic_info
    def set_genetic_info(self, genetic_info):
        self.genetic_info = genetic_info
    def get_samples(self):
        return self.samples
    def set_samples(self, samples):
        self.samples = samples
    def get_participants_tsv(self):
        return self.participants_tsv
    def set_participants_tsv(self, participants_tsv):
        self.participants_tsv = participants_tsv
    def get_participants_json(self):
        return self.participants_json
    def set_participants_json(self, participants_json):
        self.participants_json = participants_json
    def get_code(self):
        return self.code
    def set_code(self, code):
        self.code = code
    def get_derivatives(self):
        return self.derivatives
    def set_derivatives(self, derivatives):
        self.derivatives = derivatives
    def get_sourcedata(self):
        return self.sourcedata
    def set_sourcedata(self, sourcedata):
        self.sourcedata = sourcedata
    def get_stimuli(self):
        return self.stimuli
    def set_stimuli(self, stimuli):
        self.stimuli = stimuli
    def _hasContent(self):
        if (
            self.subjects or
            self.dataset_description is not None or
            self.README is not None or
            self.CHANGES is not None or
            self.LICENSE is not None or
            self.genetic_info is not None or
            self.samples is not None or
            self.participants_tsv is not None or
            self.participants_json is not None or
            self.code is not None or
            self.derivatives is not None or
            self.sourcedata is not None or
            self.stimuli is not None or
            super(Dataset, self)._hasContent()
        ):
            return True
        else:
            return False
    def to_etree(self, parent_element=None, name_='Dataset', mapping_=None, reverse_mapping_=None, nsmap_=None):
        element = super(Dataset, self).to_etree(parent_element, name_, mapping_, reverse_mapping_, nsmap_)
        for subjects_ in self.subjects:
            subjects_.to_etree(element, name_='subjects', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if self.dataset_description is not None:
            dataset_description_ = self.dataset_description
            dataset_description_.to_etree(element, name_='dataset_description', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if self.README is not None:
            README_ = self.README
            README_.to_etree(element, name_='README', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if self.CHANGES is not None:
            CHANGES_ = self.CHANGES
            CHANGES_.to_etree(element, name_='CHANGES', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if self.LICENSE is not None:
            LICENSE_ = self.LICENSE
            LICENSE_.to_etree(element, name_='LICENSE', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if self.genetic_info is not None:
            genetic_info_ = self.genetic_info
            genetic_info_.to_etree(element, name_='genetic_info', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if self.samples is not None:
            samples_ = self.samples
            samples_.to_etree(element, name_='samples', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if self.participants_tsv is not None:
            participants_tsv_ = self.participants_tsv
            participants_tsv_.to_etree(element, name_='participants.tsv', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if self.participants_json is not None:
            participants_json_ = self.participants_json
            participants_json_.to_etree(element, name_='participants.json', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if self.code is not None:
            code_ = self.code
            code_.to_etree(element, name_='code', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if self.derivatives is not None:
            derivatives_ = self.derivatives
            derivatives_.to_etree(element, name_='derivatives', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if self.sourcedata is not None:
            sourcedata_ = self.sourcedata
            sourcedata_.to_etree(element, name_='sourcedata', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if self.stimuli is not None:
            stimuli_ = self.stimuli
            stimuli_.to_etree(element, name_='stimuli', mapping_=mapping_, reverse_mapping_=reverse_mapping_, nsmap_=nsmap_)
        if mapping_ is not None:
            mapping_[id(self)] = element
        if reverse_mapping_ is not None:
            reverse_mapping_[element] = self
        return element
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        # validate simple type children
        # validate complex type children
        self.gds_check_cardinality_(self.subjects, 'subjects', min_occurs=0, max_occurs=9999999)
        self.gds_check_cardinality_(self.dataset_description, 'dataset_description', min_occurs=1, max_occurs=1)
        self.gds_check_cardinality_(self.README, 'README', min_occurs=0, max_occurs=1)
        self.gds_check_cardinality_(self.CHANGES, 'CHANGES', min_occurs=0, max_occurs=1)
        self.gds_check_cardinality_(self.LICENSE, 'LICENSE', min_occurs=0, max_occurs=1)
        self.gds_check_cardinality_(self.genetic_info, 'genetic_info', min_occurs=0, max_occurs=1)
        self.gds_check_cardinality_(self.samples, 'samples', min_occurs=0, max_occurs=1)
        self.gds_check_cardinality_(self.participants_tsv, 'participants_tsv', min_occurs=0, max_occurs=1)
        self.gds_check_cardinality_(self.participants_json, 'participants_json', min_occurs=0, max_occurs=1)
        self.gds_check_cardinality_(self.code, 'code', min_occurs=0, max_occurs=1)
        self.gds_check_cardinality_(self.derivatives, 'derivatives', min_occurs=0, max_occurs=1)
        self.gds_check_cardinality_(self.sourcedata, 'sourcedata', min_occurs=0, max_occurs=1)
        self.gds_check_cardinality_(self.stimuli, 'stimuli', min_occurs=0, max_occurs=1)
        if recursive:
            for item in self.subjects:
                item.validate_(gds_collector, recursive=True)
            if self.dataset_description is not None:
                self.dataset_description.validate_(gds_collector, recursive=True)
            if self.README is not None:
                self.README.validate_(gds_collector, recursive=True)
            if self.CHANGES is not None:
                self.CHANGES.validate_(gds_collector, recursive=True)
            if self.LICENSE is not None:
                self.LICENSE.validate_(gds_collector, recursive=True)
            if self.genetic_info is not None:
                self.genetic_info.validate_(gds_collector, recursive=True)
            if self.samples is not None:
                self.samples.validate_(gds_collector, recursive=True)
            if self.participants_tsv is not None:
                self.participants_tsv.validate_(gds_collector, recursive=True)
            if self.participants_json is not None:
                self.participants_json.validate_(gds_collector, recursive=True)
            if self.code is not None:
                self.code.validate_(gds_collector, recursive=True)
            if self.derivatives is not None:
                self.derivatives.validate_(gds_collector, recursive=True)
            if self.sourcedata is not None:
                self.sourcedata.validate_(gds_collector, recursive=True)
            if self.stimuli is not None:
                self.stimuli.validate_(gds_collector, recursive=True)
        return message_count == len(self.gds_collector_.get_messages())
    def generateRecursively_(self, level=0):
        yield (self, level)
        # generate complex type children
        level += 1
        if self.subjects:
            for o in self.subjects:
                yield from o.generateRecursively_(level)
        if self.dataset_description:
            yield from self.dataset_description.generateRecursively_(level)
        if self.README:
            yield from self.README.generateRecursively_(level)
        if self.CHANGES:
            yield from self.CHANGES.generateRecursively_(level)
        if self.LICENSE:
            yield from self.LICENSE.generateRecursively_(level)
        if self.genetic_info:
            yield from self.genetic_info.generateRecursively_(level)
        if self.samples:
            yield from self.samples.generateRecursively_(level)
        if self.participants_tsv:
            yield from self.participants_tsv.generateRecursively_(level)
        if self.participants_json:
            yield from self.participants_json.generateRecursively_(level)
        if self.code:
            yield from self.code.generateRecursively_(level)
        if self.derivatives:
            yield from self.derivatives.generateRecursively_(level)
        if self.sourcedata:
            yield from self.sourcedata.generateRecursively_(level)
        if self.stimuli:
            yield from self.stimuli.generateRecursively_(level)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        super(Dataset, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'subjects':
            obj_ = Subject.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.subjects.append(obj_)
            obj_.original_tagname_ = 'subjects'
        elif nodeName_ == 'dataset_description':
            obj_ = DatasetDescriptionFile.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.dataset_description = obj_
            obj_.original_tagname_ = 'dataset_description'
        elif nodeName_ == 'README':
            class_obj_ = self.get_class_obj_(child_, File)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.README = obj_
            obj_.original_tagname_ = 'README'
        elif nodeName_ == 'CHANGES':
            class_obj_ = self.get_class_obj_(child_, File)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CHANGES = obj_
            obj_.original_tagname_ = 'CHANGES'
        elif nodeName_ == 'LICENSE':
            class_obj_ = self.get_class_obj_(child_, File)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.LICENSE = obj_
            obj_.original_tagname_ = 'LICENSE'
        elif nodeName_ == 'genetic_info':
            class_obj_ = self.get_class_obj_(child_, JsonFile)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.genetic_info = obj_
            obj_.original_tagname_ = 'genetic_info'
        elif nodeName_ == 'samples':
            class_obj_ = self.get_class_obj_(child_, JsonFile)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.samples = obj_
            obj_.original_tagname_ = 'samples'
        elif nodeName_ == 'participants.tsv':
            obj_ = ParticipantsTsvFile.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.participants_tsv = obj_
            obj_.original_tagname_ = 'participants.tsv'
        elif nodeName_ == 'participants.json':
            obj_ = TsvSidecarFile.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.participants_json = obj_
            obj_.original_tagname_ = 'participants.json'
        elif nodeName_ == 'code':
            class_obj_ = self.get_class_obj_(child_, Folder)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.code = obj_
            obj_.original_tagname_ = 'code'
        elif nodeName_ == 'derivatives':
            class_obj_ = self.get_class_obj_(child_, Folder)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.derivatives = obj_
            obj_.original_tagname_ = 'derivatives'
        elif nodeName_ == 'sourcedata':
            class_obj_ = self.get_class_obj_(child_, Folder)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.sourcedata = obj_
            obj_.original_tagname_ = 'sourcedata'
        elif nodeName_ == 'stimuli':
            class_obj_ = self.get_class_obj_(child_, Folder)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.stimuli = obj_
            obj_.original_tagname_ = 'stimuli'
        super(Dataset, self)._buildChildren(child_, node, nodeName_, True)
# end class Dataset


GDSClassesMapping = {
    'dataset': Dataset,
    'metadata': Metadata,
}


USAGE_TEXT = """
Usage: python <Parser>.py [ -s ] <in_xml_file>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def get_root_tag(node):
    tag = Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = GDSClassesMapping.get(tag)
    if rootClass is None:
        rootClass = globals().get(tag)
    return tag, rootClass


def get_required_ns_prefix_defs(rootNode):
    '''Get all name space prefix definitions required in this XML doc.
    Return a dictionary of definitions and a char string of definitions.
    '''
    nsmap = {
        prefix: uri
        for node in rootNode.iter()
        for (prefix, uri) in node.nsmap.items()
        if prefix is not None
    }
    namespacedefs = ' '.join([
        'xmlns:{}="{}"'.format(prefix, uri)
        for prefix, uri in nsmap.items()
    ])
    return nsmap, namespacedefs


def parse(inFileName, silence=False, print_warnings=True):
    global CapturedNsmap_
    gds_collector = GdsCollector_()
    parser = None
    doc = parsexml_(inFileName, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'Dataset'
        rootClass = Dataset
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    CapturedNsmap_, namespacedefs = get_required_ns_prefix_defs(rootNode)
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_=namespacedefs,
            pretty_print=True)
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def parseEtree(inFileName, silence=False, print_warnings=True,
               mapping=None, reverse_mapping=None, nsmap=None):
    parser = None
    doc = parsexml_(inFileName, parser)
    gds_collector = GdsCollector_()
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'Dataset'
        rootClass = Dataset
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if mapping is None:
        mapping = {}
    if reverse_mapping is None:
        reverse_mapping = {}
    rootElement = rootObj.to_etree(
        None, name_=rootTag, mapping_=mapping,
        reverse_mapping_=reverse_mapping, nsmap_=nsmap)
    reverse_node_mapping = rootObj.gds_reverse_node_mapping(mapping)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(str(content))
        sys.stdout.write('\n')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj, rootElement, mapping, reverse_node_mapping


def parseString(inString, silence=False, print_warnings=True):
    '''Parse a string, create the object tree, and export it.

    Arguments:
    - inString -- A string.  This XML fragment should not start
      with an XML declaration containing an encoding.
    - silence -- A boolean.  If False, export the object.
    Returns -- The root object in the tree.
    '''
    parser = None
    rootNode= parsexmlstring_(inString, parser)
    gds_collector = GdsCollector_()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'Dataset'
        rootClass = Dataset
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:bids="https://bids.neuroimaging.io/1.6"')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def parseLiteral(inFileName, silence=False, print_warnings=True):
    parser = None
    doc = parsexml_(inFileName, parser)
    gds_collector = GdsCollector_()
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'Dataset'
        rootClass = Dataset
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from model import *\n\n')
        sys.stdout.write('import model as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def main():
    args = sys.argv[1:]
    if len(args) == 1:
        parse(args[0])
    else:
        usage()


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()

RenameMappings_ = {
}

#
# Mapping of namespaces to types defined in them
# and the file in which each is defined.
# simpleTypes are marked "ST" and complexTypes "CT".
NamespaceToDefMappings_ = {'https://bids.neuroimaging.io/1.6': [('Dataset',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('Subject',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('Session',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('File',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('DatasetDescriptionFile',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('Folder',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('DatatypeFolder',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('Artifact',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('EntityRef',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('Entity',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('Suffix',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('Modality',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('Datatype',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('EntityDep',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('DatatypeContext',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('Metadata',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('JsonFile',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('JsonFileFlatEntry',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('FileMatcher',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('ParticipantsTsvFile',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('TsvSidecarFile',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('TsvFile',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('ParticipantsTsvFileEntry',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('SidecarColumnDescriptor',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('KeyValuePair',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('GeneratedBy',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('SourceDatasets',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT'),
                                      ('GeneratedByContainer',
                                       '../ancpbids/data/schema-files/bids.xsd',
                                       'CT')]}

__all__ = [
    "Artifact",
    "Dataset",
    "DatasetDescriptionFile",
    "Datatype",
    "DatatypeContext",
    "DatatypeFolder",
    "Entity",
    "EntityDep",
    "EntityRef",
    "File",
    "FileMatcher",
    "Folder",
    "GeneratedBy",
    "GeneratedByContainer",
    "JsonFile",
    "JsonFileFlatEntry",
    "KeyValuePair",
    "Metadata",
    "Modality",
    "ParticipantsTsvFile",
    "ParticipantsTsvFileEntry",
    "Session",
    "SidecarColumnDescriptor",
    "SourceDatasets",
    "Subject",
    "Suffix",
    "TsvFile",
    "TsvSidecarFile"
]
