#!/usr/bin/env python
import os, shutil

def replaceInCard(card, replacements):
  with open(card, 'r') as f:  data = f.read()
  for r in replacements:      data = data.replace(r[0], r[1])
  with open(card, 'w') as f:  f.write(data)

#
# Create heavyNeutrino cards for given parameters
# Returns baseName, which can be used to find the cards i.e. as baseName/baseName_*.dat
# mass       - mass of the heavy neutrino particle
# coupling   - mixing parameter between the heavy neutrino and lepton
# flavours   - could be e, mu, tau, 2l (e+mu), 3l (e+mu+tau)
# onshell    - if true, MadSpin onshell options is used, otherwise 'none'
# isPre2017  - use older pdf's as used in Moriond17 campaign
# type       - trilepton (n1 --> llnu) or lljj (n1 --> ljj)
#
def makeHeavyNeutrinoCards(mass, coupling, flavours, onshell, isPre2017, type):
  baseName = 'HeavyNeutrino_' + type + '_M-' + str(mass) + '_V-' + str(coupling) + '_' + flavours + ('_onshell' if onshell else '') + ('_pre2017' if isPre2017 else '') + '_NLO'

  try:    os.makedirs(baseName)
  except: pass

  for card in ['madspin_card', 'extramodels', 'run_card', 'proc_card', 'customizecards']:
    shutil.copyfile('templateCards/HeavyNeutrino_template_NLO_' + card + '.dat', baseName + '/' + baseName + '_' + card + '.dat')

  replacements = [('MASS',     str(mass)),
                  ('COUPLING', str(coupling)),
                  ('FLAVOURS', flavours),
                  ('SPINMODE', 'onshell' if onshell else 'none'),
                  ('TYPE',     type),
                  ('EXTRA',    ('_onshell' if onshell else '') + ('_pre2017' if isPre2017 else ''))]

  if flavours == '2l':    replacements += [('l+ = e+ mu+ ta+', 'l+ = e+ mu+'), ('l- = e- mu- ta-', 'l- = e- mu-')]
  elif flavours == 'e':   replacements += [('l+ = e+ mu+ ta+', 'l+ = e+'),     ('l- = e- mu- ta-', 'l- = e-')]
  elif flavours == 'mu':  replacements += [('l+ = e+ mu+ ta+', 'l+ = mu+'),    ('l- = e- mu- ta-', 'l- = mu-')]
  elif flavours == 'tau': replacements += [('l+ = e+ mu+ ta+', 'l+ = ta+'),    ('l- = e- mu- ta-', 'l- = tau-')]

  if flavours in ['e','mu','2l']:    replacements += [('ldecay+ = e+ mu+ ta+', 'ldecay+ = e+ mu+'), ('ldecay- = e- mu- ta-', 'ldecay- = e- mu-')]
  if flavours in ['3l', '2l', 'e']:  replacements += [('set param_card numixing 1 0.000000e+00', 'set param_card numixing 1 %E' % coupling)]
  if flavours in ['3l', '2l', 'mu']: replacements += [('set param_card numixing 4 0.000000e+00', 'set param_card numixing 4 %E' % coupling)]
  if flavours in ['3l', 'tau']:      replacements += [('set param_card numixing 7 0.000000e+00', 'set param_card numixing 7 %E' % coupling)]

  if isPre2017:
    replacements += [('$DEFAULT_PDF_SETS', '292200')]
    replacements += [('$DEFAULT_PDF_MEMBERS', '292201  =  PDF_set_min\n292302  =  PDF_set_max\nTrue')]

  if type=='lljj':
    replacements += [('decay n1 > ldecay ldecay v', 'decay n1 > ldecay j j')]


  replaceInCard(baseName + '/' + baseName + '_run_card.dat',       replacements)
  replaceInCard(baseName + '/' + baseName + '_proc_card.dat',      replacements)
  replaceInCard(baseName + '/' + baseName + '_customizecards.dat', replacements)
  replaceInCard(baseName + '/' + baseName + '_madspin_card.dat',   replacements)

  return baseName

#
# Use Example:
#
if __name__ == "__main__":
  argsList = [
    (1,     0.11557,     'e',   True,    False, 'trilepton'),
    (1,     0.11505,     'mu',  True,    False, 'trilepton'),
    (1,     0.11505,     'mu',  True,    True,  'lljj'),
    (1,     0.11505,     'mu',  True,    True,  'trilepton')
  ]

  for args in argsList: makeHeavyNeutrinoCards(*args)
