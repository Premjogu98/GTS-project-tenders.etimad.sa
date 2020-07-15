from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import html
import sys, os
from datetime import datetime,timedelta
import Global_var
import wx
import string
import re
import string
app = wx.App()
from Insert_On_databse import insert_in_Local

def ChromeDriver():
    browser = webdriver.Chrome(executable_path=str(f"C:\\chromedriver.exe"))
    browser.get("""https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh?hl=en" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh%3Fhl%3Den&amp;ved=2ahUKEwivq8rjlcHmAhVtxzgGHZ-JBMgQFjAAegQIAhAB""")
    wx.MessageBox(' -_-  Add Extension and Select Proxy Between 25 SEC -_- ', 'Info', wx.OK | wx.ICON_WARNING)
    time.sleep(25)  # WAIT UNTIL CHANGE THE MANUAL VPN SETTING
    browser.get("https://tenders.etimad.sa/Tender/AllTendersForVisitor")
    browser.maximize_window()
    time.sleep(2)
    Collected_href = []
    next_page_loop = True
    clicked = False
    duplicate = 0
    while next_page_loop == True:
        for i in range(1,7,1): 
            for links in browser.find_elements_by_xpath('/html/body/div[9]/div/div/form/div[1]/div[3]/div[2]/div[1]/div['+str(i)+']/div/div/div[1]/div/div/div[1]/div/div[3]/h3/a'):
                links = links.get_attribute('href')
            for date in browser.find_elements_by_xpath('//*[@id="cardsresult"]/div[1]/div/div/div/div[1]/div/div['+str(i)+']/div[1]/div/div[1]/span'):
                Date = date.get_attribute('innerText').strip()
                break
            datetime_object = datetime.strptime(Date, '%Y-%m-%d')
            publish_date = datetime_object.strftime("%d-%m-%Y")

            datetime_object_pub = datetime.strptime(publish_date, '%d-%m-%Y')
            User_Selected_date = datetime.strptime(str(Global_var.From_date), '%d-%m-%Y')

            timedelta_obj = datetime_object_pub - User_Selected_date
            day = timedelta_obj.days

            if day >= 0:
                print('Publish Date Alive')
                if links not in Collected_href:
                    Collected_href.append(links)
                    print(f'link Count:{len(Collected_href)}')
                else:
                    duplicate += 1
                    print(f'Duplicate Link: {str(duplicate)}')
            else:
                print('Publish Date Dead')
                # print(Collected_href)
                # sys.exit()
                collect_data(Collected_href,browser)
                next_page_loop = False
                break
                
        if next_page_loop == True:
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")  # Scroll Down To Page
            time.sleep(3)
            for next_page in browser.find_elements_by_xpath('//*[@id="cardsresult"]/div[2]/div/nav/ul/li[5]/button/span'):
                next_page.click()
                time.sleep(2)
                clicked = True
                break
            if clicked ==  True:
                for next_page in browser.find_elements_by_xpath('//*[@id="cardsresult"]/div[2]/div/nav/ul/li[6]/button/span'):
                    next_page.click()
                    time.sleep(2)
                    break

