#Created By Subrahmanya Sai Jayanthi
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

DRIVER_PATH = 'C:\chromedriver.exe'
#Minimum Number Of Requests That Will Be Accepted In A Single Session
MINIMUM_THRESHOLD = 1

s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)


#wd = webdriver.Chrome(executable_path=DRIVER_PATH)
#driver = webdriver.Chrome()
driver.maximize_window()
def login():
    print("Logging In .....")
    driver.get("https://www.linkedin.com/checkpoint/rm/sign-in-another-account?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")

    # get username element
    username = driver.find_element_by_id("username")

    # send keys
    username.send_keys("Enter your mail associated with LinkedIn.com here :")

    #get password element
    password = driver.find_element_by_id("password")

    # send keys
    password.send_keys("Enter your password here :")

    sign_in_button = driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
    sign_in_button.click()

    """
    https://stackoverflow.com/questions/44457993/retrieving-the-list-elements-using-xpath-in-python
    """
    # Go to myNetwork Tab
    mynetwork_tab_xpath = '//*[@id="ember20"]'
    try:
        myElem = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, mynetwork_tab_xpath )))
        print("Page 1 is ready!")
    except TimeoutException:
        print("Loading took too much time!")
    mynetwork_tab = driver.find_element_by_xpath(mynetwork_tab_xpath)
    mynetwork_tab.click()

    """ # Get all requests loaded """
    driver.get("https://www.linkedin.com/mynetwork/invitation-manager/")



    # Get the list of all requests
    accept_button_class = 'artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view.invitation-card__action-btn'
    try:
        myElem = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, accept_button_class)))
        print("Page 2 is also ready!")
    except TimeoutException:
        print("Loading took too much time!")

    list_of_all_requests = driver.find_elements_by_class_name(accept_button_class)
    print("Total connection requests : ",len(list_of_all_requests))
    return(list_of_all_requests)
def logoff():
    driver.get("https://www.linkedin.com/m/logout/")
    return(login())
def accept_until_min_threshold(buttons, n):
    for button in buttons:
        button.click()
        print("Accept Button Clicked")
    print("Succesfully accepted",n,"connections requests, looking for more!!")


if __name__ == "__main__":
    total_requests = login()
    total_number_of_requests=len(total_requests)
    while(total_number_of_requests >= MINIMUM_THRESHOLD):
        curr_log = total_requests[:MINIMUM_THRESHOLD]
        accept_until_min_threshold(curr_log, MINIMUM_THRESHOLD)
        print("Logging Off ..")
        total_requests = logoff()
        total_number_of_requests = len(total_requests)
    else:
        accept_until_min_threshold(total_requests, total_number_of_requests)
    


    
    
