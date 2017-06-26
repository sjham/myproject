from selenium import webdriver
import time
import itertools

url = 'http://escuelasyjardines.com.ar/'
xpath_tipo_de_establecimiento = '//select[contains(@name,"Categoria1")]/option'
xpath_tipo_de_establecimiento2 = '//select[contains(@name,"Categoria2")]/option'
xpath_ubicacion = '//select[contains(@name,"Ubicacion1")]/option'
xpath_ubicacion2 = '//select[contains(@name,"Ubicacion2")]/option'
xpath_gestion = '//select[contains(@name,"Gestion")]/option'

#browser = webdriver.Firefox()
browser = webdriver.Chrome('/media/sf_share_u/chromedriver_linux64/chromedriver')
browser.get(url)

possible_combinations = []
# First, let's get the elements
options_tipo_de_establecimiento = browser.find_elements_by_xpath(xpath_tipo_de_establecimiento)
options_ubicacion = browser.find_elements_by_xpath(xpath_ubicacion)
options_ubicacion2 = browser.find_elements_by_xpath(xpath_ubicacion2)
options_gestion = browser.find_elements_by_xpath(xpath_gestion)

# Get the values
values_tipo_de_establecimiento = [option.get_attribute('value') for option in options_tipo_de_establecimiento]
values_ubicacion = [option.get_attribute('value') for option in options_ubicacion]
values_ubicacion2 = [option.get_attribute('value') for option in options_ubicacion2]
values_gestion = [option.get_attribute('value') for option in options_gestion]

# Make all possible combinations
# We click all options from the first field, to check the dynamic second field
# It can be done much better than just waiting 10 seconds
dynamic_options2 = []
for i in range(len(options_tipo_de_establecimiento)):
    options_tipo_de_establecimiento = browser.find_elements_by_xpath(xpath_tipo_de_establecimiento)
    options_tipo_de_establecimiento[i].click()
    time.sleep(10)
    options_tipo_de_establecimiento2 = browser.find_elements_by_xpath(xpath_tipo_de_establecimiento2)
    values_tipo_de_establecimiento2 = [option.get_attribute('value') for option in options_tipo_de_establecimiento2]
    dynamic_options2.append(values_tipo_de_establecimiento2)



all_combinations = []
for d_o2 in dynamic_options2:
    s = [values_tipo_de_establecimiento, values_ubicacion, values_ubicacion2, values_gestion]
    if d_o2:
        s.append(d_o2)
    new_combinations = list(itertools.product(*s))
    all_combinations += new_combinations


for combination in all_combinations:
    browser.get(url)
    options_tipo_de_establecimiento = browser.find_elements_by_xpath(xpath_tipo_de_establecimiento)
    options_ubicacion = browser.find_elements_by_xpath(xpath_ubicacion)
    options_ubicacion2 = browser.find_elements_by_xpath(xpath_ubicacion2)
    options_gestion = browser.find_elements_by_xpath(xpath_gestion)
    for option in options_tipo_de_establecimiento:
        if option.get_attribute('value') == combination[0]: option.click()
    for option in options_ubicacion:
        if option.get_attribute('value') == combination[1]: option.click()
    for option in options_ubicacion2:
        if option.get_attribute('value') == combination[2]: option.click()
    for option in options_gestion:
        if option.get_attribute('value') == combination[3]: option.click()
    if len(combination) > 4:
        time.sleep(5) # Loading dynamic option
        options_tipo_de_establecimiento2 = browser.find_elements_by_xpath(xpath_tipo_de_establecimiento2)
        for option in options_tipo_de_establecimiento2:
            if option.get_attribute('value') == combination[3]: option.click()
    # Now click submit
    # ...
