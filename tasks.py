from robocorp.tasks import task
from robocorp import browser

from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive
import time


def open_the_intranet_website():
    """Navigates to the given URL"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")
    page = browser.page()

def download_csv_file():
    """Downloads csv file from the given URL"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)

def convert_into_tables():
    """Convert the CSV-file into a table"""
    library = Tables()
    orders = library.read_table_from_csv(
    "orders.csv", columns=["Order number","Head","Body","Legs","Address"])
    return orders
        
def fill_the_form(orders):
    """Filling in the form with the information of the csv file"""
    orders = convert_into_tables()
    for row in orders:
        order_number = row['Order number']
        click_on_cookies()
        page = browser.page()
        page.select_option('#head', row['Head'])
        body = row['Body']
        if body == "1":
            page.locator('//*[@id="id-body-1"]').click()
        if body == "2":
            page.locator('//*[@id="id-body-2"]').click()
        if body == "3":
            page.locator('//*[@id="id-body-3"]').click()
        if body == "4":
            page.locator('//*[@id="id-body-4"]').click()
        if body == "5":
            page.locator('//*[@id="id-body-5"]').click()
        if body == "6":
            page.locator('//*[@id="id-body-6"]').click()
        page.fill('//input[@placeholder="Enter the part number for the legs"]', (row['Legs']))
        page.fill('#address', (row['Address']))
        page.click('//*[@id="order"]')
        if page.locator("//div[@class='alert alert-danger']").count()>0:
            page.click('//*[@id="order"]')
            if page.locator("//div[@class='alert alert-danger']").count()>0:
                page.click('//*[@id="order"]')
                if page.locator("//div[@class='alert alert-danger']").count()>0:
                    page.click('//*[@id="order"]')
                    store_receipt_as_pdf(order_number)
                else:
                    store_receipt_as_pdf(order_number)
            else:
                store_receipt_as_pdf(order_number)
        else:
            store_receipt_as_pdf(order_number)

def click_on_cookies():
    """Clicks on the cookies on the page"""
    page = browser.page()
    if page.locator("//*[text()='By using this order form, I give up all my constitutional rights for the benefit of RobotSpareBin Industries Inc.']").count()>0:
        try:
            page.click("text=OK")
        except Exception:
            pass
    else:
        print("No text")

def store_receipt_as_pdf(order_number):
    """Export the data to a pdf file"""
    pdf = PDF()
    page = browser.page()
    sales_results_html = page.locator("//div[@id='receipt']").inner_html()
    output = str('output/sales_result' + str(order_number) + '.pdf')
    pdf.html_to_pdf(sales_results_html, output)
    screenshot_robot(order_number, output)
    time.sleep(1)
    page.click('//*[@id="order-another"]')


def screenshot_robot(order_number,output):
    """Makes a screenshot of each of the three parts of the robot"""
    page = browser.page()
    page.locator("//*[@id='robot-preview-image']/img[1]").screenshot(path= "output/screenshot_head.png")
    image_path = str("output/screenshot_head.png")
    embed_screenshot_to_receipt(image_path, output)
    page.locator("//*[@id='robot-preview-image']/img[2]").screenshot(path= "output/screenshot_body.png")
    image_path = str("output/screenshot_body.png")
    embed_screenshot_to_receipt(image_path, output)
    page.locator("//*[@id='robot-preview-image']/img[3]").screenshot(path= "output/screenshot_legs.png")
    image_path = str("output/screenshot_legs.png")
    embed_screenshot_to_receipt(image_path, output)

def embed_screenshot_to_receipt(image_path, output):
    """Embeds the screenshot into the receipt"""
    pdf = PDF()
    pdf.add_files_to_pdf(files=[image_path], target_document=output, append = True)
       

def archive_receipts():
    """Archives all of the PDF files into a zip-file"""
    lib = Archive()
    lib.archive_folder_with_zip('./output', './output/archive_receipts.zip', include='*.pdf')  
    


@task
def new_robot():
    orders = convert_into_tables()
    browser.configure(
        slowmo=500,
    )
    open_the_intranet_website()
    download_csv_file()
    convert_into_tables()
    fill_the_form(orders)
    archive_receipts()
   
