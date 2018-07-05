#!/usr/bin/env python

#
# Creates both the cards, prompt and displaced gridpack, and moves them to some public directory
#

import sys, os, fnmatch, shutil, math, numpy, time
type, mass, couplings, flavor = sys.argv[1:]
queue = 'cream02'

path = './cards/production/2017/13TeV/exo_heavyNeutrino_noMadspin/'

def intOrFloat(str):
  try:    return int(str)
  except: return float(str)

def createCards(path, mass, coupling, flavor, spinmode, isPre2017, type):
  sys.path.append(path)
  from makeHeavyNeutrinoCards import makeHeavyNeutrinoCards
  cwd = os.getcwd()
  os.chdir(path)
  baseName = makeHeavyNeutrinoCards(intOrFloat(mass), float(coupling), flavor, spinmode, isPre2017, type)
  os.chdir(cwd)
  return baseName

def findGridpack(dir, baseName):
  for file in os.listdir(dir):
    if fnmatch.fnmatch(file, baseName + '*.tar.xz'):
      return file
  return None

def createGridpack(path, mass, coupling, flavor, spinmode, isPre2017, type):
  baseName = createCards(path, mass, coupling, flavor, spinmode, isPre2017, type)
  gridpack = findGridpack('/user/tomc/public/production/gridpacks/displaced', baseName)
  if gridpack:
    print gridpack + ' already exist, skipping'
    return None
  else:
    print 'Creating ' + baseName
  gridpack = findGridpack('.', baseName)
  if gridpack: return gridpack
  os.system('./gridpack_generation.sh ' + baseName + ' ' + path + '/' + baseName + ' ' + queue)
  time.sleep(10)
  gridpack = findGridpack('.', baseName)
  if gridpack: shutil.rmtree(gridpack.split('_slc')[0])
  return gridpack

if couplings=='all':
  v2s       = [5e-4, 3e-4, 2e-4, 1e-4, 7e-5, 5e-5, 3e-5, 2e-5, 1e-5, 8e-6, 6e-6]
  if   intOrFloat(mass) > 8: v2s = v2s[7:]
  elif intOrFloat(mass) > 7: v2s = v2s[6:]
  elif intOrFloat(mass) > 6: v2s = v2s[5:]
  elif intOrFloat(mass) > 5: v2s = v2s[4:]
  elif intOrFloat(mass) > 4: v2s = v2s[3:]
  elif intOrFloat(mass) > 3: v2s = v2s[2:]
  elif intOrFloat(mass) > 2: v2s = v2s[1:]
  print v2s
  couplings = [math.sqrt(v2) for v2 in v2s]
else:
  couplings = [couplings]

def logFilesOk(gridpack):
  try:
    with open(gridpack.split('LO')[0] + 'LO.log') as f:
      for line in f:
        if '+' in line: continue
        if 'tar: Error is not recoverable: exiting now' in line: return False
  except:
    pass
  return True

for coupling in couplings:
  while True:
    gridpack = createGridpack(path, mass, coupling, flavor, False, False, type)
    if (not gridpack) or logFilesOk(gridpack): break
    if gridpack: shutil.move(gridpack, gridpack + '_problem')
  time.sleep(10)
  if gridpack:
    print gridpack + ' --> prompt done'
    shutil.copyfile(gridpack, '/user/' + os.environ['USER'] + '/public/production/gridpacks/prompt/' + gridpack)
    print gridpack + ' --> fixing for displaced'
    os.system('./fixGridpackForDisplaced.sh ' + gridpack)
    shutil.move(gridpack, '/user/' + os.environ['USER'] + '/public/production/gridpacks/displaced/' + gridpack)
    print gridpack + ' --> displaced done'
    try:    os.remove(gridpack.split('LO')[0] + 'LO.log')
    except: pass
