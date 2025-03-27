import string
import random
import time
import os
import datetime
import signal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException

def generate_key():
    prefix = "DJBm"
    digit5 = random.choice(string.digits)
    char6 = random.choice(string.ascii_uppercase)
    char7_8 = ''.join(random.choice(string.ascii_lowercase) for _ in range(2))
    digit9 = "0"
    char10 = random.choice(string.ascii_lowercase)
    char11 = random.choice(string.ascii_uppercase)
    digit12 = random.choice(string.digits)
    char13 = random.choice(string.ascii_lowercase)
    char14 = random.choice(string.ascii_uppercase)
    digit15 = random.choice(string.digits)
    char16 = random.choice(string.ascii_uppercase)
    char17 = random.choice(string.ascii_lowercase)
    char18 = random.choice(string.ascii_uppercase)
    
    return prefix + digit5 + char6 + char7_8 + digit9 + char10 + char11 + digit12 + char13 + char14 + digit15 + char16 + char17 + char18

def is_login_cover_present(driver):
    try:
        cover = driver.find_element(By.CLASS_NAME, "qConnectLoginCover")
        return cover.is_displayed()
    except:
        return False

def wait_for_login_complete(driver, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if "已登录账号" in driver.page_source:
            if not is_login_cover_present(driver):
                time.sleep(2)
                return True
        time.sleep(1)
    return False

def is_exchange_successful(driver, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.ID, "exchangeModal"))
        )
        return True
    except TimeoutException:
        return False

def is_network_busy(driver, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.ID, "commonModal"))
        )
        modal_text = driver.find_element(By.ID, "modalCommonTip").text
        return "网络繁忙" in modal_text or "请稍后再试" in modal_text
    except:
        return False

def is_exchange_failed(driver, timeout=5):
    try:
        common_modal = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.ID, "commonModal"))
        )
        modal_text = driver.find_element(By.ID, "modalCommonTip").text
        return "资格码兑换失败" in modal_text or "兑换失败" in modal_text
    except TimeoutException:
        return False

def handle_common_modal(driver):
    try:
        confirm_button = driver.find_element(By.ID, "modalBtnConfirm")
        driver.execute_script("arguments[0].click();", confirm_button)
        print("已点击弹窗确定按钮")
        time.sleep(1)
        return True
    except Exception as e:
        print(f"处理弹窗出错: {str(e)}")
        return False

def reset_page_if_needed(driver):
    try:
        modals = ["delayModal", "macModal", "onlyWebModal"]
        for modal_id in modals:
            try:
                modal = driver.find_element(By.ID, modal_id)
                if "d-hide" not in modal.get_attribute("class"):
                    close_btn = modal.find_element(By.CLASS_NAME, "modal-btn-close")
                    close_btn.click()
                    print(f"关闭了弹窗: {modal_id}")
                    time.sleep(1)
                    return True
            except:
                pass
        
        try:
            input_field = driver.find_element(By.ID, "cdkInput")
            if not input_field.is_displayed() or not input_field.is_enabled():
                print("输入框不可用，刷新页面...")
                driver.refresh()
                time.sleep(3)
                return True
        except:
            print("找不到输入框，刷新页面...")
            driver.refresh()
            time.sleep(3)
            return True
            
        return False
    except Exception as e:
        print(f"检查页面状态出错: {str(e)}")
        return False

