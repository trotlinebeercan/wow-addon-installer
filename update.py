#!/usr/bin/env python

# standard imports
import errno
import os
import shutil
import subprocess
import urllib.request

# local imports
from lib.addonrepo import AddonRepo

TEST_MODE=0

PACKAGER_URL="https://raw.githubusercontent.com/BigWigsMods/packager/master/release.sh"
PACKAGER_ARGS="-d -z" # -c

SCRIPT_PATH=os.path.dirname(os.path.realpath(__file__))
WOW_ROOT_PATH=os.path.realpath(os.path.join(SCRIPT_PATH, ".."))
WOW_FLAVOR_PREFIX="=" if TEST_MODE else "_"
REPO_SOURCES_PATH=os.path.join(SCRIPT_PATH, "sources")

if TEST_MODE:
    ADDON_REPOSITORIES=[
        AddonRepo("https://github.com/fusionpit/TalentSequence", "master", REPO_SOURCES_PATH),
        AddonRepo("https://github.com/wow-rp-addons/LibMSP", "main", REPO_SOURCES_PATH),
    ]
else:
    ADDON_REPOSITORIES=[
        AddonRepo("https://github.com/snowflame0/AtlasLootClassic_Cata", "main", REPO_SOURCES_PATH),
        AddonRepo("https://github.com/tukui-org/ElvUI", "main", REPO_SOURCES_PATH),
        AddonRepo("https://github.com/WeakAuras/WeakAuras2", "main", REPO_SOURCES_PATH),
    ]

def copyanything(src, dst):
    print(f"copying {src} to {dst}")
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)
        else: raise

def create_package(repo_path):
    urllib.request.urlretrieve(PACKAGER_URL, os.path.join(repo_path, "release.sh"))
    subprocess.check_output(f"bash release.sh {PACKAGER_ARGS}".split(), cwd=repo_path)

def install_package(repo_path, flavor_path):
    release_path = os.path.join(repo_path, ".release")
    for x in os.listdir(release_path):
        src = os.path.join(release_path, x)
        dst = os.path.join(flavor_path, x)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        if os.path.isdir(src):
            copyanything(src, dst)

def main():
    wow_addons_install_paths = []
    for x in os.listdir(WOW_ROOT_PATH):
        if x.startswith(WOW_FLAVOR_PREFIX):
            pt = os.path.realpath(os.path.join(WOW_ROOT_PATH, x, "Interface", "AddOns"))
            print(f"found flavor {pt}")
            wow_addons_install_paths.append(pt)

    for repo in ADDON_REPOSITORIES:
        print(f"Running in '{repo.path()}'")
        create_package(repo.path())
        for flavor in wow_addons_install_paths:
            install_package(repo.path(), flavor)

if __name__ == "__main__":
    main()
