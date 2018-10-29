
import argparse
import os


def parse_conf(s):
    v = s.split('%')
    r = ' 0.' + v[0].strip()
    return r

def parse_coords(s):
    v = s.split(',')
    c = [0, 0, 0, 0]
    for idx, ss in enumerate(v):
        c[idx] = int(ss.split('=')[1].strip())
    c[2] = c[2] - c[0]
    c[3] = c[3] - c[1]
    return ' {:4d} {:4d} {:4d} {:4d}'.format(c[0], c[1], c[2], c[3])


parser = argparse.ArgumentParser(description='convert batch detect output to rsna submission, based on image.c mods')
parser.add_argument(
    '-i',
    '--input_file',
    help='name of file to read',
    default='result.txt')
parser.add_argument(
    '-o',
    '--output_file',
    help='name of file to write',
    default='submit.txt')

args = parser.parse_args()

#print(args.input_file, args.output_file)

f_in = open(args.input_file, 'r')
f_out = open(args.output_file, 'w')

f_out.write('patientId,PredictionString\n')

s_out = ''

for l in f_in:
    s = l.split(':')
    if len(s) == 3 and s[0].startswith('Enter'):
        if s_out != '':
            f_out.write('{}\n'.format(s_out))
        s_out = os.path.splitext(os.path.basename(s[1]))[0] + ','

    if len(s) == 2 and s[0].startswith('pneu'):
        s_out += parse_conf(s[1])

    if len(s) == 1 and s[0].startswith('L='):
        s_out += parse_coords(s[0])

if s_out != '':
    f_out.write('{}\n'.format(s_out))

f_in.close()
f_out.close()




