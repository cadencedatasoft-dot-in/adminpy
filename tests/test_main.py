from keygen import KeyPairGenerator
from os.path import exists

def test_get_names_gtr(monkeypatch):
    # provided inputs
    testnames = 'anand sneha prashant prabhakar'
    testnameslist = testnames.split()
    
    # creating iterator object
    answers = iter([testnames])

    # using lambda statement for mocking
    monkeypatch.setattr('builtins.input', lambda testnames: next(answers))

    kpobj = KeyPairGenerator()
    minsignercount = 2
    namelist = kpobj.get_names(minsignercount)
    assert len(namelist) == len(testnameslist)

def test_get_names_eq(monkeypatch):
    # provided inputs
    testnames = 'anand sneha'
    testnameslist = testnames.split()
    
    # creating iterator object
    answers = iter([testnames])

    # using lambda statement for mocking
    monkeypatch.setattr('builtins.input', lambda testnames: next(answers))

    kpobj = KeyPairGenerator()
    minsignercount = 2
    namelist = kpobj.get_names(minsignercount)
    assert len(namelist) == len(testnameslist)

def test_get_names_lt(monkeypatch):
    # provided inputs
    testnames = 'anand'
    testnameslist = testnames.split()
    
    # creating iterator object
    answers = iter([testnames])

    # using lambda statement for mocking
    monkeypatch.setattr('builtins.input', lambda testnames: next(answers))

    kpobj = KeyPairGenerator()
    minsignercount = 2
    namelist = kpobj.get_names(minsignercount)
    assert namelist == None    


def test_gen_key_pairs_04():
    testnames = 'anand sneha prashant prabhakar'
    testnameslist = testnames.split()

    kpobj = KeyPairGenerator()
    kplist, pklist = kpobj.gen_key_pairs(testnameslist)
    assert len(kplist) == len(testnameslist)
    assert len(pklist) == len(testnameslist)
    for k in list(kplist):
        assert exists(kplist[k]) == True