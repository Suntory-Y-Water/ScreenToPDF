import math
import flet as ft
from flet import (
    Container,
    UserControl,
    Theme,
    ColorScheme,
    colors,
    ThemeMode,
    OutlinedButton,
    CrossAxisAlignment,
    Page,
    Tab,
    Tabs,
    Text,
    MainAxisAlignment,
    margin,
    padding,
    Column,
    Row,
    TextField,
    icons,
    FontWeight,
    alignment,
)


def width_calculate(width:int):
    golden_ratio = (1 + math.sqrt(5)) / 2
    return width, width / golden_ratio

class ButtonOnlyLayout(UserControl):
    def __init__(self, 
                button_name:str,
                margin_param:int=100,
                icon:str=None,
                on_click_event=None):
        
        super().__init__(self)
        self.button_name = button_name
        self.margin_param = margin_param
        self.icon = icon
        self.on_click_event = on_click_event

    def build(self):
        calc_width, calc_height = width_calculate(width=500)
        self.button_only_layout = Column(
                controls=[
                    Container(
                        content=Container(
                            theme=Theme(color_scheme=ColorScheme(primary=colors.PINK_100)),
                            padding=0,
                            margin=0,
                            theme_mode=ThemeMode.LIGHT,
                            content=OutlinedButton(
                                text=self.button_name,
                                icon=self.icon,
                                on_click=self.on_click_event,
                            )
                        ),
                        margin=margin.only(top=self.margin_param),
                        padding=padding.only(left=80, top=70, bottom=70,right=80),
                        width=calc_width,
                        height=250,
                        # bgcolor=colors.WHITE54
                    ),
                ]
        )
        return self.button_only_layout



def main(page:Page):
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    width, height = width_calculate(width=1050)
    page.window_width = width
    page.window_height = height
    page.window_resizable = False
    page.update()
    screenshots_view = ButtonOnlyLayout("スクリーンショット開始", margin_param=45)
    create_pdf_view = ButtonOnlyLayout("PDF作成", margin_param=40)

    def get_directory_result(e: ft.FilePickerResultEvent):
        directory_path.content.value = e.path if e.path else ""
        directory_path.update()

    get_directory_dialog = ft.FilePicker(on_result=get_directory_result)
    directory_path = Container(
                        content=Text(
                                    size=18,
                                    weight=FontWeight.BOLD
                                ),
                        width=500,
                        height=50,
                        alignment=alignment.center
                    )

    page.overlay.append(get_directory_dialog)

    get_locates_view = ButtonOnlyLayout("座標を取得する", margin_param=-5)
    file_pick_view = ButtonOnlyLayout("ファイルを取得する", 
                                        margin_param=-5, 
                                        icon=icons.FOLDER_OPEN,
                                        on_click_event=lambda _: get_directory_dialog.get_directory_path())

    locate_edits = Column(
        controls=[
            Row(
                controls=[
                    TextField(hint_text="左上 X", expand=True, bgcolor=colors.WHITE24),
                    TextField(hint_text="左上 Y", expand=True, bgcolor=colors.WHITE24),
                    TextField(hint_text="右下 X", expand=True, bgcolor=colors.WHITE24),
                    TextField(hint_text="右下 Y", expand=True, bgcolor=colors.WHITE24)
                ],
            ),
        ],
    )



    main_layout = Tabs(
        selected_index=0,
        animation_duration=300,
        label_color=colors.PINK_100,
        overlay_color="hovered",
        width=width,
        height=height,
        tabs=[
            Tab(
                text="スクリーンショット実施",
                content=Column(
                    [
                        Row(
                            controls=[
                                Column(
                                    [
                                        Container(
                                            content=locate_edits,
                                            padding=padding.only(top=40),
                                            width=500,
                                        ),
                                        get_locates_view,
                                        Container(
                                            content=Text(
                                                "ここに座標が表示されます",
                                                weight=FontWeight.BOLD,
                                                size=32,
                                            ),
                                            width=500,
                                            alignment=alignment.center
                                        )
                                    ]
                                ),
                                #ここは変えない
                                screenshots_view,
                            ]
                        )
                    ]
                ),
            ),
            Tab(
                text="PDF作成",
                content=Column(
                    [
                        Row(
                            controls=[
                                Column(
                                    [
                                        Container(
                                            padding=padding.only(top=95),
                                            width=500,
                                        ),
                                        file_pick_view,
                                        directory_path
                                    ]
                                ),
                                #ここは変えない
                                create_pdf_view,
                            ]
                        )
                    ]
                ),
            ),
        ],
    )
    page.add(main_layout)

if __name__ == '__main__':
    ft.app(target=main)