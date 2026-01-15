import sys
import os
import flet as ft
from pdf_utils import analyze_pdf

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main(page: ft.Page):
    page.title = "PDF Font Detector"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.window_width = 800
    page.window_height = 700
    
    # State variables
    current_file_path = None
    
    # UI Elements
    
    
    theme_icon = ft.IconButton(
        content=ft.Icon("dark_mode"),
        tooltip="Toggle Theme"
    )
    
    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        theme_icon.content = ft.Icon("dark_mode" if page.theme_mode == ft.ThemeMode.LIGHT else "light_mode")
        page.update()
    
    theme_icon.on_click = toggle_theme


    logo_path = get_resource_path(os.path.join("assets", "logo.png"))
    # Fallback for dev mode where CWD might not be root
    if not os.path.exists(logo_path):
         logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")

    logo_img = ft.Image(
        src=logo_path,
        width=100,
        height=50,
        fit="contain",
        tooltip="Flex2"
    )

    header = ft.Row(
        [
            ft.Row([logo_img, ft.Text("PDF Font Detector", size=24, weight=ft.FontWeight.BOLD)], spacing=10),
            theme_icon
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    results_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    
    
    loading_indicator = ft.ProgressBar(width=400, color="blue", visible=False)
    
    status_text = ft.Text("Drag and drop a PDF file here to analyze", size=16, color="grey")

    def process_pdf(file_path):
        nonlocal current_file_path
        current_file_path = file_path
        
        # Show loading
        results_container.controls.clear()
        loading_indicator.visible = True
        status_text.value = f"Analyzing {os.path.basename(file_path)}..."
        status_text.color = "blue"
        page.update()
        
        # Run analysis (might block UI slightly if large, ideally run in thread)
        # For simplicity in this v1, running directly. Flet is async-capable but simple callbacks are sync.
        try:
            fonts = analyze_pdf(file_path)
            
            loading_indicator.visible = False
            status_text.value = f"Found {len(fonts)} unique fonts in {os.path.basename(file_path)}"
            status_text.color = "green"
            
            if not fonts:
                results_container.controls.append(ft.Text("No fonts found or document contains no text objects."))
            
            for font in fonts:
                # Create a card for each font
                is_embedded = font['is_embedded']
                icon_name = "check_circle" if is_embedded else "cancel"
                icon_color = "green" if is_embedded else "red"
                
                card = ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.ListTile(
                                    leading=ft.Icon("font_download"),
                                    title=ft.Text(font['name'], weight=ft.FontWeight.BOLD),
                                    subtitle=ft.Text(f"Type: {font['type']} | Encoding: {font['encoding']}"),
                                ),
                                ft.Row(
                                    [
                                        ft.Icon(icon_name, color=icon_color, size=16),
                                        ft.Text("Embedded" if is_embedded else "Not Embedded", size=12, color=icon_color)
                                    ],
                                    alignment=ft.MainAxisAlignment.END,
                                )
                            ]
                        ),
                        padding=10
                    )
                )
                results_container.controls.append(card)
                
        except Exception as e:
            loading_indicator.visible = False
            status_text.value = f"Error: {str(e)}"
            status_text.color = "red"
        
        page.update()



    # Simple Drop implementation using DragTarget if desired, but Flet Desktop has native drag-drop often handled via window events or Pickers.
    # However, Flet's 'on_file_drop' on the Page object is the best for Desktop drag/drop
    
    def page_drop(e):
        file_path = e.file_path
        if file_path and file_path.lower().endswith('.pdf'):
            process_pdf(file_path)
        else:
            status_text.value = "Only PDF files are supported."
            status_text.color = "red"
            page.update()

    page.on_file_drop = page_drop



    drop_zone = ft.Container(
        content=ft.Column(
            [
                ft.Icon("cloud_upload", size=60, color="blue_grey"),
                status_text,
                loading_indicator
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        border=ft.border.all(2, "blue_grey_100"),
        border_radius=10,
        padding=40,
        bgcolor="#E3F2FD"
    )
    
    page.add(
        header,
        ft.Divider(),
        drop_zone,
        ft.Divider(),
        results_container
    )

if __name__ == "__main__":
    ft.app(target=main)
