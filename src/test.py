from re import S
from SYM import SYM
from NUM import NUM
from strings import o, oo, show
from lists import map
from utils import getThe, setThe, cliffsDelta, diffs, rand, rint, rnd, setSeed, get_ofile, copy, last, has, value
from repgrid import repcols, reprows, repplace, repgrid
from csv import csv
from DATA import DATA
from bins import bins

def settings_test():
    err = 0
    val = oo(getThe())
    err += 1 if val != '{:Far 0.95 :Sample 512 :dump false :file etc/data/auto93.csv :go all :help false :min 0.5 :p 2 :seed 937162211}' else 0
    return 0

def rand_test():
    err = 0
    
    r1, r2 = [], []
    setSeed(1)
    for i in range(10000): r1.append(rint(100, 0))
    setSeed(1)
    for i in range(10000): r2.append(rint(100, 0))

    for (i, v) in enumerate(r1): assert(v == r2[i])

    return err

def sym_test():
    err, sym = 0, SYM()
    for c in ["a","a","a","a","b","b","c"]:
        sym.add(c)
    
    print(sym.mid(), rnd(sym.div()))

    if sym.mid() != "a":
        err += 1
    if sym.div() > (1.379 + 0.001) or sym.div() < (1.379 - 0.001):
        err += 1
    return err

def num_test():
    num1, num2 = NUM(), NUM()
    for i in range(1, 10001): num1.add(rand())
    for i in range(1, 10001): num2.add(rand()**2)
    print(1, rnd(num1.mid()), rnd(num1.div()))
    print(2, rnd(num2.mid()), rnd(num2.div()))
    return 0.5 == rnd(num1.mid()) and num1.mid() > num2.mid()

def csv_test():
    err, n = 0, 0
    t = csv(getThe()['file'])

    for i in range(len(t)):
        for j in range(len(t[i])):
            n += 1
    if n != 8*399:
        err += 1
    return err

def data_test():
    err = 0
    
    data = DATA(getThe()['file'])
    col = data.cols.xcols[0]
    print(col.lo, col.hi, col.mid(), col.div())
    oo(data.stats())

    return err

def stats_test():
    err = 0
    res = ''
    data = DATA(getThe()['file'], None, None)
    for k, cols in zip(['y', 'x'], [data.cols.ycols, data.cols.xcols]):
        res += k + ' mid ' + o(data.stats('mid', cols, 2)) + '\n'
        res += ' ' + ' div ' + o(data.stats('div', cols, 2))
        if k != 'x': res += '\n'
    print(res)
    get_ofile().write(res + '\n')
    err += 1 if res != 'y mid {:Acc+ 15.57 :Lbs- 2970.42 :Mpg+ 23.84}\n  div {:Acc+ 2.76 :Lbs- 846.84 :Mpg+ 8.34}\nx mid {:Clndrs 5.45 :Model 76.01 :Volume 193.43 :origin 1}\n  div {:Clndrs 1.7 :Model 3.7 :Volume 104.27 :origin 1.3273558482394003}' else 0
    return err

def clone_test():
    err = 0
    
    data1 = DATA(getThe()['file'])
    data2 = data1.clone(data1.rows)
    oo(data1.stats())
    oo(data2.stats())

    return err

def around_test():
    err = 0
    o_file = get_ofile()
    data = DATA(getThe()['file'], None, None)
    
    around_dict = data.around(data.rows[0], None)
    
    pval = str(0) + ' ' + str(0) + ' ' + o(data.rows[0].cells)
    print(pval)
    o_file.write(pval + '\n')

    for n, (r, t) in enumerate(around_dict.items()):
        if n>0 and (n+1)%50==0:
            pval = str(n+1) + ' ' + str(rnd(t['dist'], 2)) + ' ' +  str(o(t['row'].cells))
            print(pval)
            o_file.write(pval + '\n')

    return err

def half_test():
    err = 0
    o_file = get_ofile()

    data = DATA(getThe()['file'], None, None)
    left, right, A, B, mid, c = data.half(None, None, None)
    
    print(len(left), len(right))
    l, r = data.clone(left), data.clone(right)
    print('l', o(l.stats()))
    print('r', o(r.stats()))

    return err

def cluster_test():  
    err = 0

    data = DATA(getThe()['file'])
    show(data.cluster(), 'mid', data.cols.ycols, 1, None)

    return err

def optimize_test():
    err = 0

    data = DATA(getThe()['file'])
    best, rest = data.sway()

    print('\nall\t', o(data.stats()))
    print('   \t', o(data.stats(_what='div')))
    print('\nbest\t', o(best.stats()))
    print('    \t', o(best.stats(_what='div')))
    print('\nrest\t', o(rest.stats()))
    print('    \t', o(rest.stats(_what='div')))
    print('\nall ~= best?', o(diffs(best.cols.ycols, data.cols.ycols)))
    print('best ~= rest?', o(diffs(best.cols.ycols, rest.cols.ycols)))

    return err

def copy_test():
    t1 = { 'a': 1, 'b': { 'c': 2, 'd': [3] } }
    t2 = copy(t1)
    t2['b']['d'][0] = 10000
            
    print('b4\t', end='')
    get_ofile().write('b4\t')
    oo(t1)
    print('\nafter\t')
    get_ofile().write('after\t')
    oo(t2)

    return 0

