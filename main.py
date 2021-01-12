import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
import time


def print_banner():
        
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

def search_book(search_string):

    start = time.time()
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
            "file size": file_size,
            "link": link
        })


    table = Table(title="Book Searching", show_header=True, header_style="bold bright_red")

    table.add_column("[cyan]STT[/cyan]", justify="center", style="cyan")
    table.add_column("[yellow]Name[/yellow]", style="yellow")
    table.add_column("[green]Publisher[/green]", justify="left", style="green")
    table.add_column("[magenta]Authors[/magenta]", justify="left", style="magenta")
    table.add_column("[blue]Year[/blue]", justify="right", style="blue")
    table.add_column("[green_yellow]Language[/green_yellow]", justify="center", style="green_yellow")
    table.add_column("[turquoise4]File size[/turquoise4]", justify="left", style="turquoise4")


    stt = 1
    for d in data:
        table.add_row(str(stt), d['name'] + '\n', d['publisher'], ",\n".join(d['authors']), d['year'], d['language'], d['file size'])
        stt += 1

    console = Console()
    console.print(table)

    print("Time: ", time.time() - start)

if __name__ == '__main__':
    console = Console()
    
    print_banner()

    print()
    search_string = console.input("[bright_blue]Search: [/bright_blue]")
    
    search_book(search_string)

    