'''
美团外卖新建商品，适合商品批量上传失败的商品，但UPC码美团有对应商品的情况
'''
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xlrd  

# 新建一个商品
def addProduct(driver, upc, tagName1, tagName2, price, stock, k="1"):
	try:
		# 输入UPC码
		element = driver.find_element_by_xpath("//input[@placeholder='请输入UPC码']")
		element.clear()
		element.send_keys(upc)
		# 选择店内一级分类
		driver.find_element_by_xpath("//div[@class='kui-select-input-wrapper']/div/input").click()
		# 0.1秒检查一次是否出现一级分类菜单
		tagCount = len(driver.find_elements_by_xpath("//div[contains(@class, 'top-left')]/ul/li"))
		for i in range(tagCount):
			tag = driver.find_element_by_xpath("//div[contains(@class, 'top-left')]/ul/li[" + str(i+1) + "]")
			text = tag.get_attribute('textContent')
			if text == tagName1:
				tag.click()
		# 选择店内二级分类
		tagCount = len(driver.find_elements_by_xpath("//div[contains(@class, 'top-left')][2]/ul/li"))
		for i in range(tagCount):
			tag = driver.find_element_by_xpath("//div[contains(@class, 'top-left')][2]/ul/li[" + str(i+1) + "]")
			text = tag.get_attribute('textContent')
			if text == tagName2:
				tag.click()	
		# 输入价格
		element = driver.find_element_by_xpath("//div[@id='spu-price-0']/input")
		element.clear()
		element.send_keys(price)
		# 输入库存
		element = driver.find_element_by_xpath("//div[@id='spu-stock-0']/input")
		element.clear()
		element.send_keys(stock)
		# # 点击保存并继续新建
		driver.find_element(By.XPATH,'//button[text()="保存并继续新建"]').click()
		# 获取提示信息
		locator = (By.XPATH, "//div[contains(@class, 'kui-toast')]/div/span[2]")
		WebDriverWait(driver, 10, 0.1).until(EC.presence_of_element_located(locator))
		message = driver.find_element_by_xpath("//div[contains(@class, 'kui-toast')]/div/span[2]").get_attribute('textContent')
		WebDriverWait(driver, 10, 0.1).until_not(EC.presence_of_element_located(locator))
		print(k, upc, message)	
	except:
		print(k, upc, "新建商品错误")

driver = webdriver.Chrome()
driver.implicitly_wait(12)  # 隐性等待，最长等12秒
driver.get('http://e.waimai.meituan.com')
driver.add_cookie({'name':'acctId','value':'31330952'})
driver.add_cookie({'name':'token','value':'0qSx5HoHXnBkgZZ8qPVMWOOv5Smy7FfpFEeEIiqKngnU*'})
driver.add_cookie({'name':'wmPoiId','value':'3578168'})
# 跳转到商品管理
driver.get('http://e.waimai.meituan.com/#/v2/shop/productManage')
driver.switch_to.frame(0)
# 点击新建商品
driver.find_element(By.XPATH,'//button[text()="新建商品"]').click()
driver.implicitly_wait(1)

workbook = xlrd.open_workbook('mtProduct.xlsx')
booksheet = workbook.sheet_by_index(0)
for i in range(1, booksheet.nrows):
	row = booksheet.row_values(i)
	upc = row[0]
	tagName1 = row[3]
	tagName2 = row[4]
	price = str(row[1])
	stock = row[2]
	addProduct(driver, upc, tagName1, tagName2, price, stock, i)