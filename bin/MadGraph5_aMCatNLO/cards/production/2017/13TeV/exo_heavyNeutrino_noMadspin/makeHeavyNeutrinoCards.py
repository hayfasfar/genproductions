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
# type       - trilepton (n1 --> llnu) or lljj (n1 --> ljj)
#
def makeHeavyNeutrinoCards(mass, coupling, flavours, type):
  baseName = 'HeavyNeutrino_noMadspin_' + type + '_M-' + str(mass) + '_V-' + str(coupling) + '_' + flavours + '_NLO'

  try:    os.makedirs(baseName)
  except: pass

  for card in ['extramodels', 'run_card', 'proc_card', 'customizecards']:
    shutil.copyfile('templateCards/HeavyNeutrino_noMadspin_template_NLO_' + card + '.dat', baseName + '/' + baseName + '_' + card + '.dat')

  replacements = [('MASS',     str(mass)),
                  ('COUPLING', str(coupling)),
                  ('FLAVOURS', flavours),
                  ('TYPE',     type),

  if flavours in ['3l', '2l', 'e']:  replacements += [('set param_card numixing 1 0.000000e+00', 'set param_card numixing 1 %E' % coupling)]
  if flavours in ['3l', '2l', 'mu']: replacements += [('set param_card numixing 4 0.000000e+00', 'set param_card numixing 4 %E' % coupling)]
  if flavours in ['3l', 'tau']:      replacements += [('set param_card numixing 7 0.000000e+00', 'set param_card numixing 7 %E' % coupling)]

  if isPre2017:
    replacements += [('$DEFAULT_PDF_SETS', '292200')]
    replacements += [('$DEFAULT_PDF_MEMBERS', '292201  =  PDF_set_min\n292302  =  PDF_set_max\nTrue')]

  if type=='lljj':
    replacements += [('n1 > l l l v', 'n1 > l l j j')]


  replaceInCard(baseName + '/' + baseName + '_run_card.dat',       replacements)
  replaceInCard(baseName + '/' + baseName + '_proc_card.dat',      replacements)
  replaceInCard(baseName + '/' + baseName + '_customizecards.dat', replacements)

  return baseName

#
# Use Example:
#
if __name__ == "__main__":
  argsList = [
    (1, 0.11557, 'e',  'trilepton'),
    (1, 0.11505, 'mu', 'trilepton'),
    (1, 0.11505, 'mu', 'lljj'),
    (1, 0.11505, 'mu', 'trilepton')
  ]

  for args in argsList: makeHeavyNeutrinoCards(*args)
