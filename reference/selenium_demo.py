# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import time

# centos安装chrome：
'''
1.依赖redhat-lsb
yum -y install redhat-lsb

2.设置yum的google-chrome源
cd /etc/yum.repos.d/
touch google-chrome.repo
vi google-chrome.repo
写入
[google-chrome]
name=google-chrome
baseurl=http://dl.google.com/linux/chrome/rpm/stable/$basearch
enabled=1
gpgcheck=1
gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub

3.yum安装chrome(需要加上--nogpgcheck参数，国内服务器google的东东，你懂的)
yum install google-chrome-stable --nogpgcheck

4.加个软连接
which google-chrome-stable
ln -s xxx /bin/chrome

5.相关命令
查看版本:
chrome -version
启动并访问淘宝：
chrome --headless --test-type --disable-gpu --no-sandbox --log-level=3 --disable-logging --screenshot http://www.taobao.com
'''
# 安装selenium：conda install selenium
# 安装Chrome的驱动：ChromeDriver(Chrome浏览器的驱动) http://chromedriver.chromium.org/downloads，下载和当前win(liunx)上安装的chrome浏览器对应版本兼容的驱动
# selenium官方api文档: https://selenium-python.readthedocs.io/api.html
# ChromeDriver的设置说明: https://sites.google.com/a/chromium.org/chromedriver/capabilities(需要翻墙访问)

# 使用无界面chrome浏览器
# 获取chrome浏览器设置
chrome_options = Options()

# add_argument：添加启动参数
# 设置user-agent以用来模拟移动设备，移动版网站的反爬虫的能力比较弱
# 模拟 iphone 6
# chrome_options.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"')
# 模拟 android QQ浏览器
# chrome_options.add_argument('user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')

# 添加设置--no-sandbox：禁用沙箱
chrome_options.add_argument('--no-sandbox')
# 添加设置log-level级别：
# INFO = 0,
# WARNING = 1,
# LOG_ERROR = 2,
# LOG_FATAL = 3,
# default is 0
chrome_options.add_argument('--log-level=3')
# 添加设置--headless：不弹出chrome程序窗口
#chrome_options.add_argument('--headless')
# 添加设置--disable-gpu：禁用GPU
chrome_options.add_argument('--disable-gpu')
# 添加设置 --test-type 测试模式
chrome_options.add_argument('--test-type')
# 添加设置 --ignore-certificate-errors 浏览器证书错误报警提示
chrome_options.add_argument('--ignore-certificate-errors')
# 添加设置 --start-maximized 最大化浏览器
chrome_options.add_argument('--start-maximized')
# 添加设置 no-default-browser-check 不检查浏览器
chrome_options.add_argument('no-default-browser-check')
# 启动时设置默认语言为中文 UTF-8
chrome_options.add_argument('lang=zh_CN.UTF-8')

# add_experimental_option：添加实验性质的设置参数
# 禁止图片加载 （不加载图片的情况下，可以提升爬取速度，但是也有可能会带来网站解析异常的问题）
prefs = {
    'profile.default_content_setting_values' : {
        'images' : 2
    }
}
chrome_options.add_experimental_option('prefs', prefs)

# 添加浏览器扩展应用插件（selenium一般打开的是不带扩展的纯净的浏览器）
# add_extension：添加扩展应用
# extension_path = 'D:/extension/XPath-Helper_v2.0.2.crx'
# chrome_options.add_extension(extension_path)

# 获得Chrome浏览器 executable_path参数设置chromedriver.exe位置，如果已经把chromedriver配置在环境变量则无需设置，chrome_options参数传入上面的options设置
# driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=chrome_options)

# 添加代理
PROXY = "proxy_host:proxy:port"
desired_capabilities = chrome_options.to_capabilities()
desired_capabilities['proxy'] = {
    "httpProxy":PROXY,
    "ftpProxy":PROXY,
    "sslProxy":PROXY,
    "noProxy":None,
    "proxyType":"MANUAL",
    "class":"org.openqa.selenium.Proxy",
    "autodetect":False
}

# 获得Chrome浏览器
# browser = webdriver.Chrome()
# 获得Chrome浏览器 传入初始参数chrome_options
browser = webdriver.Chrome(chrome_options=chrome_options)
# 获得Chrome浏览器 传入desired_capabilities设置代理参数
# browser = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options, desired_capabilities=desired_capabilities)

# 隐式等待，当查找的元素并没有立即出现加载的时候，隐式等待一段时间再查找DOM，默认的时间是0，这里设置隐式等待10秒
browser.implicitly_wait(10)
# 设置窗体大小，可以根据桌面分辨率来定，主要是为了抓到验证码的截屏
# browser.set_window_size(1920, 1080)

