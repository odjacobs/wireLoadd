# WireLoadd, a simple library for downloading many files
# Copyright (C) 2022  odjacobs

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from multiprocessing import Pool
from os import path, mkdir
import time

# Download individual files
def getContent(args):
    import requests

    url, filename = args[0], args[1]

    t0 = time.time()
    try:
        r = requests.get(url)

        with open(filename, "wb") as f:
            f.write(r.content)
        return (url, time.time() - t0)
    except Exception:
        return f"Failed to download {url}"


# The brains of the operation
def download(urls, savePath="Downloads", threads=2):
    # See if the folder exists and if not make it
    if not (path.exists(savePath)):
        mkdir(savePath)

    # name files based on enumeration while preserving extension
    # it is assumed that every url has an extension but for the usecase
    # I see no reason to change that
    fileNames = []
    for i, url in enumerate(urls):
        fileNames.append(f"{savePath}/{i}.{url.split('.')[-1]}")
    p = Pool(threads)
    for i in p.imap_unordered(getContent, zip(urls, fileNames)):
        print(i)
