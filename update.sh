#!/bin/bash



# TODO: download svn here, cache and set in path, then delete when finished
#       https://www.visualsvn.com/files/Apache-Subversion-1.14.3.zip

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

declare -a allowed_directories=(
    ElvUI ElvUI_Libraries ElvUI_Options
    AtlasLootClassic AtlasLootClassic_Collections AtlasLootClassic_Crafting
    AtlasLootClassic_Data AtlasLootClassic_DungeonsAndRaids AtlasLootClassic_Factions
    AtlasLootClassic_Options AtlasLootClassic_PvP
)

grep_directories()
{
    echo `find $1 -mindepth 1 -maxdepth 1 -type d`
}

package_allowed_directories()
{
    for dir in `grep_directories .`; do
        dir_name=`basename $dir`
        if [[ ${allowed_directories[@]} =~ $dir_name ]]; then
            cp -r "$dir" "$1"
        #else
        #    echo $dir_name not found
        fi
    done
}

target_directory="$SCRIPT_DIR/package"

rm -rf "$target_directory"
mkdir -p "$target_directory"

# AtlasLoot
pushd AtlasLootClassic_Cata
git reset --hard
pull_result=`git pull --rebase`
package_allowed_directories "$target_directory"
popd

# ElvUI
pushd ElvUI
git reset --hard
git pull --rebase
#rm -rf .release
PACKAGER_URL="https://raw.githubusercontent.com/BigWigsMods/packager/master/release.sh"
curl -s $PACKAGER_URL | bash -s -- -c -d -z
cp -a .release/ElvUI_Libraries/* "ElvUI_Libraries/"
package_allowed_directories "$target_directory"
popd

# search for and remove previous installations, then install from package dir
warcraft_root_relpath=`realpath -s --relative-to="$SCRIPT_DIR" "$SCRIPT_DIR/../"`
for di in `find "$warcraft_root_relpath" -mindepth 1 -maxdepth 1 -type d -name "_*"`; do
    current_addons_path="$di/Interface/AddOns"
    for addon in ${allowed_directories[@]}; do
        if test -d "$current_addons_path/$addon"; then
            echo "deleting directory: $current_addons_path/$addon"
            rm -rf "$current_addons_path/$addon"
        fi
        if test -d "$target_directory/$addon"; then
            echo "moving directory: $target_directory/$addon to $current_addons_path/$addon"
            cp -r "$target_directory/$addon" "$current_addons_path"
        fi
    done
done


#### ATTIC

## if the repo exists and doesn't have an update, don't build and package it
# if [[ "$pull_result" =~ "Already up to date" ]]; then
#     echo "detected no changes, skipping"
# else
#     package_allowed_directories "$target_directory"
# fi

## allow for installation to only specified flavors
# if [[ "$di" =~ "_retail_" ]]; then
#     echo "skipping retail, for now"
#     continue
# fi
