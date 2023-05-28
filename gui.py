import os
import math
import time
import shutil
import img2pdf
import datetime
import pyautogui as pgui
import flet as ft
from flet import *
from PIL import Image
from typing import Optional
from pyautogui import FailSafeException

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
                    ),
                ]
        )
        return self.button_only_layout



def main(page:Page):
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page_scroll = Text()
    page_count = Text()
    width, height = width_calculate(width=1050)
    page.window_width = width
    page.window_height = height
    page.window_resizable = False
    page.update()

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
                                        margin_param=0, 
                                        icon=icons.FOLDER_OPEN,
                                        on_click_event=lambda _: get_directory_dialog.get_directory_path())


    # 文章は動的にする
    title_text = ft.Text(size=30,text_align=ft.TextAlign.CENTER, style=ft.TextThemeStyle.DISPLAY_MEDIUM, )
    dlg = ft.AlertDialog(
        title=title_text,
    )

    def _dialog_open_text(text:str):
        title_text.value = text
        page.dialog = dlg
        dlg.open = True
        page.update()

    def create_pdf_from_image(e):
        pdf_file_name = "book.pdf"
        path = directory_path.content.value
        ext_p = ".png"
        ext_j = ".jpg"
        
        if path == None or path == "":
            _dialog_open_text(text="PDF化するフォルダを選択してください")
            return
        
        try:
            save_directory = "output_pdf" + "_" + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            os.mkdir(save_directory)
            with open(save_directory + "/" + pdf_file_name, "wb") as f:
                imageLists = []
                for item in os.listdir(path):
                    if item.endswith(ext_p):
                        image = Image.open(path + "/" + item)
                        image = image.convert('RGB')
                        image.save(save_directory + "/" + item[:-3] + 'jpg')
                        imageLists = imageLists + [save_directory + "/" + item[:-3] + 'jpg']
                    elif item.endswith(ext_j):
                        image = Image.open(path + "/" + item)
                        image = image.convert('RGB')
                        imageLists = imageLists + [path + "/" + item]
                    imageLists.sort()

                f.write(img2pdf.convert(imageLists))
            for imageLists in imageLists:
                os.remove(imageLists)
        except ValueError:
            _dialog_open_text(text="フォルダ内に画像がありません\n強制終了しました")
            shutil.rmtree(save_directory)
            return
        
        _dialog_open_text(text="💫PDF作成終了")
        page.update()

    create_pdf_view = ButtonOnlyLayout("PDF作成", 
                                        margin_param=0,
                                        on_click_event=create_pdf_from_image)
    
    def screenshots_start_click_button(e):
        count = page_count.value

        if count == None:
            _dialog_open_text(text="空白にしないでください")
            return

        if not count.isdigit():
            _dialog_open_text(text="数字を入力してください")
            return

        if page_scroll.value == None:
            _dialog_open_text(text="ページスクロールを設定してください")
            return

        try:
            _dialog_open_text(text="5秒以内にKindleのページへ移動してください")
            page.update()

            time.sleep(5)

            page.dialog = dlg
            dlg.open = False
            page.update()

            # 出力フォルダ作成(フォルダ名：頭文字_年月日時分秒)
            folder_name = "output" + "_" + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            os.mkdir(folder_name)
            for p in range(int(count)):
                out_filename = f"picture_{str(p+1).zfill(4)}.png"
                # 範囲の対応は一旦なし
                screenshot = pgui.screenshot()
                screenshot.save(f"{folder_name}/{out_filename}")
                # ページスクロールの引数を入れる
                pgui.keyDown(page_scroll.value)
                time.sleep(0.5)
        except FailSafeException as e:
            _dialog_open_text(text="強制終了しました")
            return
        
        _dialog_open_text(text="💫スクリーンショット終了")
        page.update()

    screenshots_view = ButtonOnlyLayout("スクリーンショット開始", 
                                        margin_param=50,
                                        icon=icons.CAMERA_ALT_OUTLINED,
                                        on_click_event=screenshots_start_click_button)

    def dropdown_changed(e) -> Optional[str]:
        page_scroll.value = dropdown_list.value
        page.update()

    dropdown_list = ft.Dropdown(
                        width=100,
                        on_change=dropdown_changed,
                        options=[
                            ft.dropdown.Option("right"),
                            ft.dropdown.Option("left"),
                        ],
                    )

    def page_count_changed(e) -> Optional[int]:
        page_count.value = page_count_view.value
        page.update()

    page_count_view = TextField(
                        hint_text="ページ数を数字で入力",
                        on_change=page_count_changed,
                        expand=True, 
                        bgcolor=colors.WHITE24)
    
    locate_edits = Column(
        controls=[
            Row(
                controls=[
                    page_count_view,
                    dropdown_list
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
                                            padding=padding.only(top=40,left=40, right=60),
                                            width=500,
                                        ),
                                        Container(
                                            content=Text(
                                                weight=FontWeight.BOLD,
                                                size=32,
                                            ),
                                            width=500,
                                            alignment=alignment.center
                                        )
                                    ]
                                ),
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
                                            padding=padding.only(top=45),
                                            width=500,
                                        ),
                                        file_pick_view,
                                        directory_path
                                    ]
                                ),
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