try:
    # 用Chrome打开百度
    browser.get('https://www.baidu.com')
    # 获得id是kw的输入框
    input = browser.find_element_by_id('kw')
    # 使用css选择器查找id是kw的输入框(#代表使用id来查找)
    input_css_selector =browser.find_element_by_css_selector('#kw')
    # 使用xpath选择器查找id是kw的输入框
    input_xpath = browser.find_element_by_xpath('//*[@id="kw"]')
    # 打印后可以看出，使用三种方式查找到的id是kw的输入框element=的值是相同的，证明三种方式都可以找到相同的输入框，
    # 实际使用时根据自己的喜好选择一种，或者都宠幸组合使用
    print(input, input_css_selector, input_xpath)
    # 还有一种通用的api方法find_element，第一个参数传入选择器的类型(比如id选择器，css选择器，xpath选择器等，第二个参数传入对应选择器的语法)
    # browser.find_element(By.ID,'kw')

    # 在输入框里输入Python
    input.send_keys('Python')
    # 获取input框里的内容值
    print(input.text)
    # 获取input的id
    print(input.id)
    # 获取input的位置
    print(input.location)
    # 获取input的标签名字
    print(input.tag_name)
    # 获取input的大小
    print(input.size)
    # 之后输入回车
    input.send_keys(Keys.ENTER)
    # 显示等待，声明一个WebDriverWait，设置等待，等待超时时间20秒
    wait = WebDriverWait(browser, 20)
    # 等待id是content_left的html元素被加载出来
    wait.until(EC.presence_of_all_elements_located((By.ID, 'content_left')))
    # 输出当前url
    print(browser.current_url)
    # 输出浏览器的所有cookie
    print(browser.get_cookies())
    # 输出网页源代码
    print(browser.page_source)

    # 用Chrome打开淘宝，元素动作
    browser.get('https://www.taobao.com')
    # 获得id是p的输入框
    input = browser.find_element_by_id('q')
    # 在输入框中输入iPhone
    input.send_keys('iPhone')
    # 睡3秒
    time.sleep(3)
    # 清空输入框内容
    input.clear()
    # 在输入框中输入iPad
    input.send_keys('iPad')
    # 获取classname是btn-search的按钮
    button = browser.find_element_by_class_name('btn-search')
    # 获取button的属性值(获取class属性的值)
    print(button.get_attribute('class'))
    # 调用点击按钮
    button.click()
    # 输出当前url
    print(browser.current_url)
    # 输出网页源代码
    print(browser.page_source)

    # 交互动作连(ActionChains)
    browser.get('http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')
    # 设置等待，等待超时时间30秒
    wait = WebDriverWait(browser, 30)
    # 等待id是iframeResult的html元素被加载出来
    wait.until(EC.presence_of_all_elements_located((By.ID, 'iframeResult')))
    # 切换到id是iframeResult的iframe(iframe要特殊处理，相当于一个独立的网页，要用switch_to.frame来切换)
    browser.switch_to.frame('iframeResult')
    # 找到拖拽的原div,id=draggable
    source = browser.find_element_by_css_selector('#draggable')
    # 找到拖拽的目标div,id=droppable
    target = browser.find_element_by_css_selector('#droppable')
    # 首先申明一个动作连(ActionChains)
    actions = ActionChains(browser)
    # 调用动作连的拖拽动作
    actions.drag_and_drop(source, target)
    # 执行动作
    actions.perform()
    # 获取alert对话框(这里需要注意，如果有alter等控件弹出，浏览器的后续操作会报错，需要先点击alert后才能继续操作)
    alert = browser.switch_to.alert
    # 获取警告对话框的内容
    print(alert.text)
    # 点击接受接受弹窗
    alert.accept()
    # 切换回到父frame（因为刚才已经切换了iframe）
    browser.switch_to.parent_frame()

    # 执行JavaScript
    # 访问知乎网站
    browser.get('https://www.zhihu.com/explore')
    # 睡3秒
    time.sleep(3)
    # 执行JavaScript使浏览器滚动条拉到最低端
    browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    # 执行JavaScript弹出alert
    browser.execute_script('alert("To Botton")')
    # 获取alert对话框
    alert = browser.switch_to.alert
    # 获取警告对话框的内容
    print(alert.text)
    # 点击接受接受弹窗
    alert.accept()

    # 浏览器的前进/后退
    # 后退
    browser.back()
    time.sleep(3)
    # 前进
    browser.forward()

    # cookies操作
    # 输出浏览器的所有cookie
    print(browser.get_cookies())
    # 添加cookie,name是cookie的名字，value是对应name的值
    browser.add_cookie({'name': 'userName', 'value': 'test'})
    print(browser.get_cookies())
    # 删除所有cookie
    browser.delete_all_cookies()
    print(browser.get_cookies())

    # 选项卡
    # 增加选项卡(此方法最为通用，使用js的open方式增加选项卡)
    browser.execute_script('window.open()')
    # 打印所有窗口选项卡的引用
    print(browser.window_handles)
    # 切换到第二个选项卡
    browser.switch_to.window(browser.window_handles[1])
    browser.get('https://www.taobao.com')
    # 切换到第一个选项卡
    browser.switch_to.window(browser.window_handles[0])
    browser.get('https://www.baidu.com')

    # 异常处理 # 超时的错误并不能抓到，可能是这个过程中报了别的错
    try:
        browser.get('https://www.google.com')
    except TimeoutException:
        # 访问超时异常
        print('Time Out')

    try:
        browser.find_element_by_id('hello')
    except NoSuchElementException:
        # 元素未找到异常
        print('No Element')

finally:
    print('in finally')
    # browser.close()
    # 最好用这个方法关闭浏览器和驱动
    browser.quit()


