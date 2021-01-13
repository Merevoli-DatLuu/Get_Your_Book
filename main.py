""" 
    Công cụ tra cứu sách
    Author
    ------
    Lưu Thành Đạt
        https://github.com/Merevoli-DatLuu/Get_Your_Book
    Version
    -------
    v0.1 - Code Refactoring - 14/01/2021

    Data source: https://b-ok.asia/
"""

import requests
from bs4 import BeautifulSoup
from PIL import Image
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from climage.climage import _toAnsi
from climage.__main__ import _get_color_type
import time


def print_banner():
    """
    Print the banner
    """
    banner = """
              ''''                    ''''              
              ;'%?;'%              %;;?%';              
         ''';;''%%%%';?          ?;'%%%%'';;'''         
        ''???+;'%%%%%%'';      ;''%%%%%%';+???''        
        ''????''%%%%%%%%;;;  ;;;%%%%%%%%';????';        
      ;;;'????''%%%%%%%%%%''''%%%%%%%%%%';????';;;      
    '''?''????''%%%%%%%%%%%''%%%%%%%%%%%';????';?'''    
    ''??''????''%%%%%%%%%%%''%%%%%%%%%%%';????''??''    
    ''??''????''%%%%%%%%%%%''%%%%%%%%%%%';????''??''    
    ''??''????''%%%%%%%%%%%''%%%%%%%%%%%';????''??''    
    ''??''????''%%%%%%%%%%%''%%%%%%%%%%%';????''??''    
    ''??''????''%%%%%%%%%%%''%%%%%%%%%%%';????''??''    
    ''??''????;'%%%%%%%%%%%''%%%%%%%%%%%';????''??''    
    ''??''????;'%%%%%%%%%%%''%%%%%%%%%%%';????''??''    
    ''??''????''%%%%%%%%%%%''%%%%%%%%%%%''????''??''    
    ''??''?????';%%%%%%%%%%''%%%%%%%%%%;'?????''??''    
    ''??''???????;;?%%%%%%%''%%%%%%%?;;???????''??''    
    ''???;';???????''+%%%%%''%%%%%+''???????;';???''    
    ''?????';'';+????'';%%%''%%%;';????+;'';'?????''    
    ''??????????;'''';?;''%''%'';?;'''';??????????''    
    '';??????????????+;'''''''''';+??????????????;''    
      ''''''''''''''''''''''''''''''''''''''''''''    
    """

    info = """
    [yellow][Author]  ->  Lưu Thành Đạt[/yellow]    
    [green][Version]  ->  v0.1[/green]      
    """

    console = Console()
    banner_text = Text(banner)

    for i in range(len(banner)):
        if banner[i] == "'":
            banner_text.stylize("bright_blue", i, i+1)
        elif banner[i] == ';':
            banner_text.stylize("bright_blue", i, i+1)
        elif banner[i] == '+':
            banner_text.stylize("bright_blue", i, i+1)
        elif banner[i] == '?':
            banner_text.stylize("bright_cyan", i, i+1)
        elif banner[i] == '%':
            banner_text.stylize("bright_cyan", i, i+1)

    console.print(banner_text, justify="center")
    console.print(Panel.fit(info, title="[cyan]Get Your Book!!![/cyan]", style="cyan"), justify="center")

def print_usage_1():
    """
    Print the usage (for searching)
    """
    usage = """
        /detail or /dt <id> to view detail a book
        /download or /d <id> to download a book     
        /help or /h to view usage
        /back or /b to back     
        /quit or /q to exit
    """

    console = Console()
    console.print(Panel.fit(usage, title="[cyan]Usage[/cyan]", style="cyan"), justify="center")

def print_usage_2():
    """
    Print the usage (for view details)
    """
    usage = """
        /download or /d to download a book        
        /help or /h to view usage
        /back or /b to back     
        /quit or /q to exit
    """

    console = Console()
    console.print(Panel.fit(usage, title="[cyan]Usage[/cyan]", style="cyan"), justify="center")

