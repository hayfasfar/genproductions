#!/usr/bin/env python
import os, shutil

def replaceInCard(card, replacements):
  with open(card, 'r') as f:  data = f.read()
  for r in replacements:      data = data.replace(r[0], r[1])
  with open(card, 'w') as f:  f.write(data)

def makeHeavyNeutrinoCards(mass, coupling, flavours):
  baseName = 'HeavyNeutrino_samesign_M-' + str(mass) + '_V-' + str(coupling) + '_' + flavours + '_NLO'

  try:    os.makedirs(baseName)
  except: pass

  for card in ['madspin_card', 'extramodels', 'run_card', 'proc_card', 'customizecards']:
    shutil.copyfile('templateCards/HeavyNeutrino_samesign_template_NLO_' + card + '.dat', baseName + '/' + baseName + '_' + card + '.dat')

  replacements = [('MASS', str(mass)), ('COUPLING', str(coupling)), ('FLAVOURS', flavours)]

  if flavours == '2l':    replacements += [('l+ = e+ mu+ ta+', 'l+ = e+ mu+'), ('l- = e- mu- ta-', 'l- = e- mu-')]
  elif flavours == 'e':   replacements += [('l+ = e+ mu+ ta+', 'l+ = e+'),     ('l- = e- mu- ta-', 'l- = e-')]
  elif flavours == 'mu':  replacements += [('l+ = e+ mu+ ta+', 'l+ = mu+'),    ('l- = e- mu- ta-', 'l- = mu-')]
  elif flavours == 'tau': replacements += [('l+ = e+ mu+ ta+', 'l+ = ta+'),    ('l- = e- mu- ta-', 'l- = tau-')]

  if flavours in ['e','mu','2l']:    replacements += [('ldecay+ = e+ mu+ ta+', 'ldecay+ = e+ mu+'), ('ldecay- = e- mu- ta-', 'ldecay- = e- mu-')]

  if flavours in ['3l', '2l', 'e']:  replacements += [('set param_card numixing 1 0.000000e+00', 'set param_card numixing 1 %E' % coupling)]
  if flavours in ['3l', '2l', 'mu']: replacements += [('set param_card numixing 4 0.000000e+00', 'set param_card numixing 4 %E' % coupling)]
  if flavours in ['3l', 'tau']:      replacements += [('set param_card numixing 7 0.000000e+00', 'set param_card numixing 7 %E' % coupling)]

  replaceInCard(baseName + '/' + baseName + '_proc_card.dat',      replacements)
  replaceInCard(baseName + '/' + baseName + '_customizecards.dat', replacements)


combinations = [
  (5,      0.01,     'e'),
  (5,      0.01,     'mu'),
  (5,      0.01,     '2l'),
  (10,     0.01,     'e'),
  (10,     0.01,     'mu'),
  (10,     0.01,     '2l'),
  (20,     0.01,     'e'),
  (20,     0.01,     'mu'),
  (20,     0.01,     '2l'),
  (30,     0.01,     'e'),
  (30,     0.01,     'mu'),
  (30,     0.01,     '2l'),
]

for mass, coupling, flavour in combinations:
  makeHeavyNeutrinoCards(mass, coupling, flavour)
