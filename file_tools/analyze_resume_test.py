#coding:utf-8

import unittest
import sys
import os
from os.path import dirname,abspath
current_dir = dirname(abspath(__file__))
sys.path.append(current_dir+'/bin/')

class AnalyzeResumeperformanceTestCase(unittest.TestCase):
    def setUp(self):
        from bin.analyze_resume import analyzer
        self.analyzer = analyzer
        self.testFilePath = current_dir+'/resume/000AAA.txt'    # 使用自己的测试文件
        self.warmUp()

    def tearDown(self):
        self.analyzer = None

    def warmUp(self):
        res = self.analyzer.analyze_bin_file(self.testFilePath, mode=1, need_avatar=1)
        print 'warming up, getting result:'
        for mat in res.res_obj.to_mat_list() :
            print mat

    def runTest(self):
        import cProfile, pstats
        stats_name = 'resume_stats'
        cProfile.runctx('self.analyzer.analyze_bin_file(self.testFilePath, mode=1, need_avatar=1)', {'self':self}, {}, stats_name)
        p = pstats.Stats(stats_name)
        p.sort_stats('tottime').print_stats(20)

if __name__ == '__main__':
    unittest.main()