def download_book(url, name):
    """
    Download a book
    [ISSUE]: invalid url
    """
    content = requests.get(url).raw
    with open(name, 'w') as file:
        file.write(content)
        file.close()

def go_to_details(data):
    """
    View the details of a book
    """
    print_usage_2()
    print()
    
    with console.status("[bold green]Getting the details...") as status:
        detail_url = "https://b-ok.asia/" + data['link']
        res = requests.get(detail_url)
        soup = BeautifulSoup(res.text, 'html.parser')

        image_url = soup.findAll('a', {'class': 'lightbox details-book-cover checkBookDownloaded'})
        download_url = soup.find('a', {'class': 'btn btn-primary dlButton addDownloadedBook'})['href']
        
        if len(image_url) > 0:
            image_url = image_url[0]['href']

        # Get description
        description = soup.find('div', {'id': 'bookDescriptionBox'})
        if description:
            description = description.getText()
        else:
            description = ""

        # Get categories
        categories = soup.find('div', {'class': 'bookProperty property_categories'})
        if categories:
            categories = categories.find('div', {'class': 'property_value'}).getText()
        else:
            categories = ""

        # Get ISBN
        isbn = soup.find('div', {'class': 'bookProperty property_isbn'})
        if isbn:
            isbn = isbn.find('div', {'class': 'property_value'}).getText()
        else:
            isbn = ""

        # Get ISBN 10
        isbn_10 = soup.find('div', {'class': 'bookProperty property_isbn 10'})
        if isbn_10:
            isbn_10 = isbn_10.find('div', {'class': 'property_value'}).getText()
        else:
            isbn_10 = ""

        # Get ISBN 13
        isbn_13 = soup.find('div', {'class': 'bookProperty property_isbn 13'})
        if isbn_13:
            isbn_13 = isbn_13.find('div', {'class': 'property_value'}).getText()
        else:
            isbn_13 = ""

        # Get pages
        page = soup.find('div', {'class': 'bookProperty property_pages'})
        if page:
            page = page.find('div', {'class': 'property_value'}).getText()
        else:
            page = ""

    # Print book's cover
    print_image(image_url)

    # Print info
    if data['name'] != "":
        console.print("[green][:heavy_check_mark:] Name:[/green]", data['name'])
    if data['authors'] != "":
        console.print("[green][:heavy_check_mark:] Authors:[/green]", ", ".join(data['authors']))
    if description != "":
        console.print("[green][:heavy_check_mark:] Description:[/green]", description.strip())
    if categories != "":
        console.print("[green][:heavy_check_mark:] Categories:[/green]", categories)
    if data['language'] != "":
        console.print("[green][:heavy_check_mark:] Language:[/green]", data['language'])
    if isbn != "":
        console.print("[green][:heavy_check_mark:] ISBN:[/green]", isbn)
    if isbn_10 != "":
        console.print("[green][:heavy_check_mark:] ISBN 10:[/green]", isbn_10)
    if isbn_13 != "":
        console.print("[green][:heavy_check_mark:] ISBN 13:[/green]", isbn_13)
    if data['file'] != "":
        console.print("[green][:heavy_check_mark:] File:[/green]", data['file'])
    if data['year'] != "":
        console.print("[green][:heavy_check_mark:] Year:[/green]", data['year'])
    if data['publisher'] != "":
        console.print("[green][:heavy_check_mark:] Publisher:[/green]", data['publisher'])
    if page != "":
        console.print("[green][:heavy_check_mark:] Pages:[/green]", page)
    console.print("[green][Download][/green][yellow] ---> [/yellow]", "https://b-ok.asia/" + download_url)

    
    option = console.input("[bright_blue]>>> [/bright_blue]")

    while option not in ("/back", "/b"):
        if option in ("/quit", "/q"): 
            console.print("[bright_red]Exit[/bright_red]")
            exit(0)
        elif option in ("/download", "/d"):
            pass
        elif option in ("/help", "/h"):
            print_usage_2()
        else:
            console.print("[bright_red]Invalid Input[/bright_red]")
        option = console.input("[bright_blue]>>> [/bright_blue]")



