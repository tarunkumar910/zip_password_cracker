import zipfile
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def extract(zfile, password):
    try:
        zfile.extractall(pwd=password.encode('utf-8'))
        return password
    except:
        return None

def main():
    console.rule("[bold blue]ZIP Password Cracker[/bold blue]", style="bold green")
    
    zpath = Prompt.ask("[bold yellow]Enter the path of zip file[/bold yellow]")
    listpath = Prompt.ask("[bold yellow]Enter the path of password list[/bold yellow]")
    
    try:
        zfile = zipfile.ZipFile(zpath)
        passFile = open(listpath, 'r')
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return

    passwords = passFile.readlines()
    found = False

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        task = progress.add_task("[cyan]Cracking password...", total=None)

        for line in passwords:
            password = line.strip('\n')
            guess = extract(zfile, password)
            if guess:
                found = True
                progress.update(task, description=f"[green]Password found![/green]")
                break

    if found:
        console.print(f"[bold green]✔ Password = {password}[/bold green]")
    else:
        console.print("[bold red]✘ Password not found in the list.[/bold red]")

if __name__ == '__main__':
    main()
