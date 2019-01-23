'''
适用于美团外卖批量创建好的商品没有图片的情况，可以批量添加图片，一次添加100个商品图片
'''
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
	driver = webdriver.Chrome()
	driver.implicitly_wait(12)  # 隐性等待，最长等12秒
	driver.get('http://e.waimai.meituan.com')
	driver.add_cookie({'name':'acctId','value':'31330952'})
	driver.add_cookie({'name':'token','value':'0qSx5HoHXnBkgZZ8qPVMWOOv5Smy7FfpFEeEIiqKngnU*'})
	driver.add_cookie({'name':'wmPoiId','value':'3578168'})
	# 跳转到商品管理
	driver.get('http://e.waimai.meituan.com/#/v2/shop/productManage')
	driver.switch_to.frame(0)
	# 点击无图片筛选
	driver.find_element(By.XPATH,"//div[@class='filters']/span[5]").click()	
	driver.find_element_by_xpath("//div[contains(@class, 'pagesize-select')]").click()
	driver.find_element_by_xpath("//li/span[text()='100']").click()
	while True:
		# 获取商品标题
		product = driver.find_element_by_xpath("//div[contains(@class, 'products')]/div/div[1]")
		product = product.text.split('约')[0]
		product = product.strip()
		print(product)
		# 点击上传图片
		driver.find_element_by_xpath("//div[contains(@class, 'products')]/div/div[1]/div[2]/i").click()
		sleep(1)
		upload = driver.find_element_by_xpath("//div[contains(@class, 'select-local-file')]/input")
		# 从图片库中上传图片
		upload.send_keys('C:/Users/it03/iCloudDrive/Documents/Python/乐海/test/' + product + '.jpg')
		# 裁剪图片
		# element = driver.find_element_by_xpath("//div[contains(@class, 'cropper-container')]/div[3]")
		# driver.execute_script("arguments[0].style = 'width: 330px; height: 247.5px; transform: translateX(55px) translateY(40px);'", element)
		# element = driver.find_element_by_xpath("//div[contains(@class, 'upload-cropper-preview-box')]/img")
		# print(element.get_attribute('style'))
		# driver.execute_script("arguments[0].style = 'position: relative; display: block; width: 240px; height: 240px; min-width: 0px !important; min-height: 0px !important; max-width: none !important; max-height: none !important; transform: none; left: 0px; top: -29.0909px;'", element)
		# print(element.get_attribute('style'))
		driver.find_element_by_xpath("//button[text()='使用预览图']").click()
		sleep(3)
except Exception as err:
	print(err)
finally:
	sleep(30)
	driver.quit()