def convert_url(url, is_unicode=False, is_truecolor=False, is_256color=True, is_16color=False, is_8color=False, width=60, palette="default"):
    """
    Convert to image from URL
    Modified climage.__main__.convert()
    """
    im = Image.open(requests.get(url, stream=True).raw).convert('RGB')
    ctype = _get_color_type(is_truecolor=is_truecolor, is_256color=is_256color, is_16color=is_16color, is_8color=is_8color)
    return _toAnsi(im, oWidth=width, is_unicode=is_unicode, color_type=ctype, palette=palette)

def print_image(url):
    """
    Print book's cover
    """
    output = convert_url(url, is_unicode=True)
    console = Console()
    console.out(output)
    
def search_book(search_string):
    """
    Search books from search_string and print the book list
    """
    start = time.time()
    console = Console()

    with console.status("[bold green]Working on tasks...") as status:
        res = requests.get("https://b-ok.asia/s/?q=" + search_string)
        soup = BeautifulSoup(res.text, 'html.parser')
        items = soup.findAll('table', {'class': 'resItemTable'})
        data = []

        for item in items:
            id = item.tr.td.div['data-book_id']
            link = item.tr.td.a['href']
            head = item.tr.findAll('td', recursive = False)[1].table

            name = head.tr.td.h3.a.getText()
            publisher = head.tr.td.div.a.getText()
            authors = []
            authors_div = head.tr.td.findAll('div', recursive = False)

            if len(authors_div) > 1:
                authors = [i.getText() for i in authors_div[1].findAll('a')]

            t = head.findAll('tr', recursive = False)[1]\
                    .td\
                    .findAll('div', recursive = False)[1]\
                    .findAll('div', recursive = False)
            details = list(map(lambda x: [fr.getText() for fr in x.findAll('div', recursive = False)], t))

            year = details[0][1]
            language = details[1][1]
            file_size = details[2][1]

            data.append({
                "id": id,
                "name": name,
                "publisher": publisher,
                "authors": authors,
                "year": year,
                "language": language,
                "file": file_size,
                "link": link
            })


    table = Table(title="Book Searching", show_header=True, header_style="bold bright_red")

    table.add_column("[cyan]STT[/cyan]", justify="center", style="cyan")
    table.add_column("[yellow]Name[/yellow]", style="yellow")
    table.add_column("[green]Publisher[/green]", justify="left", style="green")
    table.add_column("[magenta]Authors[/magenta]", justify="left", style="magenta")
    table.add_column("[blue]Year[/blue]", justify="right", style="blue")
    table.add_column("[green_yellow]Language[/green_yellow]", justify="center", style="green_yellow")
    table.add_column("[turquoise4]File[/turquoise4]", justify="left", style="turquoise4")

    stt = 1
    for d in data:
        table.add_row(str(stt), d['name'] + '\n', d['publisher'], ",\n".join(d['authors']), d['year'], d['language'], d['file'])
        stt += 1

    console.print(table)
    print("Time: {:.3f}s\n".format(time.time() - start))

    print_usage_1()
    option = console.input("[bright_blue]>>> [/bright_blue]")

    while option not in ("/back", "/b"):
        if option in ("/quit", "/q"):
            console.print("[bright_red]Exit[/bright_red]")
            exit(0)
        if option in ("/help", "/h"):
            print_usage_1()
        elif len(option.split(' ')) == 2:
            optionplt = option.split()
            if optionplt[0] in ("/detail", "/dt") and\
               optionplt[1].isnumeric() and\
               1 <= int(optionplt[1]) <= len(data):
                go_to_details(data[int(optionplt[1]) - 1])
            else:
                console.print("[bright_red]Invalid Input[/bright_red]")
        else:
            console.print("[bright_red]Invalid Input[/bright_red]")
        option = console.input("[bright_blue]>>> [/bright_blue]")


if __name__ == '__main__':
    console = Console()
    
    print_banner()

    print()
    search_string = console.input("[bright_blue]Search: [/bright_blue]")
    
    while search_string not in ("/quit", "/q"):
        search_book(search_string)
        search_string = console.input("[bright_blue]Search: [/bright_blue]")



    