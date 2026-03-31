import typer
from pathlib import Path
from rich import print
from rich.progress import track

from . import vision
from . import parser
from . import utils

app = typer.Typer(help="Autonomous AI Photo Namer")

@app.command()
def process_photos(
    folder: Path = typer.Argument(
        Path.cwd(), 
        help="The directory containing the photos."
    ),
    fields: str = typer.Option(
        "date, subject, mood, principle", 
        "--fields", "-f",
        prompt="\nWhat fields do you want in the filename? (comma-separated)\n[Options: date, subject, mood, lighting, principle] (Default: date, subject, mood, principle)",
        show_default=False, 
        help="Comma-separated list of tags to include."
    ),
    separator: str = typer.Option(
        "_", 
        "--sep", "-s",
        prompt="\nWhat separator should connect the words? (e.g., '_' or '-') (Default: '_')",
        show_default=False,
        help="Character to separate the fields."
    ),
    casing: str = typer.Option(
        "pascal", 
        "--casing", "-c",
        prompt="\nWhich casing style? (pascal, snake, upper, lower) (Default: pascal)",
        show_default=False,
        help="Text formatting style."
    ),
    dry_run: bool = typer.Option(
        True, 
        "--execute", "-e",
        prompt="\nIs this a safe dry-run? (Default: Yes)",
        show_default=False,
        help="Set to False to actually rename the files."
    )
):
    """
    Scans a folder of images, uses local AI to extract visual tags, 
    and renames them according to a custom template.
    """
    valid_extensions = {".jpg", ".jpeg", ".png", ".nef"}
    images = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in valid_extensions]

    if not images:
        print(f"[bold red]No valid images found in {folder}[/bold red]")
        raise typer.Exit()

    allowed_fields = {"date", "subject", "mood", "lighting", "principle"}
    
    selected_fields = [f.strip().lower() for f in fields.split(",")]
   
    for field in selected_fields:
        if field not in allowed_fields:
            print(f"\n[bold red]Error: '{field}' is not a valid option.[/bold red]")
            print(f"[yellow]Please choose from: {', '.join(allowed_fields)}[/yellow]\n")
            raise typer.Exit(code=1)
            
    generated_template = separator.join([f"{{{f}}}" for f in selected_fields])

    print(f"\n[bold blue]Found {len(images)} images.[/bold blue]")
    print(f"[dim]Generated Naming Template: {generated_template}[/dim]\n")
    
    if dry_run:
        print("[bold yellow]DRY RUN MODE ACTIVATED. No files will actually be changed.[/bold yellow]\n")

    analyzer = vision.ImageAnalyzer()

    for img_path in track(images, description="Processing Photos..."):
        
        original_ext = img_path.suffix
        date_str = utils.get_photo_date(img_path)
        
        raw_ai_text = analyzer.analyze_image(img_path)
        
        tags = parser.parse_ai_output(raw_ai_text)
        
        base_name = parser.format_filename(tags, date_str, generated_template, casing)
        
        new_path = utils.get_safe_filepath(folder, base_name, original_ext)
        
        if dry_run:
            print(f"[dim]Preview:[/dim] {img_path.name} [bold green]➔[/bold green] {new_path.name}")
        else:
            try:
                img_path.rename(new_path)
                print(f"[dim]Renamed:[/dim] {img_path.name} [bold green]➔[/bold green] {new_path.name}")
            except Exception as e:
                print(f"[bold red]Failed to rename {img_path.name}: {e}[/bold red]")

    print("\n[bold green]Processing complete![/bold green]\n")

if __name__ == "__main__":
    app()