def collect_data(Collected_href,browser):

    print(f'Tolal Links: {len(Collected_href)}')
    OG_Href_list = []
    for link in Collected_href:
        if link not in OG_Href_list:
            OG_Href_list.append(link)
    print(f'Tolal OG Links: {len(OG_Href_list)}')
    for href in OG_Href_list:
        browser.get(href)
        loop = True
        while loop == True:
            try: 
                Primary_warranty_address = ''
                reference_number = ''
                The_name_of_the_competition = ''
                Governmental_authority = ''
                Competition_number = ''
                The_purpose_of_the_competition = ''
                Competition_type = ''
                Method_of_submitting_offers = ''
                A_primary_warranty_is_required = ''
                The_value_of_competition_documents = ''
                The_deadline_for_submitting_offers = ''
                d2_html_source = ''
                d3_html_source = ''
                
                for d1_html_source in browser.find_elements_by_xpath('//*[@id="d-1"]'):
                    d1_html_source = d1_html_source.get_attribute('outerHTML')
                    for reference_number in browser.find_elements_by_xpath('//*[@id="basicDetials"]/div[2]/ul/li[3]/div/div[2]/span'):
                        reference_number = reference_number.get_attribute('innerText').strip()
                        # print(reference_number)
                        break
                    for The_name_of_the_competition in browser.find_elements_by_xpath('//*[@id="basicDetials"]/div[2]/ul/li[1]/div/div[2]/span'):
                        The_name_of_the_competition = The_name_of_the_competition.get_attribute('innerText').strip()
                        # print(The_name_of_the_competition)
                        break
                    for Governmental_authority in browser.find_elements_by_xpath('//*[@id="basicDetials"]/div[3]/ul/li[3]/div/div[2]/span'):
                        Governmental_authority = Governmental_authority.get_attribute('innerText').strip()
                        # print(Governmental_authority)
                        break
                    for Primary_warranty_address in browser.find_elements_by_xpath('//*[@id="basicDetials"]/div[3]/ul/li[7]/div/div[2]/span'):
                        Primary_warranty_address = Primary_warranty_address.get_attribute('innerText').strip()
                        # print(Primary_warranty_address)
                        break
                    for Competition_number in browser.find_elements_by_xpath('//*[@id="basicDetials"]/div[2]/ul/li[2]/div/div[2]/span'):
                        Competition_number = Competition_number.get_attribute('innerText').strip().replace(' ','').replace('.','')
                        # print(Competition_number)
                        break
                    for Where_to_open_the_show in browser.find_elements_by_xpath('//*[@id="basicDetials"]/div[2]/ul/li[6]/div/div[2]/span'):
                        Where_to_open_the_show = Where_to_open_the_show.get_attribute('innerText').strip()
                        # print(Where_to_open_the_show)
                        break
                    a = True
                    while a == True:
                        try:
                            for showmore in browser.find_elements_by_xpath('//*[@id="subPurposSapn"]/i'):
                                showmore.click()
                                time.sleep(1)
                                a = False
                                break
                            if a == True:
                                for showmore in browser.find_elements_by_xpath('//*[@id="purposeSpan"]/i'):
                                    showmore.click()
                                    time.sleep(1)
                                    a = False
                                    break
                        except:
                            print('Error On Show More Element')
                            time.sleep(2)
                            a == True
                    for The_purpose_of_the_competition in browser.find_elements_by_xpath('//*[@id="purposeSpan"]'):
                        The_purpose_of_the_competition = The_purpose_of_the_competition.get_attribute('innerText').strip().replace('...عرض الأقل...','').replace('...عرض المزيد...','')
                        # print(The_purpose_of_the_competition)
                        break
                    for Competition_type in browser.find_elements_by_xpath('//*[@id="basicDetials"]/div[3]/ul/li[1]/div/div[2]/span'):
                        Competition_type = Competition_type.get_attribute('innerText').strip()
                        # print(Competition_type)
                        break
                    for Competition_case in browser.find_elements_by_xpath('//*[@id="basicDetials"]/div[3]/ul/li[2]/div/div[2]/span'):
                        Competition_case = Competition_case.get_attribute('innerText').strip()
                        # print(Competition_case)
                        break
                    for Method_of_submitting_offers in browser.find_elements_by_xpath('//*[@id="basicDetials"]/div[3]/ul/li[5]/div/div[2]/span'):
                        Method_of_submitting_offers = Method_of_submitting_offers.get_attribute('innerText').strip()
                        # print(Method_of_submitting_offers)
                        break
                    for A_primary_warranty_is_required in browser.find_elements_by_xpath('//*[@id="basicDetials"]/div[3]/ul/li[6]/div/div[2]/span'):
                        A_primary_warranty_is_required = A_primary_warranty_is_required.get_attribute('innerText').strip()
                        # print(A_primary_warranty_is_required)
                        break
                    for The_value_of_competition_documents in browser.find_elements_by_xpath('//*[@id="basicDetials"]/div[2]/ul/li[5]/div/div[2]/span'):
                        The_value_of_competition_documents = The_value_of_competition_documents.get_attribute('innerText').strip()
                        # print(The_value_of_competition_documents)
                        break
                    break
                b = True
                while b == True:
                    try:
                        for Click_on_schedule_tab in browser.find_elements_by_xpath('//*[@id="tenderDatesTab"]'):
                            Click_on_schedule_tab.click()
                            time.sleep(2)
                            break
                        b = False
                    except:
                        print('Error On Click_on_schedule_tab Element')
                        time.sleep(2)
                        b = True

                for d2_html_source in browser.find_elements_by_xpath('//*[@id="d-2"]'):
                    d2_html_source = d2_html_source.get_attribute('outerHTML')
                    for The_deadline_for_submitting_offers in browser.find_elements_by_xpath('//*[@id="offerDetials"]/div[2]/ul/li[2]/div/div[2]/span[1]'):
                        The_deadline_for_submitting_offers = The_deadline_for_submitting_offers.get_attribute('innerText').strip()
                        # print(The_deadline_for_submitting_offers)
                        break
                    break
                c = True
                while c == True:
                    try:
                        for Click_on_list_tab in browser.find_elements_by_xpath('//*[@id="relationStepTab"]'):
                            Click_on_list_tab.click()
                            time.sleep(2)
                            break
                        c = False
                    except:
                        print('Error On Click_on_list_tab Element')
                        time.sleep(2)
                        c = True
            
                for d3_html_source in browser.find_elements_by_xpath('//*[@id="d-3"]'):
                    d3_html_source = d3_html_source.get_attribute('outerHTML')
                    break
                get_htmlsource = d1_html_source+d2_html_source+d3_html_source
                # print(get_htmlsource)
                if get_htmlsource != '':
                    scrap_data(get_htmlsource,reference_number,The_name_of_the_competition,Governmental_authority,Primary_warranty_address,Competition_number,The_purpose_of_the_competition,
                    Competition_type,Method_of_submitting_offers,A_primary_warranty_is_required,The_value_of_competition_documents,The_deadline_for_submitting_offers,Competition_case,href,Where_to_open_the_show)
                    print(f'Total: {str(Global_var.Total)} Deadline Not given: {Global_var.deadline_Not_given} duplicate: {Global_var.duplicate} inserted: {Global_var.inserted} expired: {Global_var.expired} QC Tenders: {Global_var.QC_Tenders}')
                    time.sleep(3)
                    loop = False
                else:
                    wx.MessageBox(' get_htmlSource Var Blank ','tenders.etimad.sa', wx.OK | wx.ICON_INFORMATION)

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                    exc_tb.tb_lineno)
                loop = True
                time.sleep(5)
    print('Process Done')
    wx.MessageBox(f'Total: {str(len(Collected_href))}\nDeadline Not given: {Global_var.deadline_Not_given}\nduplicate: {Global_var.duplicate}\ninserted: {Global_var.inserted}\nexpired: {Global_var.expired}\nQC Tenders: {Global_var.QC_Tenders}','tenders.etimad.sa', wx.OK | wx.ICON_INFORMATION)
    sys.exit()

