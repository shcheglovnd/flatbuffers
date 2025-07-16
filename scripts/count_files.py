#!/usr/bin/env python3
#
# Copyright 2024 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
from pathlib import Path


def count_files(root_dir, exclude_dirs=None, include_hidden=False, verbose=False):
    """
    Count the number of files in the repository using pathlib.
    
    Args:
        root_dir: Root directory to start counting from
        exclude_dirs: Set of directory names to exclude from counting
        include_hidden: Whether to include hidden files and directories
        verbose: Whether to print detailed information
    
    Returns:
        Total number of files found
    """
    # Note: exclude_dirs=None means no exclusions, different from default behavior
    
    file_count = 0
    excluded_files = 0
    root_path = Path(root_dir).resolve()
    
    # Use pathlib to recursively find all files
    for file_path in root_path.rglob('*'):
        if file_path.is_file():
            # Check if path should be excluded based on exclude_dirs
            excluded_by_dir = False
            if exclude_dirs:
                relative_parts = file_path.relative_to(root_path).parts
                excluded_by_dir = any(part in exclude_dirs for part in relative_parts)
            
            # Check if file should be included based on include_hidden
            included_by_visibility = include_hidden or not file_path.name.startswith('.')
            
            if excluded_by_dir:
                excluded_files += 1
            elif included_by_visibility:
                file_count += 1
            else:
                # Hidden file, not included due to visibility, not directory exclusion
                excluded_files += 1
    
    if verbose:
        print(f"Files included: {file_count}")
        print(f"Files excluded: {excluded_files}")
        print(f"Total files found: {file_count + excluded_files}")
    
    return file_count


def main():
    parser = argparse.ArgumentParser(
        description='Count the number of files in the FlatBuffers repository'
    )
    parser.add_argument(
        '--root',
        default='.',
        help='Root directory to count files from (default: current directory)'
    )
    parser.add_argument(
        '--include-hidden',
        action='store_true',
        help='Include hidden files and directories in the count'
    )
    parser.add_argument(
        '--exclude',
        nargs='*',
        default=['.git', '__pycache__', '.pytest_cache', 'node_modules', 
                'build', 'CMakeFiles', '.bazelci', '.github'],
        help='Directories to exclude from counting (default: common build/cache dirs)'
    )
    parser.add_argument(
        '--no-exclude',
        action='store_true',
        help='Do not exclude any directories'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed information about counting process'
    )
    
    args = parser.parse_args()
    
    # Get the script path and derive the root path
    script_path = Path(__file__).parent.resolve()
    root_path = script_path.parent.absolute() if args.root == '.' else Path(args.root).resolve()
    
    exclude_dirs = None if args.no_exclude else set(args.exclude)
    
    # Set default exclusions if not explicitly disabled
    if exclude_dirs is not None and not exclude_dirs:
        exclude_dirs = {'.git', '__pycache__', '.pytest_cache', 'node_modules', 
                       'build', 'CMakeFiles', '.bazelci', '.github'}
    
    if args.verbose:
        print(f"Exclude directories: {exclude_dirs}")
        print(f"Include hidden files: {args.include_hidden}")
    
    file_count = count_files(root_path, exclude_dirs, args.include_hidden, args.verbose)
    
    print(f"Total files in {root_path}: {file_count}")
    
    if exclude_dirs:
        print(f"Excluded directories: {', '.join(sorted(exclude_dirs))}")
    else:
        print("No directories excluded")


if __name__ == '__main__':
    main()