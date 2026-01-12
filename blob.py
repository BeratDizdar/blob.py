'''
  blob.py - Binary to C Header Packer
  
  Copyright (c) 2026 BeratDizdar

  This software is provided 'as-is', without any express or implied
  warranty. In no event will the authors be held liable for any damages
  arising from the use of this software.

  Permission is granted to anyone to use this software for any purpose,
  including commercial applications, and to alter it and redistribute it
  freely, subject to the following restrictions:

  1. The origin of this software must not be misrepresented; you must not
     claim that you wrote the original software. If you use this software
     in a product, an acknowledgment in the product documentation would be
     appreciated but is not required.
  2. Altered source versions must be plainly marked as such, and must not be
     misrepresented as being the original software.
  3. This notice may not be removed or altered from any source distribution.
'''

import os, sys, argparse

parser = argparse.ArgumentParser(description="Binary to C Header tool")
parser.add_argument("file", type=argparse.FileType('rb'), help="input path")
parser.add_argument("--output", "-o", type=str, default="a.h", help="output name")
args = parser.parse_args()

try:
    data = args.file.read()
finally:
    raw_filename = args.file.name
    args.file.close()

base_name = os.path.basename(raw_filename)
clean_name = base_name.replace(".", "_").replace("-", "_")
var_upper = clean_name.upper()

with open(args.output, 'w') as f_out:
    f_out.write(f"#ifndef {var_upper}_H\n")
    f_out.write(f"#define {var_upper}_H\n\n")
    f_out.write(f"unsigned int {clean_name}_len = {len(data)};\n\n")
    f_out.write(f"unsigned char {clean_name}[] = {{\n")

    cols = 12
    for i in range(0, len(data), cols):
        chunk = data[i:i+cols]
        hex_str = ", ".join([f"0x{b:02x}" for b in chunk])
        f_out.write(f"    {hex_str},\n")

    f_out.write("};\n\n")
    f_out.write(f"#endif // {var_upper}_H\n")