def safe_click(driver, element, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        try:
            driver.execute_script("arguments[0].click();", element)
            time.sleep(0.5)
            return True
        except ElementClickInterceptedException:
            print(f"点击被拦截，等待并重试... ({attempts+1}/{max_attempts})")
            if is_login_cover_present(driver):
                print("检测到登录遮罩层仍然存在，请检查登录状态")
                input("请确认登录完成后按回车继续...")
            time.sleep(2)
            attempts += 1
        except StaleElementReferenceException:
            print("元素已过期，重新获取...")
            return False
        except Exception as e:
            print(f"点击出错: {str(e)}")
            break
    return False

def main():
    options = webdriver.ChromeOptions()
    
    try:
        home_dir = os.path.expanduser("~")
        chromedriver_path = os.path.join(home_dir, "下载", "chromedriver-mac-arm64", "chromedriver")
        
        if not os.path.exists(chromedriver_path):
            chromedriver_path = os.path.join(home_dir, "Downloads", "chromedriver-mac-arm64", "chromedriver")
            
        print(f"使用ChromeDriver路径: {chromedriver_path}")
        
        if os.path.exists(chromedriver_path):
            os.chmod(chromedriver_path, 0o755)
            print("已设置ChromeDriver执行权限")
        else:
            print(f"警告: ChromeDriver文件未找到: {chromedriver_path}")
            print("请输入正确的ChromeDriver路径:")
            user_path = input().strip()
            if user_path:
                chromedriver_path = user_path
                if os.path.exists(chromedriver_path):
                    os.chmod(chromedriver_path, 0o755)
                    print("已设置ChromeDriver执行权限")
                else:
                    print(f"警告: 输入的路径也不存在: {chromedriver_path}")
        
        from selenium.webdriver.chrome.service import Service
        service = Service(executable_path=chromedriver_path)
        
        print("正在启动Chrome浏览器...")
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        
        driver.get("https://rocom.qq.com/act/a20250325cdkey/web/index.html")
        
        print("请手动登录网页，完成后程序将继续...")
        
        print("等待登录完成并且登录遮罩层消失...")
        if not wait_for_login_complete(driver, timeout=120):
            print("登录等待超时或未完全完成")
            user_input = input("如果已完成登录，请输入'y'强制继续: ")
            if user_input.lower() != 'y':
                driver.quit()
                return
        
        print("登录已完成，开始尝试兑换码...")
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "cdkInput"))
            )
        except TimeoutException:
            print("找不到兑换码输入框")
            driver.quit()
            return
        
        attempts = 0
        successful_attempts = 0
        start_time = time.time()
        
        network_busy_count = 0
        delay_time = 1.0
        
        print("持续兑换模式已启动，按Ctrl+C可随时停止...")
        
        try:
            while True:
                attempts += 1
                current_time = time.time()
                elapsed = current_time - start_time
                hours, remainder = divmod(elapsed, 3600)
                minutes, seconds = divmod(remainder, 60)
                
                if attempts % 50 == 0:
                    print(f"\n已运行: {int(hours)}小时 {int(minutes)}分钟 {int(seconds)}秒")
                    print(f"已尝试: {attempts}次, 成功: {successful_attempts}次")
                    print(f"当前延迟: {delay_time:.2f}秒, 网络繁忙次数: {network_busy_count}\n")
                
                if reset_page_if_needed(driver):
                    print("页面已重置，等待重新加载...")
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, "cdkInput"))
                        )
                    except:
                        print("重新加载后找不到输入框，尝试刷新...")
                        driver.refresh()
                        time.sleep(3)
                        continue
                
                key = generate_key()
                
                try:
                    input_field = driver.find_element(By.ID, "cdkInput")
                    input_field.clear()
                    for char in key:
                        input_field.send_keys(char)
                        time.sleep(random.uniform(0.01, 0.05))
                    
                    time.sleep(random.uniform(0.3, 0.8))
                    
                    exchange_button = driver.find_element(By.ID, "btnCdkActive")
                    
                    print(f"尝试第 {attempts} 次，使用Key: {key}")
                    
                    driver.execute_script("arguments[0].click();", exchange_button)
                    
                    time.sleep(1)
                    
                    if is_network_busy(driver):
                        network_busy_count += 1
                        print(f"检测到网络繁忙提示 (第{network_busy_count}次)")
                        handle_common_modal(driver)
                        
                        delay_time = min(30.0, delay_time * 1.5)
                        wait_time = random.uniform(delay_time, delay_time + 5.0)
                        print(f"增加等待时间至 {wait_time:.2f} 秒")
                        time.sleep(wait_time)
                        continue
                    
                    if is_exchange_successful(driver):
                        successful_attempts += 1
                        print(f"\n兑换成功！成功使用的Key是: {key}")
                        print(f"成功时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        print(f"当前尝试次数: {attempts}, 总成功次数: {successful_attempts}")
                        
                        try:
                            confirm_button = driver.find_element(By.ID, "exchangeCommit")
                            driver.execute_script("arguments[0].click();", confirm_button)
                            print("已点击确认按钮，继续尝试下一个兑换码...")
                            
                            with open("successful_keys.txt", "a") as f:
                                f.write(f"成功的Key: {key}\n")
                                f.write(f"时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                                f.write(f"成功位置: 第{attempts}次尝试\n")
                                f.write("-" * 50 + "\n")
                            
                            print("成功信息已追加到successful_keys.txt文件")
                            
                            delay_time = max(1.0, delay_time * 0.8)
                        except Exception as e:
                            print(f"点击确认按钮出错: {str(e)}")
                    
                    elif is_exchange_failed(driver):
                        print("检测到兑换失败弹窗")
                        handle_common_modal(driver)
                    
                    wait_time = random.uniform(delay_time, delay_time + random.random() * 3)
                    time.sleep(wait_time)
                
                except StaleElementReferenceException:
                    print("页面元素已过期，刷新页面...")
                    driver.refresh()
                    time.sleep(3)
                    continue
                except Exception as e:
                    print(f"尝试兑换时出错: {str(e)}")
                    time.sleep(2)
                    if "cdkInput" not in driver.page_source:
                        print("页面状态异常，刷新页面...")
                        driver.refresh()
                        time.sleep(3)
        
        except KeyboardInterrupt:
            print("\n检测到用户中断，程序停止")
            print(f"共尝试了 {attempts} 次，成功 {successful_attempts} 次")
        
        print("操作完成，保持浏览器打开10秒...")
        time.sleep(10)
        driver.quit()
    
    except Exception as e:
        print(f"发生错误: {str(e)}")
        print("\nMac系统的ChromeDriver相关建议:")
        print("1. 确保已下载与Chrome浏览器匹配的ChromeDriver (134.0.6998.165)")
        print("2. 确保ChromeDriver有执行权限 (可以在终端执行: chmod +x /path/to/chromedriver)")
        print("3. 如果持续出错，请尝试重启程序")

if __name__ == "__main__":
    main()