def repcols_test():
    t = repcols(getThe()['file'])
    
    try:
        for col in t.cols.xcols:
            print('{' + 'a NUM' + ' :at {}'.format(col.get_pos()) + ' :hi {}'.format(col.hi) + ' :lo {}'.format(col.lo) + ' :m2 {}'.format(rnd(col.m2, 3)) + ' :mu {}'.format(rnd(col.mu), 3) + ' :n {}'.format(col.total) + ' :txt {}'.format(col.get_name()) + '}')
            get_ofile().write('{' + 'a NUM' + ' :at {}'.format(col.get_pos()) + ' :hi {}'.format(col.hi) + ' :lo {}'.format(col.lo) + ' :m2 {}'.format(rnd(col.m2, 3)) + ' :mu {}'.format(rnd(col.mu), 3) + ' :n {}'.format(col.total) + ' :txt {}'.format(col.get_name()) + '}\n')
    except Exception:
        pass

    try:
        for row in t.rows:
            print('{' + 'a ROW :cells ' + str(row.cells) + '}')
            get_ofile().write('{' + 'a ROW :cells ' + str(row.cells) + '}\n')
    except Exception:
        pass

    return 0

def reprows_test():
    t = reprows(getThe()['file'])
    
    try:
        for col in t.cols.xcols:
            print('{' + 'a NUM' + ' :at {}'.format(col.get_pos()) + ' :hi {}'.format(col.hi) + ' :lo {}'.format(col.lo) + ' :m2 {}'.format(rnd(col.m2, 3)) + ' :mu {}'.format(rnd(col.mu), 3) + ' :n {}'.format(col.total) + ' :txt {}'.format(col.get_name()) + '}')
            get_ofile().write('{' + 'a NUM' + ' :at {}'.format(col.get_pos()) + ' :hi {}'.format(col.hi) + ' :lo {}'.format(col.lo) + ' :m2 {}'.format(rnd(col.m2, 3)) + ' :mu {}'.format(rnd(col.mu), 3) + ' :n {}'.format(col.total) + ' :txt {}'.format(col.get_name()) + '}\n')
    except Exception:
        pass

    try:
        for row in t.rows:
            print('{' + 'a ROW :cells ' + str(row.cells) + '}')
            get_ofile().write('{' + 'a ROW :cells ' + str(row.cells) + '}\n')
    except Exception:
        pass

    return 0

def synonyms_test():
    t = repcols(getThe()['file'])
    clustered = t.cluster(cols=t.cols.xcols)
    show(clustered)

    return 0

def prototypes_test():
    t = reprows(getThe()['file'])
    clustered = t.cluster(cols=t.cols.xcols)
    show(clustered)

    return 0

def position_test():
    t = reprows(getThe()['file'])
    clustered = t.cluster()
    
    repplace(clustered)

    return 0

def every_test():
    repgrid(getThe()['file'])

    return 0

def reservoir_test():
    options = getThe()
    options['Max'] = 32
    setThe(options)

    num1 = NUM()
    for i in range(1, 10001):
        num1.add(i)
    oo(has(num1))

    return 0

def cliffs_test():
    assert(False == cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [8, 7, 6, 2, 5, 8, 7, 3]), '1')
    assert(True == cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [9, 9, 7, 8, 10, 9, 6]), '2')

    t1, t2 = [], []
    for i in range(1, 1001): t1.append(rand())
    for i in range(1, 1001): t2.append(rand()**0.5)
    
    assert(False == cliffsDelta(t1, t1), '3')
    assert(True == cliffsDelta(t1, t2), '4')

    diff, j = False, 1.0
    def fun(x):
        return x*j, None
    while not diff:
        t3 = map(t1, fun)
        diff = cliffsDelta(t1, t3)
        print(">", rnd(j), diff)
        get_ofile().write("> " + rnd(j) + ' ' + diff + '\n')
        j = j*1.025

    return 0

def dist_test():
    data = DATA(getThe()['file'])
    num = NUM()
    for _, row in enumerate(data.rows):
        num.add(data.dist(row, data.rows[0]))
    oo({'lo': num.lo, 'hi': num.hi, 'mid': rnd(num.mid()), 'div': rnd(num.div())})

    return 0

def bins_test():
    data = DATA(getThe()['file'])
    best, rest = data.sway()

    print('all\t', o({'best': len(best.rows), 'rest': len(rest.rows)}))
    get_ofile().write('all\t' + o({'best': len(best.rows), 'rest': len(rest.rows)}) + '\n')
    for k, t in enumerate(bins(data.cols.xcols, {'best': best.rows, 'rest': rest.rows})):
        for single_range in t:
            print('{}\t{}\t{}\t{}\t{}'.format(single_range['txt'], single_range['lo'], single_range['hi'], rnd(value(single_range['y'].has, len(best.rows), len(rest.rows), 'best')), single_range['y'].has))
            get_ofile().write('{}\t{}\t{}\t{}\t{}'.format(single_range['txt'], single_range['lo'], single_range['hi'], rnd(value(single_range['y'].has, len(best.rows), len(rest.rows), 'best')), single_range['y'].has) + '\n')
        print()
        get_ofile().write('\n')

    return 0
