#!/usr/bin/env bash

set -e

# GNU prefix command for bsd/mac os support (gsed, gsplit)
GP=
if [[ "$OSTYPE" == *bsd* ]] || [[ "$OSTYPE" =~ darwin* ]]; then
  GP=g
fi

RED='\033[0;31m'
NC='\033[0m' # No Color

DEBUG=$1

RETURN_CODE=0
MODULES=()

while read -r LINE; do
  FILE=$(echo "${LINE}" | cut -d: -f1)
  SETTING=$(echo "${LINE}" | cut -d: -f2,3,4,5,6 | ${GP}sed -r 's/^.*static +const +inline +QgsSettingsEntry[^ ]+ +(\w+).*$/\1/')
  MODULE=$(echo "${FILE}" | cut -d/ -f2)
  SUBFOLDER=$([[ ${MODULE} =~ (core|gui) ]] && echo "settings" || echo "")
  REG_FILE="src/${MODULE}/${SUBFOLDER}/qgssettingsregistry${MODULE}.cpp"
  COUNT_VAR="COUNT_${MODULE}"

  if [[ ${DEBUG} -eq 1 ]]; then
    echo LINE: "${LINE}"
    echo SETTING: "${SETTING}"
    echo MODULE: "${MODULE}"
    echo SUBFOLDER: "${SUBFOLDER}"
    echo REG_FILE: "${REG_FILE}"
    echo COUNT_VAR: "${COUNT_VAR} => ${!COUNT_VAR}"
  fi

  if [[ -z "${!COUNT_VAR}" ]]; then
    MODULES+=("${MODULE}")
    declare "COUNT_${MODULE}"=1
  else
    declare "COUNT_${MODULE}=$(( ${!COUNT_VAR} + 1 ))"
  fi

  if ( ! grep -E -q "addSettingsEntry. \&(\w+::)?${SETTING} " "${REG_FILE}" ); then
    # check if the setting is not in a group
    GROUP_LINE=$(git grep -E "QgsSettingsEntryGroup\([^()]*${SETTING}" ${FILE} | head -1)
    if [[ -n "${GROUP_LINE}" ]]; then
      GROUP_NAME=$(echo "${GROUP_LINE}" | cut -d: -f2 | ${GP}sed -r 's/^.*QgsSettingsEntryGroup +(\w+) *=.*$/\1/')
      GROUP_COUNT_VAR_NAME="GROUP_COUNT_${MODULE}_${GROUP_NAME}"
      if [[ -z "${!GROUP_COUNT_VAR_NAME}" ]]; then
        declare "GROUP_COUNT_${MODULE}_${GROUP_NAME}"=1
      else
        declare "GROUP_COUNT_${MODULE}_${GROUP_NAME}=$(( ${!GROUP_COUNT_VAR_NAME} + 1 ))"
      fi
    else
      echo -e "ERROR: setting ${RED}${SETTING}${NC} defined in ${RED}${FILE}${NC} not added to the registry (${REG_FILE})"
      RETURN_CODE=1
    fi
  fi

done <<< $(git grep -E --perl-regex 'static +const( +inline)? +QgsSettingsEntry(?!Group)[^ ]+ +\w+' src)

echo "*** Self-check"
# check that the number of items in each registry corresponds to what was found (for safety on this script)
for MODULE in "${MODULES[@]}"; do
  SUBFOLDER=$([[ ${MODULE} =~ (core|gui) ]] && echo "settings" || echo "")
  REG_FILE="src/${MODULE}/${SUBFOLDER}/qgssettingsregistry${MODULE}.cpp"
  COUNT=$(${GP}grep --only-matching -c --perl-regex 'addSettingsEntry(?!Group)' "${REG_FILE}")
  # also add the grouped settings
  while read -u 3 -r GROUP_LINE; do
    GROUP_NAME=$(echo "${GROUP_LINE}" | ${GP}sed -r 's/^.*addSettingsEntryGroup\( *(\&\w+::)?(\w+) *\).*$/\2/')
    GROUP_COUNT_VAR_NAME="GROUP_COUNT_${MODULE}_${GROUP_NAME}"
    if [[ -z "${!GROUP_COUNT_VAR_NAME}" ]]; then
      if [[ ${RETURN_CODE} == 0 ]]; then
        echo "Hmmm ${GROUP_COUNT_VAR_NAME} variable doesn't exist. Test might be broken if the code is compiling"
        RETURN_CODE=1
      fi
    else
      COUNT=$((COUNT+${!GROUP_COUNT_VAR_NAME}))
    fi
  done 3< <(git grep --only-matching -E 'addSettingsEntryGroup\( *(\&\w+::)?(\w+) *\)' ${REG_FILE})
  COUNT_VAR="COUNT_${MODULE}"
  if [[ ${COUNT} == "${!COUNT_VAR}" ]]; then
    echo "${MODULE}: OK: ${COUNT} settings"
  else
    echo "${MODULE}: ERROR settings count mismatch for (${COUNT} vs ${!COUNT_VAR})"
    if [[ ${RETURN_CODE} == 0 ]]; then
      echo "Hmmm it looks like this test is broken! (some errors should have been raised before)"
    fi
    RETURN_CODE=1
  fi
done

exit ${RETURN_CODE}
