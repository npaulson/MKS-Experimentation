# -*- coding: utf-8 -*-
"""
Created on Tue Sep 02 11:45:04 2014

@author: nhpnp3
"""

el = 21;
ns = 10;
set_id = 'test1'

## put the function nodesets here

top50_f = open('50top.inp', 'r')
top50 = top50_f.read()
top50_f.close()

nodesets_f = open('nodesets.inp', 'r')
nodesets = nodesets_f.read()
nodesets_f.close()

BCs_f = open('periodicCE.inp','r')
BCs = BCs_f.read()
BCs_f.close()

bottom50_f = open('50bottom.inp','r')
bottom50 = bottom50_f.read()
bottom50_f.close()

l1 = '**** ------------------------------------------------\n'
l2 = '** MATERIALS\n'
l3 = '**\n'
l4 = '** Orientation file is included separately as a distribution table\n'
l5 = '**\n'
l7 = '**\n'
l9 = '1.\n'
l10 = '**\n'

sn = 5

inpfile = open('ti_alpha_' + str(sn) + '_' + set_id + '.inp', 'w+')
inpfile.write(top50 + '\n')
inpfile.write(nodesets + '\n')
inpfile.write(BCs + '\n')

l6 = '*Include, input=orientation' + str(sn) + '.inp\n'
l8 = '*Solid Section, elset=allel, material=material-1, orientation=ori' + str(sn) + '\n'
inpfile.write(l1 + l2 + l3 + l4 + l5 + l6 + l7 + l8 + l9 + l10)

inpfile.write(bottom50)

inpfile.close()