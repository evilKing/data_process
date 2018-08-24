import auto_annotation.utils as utils

'''
文档快速生成注释的方法介绍,首先我们要用到__all__属性
在Py中使用为导出__all__中的所有类、函数、变量成员等
在模块使用__all__属性可避免相互引用时命名冲突
'''
__all__ = ['Login', 'check', 'Shop', 'upDateIt', 'findIt', 'deleteIt', 'createIt']


@utils.debugger(prefix='Login')
class Login:
    '''
    测试注释一可以写上此类的作用说明等
    例如此方法用来写登录
    '''

    @utils.debugger(prefix='Login')
    def __init__(self):
        '''
        初始化你要的参数说明
        那么登录可能要用到
        用户名username
        密码password
        '''
        pass

    @utils.debugger(prefix='Login')
    def check(self):
        '''
        协商你要实现的功能说明
        功能也有很多例如验证
        判断语句，验证码之类的
        '''
        pass

@utils.debugger(prefix='Shop')
class Shop:
    '''
    商品类所包含的属性及方法
    update改/更新
    find查找
    delete删除
    create添加
    '''

    @utils.debugger(prefix='Shop')
    def __init__(self):
        '''
        初始化商品的价格、日期、分类等
        '''
        pass

    @utils.debugger(prefix='Shop')
    def upDateIt(self):
        '''
        用来更新商品信息
        '''
        pass

    @utils.debugger(prefix='Shop')
    def findIt(self):
        '''
        查找商品信息
        a = 1
        b = 2
        c = 3
        '''
        c = a + b
        pass

    @utils.debugger(prefix='Shop')
    def deleteIt(self):
        '''
        删除过期下架商品信息
        '''
        pass

    def createIt(self):
        '''
        创建新商品及上架信息
        '''
        pass


shop = Shop()

if __name__ == "__main__":
    from auto_annotation import autoannot

    # print(help(autoannot))
    shop.findIt()
    utils.print_res()