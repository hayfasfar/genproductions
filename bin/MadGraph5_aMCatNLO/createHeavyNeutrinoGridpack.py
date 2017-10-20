#!/usr/bin/env python

#
# Creates both the cards, prompt and displaced gridpack, and moves them to some public directory
#

import sys, os, fnmatch, shutil
type, mass, coupling, flavor = sys.argv[1:]
queue = 'cream02'

path = './cards/production/2017/13TeV/exo_heavyNeutrino/'

def intOrFloat(str):
  try:    return int(str)
  except: return float(str)

def createCards(path, mass, coupling, flavor, spinmode, isPre2017, type):
  sys.path.append(path)
  from makeHeavyNeutrinoCards import makeHeavyNeutrinoCards
  cwd = os.getcwd()
  os.chdir(path)
  print os.getcwd()
  baseName = makeHeavyNeutrinoCards(intOrFloat(mass), float(coupling), flavor, spinmode, isPre2017, type)
  os.chdir(cwd)
  return baseName

def createGridpack(path, mass, coupling, flavor, spinmode, isPre2017, type):
  baseName = createCards(path, mass, coupling, flavor, spinmode, isPre2017, type)
  os.system('./gridpack_generation.sh ' + baseName + ' ' + path + '/' + baseName + ' ' + queue)
  for file in os.listdir('.'):
    if fnmatch.fnmatch(file, baseName + '*.tar.xz'):
      return file


gridpack = createGridpack(path, mass, coupling, flavor, 'onshell', True, type)
shutil.copyfile(gridpack, '~/public/production/gridpacks/prompt/' + gridpack)
os.system('./fixGridpackForDisplaced.sh ' + gridpack)
shutil.move(gridpack, '~/public/production/gridpacks/displaced/' + gridpack)
shutil.rmtree(gridpack.split('_slc')[0])
