from gexecjs import RunJs

if __name__ == '__main__':
    run_js = RunJs('/Users/gaogzhen/devTools/python/projects/data/1.js')
    print(run_js.run('test01', '1111'))