# this script is to get the aligned regions from the sequence alignment
# algorithm.

import Bio.PDB as bpdb
import sys

print('Please input the following: inputpdb  outpdb  target_start  template_start  alignmentfile\n')

input = sys.argv[1]
outname = sys.argv[2]

targ_start = int(sys.argv[3])
temp_start = int(sys.argv[4])

alignment = sys.argv[5]

f = open(alignment, 'r')
strs = f.readline().split()
target = strs[0]
strs = f.readline().split()
template = strs[0]

#target = 'HKTCKLTAFDQIA--PPDQVPIIYFYNSSN---IHNIREQLVKSLSETLTKFYPLAGRFVQDGFYVDCNDEGVLYVEAEVNI---------------PLNEFIGQAKKNIQLINDLVPKKNFKDI-----HSYENPIVGLQMSYFKCGGLAICMYLSHVVADGYTAAAFTKEWSNTTNGIING-------DQLVSSSPINFELATLVPARDLSTVIKPAVMPPSKIKETKVVTRRFLFDENAISAFKDHVIKS--ESVNRPTRVEVVTSVLWKALINQSK-----LPSSTLYFHLNFRGKTGINTPPLDNHFSLCGNFYTQVPTRFRGGNQTKQDLELHELVKLLRGKLRNTLKNCSEINTADGLFLEAASNFNIIQEDLEDEQVDVRIFTTLCRMPLYETEFG--WGKPEWVTIPEMHL-E-IVFLLDTKCGTGIEALVSMDEADMLQFELDPTISAFAS';
#template = 'AFKIQLDTLGQLPGLLSIYTQISLLYPVSDSSQYPTIVSTFEQGLKRFSEAVPWVAGQVKAEG--ISEGNTGTSFIVPFEDVPRVVVKDLRDDPSAPTIEGMRKAGYPMAMFDENIIAPRKTLPIGPGTGPDDPKPVILLQLNFIK-GGLILTVNGQHGAMDMVGQDAVIRLLSKACRNDPFTEEEMTAMNLDRKTIVPYLENYTIGPEVDHQIVKADVAGGDAVLTPVSASWAFFTFSPKAMSELKDAATKTLDASTKFVSTDDALSAFIWKSASRVRLERIDGSAPTEFCRAVDARPAM-----GVSNN--YPGLLQNMTYHNSTIGEIA--NESLGATASRLRSELDPAS-MRQRTRG-LATYLHNNPDKSNVSLTADADPSTSVMLSSWAKVGLWDYDFGLGLGKPETVRRPIFEPVESLMYFMPKKPDGEFCAALSLRDEDMDRLKADKEWTKYAQ';

print('target length is: ' + str(len(target)))
print('template length is: ' + str(len(template)))


if len(target) != len(template):
    print('target length is not equal to template length')


#targ_start = 24;
#temp_start = 2;
targ_ind = targ_start - 1
temp_ind = temp_start - 1
targ_seq = []
temp_seq = []

for i in range(len(target)):
    if template[i] != '-':
        temp_ind = temp_ind + 1
    if target[i] != '-':
        targ_ind = targ_ind + 1
    if target[i] != '-' and template[i] != '-':
        targ_seq.append(targ_ind)
        temp_seq.append(temp_ind)

s = bpdb.PDBParser().get_structure('temp', input)
chain_id = 'A'

print(temp_seq)
print(targ_seq)


def find(resid, seqind):
    for i in range(len(seqind)):
        if resid == seqind[i]:
            return (i + 1)


class ResSelect(bpdb.Select):
    def accept_residue(self, res):
        ind = find(res.id[1], temp_seq)
        if find(res.id[1], temp_seq) > 0 and res.parent.id == chain_id:
            #res.id[1] = targ_seq[ind-1];
            # print ind
            return True
        else:
            return False


io = bpdb.PDBIO()
io.set_structure(s)
io.save('temp1.pdb', ResSelect())


s = bpdb.PDBParser().get_structure('temp', 'temp1.pdb')
chain_id = 'A'
model = s[0]
chain = model['A']
resind = 0
for residue in chain:
    resind = targ_seq[find(residue.id[1], temp_seq) - 1]
    residue.id = (' ', resind, ' ')
io2 = bpdb.PDBIO()
io2.set_structure(s)
io2.save(outname)