def scrap_data(get_htmlSourcenew,reference_number,The_name_of_the_competition,Governmental_authority,Primary_warranty_address,Competition_number,The_purpose_of_the_competition,
    Competition_type,Method_of_submitting_offers,A_primary_warranty_is_required,The_value_of_competition_documents,The_deadline_for_submitting_offers,Competition_case,href,Where_to_open_the_show):
    
    html_data = get_htmlSourcenew
    html_data_removed_image = html_data.partition('class="pull-right">')[2].partition("</span>")[0].strip()
    html_data = html_data.replace(str(html_data_removed_image),'')
    get_htmlSource1 = html.unescape(str(html_data))
    SegField = []
    for data in range(42):
        SegField.append('')

    a = True
    while a == True:
        try:
            if Primary_warranty_address != '':
                SegField[2] = Primary_warranty_address
            else:
                SegField[2] = f'{Where_to_open_the_show}, Saudi Arabia'
            SegField[12] = Governmental_authority
            SegField[13] = reference_number
            SegField[19] = The_name_of_the_competition

            datetime_object = datetime.strptime(The_deadline_for_submitting_offers, '%d/%m/%Y')
            Deadline = datetime_object.strftime("%Y-%m-%d")
            SegField[24] = Deadline

            SegField[18] = f"{str(SegField[19])}<br>\nالغرض من المنافسة: {The_purpose_of_the_competition}<br>\nقيمة وثائق المنافسة: {The_value_of_competition_documents}<br>\nرقم المنافسة: {Competition_number}\
                <br>\nA Primary Warranty Is Required: {A_primary_warranty_is_required}<br>\nطريقة تقديم العروض: {Method_of_submitting_offers}<br>\nCompetition case: {Competition_case} "
            
            SegField[28] = href

            SegField[31] = 'tenders.etimad.sa'
            SegField[27] = "0"
            SegField[22] = "0"
            SegField[26] = "0.0"
            SegField[7] = "SA"
            SegField[14] = '2'
            SegField[16] = '1'
            SegField[17] = '0'

            for SegIndex in range(len(SegField)):
                print(SegIndex, end=' ')
                print(SegField[SegIndex])
                SegField[SegIndex] = html.unescape(str(SegField[SegIndex]))
                SegField[SegIndex] = str(SegField[SegIndex]).replace("'", "''")
            
            if len(SegField[19]) > 250:
                    SegField[19] = SegField[19][:247] + '...'

            if SegField[19] == '':
                wx.MessageBox(' Short Desc Blank ','tenders.etimad.sa', wx.OK | wx.ICON_INFORMATION)
            else:
                check_date(SegField,get_htmlSource1)
            a = False
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                  exc_tb.tb_lineno)
            a = True
            time.sleep(5)

def check_date(SagField,get_htmlSource1):

    deadline = str(SagField[24])
    curdate = datetime.now()
    curdate_str = curdate.strftime("%Y-%m-%d")
    try:
        if deadline != '':
            datetime_object_deadline = datetime.strptime(deadline, '%Y-%m-%d')
            datetime_object_curdate = datetime.strptime(curdate_str, '%Y-%m-%d')
            timedelta_obj = datetime_object_deadline - datetime_object_curdate
            day = timedelta_obj.days
            if day > 0:
                insert_in_Local(get_htmlSource1, SagField)
                print("Live Tender")
            else:
                print("Expired Tender")
                Global_var.expired += 1
        else:
            print("Deadline Not Given")
            Global_var.deadline_Not_given += 1
    except Exception as e:
        exc_type , exc_obj , exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname , "\n" ,exc_tb.tb_lineno)

ChromeDriver()