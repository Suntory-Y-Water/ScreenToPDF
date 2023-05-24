import os
import math
import time
import datetime
import pyautogui as pgui

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




def locate():
    print("実行されました")
    try:
        while True:
            x, y = pgui.position()
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)
    except KeyboardInterrupt:
        print('\n')


def page_screenshots(page_count:int, x1:int, y1:int, x2:int, y2:int):

    pgui.confirm(text='Kindleの画面に移動しましたか？',title='確認',buttons=['はい','いいえ'])

    # 出力フォルダ作成(フォルダ名：頭文字_年月日時分秒)
    folder_name = "output" + "_" + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    os.mkdir(folder_name)

    for p in range(page_count):
        out_filename = f"picture_{str(p+1).zfill(4)}.png"
        screenshot = pgui.screenshot(region=(x1, y1, x2, y2))
        screenshot.save(f"{folder_name}/{out_filename}")
        # ページスクロールの引数を入れる
        pgui.keyDown('right')
        time.sleep(0.5)


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
    
    get_locates_view = ButtonOnlyLayout(button_name="座標を取得する", 
                                        margin_param=-5,
                                        # 終了条件を返していないし、画面に表示できていない
                                        on_click_event=lambda _: get_directory_dialog.get_directory_path())
    
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
                        alignment=alignment.center,
                    )

    page.overlay.append(get_directory_dialog)
    
    file_pick_view = ButtonOnlyLayout("ファイルを取得する", 
                                        margin_param=-5, 
                                        icon=icons.FOLDER_OPEN,
                                        on_click_event=lambda _: get_directory_dialog.get_directory_path())

    locate_edits = Column(
        controls=[
            Row(
                controls=[
                    TextField(hint_text="左上X", expand=True, bgcolor=colors.WHITE24),
                    TextField(hint_text="左上Y", expand=True, bgcolor=colors.WHITE24),
                    TextField(hint_text="右下X", expand=True, bgcolor=colors.WHITE24),
                    TextField(hint_text="右下Y", expand=True, bgcolor=colors.WHITE24),
                    TextField(hint_text="数", expand=True, bgcolor=colors.WHITE24),
                    TextField(hint_text="ページ送り", expand=True, bgcolor=colors.WHITE24),
                ],
            ),
        ],
    )

    def button_clicked(e):
        if button_content.text == "押したらEnterキーを押す":
            button_content.text = "処理を終了する"
            clicked_change_theme.color_scheme.primary = colors.BLUE_100
        elif button_content.text == "処理を終了する":
            button_content.text = "押したらEnterキーを押す"
            clicked_change_theme.color_scheme.primary = colors.PINK_100
        page.update()

    button_content = OutlinedButton(text="押したらEnterキーを押す", on_click=button_clicked)
    clicked_change_theme = Theme(color_scheme=ColorScheme(primary=colors.PINK_100))

    button_width, _ = width_calculate(width=500)
    text_layout = Container(
                        content=Text(
                                    value="test",
                                    size=18,
                                    weight=FontWeight.BOLD
                                ),
                        width=500,
                        height=50,
                        alignment=alignment.center
                    )
    locate_button_layout = Column(
            controls=[
                Container(
                    content=Container(
                        theme=clicked_change_theme,
                        padding=0,
                        margin=0,
                        theme_mode=ThemeMode.LIGHT,
                        content=button_content
                    ),
                    margin=margin.only(top=-5),
                    padding=padding.only(left=80, top=70, bottom=70, right=80),
                    width=button_width,
                    height=250,
                ),
            ]
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
                                        locate_button_layout,
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